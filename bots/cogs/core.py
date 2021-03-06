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

info_string = '''
Bastion is a bot created by Bryan Orabutt. This bot is a pet project intended only for use in friend's servers. The source code is available for free under MIT liscense located here: https://github.com/BryanOrabutt/discbot
To contact me about any questions or comments with regards to Bastion please use one of the points of contact listed below:
email: bryan@bryanorabutt.com
discord: borabut#7826
'''

cat_facts = ["In the Middle Ages, during the Festival of Saint John, cats were burned alive in town squares.","Six-toed kittens are so common in Boston and surrounding areas of Massachusetts that experts consider it an established mutation.","The cat's front paw has 5 toes, but the back paws have 4. Some cats are born with as many as 7 front toes and extra back toes (polydactl).","Cat's urine glows under a black light.","Cats can be prone to fleas in the summertime: 794 fleas were counted on one cat by a Cats Protection volunteer in the summer of 1992.","Cats have an average of 24 whiskers, arranged in four horizontal rows on each side.","Contrary to popular belief, the cat is a social animal. A pet cat will respond and answer to speech , and seems to enjoy human companionship.","Many cats love having their forehead gently stroked.","Jaguars are the only big cats that don't roar.","A sexually-active feral tom-cat \"owns\" an area of about three square miles and \"sprays\" to mark his territory with strong smelling urine.","Almost 10% of a cat's bones are in its tail, and the tail is used to maintain balance.","Cats come back to full alertness from the sleep state faster than any other creature.","Many cats cannot properly digest cow's milk. Milk and milk products give them diarrhea.","A cat uses its whiskers for measuring distances. The whiskers of a cat are capable of registering very small changes in air pressure.","Ancient Egyptian family members shaved their eyebrows in mourning when the family cat died.","Most cats killed on the road are un-neutered toms, as they are more likely to roam further afield and cross busy roads.","Cats should not be fed tuna exclusively, as it lacks taurine, an essential nutrient required for good feline health.","A tortoiseshell is black with red or orange markings and a calico is white with patches of red, orange and black.","The leopard is the most widespread of all big cats.","The color of the points in Siamese cats is heat related. Cool areas are darker.","A happy cat holds her tail high and steady.","A cat sees about 6 times better than a human at night.","Julius Ceasar, Henri II, Charles XI, and Napoleon were all afraid of cats.","Cats do not think that they are little people. They think that we are big cats.","An adult lion's roar can be heard up to five miles (eight kilometers) away.","A cat has approximately 60 to 80 million olfactory cells (a human has between 5 and 20 million).","Both humans and cats have identical regions in the brain responsible for emotion.","If your cat snores or rolls over on his back to expose his belly, it means he trusts you.","A cat's normal pulse is 140-240 beats per minute.","There are approximately 100 breeds of cat.","Cats can be right-pawed or left-pawed.","The word cat refers to a family of meat-eating animals that include tigers, lions, leopards, and panthers.","Cats have true fur, in that they have both an undercoat and an outercoat.","Cats sleep 16 to 18 hours per day.","A female cat may have 3 to 7 kittens every 4 months.","A cat can jump even 7 times as high as it is tall.","Cats respond better to women than to men.","You can tell a cat's mood by looking into its eyes.","Cats must have fat in their diet because they can't produce it on their own.","Cats with white fur and skin on their ears are very prone to sunburn.","Cats respond most readily to names that end in an \"ee\" sound.","A cat can spend 5 or more hours a day grooming.","Cats take between 20 to 40 breaths per minute.","Kittens remain with their mother until the age of 9 weeks.","It is estimated that cats can make over 60 different sounds.","A queen (female cat) can begin mating when she is between 5 and 9 months old.","A cat is pregnant for about 58 to 65 days.","A tomcat (male cat) can begin mating when he is between 7 and 10 months old.","The cat has 500 skeletal muscles.","Cats have 30 teeth: 12 incisors, 10 premolars, 4 canines, and 4 molars.","A cat cannot see directly under its nose. This is why cats appear unable to find tidbits on the floor.","A group of cats is called a chowder.","Female cats tend to be right pawed while males tend to be left pawed.","Cats can't climb down trees headfirst because all their claws point the same way. They must back down.","The first cat in space was a French cat named Felicette.","Around 40 thousand people are bitten by cats in the U.S. every year.","Cats can travel at a top speed of about 49 km/h (31 mph) over short distances.","The largest known litter of cats had 19 kittens.","Smuggling a cat out of ancient Egypt was punishable by death.","The Siberian Tiger is the largest wild cat species. They can grow to more than 3.6m (12 ft) and 317 kg (700 lbs).","The Black-footed Cat is the smallest wild cat species. Females are less than 50cm (20 inches) and 1.2kg (2.5 lbs).","Persian cats are the most popular pedigree.","Cats do not like water because their fur does not insulate well when it's wet.","Cats have about 12 whiskers on each side of their faces.","Cats have better night vision than humans, but cannot perceive colors as well.","In the original version of Cinderella, the fairy godmother was a cat.","Cats rarely meow at each other- this is generally reserved for humans.","A cat's jaw cannot move sideways, so they cannot chew large chunks of food.","All cats have claws, and all except the cheetah sheath them when at rest.","The cheetah is unique in the cat family because it runs down its prey instead of stalking and leaping.","One reason kittens are often sleeping is because a growth hormone is only released during sleep.","A cat's normal body temperature is between 100.5 and 102.5 Fahrenheit.","If they have enough water, cats can tolerate temperatures up to 133 Fahrenheit.","A cat's heart beats nearly twice as fast as a human's. About 110 to 140 beats a minute.","Cats are able to detect earthquake tremors about 10 or 15 minutes before humans can.","Cats can be allergic to humans.","Cats develop strategies for sharing space with other domestic cats.","Cats may drink water by licking it off their paws if they don't like the shape of their drinking bowl.","Cats can drink salt water to stay hydrated. Their kidneys can filter out the salt.","Cats sweat through their paws. Whenever they walk or scratch something they mark their territory.","Disneyland owns more than 200 cats. They are released every night to hunt down mice in the park.","Cats are more likely to be hurt falling from a 6 story building than a 32 story building."]


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='50/50', aliases=['ff'])
    async def fifty_fifty(self, ctx, *, msg: str='<none>'):
        """
        50/50 chance of Bastion complimenting or insulting someone.
        
        Example:
        !50/50 <name>
        !50/50
        """
        toss = randint(0,1)

        jm = 141039412862648321

        if(ctx.message.author.id == jm or msg.lower() == 'john moan'):
            toss = randint(0, 999)
                        

        if(toss == 0):
            resp = requests.get('https://www.complimentr.com/api')
            ans = re.findall(r'(?<="compliment":.)([^"]+)', resp.text)[0]
            if(msg != '<none>'):
                fix = '' + msg + ' is'
                ans = ans.replace("you are", fix)
                fix = '' + msg + ' has'
                ans = ans.replace("you have", fix)
                return await ctx.send(ans.capitalize())
            else:
                return await ctx.send(ans.capitalize())
        else:
            if(msg != '<none>'):
                url = 'https://insult.mattbas.org/api/insult.txt?who=' + msg
                resp = requests.get(url)
                return await ctx.send(resp.text)
            else:
                resp = requests.get('https://insult.mattbas.org/api/insult.txt')
                return await ctx.send(resp.text)


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
        msg = msg.lower()
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
            'Outlook not so good',
            'Very doubtful'
            ]
        index = randint(0, 19)
        return await ctx.send(answers[index])


    @commands.command(name='robot',aliases=['robots','robo','kitty'])
    async def robot(self, ctx, *, msg: str):
        """
        Generates a unique robot from hashing your input string.
        example: !robot Bastion
        """
        if(msg == None):
            msg = 'Bastion'

        inp = ctx.message.content.split(' ')
        token = str(inp[0])

        roboname = 'https://robohash.org/' + str(msg)


        if(token == '!kitty'):
            roboname = roboname + '?set=set4'

        roboname = roboname.replace(' ', '%20')
        roboname = roboname.replace('\'', '%27')
        return await ctx.send(roboname)

    @commands.command(name='fuckoff',aliases=['foff','fu','fo','fuckyou','fuck'])
    async def fuckoff(self, ctx, *, msg: str='default'):
        """
        Fuck off
        examples: !fuckoff
                  !fuckoff <name>
        """

        options0 = ['asshole', 'awesome', 'bag', 'because', 'bucket', 'bye', 'cool', 'cup', 'diabetes',
                'everyone', 'everything', 'family', 'fascinating', 'flying', 'fyyff','give', 'horse',
                'immensity', 'life', 'looking', 'maybe', 'me', 'mornin', 'no', 'pink', 'question',
                'ratarse', 'retard', 'ridiculous', 'sake', 'shit', 'single', 'thanks', 'that', 'this',
                'too', 'tucker', 'what', 'zayn', 'zero']
        options1 = ['back', 'blackadder', 'bus', 'chainsaw', 'cocksplat', 'deraadt', 'donut',
                'fts', 'ing', 'keep', 'linus', 'madison', 'nugget', 'off', 'outside', 'problem', 'shakespeare',
                'shutup', 'think', 'thinking', 'yoda', 'you']

        url = 'https://www.foaas.com/'
        if msg == 'default':
            index = randint(0, len(options0)-1)
            modifier = str(options0[index])
            url = url + modifier + '/'
            content = ctx.message.content
            caller = ctx.message.author.display_name
            url = url + '%20'
            resp = requests.get(url)
            txt = re.findall(r'(?<=content=.)([^"]+)', resp.text)[0]
        else:
            index = randint(0, len(options1)-1)
            modifier = str(options1[index])
            url = url + modifier + '/' + msg + '/' + '%20'
            resp = requests.get(url)
            txt = re.findall(r'(?<=content=.)([^"]+)', resp.text)[0]
        txt = txt.replace('-', '')
        return await ctx.send(txt)

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
            total = 0
            for item in res:
                total += item
            return await ctx.send("%s\nTotal: %d" %(", ".join(map(str, res)), total))
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
            if str(items[1]) == 'list' and str(items[2]) == 'categories':
                categories = catapi.getCategories()
                returnmsg = 'categories:\n' + '\n'.join(categories)
                return await ctx.send(pre_text(returnmsg))
            elif str(items[1]) == 'category':
                category = None
                if str(items[1]) == 'category':
                    category = str(items[2])
                img,imgid = catapi.getCat(None,category)
                returnmsg = img + '\nimage id=' + join(imgid)
                return await ctx.send(returnmsg)
            elif str(items[1]) == 'favourites':
                favs = catapi.getFavs(ctx.message.author.id)
                returnmsg = '\n'.join(favs)
                return await ctx.send(returnmsg)
            elif str(items[1]) == 'id':
                if len(items) == 3:
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


def setup(bot):
    bot.add_cog(Commands(bot))
    print('Core commands loaded')
