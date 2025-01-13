#!/usr/bin/env python3
# coding: utf-8
# ---------------------------------------------------
# TODO
# [/] Display results more concisely
# [/] Allow for stacked rolls
# [/] Display both dice results for advantage and disadvantage
# [/] Modifiers to allow positive and negative numbers
# [/] Allow for previous rolls to be specific to the user that requested them
# [/] Build docker container for deployment
# [/] Add error handling
# [/] Add logging
# [/] Add support for non-leading integer for dice types (e.g., d8, d10)
# [] Comment code blocks for future reference
# [] Strip incoming message to allow for designated dice rolls and modifiers to display seperate totals before adding into final total
# [/] Add support for D2, D50, D100, and precentile dice
# [/] Add reroll function
# ---------------------------------------------------
version = 'v0.6.0'
# ---------------------------------------------------
import traceback
import discord
import asyncio
import random
import re
import os
from response import success_message as success, error_message as error, failure_message as failure, reroll_message as reroll

global e_message
e_message = random.choice(error)
# ---------------------------------------------------
intents = discord.Intents.default() # Default intents
intents.message_content = True # Enable message content
client = discord.Client(intents=intents) # Create Discord client
user_rolls = {} # Dictionary to store user rolls, keyed by user ID
# ---------------------------------------------------
# D2 die
class D2():
    def __init__(self):
        pass
    def roll(self, request):
        return random.randint(1, 2)

