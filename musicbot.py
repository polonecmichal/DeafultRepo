import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure yt-dlp for fast extraction
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'ignoreerrors': True,
    'source_address': '0.0.0.0',
}

queues = {}

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_audio_url(song_url):
    """Extract audio URL quickly"""
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_url, download=False)
            
            if info is None:
                return None, None
            
            # Handle playlists
            if 'entries' in info and info['entries']:
                info = info['entries'][0]
            
            title = info.get('title', 'Unknown')
            
            # Get audio URL - prefer formats that work well with discord.py
            audio_url = None
            
            # Try to get webm format first (works best with discord)
            if info.get('formats'):
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('ext') == 'webm':
                        audio_url = f['url']
                        print(f"Found webm format")
                        break
                
                # Fallback to best audio format
                if not audio_url:
                    audio_formats = [f for f in info['formats'] if f.get('acodec') != 'none']
                    if audio_formats:
                        audio_url = audio_formats[-1]['url']
                        print(f"Using fallback format")
            
            # Last resort
            if not audio_url and info.get('url'):
                audio_url = info['url']
            
            return audio_url, title
            
    except Exception as e:
        print(f"Extraction error: {e}")
        return None, None

async def play_song(ctx, song_url):
    """Play a song with stable voice connection"""
    voice_client = ctx.voice_client
    if not voice_client:
        return

    try:
        # Send initial message
        await ctx.send(f"🔄 Načítavam...")
        
        # Get audio URL (run in thread to avoid blocking)
        loop = asyncio.get_event_loop()
        audio_url, title = await loop.run_in_executor(None, get_audio_url, song_url)
        
        if not audio_url:
            await ctx.send("❌ Nepodarilo sa načítať audio!")
            await next_song(ctx)
            return
        
        print(f"Playing: {title}")
        
        # Create FFmpeg source with optimal settings
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -b:a 128k -bufsize 128k'
        }
        
        source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        source = discord.PCMVolumeTransformer(source, volume=0.5)
        
        # Play the song
        voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(next_song(ctx), bot.loop)
        )
        
        await ctx.send(f"🎵 Teraz hrám: **{title}**")
        
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"❌ Chyba: {str(e)[:100]}")
        await next_song(ctx)

async def next_song(ctx):
    """Play next song in queue"""
    guild_id = ctx.guild.id
    
    if guild_id in queues and queues[guild_id]:
        next_song_url = queues[guild_id].pop(0)
        await play_song(ctx, next_song_url)
    else:
        # Don't disconnect immediately - wait for potential next songs
        pass

@bot.command(name='prehraj', aliases=['p'])
async def prehraj_prefix(ctx, *, url):
    """Prehrá pieseň z YouTube"""
    # Check voice channel
    if not ctx.author.voice:
        await ctx.send("❌ Musíš byť v hlasovom kanáli!")
        return
    
    voice_channel = ctx.author.voice.channel
    voice_client = ctx.voice_client
    
    # Connect or move to voice channel
    if voice_client is None:
        await voice_channel.connect()
        voice_client = ctx.voice_client
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)
    
    # Add to queue
    guild_id = ctx.guild.id
    if guild_id not in queues:
        queues[guild_id] = []
    
    queues[guild_id].append(url)
    await ctx.send(f"✅ Pridané do poradia! ({len(queues[guild_id])} v poradí)")
    
    # Start playing if nothing is playing
    if voice_client and not voice_client.is_playing():
        song_url = queues[guild_id].pop(0)
        await play_song(ctx, song_url)

@bot.command(name='preskoc', aliases=['s'])
async def preskoc_prefix(ctx):
    """Skip current song"""
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("⏭️ Preskakujem!")
    else:
        await ctx.send("❌ Nič nehrá!")

@bot.command(name='vypni', aliases=['stop'])
async def vypni_prefix(ctx):
    """Stop and clear queue"""
    guild_id = ctx.guild.id
    if guild_id in queues:
        queues[guild_id] = []
    
    voice_client = ctx.voice_client
    if voice_client:
        voice_client.stop()
        await voice_client.disconnect()
        await ctx.send("⏹️ Vypnuté!")
    else:
        await ctx.send("❌ Nie som v hlasovke!")

@bot.command(name='poradie', aliases=['q'])
async def poradie_prefix(ctx):
    """Show queue"""
    guild_id = ctx.guild.id
    
    if guild_id not in queues or not queues[guild_id]:
        await ctx.send("📭 Poradie je prázdne!")
        return
    
    queue_list = []
    for i, url in enumerate(queues[guild_id][:10], 1):
        queue_list.append(f"{i}. {url[:80]}...")
    
    await ctx.send(f"**📋 Poradie ({len(queues[guild_id])} piesní):**\n" + "\n".join(queue_list))

@bot.event
async def on_voice_state_update(member, before, after):
    """Auto-leave when alone in voice channel"""
    if member == bot.user:
        return
    
    voice_client = member.guild.voice_client
    if voice_client and voice_client.channel:
        # If bot is alone in voice channel, leave after 60 seconds
        if len(voice_client.channel.members) == 1:
            await asyncio.sleep(60)
            if len(voice_client.channel.members) == 1:
                await voice_client.disconnect()
                print("Left voice channel - no users")

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online!')
    print(f'📊 Bot is in {len(bot.guilds)} guilds')
    print(f'\n🎵 Commands: !prehraj (or !p) <URL>')
    print(f'   Example: !p https://youtu.be/dQw4w9WgXcQ')

if __name__ == "__main__":
    bot.run(TOKEN)
