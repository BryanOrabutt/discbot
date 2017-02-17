#!/usr/bin/env python
#-*- coding: utf-8 -*-
from botinfo import *
import wolframalpha
from PIL import Image
import re, urlmarker

bot_name = "Bastion"
client = discord.Client()
logger = create_logger(bot_name)
bot_data = create_filegen(bot_name)

help_msg = '''
Commands available:\n!wrq <query> - Queries Wolfram Alpha with the provided input query
'''

@register_command
async def WolframQuery(msg, mobj):
    try:
        with open(join(KEY_FOLDER, "{}.key".format(bot_name)), 'r') as f:
            q = f.read().strip("\n").strip("\r").replace("\n", "")
            f.close()
    except:
        raise IOError("Can't read key")

    client = wolframalpha.Client(q)
    res = client.query(str(msg))
    for pod in res.pods:
        for sub in pod.subpods:
             imgs = re.findall(urlmarker.URL_REGEX, str(sub))
             results = ''
             for s in imgs:
                 results = results + s + '\n'
     return await client.send_message(mobj.channel, pre_text(results))

@register_command
async def howto(msg, mobj):
    return await client.send_message(mobj.channel, pre_text(help_msg))
