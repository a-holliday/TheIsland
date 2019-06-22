from datetime import datetime
import asyncio
import random
import json
import os
import discord
from discord.ext import commands

os.chdir(r'C:\Users\acaci\PycharmProjects\discordbots\venv\Include')

class Gatherable:
    island_limit = 5
    island_count = 0
    def __init__(self, client):
        self.client = client
        self.inventorysum =0
        self.inventory = {}




    @commands.command(pass_context=True,
                      aliases=['find'])
    async def gather(self, context, food = ''):


        if Gatherable.island_count > Gatherable.island_limit:  #checks to see if island depleted
            await self.client.say("The island needs time to replenish")
            await asyncio.sleep(60)
            Gatherable.island_count = 0
            return

        gather_list = [   #all the items you can gather
            'plant_fiber',
            'driftwood',
            'rock',
            'cockle_shell',
            'grass_clump',
            'clay_lump',
            'tar_glob',
            'stick'

            ] #gather items that can go bad and their conditions
        perishables = ['coconut', 'mango', 'papaya', 'passion_fruit', 'medicinal_herb', 'banana']
        conditions = {1:'green', 2:'ripe', 3:'moldy'}

        # 0 - amount 1- green 2 - ripe 3-rotten 4 - timestamp
        if food == '':
            bounty = random.choice(gather_list) # a random non edible item is chosen place in bounty variable
        if food == 'food':
            bounty = random.choice(perishables)
        self.inventory[bounty] = []
        amount = random.randint(1, 2) # random amount generated for gathered amount
        condition = random.randint(1,2) #green or ripe fruit genereated from condition
        if amount == 0: # stop function if found nothing
            await self.client.say("{} failed to gather anything.".format(context.message.author.mention))
            return
        self.inventory[bounty].append(amount) #0 index append the amount in 0 index


            # 0 - amount 1- green 2 - ripe 3-rotten 4 - timestamp


        if bounty in perishables: #if bounty can go bad set up the other values in list for each condition

            if condition == 1:
                self.inventory[bounty].append(amount) #1 index green append amount all others 0
                self.inventory[bounty].append(0)      #2 index ripe
                self.inventory[bounty].append(0)      #3 index rotten
                self.inventory[bounty].append(str(datetime.now())) #4 index
                print('put a time on bounty', bounty)

            elif condition == 2:
                self.inventory[bounty].append(0) #1 index green
                self.inventory[bounty].append(amount) #2 index ripe append amount all others 0
                self.inventory[bounty].append(0) #3 index rotten
                self.inventory[bounty].append(str(datetime.now()))
                print('put a time on bounty', bounty)




        # fill users with json info
        with open('usersjson', 'r') as f:  # read json file to users
            users = json.load(f)
        user = str(context.message.author.id)
        usern = str(context.message.author.mention)



        if user not in users: #if new user go ahead create inventory and hungry keys
            print('new item perishable or non line 95')
            users[user]= {}
            users[user]['inventory'] = {}
            users[user]['inventory'] = self.inventory
            users[user]['Hungry'] = []
            users[user]['Hungry'].append(str(datetime.now()))
            users[user]['Hungry'].append(False)

            # then put the information in users
            with open('usersjson', 'w') as f:
                json.dump(users, f)
            #respond according to if perishable or not
            if bounty not in perishables:
                await self.client.say('{} gathered {} {}(s)'.format(usern, amount,
                                                                bounty))
            else:
                await self.client.say('{} gathered {} {} {}(s)'.format(usern, amount, conditions[condition],
                                                                    bounty))
            Gatherable.island_limit +=1 #the island loses resources
            return
        elif users[user]['Hungry'][1] :
            await self.client.say('{} is too hungry  to gather.'.format(context.message.author.mention))
            return
        elif "541324003864870932" in [y.id for y in context.message.author.roles]:
            await self.client.say('{} is too sick to gather. '.format(context.message.author.mention))
            return
        # if not new user than check if hungry
        hungry = users[user]['Hungry'][0][:-7]
        hungry = datetime.strptime(hungry, "%Y-%m-%d %H:%M:%S")
        hungry = (datetime.now() - hungry).total_seconds()
        hungry = int(hungry)
        if hungry > 240:
            users[user]['Hungry'][1] = True
            role = discord.utils.get(context.message.server.roles, name='Weakened')
            await self.client.add_roles(context.message.author, role)
            await self.client.say('{} is too hungry to gather.'.format(context.message.author.mention))
            with open('usersjson', 'w') as f:
                json.dump(users, f)
            return

        #must be old user and not hungry if past this part so now check if inventory is full
        for thing in gather_list:
            if thing in users[user]['inventory'].keys():
                self.inventorysum += users[user]['inventory'][thing][0]
                break
        if self.inventorysum >= 30:
            await self.client.say('Inventory full')

            return

        #if new item create key and give amount to json
        if bounty not in users[user]['inventory'].keys():
            users[user]['inventory'][bounty] = self.inventory[bounty]
            users[user]['inventory'][bounty][0] = amount #might not need this line
            with open('usersjson', 'w') as f:
                        json.dump(users, f)

            if bounty in perishables: #if perishable give correct response
                await self.client.say('{} gathered {} {} {}(s)'.format(usern,  amount, conditions[condition],
                                                                bounty))

            else:
                await self.client.say('{} gathered {} {}(s)'.format(usern, amount,
                                                                       bounty))

            Gatherable.island_count += 1
            return
        #logic for if old item and perishable
        elif bounty in users[user]['inventory'].keys():
            if bounty in perishables:
                if condition == 1:
                    #print('original amount is {}, now adding {}'.format( str(users[user]['inventory'][bounty][0]), amount))
                    users[user]['inventory'][bounty][0] += amount #index  amount added to  total amount
                    users[user]['inventory'][bounty][1] += amount #index 1 amount added to green fruit
                    #print('new total amount is {}'.format(str(users[user]['inventory'][bounty][0])) )
                    with open('usersjson', 'w') as f:
                        json.dump(users, f)
                    Gatherable.island_count += 1
                elif condition == 2:
                    #print('original amount is {}, now adding {}'.format( str(users[user]['inventory'][bounty][0]), amount))
                    users[user]['inventory'][bounty][0] += amount #index 0 amount added to total amount
                    users[user]['inventory'][bounty][2] += amount # amount added to ripe
                    #print('the new total amount is {}'.format(str(users[user]['inventory'][bounty][0]) ))
                    with open('usersjson', 'w') as f:
                        json.dump(users, f)

                    Gatherable.island_count += 1
                await self.client.say('{} gathered {} {} {}(s)'.format(usern,amount,conditions[condition],bounty))
            else:
                users[user]['inventory'][bounty][0] += amount
                with open('usersjson', 'w') as f:
                    json.dump(users, f)
                await self.client.say('{} gathered {} {}(s)'.format(context.message.author.mention, amount, bounty))
                Gatherable.island_count += 1

def setup(client):
        client.add_cog(Gatherable(client))