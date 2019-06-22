from datetime import datetime
import asyncio
import random
import json
import os
import discord
from discord.ext import commands

os.chdir(r'C:\Users\acaci\PycharmProjects\discordbots\venv\Include')

class Inventory:
    def __init__(self, client):
        self.client = client
        self.perishables = ['coconut', 'mango', 'papaya', 'passion_fruit', 'medicinal_herb', 'banana']
        self.conditions = {1: 'green', 2: 'ripe', 3: 'overripe'}
    @commands.command(pass_context = True,
                      aliases=['inv'])
    async def inventory(self,context):

        with open('usersjson', 'r') as f:  # read json file to users
            users = json.load(f)

        user = context.message.author.id
        usern = context.message.author.mention

        # block for ripening fruit
        if user in users:

            for item, list_amount in users[user]['inventory'].items():
                if item in self.perishables:
                    otime = list_amount[4][:-7]
                    otime = datetime.strptime(otime, "%Y-%m-%d %H:%M:%S")
                    otime = (datetime.now() - otime).total_seconds()
                    otime = int(otime)


                    if otime > 3600:
                        if list_amount[2] != 0:
                            ripe = list_amount[2]
                            users[user]['inventory'][item][2] -=  ripe
                            users[user]['inventory'][item][3] += ripe

                        if list_amount[1] != 0:
                            green = list_amount[1]
                            users[user]['inventory'][item][1] -= green
                            users[user]['inventory'][item][2] += green
                        users[user]['inventory'][item][4]=str(datetime.now())
            with open('usersjson', 'w') as f:
                json.dump(users, f)












            await self.client.say('{} has the following items: '.format(usern))
            inv_list = []
            for item, list_amount in users[user]['inventory'].items():

                if item in self.perishables:

                    if list_amount[1] != 0:
                        inv_list.append('{} {} {}(s)\n'.format(list_amount[1],self.conditions[1], item))
                    if list_amount[2] != 0:
                        inv_list.append('{} {} {}(s)\n'.format(list_amount[2], self.conditions[2], item))
                    if list_amount[3] != 0:

                        inv_list.append('{} {} {}(s)\n'.format(list_amount[3], self.conditions[3], item))

                if item not in self.perishables:
                    inv_list.append('{} {}(s)\n'.format(list_amount[0], item))

            full_list = ''.join(inv_list)
            await self.client.say(full_list)
        else:
                await self.client.say('{} has nothing in their inventory.'.format(context.message.author.mention))

    @commands.command(pass_context=True,
                      aliases=['toss'])
    async def discard(self, context, amount, name):
        amount = int(amount)
        with open('usersjson', 'r') as f:  # read json file to users
            users = json.load(f)
        user = context.message.author.id
        if user in users:
            print(str(user in users))
            if users[user]['inventory'][name][0] == amount:
                del users[user]['inventory'][name]
                await self.client.say('Tossed all {}(s)'.format(name))
            elif name in self.perishables:
                print(str (name in self.perishables))
                print(str(users[user]['inventory'][name][0] < amount))
                print(str(users[user]['inventory'][name][0]))
                if users[user]['inventory'][name][0] > amount:
                    users[user]['inventory'][name][0] -= amount
                    lessfruit = amount
                    if users[user]['inventory'][name][3] != 0:
                        amount -= users[user]['inventory'][name][0]
                        users[user]['inventory'][name][3] -= lessfruit
                        await self.client.say('Tossed {} {} {}(s)'.format(str(lessfruit), self.conditions[3], name))
                    elif users[user]['inventory'][name][2] != 0 and amount !=0:
                        lessfruit = amount
                        amount -= users[user]['inventory'][name][2]
                        users[user]['inventory'][name][2] -= lessfruit
                        await self.client.say('Tossed {} {} {}(s)'.format(str(lessfruit), self.conditions[2], name))

                    elif users[user]['inventory'][name][1] != 0 and amount !=0:
                        users[user]['inventory'][name][2] -= amount
                        await self.client.say('Tossed {} {} {}(s)'.format(str(amount), self.conditions[3], name))

            else:
                users[user]['inventory'][name][0] -= amount
                await self.client.say('Tossed {} {}(s)'.format(str(amount), name))

            with open('usersjson', 'w') as f:
                json.dump(users, f)

    @commands.command(pass_context=True
                      )
    async def eat (self, context, food):
        with open('usersjson', 'r') as f: #open users json file and read to users, user is message author
            users = json.load(f)
            user = context.message.author.id
        #block for ripening fruit
        if user in users:

            for item, list_amount in users[user]['inventory'].items():
                if item in self.perishables:
                    otime = list_amount[4][:-7]
                    otime = datetime.strptime(otime, "%Y-%m-%d %H:%M:%S")
                    otime = (datetime.now() - otime).total_seconds()
                    otime = int(otime)
                    if otime > 3600:
                        if list_amount[2] != 0:
                            ripe = list_amount[2]
                            users[user]['inventory'][item][2] -= ripe
                            users[user]['inventory'][item][3] += ripe

                        if list_amount[1] != 0:
                            green = list_amount[1]
                            users[user]['inventory'][item][1] -= green
                            users[user]['inventory'][item][2] += green
                        users[user]['inventory'][item][4] = str(datetime.now())
            with open('usersjson', 'w') as f:
                json.dump(users, f)
            #block for ripening fruit ends
        if user not in users: #if user not in json file, give message and end function
            self.client.say("Try gathering food first.")
            return
        if not users[user]['Hungry'][1] and "541324003864870932" not in [y.id for y in context.message.author.roles] :  # if user has false in Hungry[1] value then don't perform function, tell user
            await self.client.say('{} is not hungry'.format(context.message.author.mention))
            return

        if food in users[user]['inventory'] and food == 'medicinal_herb': #if user has medicinal herb
                high_cure = random.randint(1, 2) # cure ratios
                low_cure = random.randint(1,3)

                if users[user]['inventory'][food][1] >=1: #if  have at least one green medicinal herb
                    print('fresh med herb')
                    users[user]['inventory'][food][1] -=1 #subtract from green
                    users[user]['inventory'][food][0] -= 1 #subtract from total herbs
                    with open('usersjson', 'w') as f:      #update json from users
                        json.dump(users, f)
                    if high_cure % 2 == 0 and "541324003864870932" in [y.id for y in context.message.author.roles]:
                        #if high cure made it and if user is sick remove sick tell user
                        role = discord.utils.get(context.message.server.roles, name='Sick')
                        await self.client.remove_roles(context.message.author, role)
                        await self.client.say('{} was cured of any ailments!'.format(context.message.author.mention))

                    else:
                        self.client.say('medicinal_herb had no effect')

                elif users[user]['inventory'][food][2] >= 1: #if have at least one ripe herb
                    users[user]['inventory'][food][2] -= 1   # decrease ripe herbs by one
                    users[user]['inventory'][food][1] -= 1   # decrease total herbs by one
                    with open('usersjson', 'w') as f:        # write changes
                        json.dump(users, f)
                    if low_cure % 3 == 0: #if herb succesful remove sick role tell user
                        role = discord.utils.get(context.message.server.roles, name='Sick')
                        await self.client.remove_roles(context.message.author, role)
                        await self.client.say('{} was cured of any ailments!')

                    else:
                        self.client.say('medicinal_herb had no effect')

                else:
                    await self.client.say(
                        'Eating rotten herbs will only make or keep {} sick.'.format(context.message.author.mention))
                    users[user]['inventory'][food][0] -= 1
                    users[user]['inventory'][food][3] -= 1
                    if users[user]['inventory'][food][0] == 0:
                        del users[user]['inventory'][food]
                    with open('usersjson', 'w') as f:
                        json.dump(users, f)
                return

        if users[user]['inventory'][food][0] == 0:
            del users[user]['inventory'][food]
            with open ('usersjson', 'w') as f:
                    json.dump(users, f)



        if  users[user]['inventory'][food][2] >= 1: #if user has food that is ripe
            print('food in inventory and ripe')
            users[user]['inventory'][food][2] -= 1 #decrement ripe fruit by one
            users[user]['inventory'][food][0] -= 1 #decrement total fruit by one
            role = discord.utils.get(context.message.server.roles, name='Weakened')

            await self.client.remove_roles(context.message.author, role) #remove sick role
            await self.client.say('{} recovered their strength.'.format(context.message.author.mention))
            users[user]['Hungry'][0] = (str(datetime.now())) #give new timestamp for hunger
            users[user]['Hungry'][1] = False
            if users[user]['inventory'][food][0] == 0:
                del users[user]['inventory'][food]


            with open ('usersjson', 'w') as f:
                json.dump(users, f)
            return
        elif users[user]['inventory'][food][3] >= 1: #if user has overripe fruit
            print('food in inventory and overrripe')
            users[user]['inventory'][food][0] -= 1 #decrement user overripe fruit
            users[user]['inventory'][food][3] -= 1 #decrement total fruit

            with open('usersjson', 'w') as f:
                json.dump(users, f)

            bad_fruit = random.randint(1, 3)
            if bad_fruit % 3 == 0: #if a bad fruit tell user and get sick role
                await self.client.say('{} got sick off bad food!'.format(context.message.author.mention))
                role = discord.utils.get(context.message.server.roles, name='Sick')
                await self.client.add_roles(context.message.author, role)

            else: #recover strength if not bad fruit
                await self.client.say('{} recovered their strength.'.format(context.message.author.mention))
                users[user]['Hungry'][0] = (str(datetime.now()))
                users[user]['Hungry'][1] = False

                with open('usersjson', 'w') as f:
                    json.dump(users, f)

        elif users[user]['inventoru'][food][1] >= 1: #else if user has green fruit
            await self.client.say("Only green {}(s) left, its best to let it ripen.".format(food))

        if users[user]['inventory'][food][0] == 0:
            del users[user]['inventory'][food]
            with open('usersjson', 'w') as f:
                json.dump(users, f)










def setup(client):
    client.add_cog(Inventory(client))
