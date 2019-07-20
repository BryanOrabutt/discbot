#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import random
import math


class CombatInfo:
    BODY_LOCATIONS = [
        "Left Leg",
        "Head",
        "Torso",
        "Torso",
        "Torso",
        "Torso",
        "Right Arm",
        "Left Arm",
        "Right Leg",
        "Right Leg",
        "Left Leg"
    ]

    COMBAT_FUMBLES = [
        "null",
        "No Fumble. You just screw up.",
        "No Fumble. You just screw up.",
        "No Fumble. You just screw up.",
        "No Fumble. You just screw up.",
        "You drop your weapon.",
        "Weapon discharges or strikes something harmless.",
        "Weapon jams or imbeds itself in the ground for one turn.",
        "You manage to wound yourself.",
        "You wound a member of your party.",
        "You wound a member of your party."
    ]


class Attack:
    def _init_(self, hit=False, dmg=0, fum="", loc="", mode="Single Shot"):
        self.HitTarget = hit
        self.Damage = dmg
        self.Fumble = fum
        self.Location = loc
        self.FireMode = mode
        self.FumbleDamage = 0

    def Summary(self):
        objString = "Hit Target: " + str(self.HitTarget)
        objString += "\nDamage : " + str(self.Damage)
        objString += "\nBody Location: " + self.Location
        objString += "\nFumble: " + self.Fumble
        objString += "\nDamage done by Fumble: " + str(self.FumbleDamage)
        objString += "\nFire Mode: " + self.FireMode

        return objString


class CombatResult:
    def _init_(self):
        self.Attacks = []

    def TotalHits(self):
        hits = 0

        for atk in self.Attacks:
            if atk.HitTarget:
                hits += 1

        return hits

    def TotalMisses(self):
        misses = 0

        for atk in self.Attacks:
            if not atk.HitTarget:
                misses += 1

        return misses

    def GetTotalDamage(self):
        dmg = 0

        for atk in self.Attacks:
            if atk.HitTarget:
                dmg += atk.Damage

        return dmg

    def GetTotalFumblesMade(self):
        fumbles = []

        for atk in self.Attacks:
            if atk.Fumble != "":
                fumbles.append(atk.Fumble)

        return fumbles.count()

     def GetDamageByLocation(self, location):
        locDmg = []

        for atk in self.Attacks:
            if atk.HitTarget and atk.Location == location:
                locDmg.append(atk.Damage)

        return locDmg

    def GetDamageDetails(self):
        headDmg = self.GetDamageByLocation("Head")
        torsoDmg = self.GetDamageByLocation("Torso")
        laDmg = self.GetDamageByLocation("Left Arm")
        raDmg = self.GetDamageByLocation("Right Arm")
        llDmg = self.GetDamageByLocation("Left Leg")
        rlDmg = self.GetDamageByLocation("Right Leg")

        locationDamage = dict({'Head': headDmg, 'Torso': torsoDmg, 'Left Arm': laDmg,
                               'Right Arm': raDmg, 'Left Leg': llDmg, 'Right Leg': rlDmg})

        return locationDamage

    def Summary(self):
        attackInfo = self.GetDamageDetails()
        objStr = "Attacks Made: " + str(len(self.Attacks))
        objStr += "\nHead: " + str(attackInfo['Head'])
        objStr += "\nTorso: " + str(attackInfo['Torso'])
        objStr += "\nLeft Arm: " + str(attackInfo['Left Arm'])
        objStr += "\nRight Arm: " + str(attackInfo['Right Arm'])
        objStr += "\nLeft Leg: " + str(attackInfo['Left Leg'])
        objStr += "\nRight Leg: " + str(attackInfo['Right Leg'])
        objStr += "\n\nFumbles Made: " + str(self.GetTotalFumblesMade())
        objStr += "\n\nTotal Hits: " + str(self.TotalHits())
        objStr += "\nTotal Misses: " + str(self.TotalMisses())
        objStr += "\nTotal Damage: " + str(self.GetTotalDamage())

        return objStr