# D4 die
class D4():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D4' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D4']) / len(user_rolls[user_id]['D4'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request): # Dice rolling algorithm for D4
        avg_roll = self.Average()
        roll = 0
        
        while roll == 0: # Roll dice until a non-zero value is returned
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 2:
                roll = random.choice(self.high())
            elif avg_roll < 3:
                roll = random.choice(self.weighted())
            elif avg_roll < 5:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D4'] = [] if 'D4' not in user_rolls[user_id] else user_rolls[user_id]['D4']
        
        if len(user_rolls[user_id]['D4']) < 4:
            user_rolls[user_id]['D4'].append(roll)
        else:
            user_rolls[user_id]['D4'] = []
        return roll
    
    def standard(self): # Normal 4-sided die roll
        return list(range(1, 5))
    def weighted(self): # Altered 4-sided die roll
        return list(range(1, 5)) + list(range(3, 5))
    def high(self): # Heavy-weighted 4-sided die roll towards success
        return list(range(1, 5)) + list(range(3, 5))* 2
    def low(self): # low-weighted 4-sided die roll towards failure
        return list(range(1, 5)) + list(range(1, 3))* 2
# D6 die
class D6():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D6' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D6']) / len(user_rolls[user_id]['D6'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request):
        avg_roll = self.Average()
        roll = 0
        while roll == 0:
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 2:
                roll = random.choice(self.high())
            elif avg_roll < 4:
                roll = random.choice(self.weighted())
            elif avg_roll < 7:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D6'] = [] if 'D6' not in user_rolls[user_id] else user_rolls[user_id]['D6']
        
        if len(user_rolls[user_id]['D6']) < 4:
            user_rolls[user_id]['D6'].append(roll)
        else:
            user_rolls[user_id]['D6'] = []
        return roll

    def standard(self):
        return list(range(1, 7))

    def weighted(self):
        return list(range(1, 7)) + list(range(4, 7))

    def high(self):
        return list(range(1, 7)) + list(range(4, 7))* 2

    def low(self):
        return list(range(1, 7)) + list(range(1, 3))* 2
# D8 die
class D8():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D8' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D8']) / len(user_rolls[user_id]['D8'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request):
        avg_roll = self.Average()
        roll = 0
        
        while roll == 0:
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 3:
                roll = random.choice(self.high())
            elif avg_roll < 7:
                roll = random.choice(self.weighted())
            elif avg_roll < 9:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D8'] = [] if 'D8' not in user_rolls[user_id] else user_rolls[user_id]['D8']
        
        if len(user_rolls[user_id]['D8']) < 4:
            user_rolls[user_id]['D8'].append(roll)
        else:
            user_rolls[user_id]['D8'] = []
        return roll
    
    def standard(self):
        return list(range(1, 9))
    
    def weighted(self):
        return list(range(1, 9)) + list(range(6, 9))
    
    def high(self):
        return list(range(1, 9)) + list(range(6, 9))* 2
    
    def low(self):
        return list(range(1, 9)) + list(range(1, 3))* 2
# D10 die
class D10():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D10' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D10']) / len(user_rolls[user_id]['D10'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request):
        avg_roll = self.Average()
        roll = 0
        
        while roll == 0:
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 3:
                roll = random.choice(self.high())
            elif avg_roll < 6:
                roll = random.choice(self.weighted())
            elif avg_roll < 11:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D10'] = [] if 'D10' not in user_rolls[user_id] else user_rolls[user_id]['D10']
        
        if len(user_rolls[user_id]['D10']) < 4:
            user_rolls[user_id]['D10'].append(roll)
        else:
            user_rolls[user_id]['D10'] = []
        return roll
    
    def standard(self):
        return list(range(1, 11))
    
    def weighted(self):
        return list(range(1, 11)) + list(range(8, 11))
    
    def high(self):
        return list(range(1, 11)) + list(range(8, 11))* 2
    
    def low(self):
        return list(range(1, 11)) + list(range(1, 5))* 2
# D12 die
class D12():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D12' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D12']) / len(user_rolls[user_id]['D12'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request):
        avg_roll = self.Average()
        roll = 0
        
        while roll == 0:
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 4:
                roll = random.choice(self.high())
            elif avg_roll < 9:
                roll = random.choice(self.weighted())
            elif avg_roll < 13:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D12'] = [] if 'D12' not in user_rolls[user_id] else user_rolls[user_id]['D12']
        
        if len(user_rolls[user_id]['D12']) < 4:
            user_rolls[user_id]['D12'].append(roll)
        else:
            user_rolls[user_id]['D12'] = []
        return roll

    def standard(self):
        return list(range(1, 13))

    def weighted(self):
        return list(range(1, 13)) + list(range(9, 13))

    def high(self):
        return list(range(1, 13)) + list(range(9, 13))* 2

    def low(self):
        return list(range(1, 13)) + list(range(1, 6))* 2
# D20 die
class D20():
    def __init__(self):
        pass
    
    def Average(self):
        if user_id not in user_rolls or 'D20' not in user_rolls[user_id]:
            average = 0
        else:
            try:
                average = sum(user_rolls[user_id]['D20']) / len(user_rolls[user_id]['D20'])
            except ZeroDivisionError:
                average = 0
        return average
    
    def roll(self, request):
        avg_roll = self.Average()
        roll = 0
        
        while roll == 0:
            if avg_roll == 0:
                roll = random.choice(self.standard())
            elif avg_roll < 5:
                roll = random.choice(self.high())
            elif avg_roll < 15:
                roll = random.choice(self.weighted())
            elif avg_roll < 21:
                roll = random.choice(self.low())
                
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D20'] = [] if 'D20' not in user_rolls[user_id] else user_rolls[user_id]['D20']
        
        if len(user_rolls[user_id]['D20']) < 4:
            user_rolls[user_id]['D20'].append(roll)
        else:
            user_rolls[user_id]['D20'] = []
        return roll
    
    def roll_twice(self, request):
        roll1 = self.roll(request)
        roll2 = self.roll(request)
        return roll1, roll2
    
    def standard(self):
        return list(range(1, 21))
    
    def weighted(self):
        return list(range(1, 21)) + list(range(10, 21))
    
    def high(self):
        return list(range(1, 21)) + list(range(15, 21))* 2
    
    def low(self):
        return list(range(1, 21)) + list(range(1, 6))* 2

# D50 die
class D50():
    def __init__(self):
        pass
    
    def roll(self, request):
        return random.choice(list(range(1, 51)))
# D100 die
class D100():
    def __init__(self):
        pass
    
    def roll(self, request):
        return random.choice(list(range(1, 101)))

# D% die
class Dpercent():
    def __init__(self):
        pass
    
    def roll(self):
        tens = random.choice(list(range(0, 101, 10)))
        ones = random.choice(list(range(0, 11)))
        return tens, ones
# ---------------------------------------------------
d2 = D2() # D2 die instance
d4 = D4() # D4 die instance
d6 = D6() # D6 die instance
d8 = D8() # D8 die instance
d10 = D10() # D10 die instance
d12 = D12() # D12 die instance
d20 = D20() # D20 die instance
d50 = D50() # D50 die instance
d100 = D100() # D100 die instance
dpercent = Dpercent() # D% die instance
# ---------------------------------------------------
def previous_roll(user_request):
    if user_id not in user_rolls: 
        user_rolls[user_id] = {} 
    else:
        user_rolls[user_id]
    if 'p_roll' not in user_rolls[user_id]:
        user_rolls[user_id]['p_roll'] = [] 
    else:
        user_rolls[user_id]['p_roll']
    user_rolls[user_id]['p_roll'] = user_request
    request = user_rolls[user_id]['p_roll']
    return request

def coin_flip():
    return 'heads' if random.choice([True, False]) else 'tails'

def extract_modifiers(request):
    dices = extract_dices(request)
    
    for dice in dices:
        request = request.replace(dice, '')
    match = re.findall(r'[+-]\d+', request)
    if match:
        modifiers = [int(i) for i in match]
    else:
        modifiers = [0]
    return modifiers

def extract_dices(request):
    request = re.sub(r'(?<!\d)d', '1d', request)
    dices = re.findall(r'\d+d\d+', request)
    return dices

#def dice_roll(request):
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    global user_id
    
    if message.author == client.user:
        return
    elif message.content.startswith('!!error!!') or message.content.startswith('!!err!!'):
        await message.channel.send(random.choice(error))
    elif message.content.startswith('!!success!!'):
        await message.channel.send(random.choice(success))
    elif message.content.startswith('!!failure!!') or message.content.startswith('!!fail!!'):
        await message.channel.send(random.choice(failure))
    elif message.content.startswith('!version') or message.content.startswith('!ver') or message.content.startswith('!v'):
        await message.channel.send(embed=discord.Embed(
            title='Version', 
            description=f'{version}', 
            color=discord.Color.blue()))
    elif message.content.startswith('!info'):
        await message.channel.send(embed=about_embed)
    elif message.content.startswith('!help'):
        await message.channel.send(embed=help_embed)
    elif message.content.startswith('!%') or message.content.startswith('!precent') or message.content.startswith('!precentile'):
        percent = dpercent.roll()
        await message.channel.send(embed=discord.Embed(
title=f"{message.author.display_name} rolled a percentile, **{sum(percent)}%**",
description=f'''
{' and '.join(map(str, percent))}
''',
color=discord.Color.darker_grey()
            ))
    elif message.content.startswith('!coin') or message.content.startswith('!coinflip') or message.content.startswith('!flip'):
        await message.channel.send(embed=discord.Embed(
title=f'{message.author.display_name} got {coin_flip()}!', 
color=discord.Color.lighter_grey()))
    elif message.content.lower().startswith('!rr') or message.content.lower().startswith('!reroll') or message.content.lower().startswith('!re-roll') or message.content.lower().startswith('!re'):
        user_id = message.author.id # Debugging line to check user ID
        print(f'user_id: {user_id}')
        if 'p_roll' not in user_rolls[user_id]:
            await message.channel.send('You have not rolled any dice yet.')
            return
        else:
            await message.channel.send(random.choice(reroll))
            await asyncio.sleep(1.5)
            request = user_rolls[user_id]['p_roll'] # Get the last roll from user_rolls dictionary

        await get_dice(request, message)
    elif message.content.lower().startswith('!r') or message.content.lower().startswith('!roll'):
        user_id = message.author.id # Debugging line to check user ID
        print(f'User id: {user_id}')
        if message.content.lower().startswith('!r'):
            user_request = message.content[3:].strip().lower()
        else:
            user_request = message.content[6:].strip().lower()
        request = previous_roll(user_request)
        await get_dice(request, message)
        
async def get_dice(request, message):
    results = []
    d20_result = []
    total = 0
    dice_type = 0
    die_roll = 0
            
    print(f'Request: {request}') # Debugging line to check the stripped content of the message
    rolls = extract_dices(request)
    print(f'Rolls: {rolls}') # Debugging line to check the extracted dice rolls
    modifiers = extract_modifiers(request)
    print(f'Modifiers: {modifiers}') # Debugging line to check the extracted modifiers
    print(f'D20 results: {d20_result}')
    try:
        if 'd20a' in request:
            result = d20.roll_twice(request)
            die_roll = str(max(result))
            results.append(die_roll) if die_roll != '20' or die_roll != '1' else results
            total += int(die_roll)
            results.append(f'||*({d20_result[0]} and {d20_result[1]})*||')
        elif 'd20d' in request:
            result = d20.roll_twice(request)
            die_roll, d20_result = str(min(result))
            results.append(die_roll) if die_roll != '20' or die_roll != '1' else results
            total += int(die_roll)
            results.append(f'||*({d20_result[0]} and {d20_result[1]})*||')
        else:
            for roll_str in rolls:
                num_dice, dice_type = map(int,roll_str.split('d'))
                if dice_type == 2:
                    for i in range(num_dice):
                        result = d2.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D2)*')
                elif dice_type == 4:
                    for i in range(num_dice):
                        result = d4.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D4)*')
                elif dice_type == 6:
                    for i in range(num_dice):
                        result = d6.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D6)*')
                elif dice_type == 8:
                    for i in range(num_dice):
                        result = d8.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D8)*')
                elif dice_type == 10:
                    for i in range(num_dice):
                        result = d10.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D10)*')
                elif dice_type == 12:
                    for i in range(num_dice):
                        result = d12.roll(request)
                        results.append((str(result)))
                        total += result
                    results.append(f'*(from {num_dice}D12)*')
                elif dice_type == 20:
                    for i in range(num_dice):
                        result = d20.roll(request)
                        die_roll = str(d20_result)
                        results.append(str(result)) and d20_result.append(str(result))
                        total += result
                    results.append(f'*(from {num_dice}D20)*')
                elif dice_type == 50:
                    for i in range(num_dice):
                        result = d50.roll(request)
                        results.append(str(result))
                        total += result
                    results.append(f'*(from {num_dice}D50)*')
                elif dice_type == 100:
                    for i in range(num_dice):
                        result = d100.roll(request)
                        results.append(str(result))
                        total += result
                    results.append(f'*(from {num_dice}D100)*')
                    
            total += sum(modifiers) # Add modifiers
            
        print(f'die roll:{die_roll}') # Debugging line to check the initial state of 'die_roll'
        print(f'dice type:{dice_type}')  # Debugging line to check the initial state of 'dice_type'
        print(f'results:{results}') # Debugging line to check the initial state of 'results' list
        print(f'total:{total}') # Debugging line to check the initial state of 'total'
        print(f'user_rolls: {user_rolls}') # Debugging line to check the state of 'user_rolls'
        print(f'D4 average: {d4.Average()}') # Debugging line to check the average of the D4 die
        print(f'D6 average: {d6.Average()}') # Debugging line to check the average of the D6 die
        print(f'D8 average: {d8.Average()}') # Debugging line to check the average of the D8 die
        print(f'D10 average: {d10.Average()}') # Debugging line to check the average of the D10 die
        print(f'D12 average: {d12.Average()}') # Debugging line to check the average of the D12 die
        print(f'D20 average: {d20.Average()}') # Debugging line to check the average of the D20 die
        dice_embed = discord.Embed(
    title=f"{message.author.display_name} rolled a **{total}**",
description=f'''
Die Results: {', '.join(results)}
Modifiers: {sum(modifiers)}
Total: **{total}**
''',
color=discord.Color.purple()
    )
        success_embed = discord.Embed(
title=f"**!!CRITICAL SUCCESS!!**",
description=f'''
{message.author.display_name} rolled a **20**!!

Die Results: **20!!** {', '.join(results)}
Modifiers: {sum(modifiers)}
Total: **{total}**
''',
color=discord.Color.green()
    )
        failure_embed = discord.Embed(
title=f"**!!CRITICAL FAILURE!!**",
description=f'''
{message.author.display_name} rolled a **1!!**

Die Results: **1!!** {', '.join(results)}
Modifiers: {sum(modifiers)}
Total: **{total}**
''',
color=discord.Color.red()
)        

        if total == 0:
            await message.channel.send(f'{message.author.display_name}. {e_message}')
            return
        if 'd20a' in request or 'd20d' in request or dice_type == 20:
            for i in d20_result:
                if i == '20':
                    await message.channel.send(embed=success_embed)
                    await message.channel.send(f'{random.choice(success)}')
                    return
                if i == '1':
                    await message.channel.send(embed=failure_embed)
                    await message.channel.send(f'{random.choice(failure)}')
                    return
                else:
                    continue
            else:
                await message.channel.send(embed=dice_embed)
                return
        else:
            await message.channel.send(embed=dice_embed)
    except Exception as e: # Catch any exceptions that occur during the process and print them for debugging purposes
        traceback.print_exc() # Print detailed information about the exception, including its type, value, and a traceback of the stack where it occurred. This is useful for debugging.
        await message.channel.send(f'{message.author.display_name}.  {e_message}') # Send a message to the channel indicating that there was an error with the request.
        return # Return from the function to stop further execution if an error occurs.
    return

