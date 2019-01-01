#!/usr/bin/env python3.6
#-*- coding: utf-8 -*-

import wolframalpha
import re
from . import urlmarker
from random import randint, choice
import requests
from linereader import dopen
from . import catapi
import json
from utils import *
import discord
from discord.ext import commands

wrclient = wolframalpha.Client(read_key('wolfram'))

cat_facts = ["In the Middle Ages, during the Festival of Saint John, cats were burned alive in town squares.","Six-toed kittens are so common in Boston and surrounding areas of Massachusetts that experts consider it an established mutation.","The cat's front paw has 5 toes, but the back paws have 4. Some cats are born with as many as 7 front toes and extra back toes (polydactl).","Cat's urine glows under a black light.","Cats can be prone to fleas in the summertime: 794 fleas were counted on one cat by a Cats Protection volunteer in the summer of 1992.","Cats have an average of 24 whiskers, arranged in four horizontal rows on each side.","Contrary to popular belief, the cat is a social animal. A pet cat will respond and answer to speech , and seems to enjoy human companionship.","Many cats love having their forehead gently stroked.","Jaguars are the only big cats that don't roar.","A sexually-active feral tom-cat \"owns\" an area of about three square miles and \"sprays\" to mark his territory with strong smelling urine.","Almost 10% of a cat's bones are in its tail, and the tail is used to maintain balance.","Cats come back to full alertness from the sleep state faster than any other creature.","Many cats cannot properly digest cow's milk. Milk and milk products give them diarrhea.","A cat uses its whiskers for measuring distances. The whiskers of a cat are capable of registering very small changes in air pressure.","Ancient Egyptian family members shaved their eyebrows in mourning when the family cat died.","Most cats killed on the road are un-neutered toms, as they are more likely to roam further afield and cross busy roads.","Cats should not be fed tuna exclusively, as it lacks taurine, an essential nutrient required for good feline health.","A tortoiseshell is black with red or orange markings and a calico is white with patches of red, orange and black.","The leopard is the most widespread of all big cats.","The color of the points in Siamese cats is heat related. Cool areas are darker.","A happy cat holds her tail high and steady.","A cat sees about 6 times better than a human at night.","Julius Ceasar, Henri II, Charles XI, and Napoleon were all afraid of cats.","Cats do not think that they are little people. They think that we are big cats.","An adult lion's roar can be heard up to five miles (eight kilometers) away.","A cat has approximately 60 to 80 million olfactory cells (a human has between 5 and 20 million).","Both humans and cats have identical regions in the brain responsible for emotion.","If your cat snores or rolls over on his back to expose his belly, it means he trusts you.","A cat's normal pulse is 140-240 beats per minute.","There are approximately 100 breeds of cat.","Cats can be right-pawed or left-pawed.","The word cat refers to a family of meat-eating animals that include tigers, lions, leopards, and panthers.","Cats have true fur, in that they have both an undercoat and an outercoat.","Cats sleep 16 to 18 hours per day.","A female cat may have 3 to 7 kittens every 4 months.","A cat can jump even 7 times as high as it is tall.","Cats respond better to women than to men.","You can tell a cat's mood by looking into its eyes.","Cats must have fat in their diet because they can't produce it on their own.","Cats with white fur and skin on their ears are very prone to sunburn.","Cats respond most readily to names that end in an \"ee\" sound.","A cat can spend 5 or more hours a day grooming.","Cats take between 20 to 40 breaths per minute.","Kittens remain with their mother until the age of 9 weeks.","It is estimated that cats can make over 60 different sounds.","A queen (female cat) can begin mating when she is between 5 and 9 months old.","A cat is pregnant for about 58 to 65 days.","A tomcat (male cat) can begin mating when he is between 7 and 10 months old.","The cat has 500 skeletal muscles.","Cats have 30 teeth: 12 incisors, 10 premolars, 4 canines, and 4 molars.","A cat cannot see directly under its nose. This is why cats appear unable to find tidbits on the floor.","A group of cats is called a chowder.","Female cats tend to be right pawed while males tend to be left pawed.","Cats can't climb down trees headfirst because all their claws point the same way. They must back down.","The first cat in space was a French cat named Felicette.","Around 40 thousand people are bitten by cats in the U.S. every year.","Cats can travel at a top speed of about 49 km/h (31 mph) over short distances.","The largest known litter of cats had 19 kittens.","Smuggling a cat out of ancient Egypt was punishable by death.","The Siberian Tiger is the largest wild cat species. They can grow to more than 3.6m (12 ft) and 317 kg (700 lbs).","The Black-footed Cat is the smallest wild cat species. Females are less than 50cm (20 inches) and 1.2kg (2.5 lbs).","Persian cats are the most popular pedigree.","Cats do not like water because their fur does not insulate well when it's wet.","Cats have about 12 whiskers on each side of their faces.","Cats have better night vision than humans, but cannot perceive colors as well.","In the original version of Cinderella, the fairy godmother was a cat.","Cats rarely meow at each other- this is generally reserved for humans.","A cat's jaw cannot move sideways, so they cannot chew large chunks of food.","All cats have claws, and all except the cheetah sheath them when at rest.","The cheetah is unique in the cat family because it runs down its prey instead of stalking and leaping.","One reason kittens are often sleeping is because a growth hormone is only released during sleep.","A cat's normal body temperature is between 100.5 and 102.5 Fahrenheit.","If they have enough water, cats can tolerate temperatures up to 133 Fahrenheit.","A cat's heart beats nearly twice as fast as a human's. About 110 to 140 beats a minute.","Cats are able to detect earthquake tremors about 10 or 15 minutes before humans can.","Cats can be allergic to humans.","Cats develop strategies for sharing space with other domestic cats.","Cats may drink water by licking it off their paws if they don't like the shape of their drinking bowl.","Cats can drink salt water to stay hydrated. Their kidneys can filter out the salt.","Cats sweat through their paws. Whenever they walk or scratch something they mark their territory.","Disneyland owns more than 200 cats. They are released every night to hunt down mice in the park.","Cats are more likely to be hurt falling from a 6 story building than a 32 story building."]

