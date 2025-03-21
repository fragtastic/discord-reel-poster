import discord
import logging
import logging.handlers
import os
import re
from instapydl import Reel
import sys


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

pattern_url = r'^(?P<url>https:\/\/(www\.)?instagram\.com\/reel\/(?P<reel_id>[a-zA-Z0-9_\-]+)(\/)?)(\?igsh=[a-zA-Z0-9\=]+)?'

console_handler = logging.StreamHandler(sys.stdout)  # Or use sys.stderr if preferred
file_handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class MyClient(discord.Client):
    async def on_ready(self):        
        logger.info(f"Logged in as {client.user.name} - {client.user.id}")

    async def on_message(self, message):
        if message.author == self.user:
            logger.debug('Ignoring self message')
            return

        logger.debug(f'Processing message from {message.author}({message.author.id}) in #{message.channel.name}({message.channel.id}): {message.content}')
        match = re.search(pattern_url, message.content)
        if match.group('url'):
            logger.debug(f'Found reel: "{match.group('url')}"')

            reel = Reel(match.group('url'))

            # Scrape and get metadata of that post
            metadata = reel.scrape_post()
            logger.debug(metadata)

            filename = f"{match.group('reel_id')}.mp4"
            reel_bytes = reel.get_bytes()
            reel_bytes.name = filename
            logger.debug('Video downloaded to memory "{filename}"')
            tmp_file = discord.File(reel_bytes, filename=filename)
            await message.channel.send(f'{message.author.mention} {match.group('url')}', file=tmp_file, suppress_embeds=True)
            logger.debug(f'Post submitted for {message.author.mention} {match.group('url')}')

            await message.delete()  # Delete the original message
            logger.debug('Original Post deleted')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True  # Allow handling direct messages

client = MyClient(intents=intents)

# Assume client refers to a discord.Client subclass...
# Suppress the default configuration since we have our own
client.run(os.environ.get('DISCORD_BOT_TOKEN'), log_handler=None)
