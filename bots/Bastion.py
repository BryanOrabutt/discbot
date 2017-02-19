#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from botinfo import *
import wolframalpha
from PIL import Image
import re, urlmarker
from random import randint, choice
import requests

bot_name = "Bastion"
client = discord.Client()
logger = create_logger(bot_name)
bot_data = create_filegen(bot_name)
wrclient = wolframalpha.Client('L247V6-5JHVJQVEYE')

help_msg = '''
Commands available:
!wrq - Ask Wolfram Alpha
!cat - Shows an image of a random cuddly kitty :)
!rtd - Roll dice
!robot - Generate a unique robot
!eball - Ask the 8-ball

For more details do !howto <command> (eg. !howto eball)
'''

help_wrq ='''
Wolfram Alpha Query\n
Allows you to ask Wolfram Alpha a question and gives you the answers thatvWolfram Alpha comes up with.

Examples:
!wrq plot x^2
!wrq 5*6
!wrq number of hours in a week
'''

help_rtd ='''
Roll the dice\n
Allows you to roll dice provided the number of sides and number of rolls.

Examples:
!rtd 1d20
!rtd 3d6
!rtd 5d100
'''

help_robot = '''
Robohash generator\n
Allows you to generate a unique robot provided you give it a name.

Examples:
!robot Cyber
!robot Mr. Robot
!robot Hal 9000
'''

help_eball = '''
Ask the magic 8-ball\n
Ask your question to the magic 8-ball and get a cryptic non-answer in reply!

Examples:
!eball Should I get out of bed?
!eball Will I ever be famous?
!eball Do you hate me?
'''

help_cat = '''
Random Cat\n
Treat yourself to a picture of a random cuddly kitty!

Example:
!cat
'''

@register_command
async def eball(msg, mobj):
    answers = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes, definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy, try again later',
        'Ask again another time',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook no so good',
        'Very doubtful'
        ]
    index = randint(0, 19)
    return await client.send_message(mobj.channel, answers[index])

@register_command
async def robot(msg, mobj):
    """
    Generates a unique robot from hashing your input string.
    """
    if(msg == ''):
        msg = 'Bastion'
    roboname = 'https://robohash.org/' + str(msg)
    roboname = roboname.replace(' ', '%20')
    roboname = roboname.replace('\'', '%27')
    return await client.send_message(mobj.channel, roboname)

@register_command
async def rtd(msg, mobj):
    """
    Roll a d<N> di[c]e <X> number of times
    Example: !rtd 2d10 - rolls two d10 dice
    """
    if msg == "":
        return await client.send_message(mobj.channel, "You didn't say anything!")
    try:
        times, sides = list(map(int, msg.lower().split("d")))
        res = [randint(1, sides) for x in range(times)]
        return await client.send_message(mobj.channel, ", ".join(map(str, res)))
    except Exception as ex:
        logger("Error: {}".format(ex))
    return await client.send_message(mobj.channel, "Error: bad input args")

@register_command
async def cat(msg, mobj):
    """
    Retrieves a random cat image for the user.
    Example: !cat
    """
    resp = requests.get('http://random.cat/meow')
    img = re.sub(r'[\\]', '', resp.text)
    catlink = re.findall(urlmarker.URL_REGEX, str(img))
    return await client.send_message(mobj.channel, str(catlink[0]))

@register_command
async def wrq(msg, mobj):
    """
    Queries wolfram alpha using the provided message and returns the image data.
    Example: !wrq plot x^2
    """
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
    """
    Displays a general help message about available commands, or a specific help
    message for a provided command.
    Example 1: !howto
    Example 2: !howto wrq
    """
    if(msg == 'wrq'):
        return await client.send_message(mobj.channel, pre_text(help_wrq))
    elif(msg == 'cat'):
        return await client.send_message(mobj.channel, pre_text(help_cat))
    elif(msg == 'rtd'):
        return await client.send_message(mobj.channel, pre_text(help_rtd))
    elif(msg == 'eball'):
        return await client.send_message(mobj.channel, pre_text(help_eball))
    elif(msg == 'robot'):
        return await client.send_message(mobj.channel, pre_text(help_robot))
    else:
        return await client.send_message(mobj.channel, pre_text(help_msg))

setup_all_events(client, bot_name, logger)
if __name__ == "__main__":
    run_the_bot(client, bot_name, logger)