help_msg = '''
Commands available:
!wrq - Ask Wolfram Alpha
!cat - Shows an image of a random cuddly kitty :)
!rtd - Roll dice
!robot - Generate a unique robot
!eball - Ask the 8-ball
!choose - Make Bastion choose
!catfacts - Bastion tells you a cat fact
!doge - Get a doge
!dog - Shows an image of a random puppy :D
!botinfo - Displays developer information

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
Cat pictures\n
Treat yourself to a picture of a cuddly kitty! Can let Bastion pick for you or provide the ID of a cat you want to see! Can also vote (1-10), favourite, and report pictures.

Example:
!cat
!cat list categories
!cat category <category item>
!cat id <image id>
!cat id <image id> vote <1-10>
!cat favourites
!cat id <image id> addfav
!cat id <image id> remfav
!cat id <image id> report <reason>
'''

info_string = '''
Bastion is a bot created by Bryan Orabutt. This bot is a pet project intended only for use in friend's servers. The source code is available for free under MIT liscense located here: https://github.com/BryanOrabutt/discbot

To contact me about any questions or comments with regards to Bastion please use one of the points of contact listed below:
email: bryan.orabutt@gmail.com
discord: borabut#7826
'''

help_info = '''
Bot Developer information\n
Displays information about the bot and it's developer for those that are curious.

Example:
!botinfo
'''

help_choose = '''
Choose\n
For when you're in a quandry that only Bastion can solve. Give Bastion a list of choices and he will tell you which one is the best choice for you!

Examples:
!choose watch Netflix, play Overwatch, contemplate my existence
'''

help_catfacts = '''
Catfacts\n
Bastion know's all there is to know about cats and is happy to share!

Example:
!catfacts
'''

help_doge = '''
Doge\n
Wow, such doge

Examples:
!doge wow, such doge, very excite, wow
!doge msg1, msg2, msg3, etc
'''

