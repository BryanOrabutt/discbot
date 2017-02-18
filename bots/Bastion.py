#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from botinfo import *
import wolframalpha
from PIL import Image
import re, urlmarker

bot_name = "Bastion"
client = discord.Client()
logger = create_logger(bot_name)
bot_data = create_filegen(bot_name)
wrclient = wolframalpha.Client('L247V6-5JHVJQVEYE')

help_msg = '''
Commands available:\n!wrq <query> - Queries Wolfram Alpha with the provided input query
'''

@register_command
async def wrq(msg, mobj):
    res = wrclient.query(str(msg))
    results = ''
    for pod in res.pods:
        for sub in pod.subpods:
             imgs = re.findall(urlmarker.URL_REGEX, str(sub))
             for s in imgs:
                 results = results + s + ' '
    return await client.send_message(mobj.channel, results)

@register_command
async def howto(msg, mobj):
    return await client.send_message(mobj.channel, pre_text(help_msg))

setup_all_events(client, bot_name, logger)
if __name__ == "__main__":
    run_the_bot(client, bot_name, logger)
