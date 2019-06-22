from datetime import datetime
import asyncio
import random
import json
import os
import discord
from discord.ext import commands

os.chdir(r'C:\Users\acaci\PycharmProjects\discordbots\venv\Include')

class GiveCraft:
    def __init__(self, client):
        self.client = client
        self.perishables = ['coconut', 'mango', 'papaya', 'passion_fruit', 'medicinal_herb', 'banana']
        self.gather_list = ['plant_fiber', 'driftwood', 'stick','rock', 'cockle_shell', 'grass_clump', 'clay_lump', 'tar_glob']
        self.clay_bowl = ["clay_lump", "clay_lump", "clay_lump"]
        #self.hatchet =
        #self.string =
        #self.spear = []


    @commands.command(pass_context=True,
                      aliases = ['give'])
    async def Give(self,context, recipient, amount, condition, item):
        amount = int(amount)
        with open ('usersjson', 'r') as f:
            users = json.load(f)
            recipient = recipient[2:]#used to strip off characters for json
            recipient = recipient[:-1]#used to strip off characters for json
            recip_name = await self.client.get_user_info(recipient)

        user = context.message.author.id
        if user in users and item in users[user]['inventory']:
            if amount <= users[user]['inventory'][item][0] and item not in self.perishables:
                users[user]['inventory'][item][0] -= amount
                if recipient in users:
                    users[recipient]['inventory'][item][0] += amount
                    await self.client.say('{} {}(s) was given to {} '.format(amount, item, recip_name.name))
                else:
                    users[recipient]['inventory'][item][0].append(amount)
                    await self.client.say('{} {}(s) was given to {} '.format(amount, item, recip_name.name))


            elif amount <= users[user]['inventory'][item][0] and item in self.perishables:
                print('User has amount and item is perishable')
                if recipient not in users:
                    users[recipient] = {}
                    users[recipient]['inventory'] = {}
                if item not in users[recipient]['inventory']:
                    print('item made it through check of new recipient and perishable')
                    users[recipient]['inventory'][item] = [0, 0, 0, 0]
                    users[recipient]['inventory'][item].append(users[user]['inventory'][item][4])

                if condition == 'green' and users[user]["inventory"][item][1] >= amount:
                    users[recipient]['inventory'][item][0] += amount
                    users[recipient] ['inventory'][item][1] += amount
                    users[user]['inventory'][item][0] -= amount
                    users[user]['inventory'][item][1] -= amount
                    await self.client.say('{} {}(s) was given to {} '.format(amount, item, recip_name.name))

                elif condition == 'ripe' and users[user]['inventory'][item][2]>= amount:
                    users[recipient]['inventory'][item][0] += amount
                    users[recipient]['inventory'][item][2] += amount
                    users[user]['inventory'][item][0] -= amount
                    users[user]['inventory'][item][2] -= amount
                    await self.client.say('{} {}(s) was given to {} '.format(amount, item, recip_name.name))

                elif condition == 'overripe' and users[user]['inventory'][item][3]>= amount:
                    users[recipient]['inventory'][item][0] += amount
                    users[recipient]['inventory'][item][3] += amount
                    users[user]['inventory'][item][0] -= amount
                    users[user]['inventory'][item][3] -= amount
                    await self.client.say('{} {}(s) was given to {} '.format(amount, item, recip_name.name))
                else:
                    await self.client.say('Missing required items.')

            if users[user]['inventory'][item][0] == 0:
                del users[user]['inventory'][item]
            with open('usersjson', 'w') as f:
                json.dump(users, f)

    @commands.command(pass_context=True,
                      aliases = ['craft'])
    async def Craft(self,context, *item ):
        copy_bowl = self.clay_bowl
        for value in item:
            if value in copy_bowl:
                copy_bowl.pop(value)
        if not copy_bowl:


        
def setup(client):
    client.add_cog(GiveCraft(client))