help_dog = '''
Dog\n
Shows a randome cuddly puppy :D

Example:
!dog
'''

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dog',aliases=['puppers','doggos'])
    async def dog(self, ctx):
        """
        Retrieves a random dog for your viewing pleasure!
        example: !dog
        """
        resp = requests.get('https://random.dog/woof')
        dog = 'http://random.dog/' + str(resp.text)
        return await ctx.send(str(dog))


    @commands.command(name='doge')
    async def doge(self, ctx, *, msg: str):
        """
        Doge speaks the truth. Wow.
        example: !doge doge is very cool, such awesome, wow
        """

        doge = 'http://dogr.io'
        tokens = msg.replace(' ', '').split(',')
        for word in tokens:
            doge = doge + '/' + word
        doge = doge + '.png'
        return await ctx.send(str(doge)) 
        

    @commands.command(name='catfacts',aliases=['cf', 'catf'])
    async def catfacts(self, ctx):
        """
        Learn more about cats from Bastion.
        example: !catfacts
        """

        num = randint(0, len(cat_facts)-1);
        return await ctx.send(str(cat_facts[num]))


    @commands.command(name='choose',aliases=['choices','pick'])
    async def choose(self, ctx, *, msg: str):
        """
        Bastion will choose for you.
        example: !choose a, b, c
        """

        choices = msg.split(',')
        c = randint(0, len(choices)-1)
        return await ctx.send(str(choices[c]))


    @commands.command(name='botinfo',aliases=['info','owner'])
    async def botinfo(self, ctx):
        return await ctx.send(pre_text(info_string))


    @commands.command(name='eball',aliases=['eightball','eb','ball'])
    async def eball(self, ctx, *, msg: str):
        """
        Bastion doubles as a magic 8-ball
        example: !eball Am I cool?
        """

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
        return await ctx.send(answers[index])


    @commands.command(name='robot',aliases=['robots','robo'])
    async def robot(self, ctx, *, msg: str):
        """
        Generates a unique robot from hashing your input string.
        example: !robot Bastion
        """
        if(msg == ''):
            msg = 'Bastion'
        roboname = 'https://robohash.org/' + str(msg)
        roboname = roboname.replace(' ', '%20')
        roboname = roboname.replace('\'', '%27')
        return await ctx.send(roboname)


    @commands.command(name='rtd',aliases=['dice','roll'])
    async def rtd(self, ctx, msg: str):
        """
        Roll a d<N> dice <X> number of times
        Example: !rtd 2d10 - rolls two d10 dice
        """

        if msg == "":
            return await ctx.send("You didn't say anything!")
        try:
            times, sides = list(map(int, msg.lower().split("d")))
            res = [randint(1, sides) for x in range(times)]
            return await ctx.send(", ".join(map(str, res)))
        except Exception as ex:
            logger("Error: {}".format(ex))
        return await ctx.send("Error: bad input args")


    @commands.command(name='cat',aliases=['kitties','kitters','cats','kitten','kittens'])
    async def cat(self, ctx, msg: str=''):
        """
        Retrieves a random cat image for the user.
        Example: !cat
        """

        if msg == '':
            img,imgid = catapi.getCat(None,None)
            returnmsg = img + '\nimage id = ' + imgid
            return await ctx.send(returnmsg)
        else:
            items = ctx.message.content.split(' ')
            if str(items[1]) == 'list':
                categories = catapi.getCategories()
                categories.remove('kittens')
                returnmsg = '\n'.join(categories)
                returnmsg += '\nhats'
                return await ctx.send(pre_text(returnmsg))
            elif str(items[1]) == 'category':
                img,imgid = catapi.getCat(None,str(items[2]))
                returnmsg = img + '\nimage id=' + join(imgid)
                return await ctx.send(returnmsg)
            elif str(items[1]) == 'favourites':
                favs = catapi.getFavs(ctx.message.author.id)
                returnmsg = '\n'.join(favs)
                return await ctx.send(returnmsg)
            elif str(items[1]) == 'id':
                if len(items) == 2:
                    img,imgid = catapi.getCat(str(items[2]),None)
                    returnmsg = img + '\nimage id=' + imgid
                    return await ctx.send(returnmsg)
                elif str(items[3]) == 'vote':
                    catapi.vote(str(ctx.message.author.id), str(items[2]), str(items[4]))
                    return await ctx.send("Thanks for voting!")
                elif str(items[3]) == 'addfav':
                    catapi.favourite(ctx.message.author.id, str(items[2]), 'add')
                    return await ctx.send("You have added a cat to your favourites.")
                elif str(items[3]) == 'remfav':
                    catapi.favourite(ctx.message.author.id, str(items[2]), 'remove')
                    return await ctx.send("You have removed a cat from your favourites.")
                elif str(items[3]) == 'report':
                    return await ctx.send("You have reported a cat image. Thanks for helping us make our service better!")
            else:
                return await ctx.send("Invalid input")


    @commands.command(name='wrq',aliases=['wolfram','math','wra'])
    async def wrq(self, ctx, *, msg: str):
        """
        Queries wolfram alpha using the provided message and returns the image data.
        Example: !wrq plot x^2
        """

        res = wrclient.query(msg)
        results = ''
        for pod in res.pods:
            for sub in pod.subpods:
                 imgs = re.findall(urlmarker.URL_REGEX, str(sub))
                 for s in imgs:
                     results = results + s + ' '
        return await ctx.send(results)    


    @commands.command(name='howto',aliases=['faq','commands','list'])
    async def howto(self, ctx, *, msg: str='default'):
        """
        Displays a general help message about available commands, or a specific help
        message for a provided command.
        Example 1: !howto
        Example 2: !howto wrq
        """
        
        #msg = ctx.message.content
        #msg = re.findall('\s(.*)', msg)

        if(msg == 'wrq'):
            return await ctx.send(pre_text(help_wrq))
        elif(msg == 'cat'):
            return await ctx.send(pre_text(help_cat))
        elif(msg == 'rtd'):
            return await ctx.send(pre_text(help_rtd))
        elif(msg == 'eball'):
            return await ctx.send(pre_text(help_eball))
        elif(msg == 'robot'):
            return await ctx.send(pre_text(help_robot))
        elif(msg == 'choose'):
            return await ctx.send(pre_text(help_choose))    
        elif(msg == 'botinfo'):
            return await ctx.send(pre_text(help_info))
        elif(msg == 'catfacts'):
            return await ctx.send(pre_text(help_catfacts))
        elif(msg == 'doge'):
            return await ctx.send(pre_text(help_doge))    
        elif(msg == 'dog'):
            return await ctx.send(pre_text(help_dog))
        else:
            return await ctx.send(pre_text(help_msg))

def setup(bot):
    bot.add_cog(Commands(bot))