class Combat:
    def __init__(self, bot):
        self.bot = bot

    Info = CombatInfo()

    def RollHitLocation(self):
        diceResult = random.randrange(1, 10)
        location = self.Info.BODY_LOCATIONS[diceResult]
        return location

    def RollCombatFumble(self):
        diceResult = random.randrange(1, 10)
        fumble = self.Info.COMBAT_FUMBLES[diceResult]
        return fumble

    def RollBurstbulletsHit(self):
        diceResult = random.randrange(1, 6)
        bulletsLanded = math.ceil(diceResult/2)
        return bulletsLanded

    def RollDamage(self, numOfDice, sides, mod):
        dmg = 0

        for di in range(numOfDice):
            dmg += random.randrange(1, sides)

        dmg += mod

        return dmg

    def RollSingleShotAttack(self, reflex, skill, numOfDice, sides, mod, distance):
        info = CombatInfo()
        combatResult = CombatResult()
        attacks = []
        anAttack = Attack()
        diceResult = random.randrange(1, 10)
        attackRoll = diceResult + reflex + skill
        damage = self.RollDamage(numOfDice, sides, mod)

        if attackRoll >= distance:
            anAttack.HitTarget = True
            anAttack.Damage = damage
            anAttack.FireMode = "Single Shot"
            anAttack.Location = self.RollHitLocation()
            anAttack.Fumble = ""
            anAttack.FumbleDamage = 0

            if diceResult == 1:
                fumbleResult = random.randrange(1, 10)
                anAttack.Fumble = info.COMBAT_FUMBLES[fumbleResult]

                if fumbleResult >= 8:
                    fumbleDamage = combat.RollDamage(numOfDice, sides, 0)
                    anAttack.FumbleDamage = fumbleDamage

            attacks.append(anAttack)

        else:
            anAttack.HitTarget = False
            anAttack.Damage = 0
            anAttack.FireMode = "Single Shot"
            anAttack.Location = "Miss"
            anAttack.Fumble = ""
            anAttack.FumbleDamage = 0
            attacks.append(anAttack)

        combatResult.Attacks = attacks
        return combatResult

    def RollBurstAttack(self, reflex, skill, numOfDice, sides, mod, distance):
        info = CombatInfo()
        attacks = []
        combatResult = CombatResult()
        diceResult = random.randrange(1, 10)
        attackRoll = diceResult + reflex + skill + 3
        bulletslanded = self.RollBurstbulletsHit()
        remainder = 3 - bulletslanded

        if attackRoll >= distance:
            for i in range(bulletslanded):
                anAttack = Attack()
                anAttack.HitTarget = True
                anAttack.Location = self.RollHitLocation()
                anAttack.Damage = self.RollDamage(numOfDice, sides, mod)
                anAttack.FireMode = "Burst"
                anAttack.Fumble = ""
                anAttack.FumbleDamage = 0

                if diceResult == 1:
                    fumbleResult = random.randrange(1, 10)
                    anAttack.Fumble = info.COMBAT_FUMBLES[fumbleResult]

                    if fumbleResult >= 8:
                        fumbleDamage = combat.RollDamage(numOfDice, sides, 0)
                        anAttack.FumbleDamage = fumbleDamage

                attacks.append(anAttack)

            if remainder > 0:
                for i in range(remainder):
                    anAttack = Attack()
                    anAttack.HitTarget = False
                    anAttack.Damage = 0
                    anAttack.Location = "Miss"
                    anAttack.FireMode = "Burst"
                    anAttack.Fumble = ""
                    anAttack.FumbleDamage = 0
                    attacks.append(anAttack)

        else:
            for i in range(3):
                anAttack = Attack()
                anAttack.HitTarget = False
                anAttack.Damage = 0
                anAttack.Location = "Miss"
                anAttack.FireMode = "Burst"
                anAttack.Fumble = ""
                anAttack.FumbleDamage = 0
                attacks.append(anAttack)

        combatResult.Attacks = attacks
        return combatResult

    def RollFullAutoAttack(self, reflex, skill, shotsFired, numOfDice, sides, mod, distance):
        info = CombatInfo()
        attacks = []
        combatResult = CombatResult()
        diceResult = random.randrange(1, 10)
        attackBonus = int(shotsFired / 10)
        attackRoll = diceResult + reflex + skill + attackBonus
        bulletslanded = abs(attackRoll - distance)
        remainder = shotsFired - bulletslanded

        if bulletslanded > 0:
            for i in range(bulletslanded):
                anAttack = Attack()
                anAttack.HitTarget = True
                anAttack.Location = self.RollHitLocation()
                anAttack.Damage = self.RollDamage(numOfDice, sides, mod)
                anAttack.FireMode = "Full Auto"
                anAttack.Fumble = ""
                anAttack.FumbleDamage = 0

                if diceResult == 1:
                    fumbleResult = random.randrange(1, 10)
                    anAttack.Fumble = info.COMBAT_FUMBLES[fumbleResult]

                    if fumbleResult >= 8:
                        fumbleDamage = combat.RollDamage(numOfDice, sides, 0)
                        anAttack.FumbleDamage = fumbleDamage

                attacks.append(anAttack)

            if remainder > 0:
                for i in range(remainder):
                    anAttack = Attack()
                    anAttack.HitTarget = False
                    anAttack.Damage = 0
                    anAttack.FireMode = "Full Auto"
                    anAttack.Location = "Miss"
                    anAttack.Fumble = ""
                    anAttack.FumbleDamage = 0

                    attacks.append(anAttack)

        else:
            for i in range(shotsFired):
                anAttack = Attack()
                anAttack.HitTarget = False
                anAttack.Damage = 0
                anAttack.FireMode = "Full Auto"
                anAttack.Location = "Miss"
                anAttack.Fumble = ""
                anAttack.FumbleDamage = 0

                attacks.append(anAttack)

        combatResult.Attacks = attacks
        return combatResult

    @commands.command(name="SingleShot", aliases=['Shoot'])
    async def single_shot(self, ctx, *, msg: str):
        """
            Performs a Combat roll for a single shot attack.

            Example:
            !SingleShot reflex, skill, number of dice, dice sides, damage modifier, distance
        """
        params = msg.split(',')

        if(len(params) == 6):
            result = self.RollSingleShotAttack(
                int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]))
            await ctx.send(result.Summary())
        else:
            await ctx.send('You are missing a piece of information.')

    @commands.command(name="BurstShot", aliases=['Burst'])
    async def burst_shot(self, ctx, *, msg: str):
        """
            Performs a Combat roll for a burst attack.

            Example:
            !BurstShot reflex, skill, number of dice, dice sides, damage modifier, distance
        """
        params = msg.split(',')

        if(len(params) == 6):
            result = self.RollBurstAttack(
                int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]))
            await ctx.send(result.Summary())
        else:
            await ctx.send('You are missing a piece of information.')

    @commands.command(name="FullAutoShot", aliases=['FAS'])
    async def full_auto_shot(self, ctx, *, msg: str):
        """
            Performs a Combat roll for a full auto attack.

            Example:
            !FullAutoShot reflex, skill, shotsFired, number of dice, dice sides, damage modifier, distance
        """
        params = msg.split(',')

        if(len(params) == 7):
            result = self.RollFullAutoAttack(
                int(params[0]), int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]), int(params[6]))
            await ctx.send(result.Summary())
        else:
            await ctx.send('You are missing a piece of information.')


def setup(bot):
    bot.add_cog(Combat(bot))
    print('Combat loaded')
