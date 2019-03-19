import discord
from discord.ext import commands
from utils import *
import sys, traceback
from discord.voice_client import VoiceClient
from discord.utils import get
import requests
import json

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.core', 'cogs.music']#music2 is another implmenation. use music if it does not work

bot = commands.Bot(command_prefix=get_prefix, description='Beep boop, I am a robot!')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_message(message):
    if(message.author.id == 141039412862648321):
        emoji = u"\U0001F1E8\U0001F1F3"
        emoji2 = u"\U0001F1E7\U0001F1F7"
        txt = message.content
        if(txt[0] != '!'):
            tkey = read_key('translate')
            url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='
            url = url + tkey
            url = url + '&text='+txt
            url = url + '&lang=en-zh'
            url = url + '&format=plain'
            resp = requests.get(url)
            resp_json = json.loads(resp.text)
            translation = str(resp_json['text'])
            translation = translation[2:]
            translation = translation[:-2]
            translation = "In John Moan's mother tongue: " + translation
            channel = message.channel
            await channel.send(translation)
        await message.add_reaction(emoji)
        await message.add_reaction(emoji2)
                
    await bot.process_commands(message)

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    activity = discord.Game(name='Use !help for list of commands', type=1, url='https://www.github.com/BryanOrabutt/discbot/')
    await bot.change_presence(status=discord.Status.online,activity=activity)
    print(f'Successfully logged in and booted...!')

token = read_key('Bastion')
bot.run(token, bot=True, reconnect=True)