about_embed = discord.Embed(
title='About',

description='''
This program aims to act as a balanced 'weighted die'. It skews towards more favorable results while punishing too many of them. This offers the chance to have passible rolls without breaking the game and still allows for low/nat-1 rolls - those can be fun too!

Type **'!help'** for more information on how to use this bot.
*Link to project: https://github.com/Kahros/Discord-Adaptive-Dice-Roller*
    ''',
    color=discord.Color.blue())
help_embed = discord.Embed(
title='**Commands:**',
description='''
**!help**
- Displays this help message.
**!info**
- Displays information about the bot.
**!roll, !r**
- Roll command.
**!coin, !coinflip, !flip**
- Flips a coin.
**!%, !precent, !precentile**
- Rolls precentile dice.
**!roll <*optional* dice count><dice type>**
- Rolls the specified number of dice of the specified type.  *!roll 2d4, !r 4d6, !roll d8*
**!roll <dice type> +-<modifier>**
- Rolls the specified number of dice of the specified type and applies the specified modifier.  *!roll d6 +2, !r d4 -1*
**!roll d20a**
- Rolls D20 dice with advantage
**!roll d20d**
- Rolls D20 dice with disadvantage
**!reroll, !re-roll, !re, !rr**
- Rerolls last dice roll for player. *This does not apply to coin flips or precentile dice.*
**coin flips and precentile dice cannot be used with other rolls**

**Supported dice are D2, D4, D6, D8, D10, D12, D20, D50, D100, precentile**
*NOTE: coin, D2, D50, D100, and precentile are not adaptive.*
    ''',
color=discord.Color.blue())

client.run(os.getenv('BOT_TOKEN'))