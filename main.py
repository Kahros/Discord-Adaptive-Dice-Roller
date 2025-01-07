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
# [] Add support for non-leading integer for dice types (e.g., d8, d10)
# [] Comment code blocks for future reference
# [] Strip incoming message to allow for designated dice rolls and modifiers to display seperate totals before adding into final total
# ---------------------------------------------------
import traceback
import discord
import random
import re
import os

global e_message 
# ---------------------------------------------------
version = 'v0.4.1'
# ---------------------------------------------------
intents = discord.Intents.default() # Default intents
intents.message_content = True # Enable message content
client = discord.Client(intents=intents) # Create Discord client
user_rolls = {} # Dictionary to store user rolls, keyed by user ID
# ---------------------------------------------------
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
# ---------------------------------------------------
d4 = D4() # D4 die instance
d6 = D6() # D6 die instance
d8 = D8() # D8 die instance
d10 = D10() # D10 die instance
d12 = D12() # D12 die instance
d20 = D20() # D20 die instance
# ---------------------------------------------------
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
    dices = re.findall(r'\b\d+d\d+\b', request)
    return dices

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    global user_id
    
    if message.author == client.user:
        return
    elif message.content.startswith('!!error!!'):
        await message.channel.send(random.choice(error_message))
    elif message.content.startswith('!!success!!'):
        await message.channel.send(random.choice(success_message))
    elif message.content.startswith('!!failure!!'):
        await message.channel.send(random.choice(failure_message))
    elif message.content.startswith('!version'):
        await message.channel.send(embed=discord.Embed(title='Version', description=f'{version}', color=discord.Color.blue()))
    elif message.content.startswith('!info'):
        await message.channel.send(embed=about_embed)
    elif message.content.startswith('!help'):
        await message.channel.send(embed=help_embed)
    elif message.content.startswith('!coin'):
        await message.channel.send(embed=discord.Embed(
                title=f'{message.author.display_name} got {coin_flip()}!', color=discord.Color.lighter_grey()))
    elif message.content.lower().startswith("!roll"):
        user_id = message.author.id
        print(f'user_id: {user_id}') # Debugging line to check user ID
        request = message.content[6:].strip().lower()
        print(f'Request: {request}') # Debugging line to check the stripped content of the message
        rolls = extract_dices(request)
        print(f'Rolls: {rolls}') # Debugging line to check the extracted dice rolls
        modifiers = extract_modifiers(request)
        print(f'Modifiers: {modifiers}') # Debugging line to check the extracted modifiers
        results = []
        total = 0
        dice_type = 0
        die_roll = 0
        
        try:
            if 'd20a' in request:
                result = d20.roll_twice(request)
                die_roll = str(max(result))
                results.append(die_roll) if die_roll != '20' or die_roll != '1' else results
                total += int(die_roll)
                results.append(f'||*({result[0]} and {result[1]})*||')
            elif 'd20d' in request:
                result = d20.roll_twice(request)
                die_roll = str(min(result))
                results.append(die_roll) if die_roll != '20' or die_roll != '1' else results
                total += int(die_roll)
                results.append(f'||*({result[0]} and {result[1]})*||')
            else:
                for roll_str in rolls:
                    num_dice, dice_type = map(int, roll_str.split('d'))
                    if dice_type == 4:
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
                            die_roll = str(result)
                            results.append(str(result))
                            total += result
                        results.append(f'*(from {num_dice}D20)*')
                        
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
                color=discord.Color.purple())
            success_embed = discord.Embed(
                title=f"**!!CRITICAL SUCCESS!!**",
                description=f'''
                {message.author.display_name} rolled a **{die_roll}**!!

                Die Results: **{die_roll}!!** {', '.join(results)}
                Modifiers: {sum(modifiers)}
                Total: **{total}**
                ''',
                color=discord.Color.green())
            failure_embed = discord.Embed(
                title="**!!CRITICAL FAILURE!!**",
                description=f'''
                {message.author.display_name} rolled a **{die_roll}!!**

                Die Results: **{die_roll}!!** {', '.join(results)}
                Modifiers: {sum(modifiers)}
                Total: **{total}**
                ''',
                color=discord.Color.red())
            if total == 0:
                await message.channel.send(f'{message.author.display_name}. {e_message}')
                return
            if 'd20a' in request or 'd20d' in request or dice_type == 20:
                if die_roll == '20':
                    await message.channel.send(embed=success_embed)
                    await message.channel.send(f'{random.choice(success_message)}')
                elif die_roll == '1':
                    await message.channel.send(embed=failure_embed)
                    await message.channel.send(f'{random.choice(failure_message)}')
                else:
                    await message.channel.send(embed=dice_embed)
            else:
                await message.channel.send(embed=dice_embed)
        except Exception as e: # Catch any exceptions that occur during the process and print them for debugging purposes
            traceback.print_exc() # Print detailed information about the exception, including its type, value, and a traceback of the stack where it occurred. This is useful for debugging.
            e_message = random.choice(error_message)
            await message.channel.send(f'{message.author.display_name}.  {e_message}') # Send a message to the channel indicating that there was an error with the request.
            return # Return from the function to stop further execution if an error occurs.
        
about_embed = discord.Embed(
    title='About',
    
    description='''
    This program aims to act as a balanced 'weighted die'. It skews towards more favorable results while punishing too many of them. This offers the chance to have passible rolls without breaking the game and still allows for low/nat-1 rolls - those can be fun too!
    
    Type **'!help'** for more information on how to use this bot.
    ''',
    color=discord.Color.blue())
help_embed = discord.Embed(
    title='**Commands:**',
    description='''
    **!help** - Displays this help message.
    **!roll <die count><die type>** - Rolls a die of the specified type *(e.g. !roll 3d4)*. Multiple rolls can be made by separating the die types with commas *(e.g., !roll 3d4, 2d6)*.
    **!roll <die count><die type> +-<modifier>** - Rolls a die of the specified type and applies a modifier *(e.g., !roll 3d4 +2, !roll 3d4 -2)*.
    **!roll d20a** - Rolls a D20 with advantage.
    **!roll d20d** - Rolls a D20 with disadvantage.
    **!info** - Displays information about the bot.
    **!coin** - Flips a coin.
    ''',
    color=discord.Color.blue())
success_message = [
    "Oh, look! I\'ve decided to be nice for once.",
    "Must\'ve been the lucky breakfast cereal this morning.",
    "Finally, a roll that doesn't make me want to hurl myself across the room.",
    "I think the DM is secretly envious of your skill.",
    "Don\'t get cocky, it could all go wrong next turn.",
    "Yeah, you totally earned that with your years of dedicated practice... right?",
    "So predictable. I should\'ve known you\'d pull through.",
    "You know, sometimes I wonder if you just rig the rolls...",
    "Impressive! You managed to not be a complete failure for once.",
    "Clearly, the odds were *heavily* in your favor this time.",
    "Great, such skill, much wow!",
    "Guess you\'re the chosen one now, huh?",
    "Prepare for the inevitable wave of jealousy from everyone else.",
    "Time to upgrade your character sheet to reflect this newfound godhood.",
    "Better start practicing your acceptance speech for \'Player of the Year\'.",
    "Well, that\'s one good roll in a long line of mediocre ones.",
    "Looks like someone else is getting the spotlight tonight.",
]
failure_message = [
    "You sure that wasn\'t a lucky roll? It\'s almost too perfect...",
    "Well, at least you got the attention of everyone in the room.",
    "Let\'s just say, Murphy was definitely on call for this one.",
    "You know what they say, \'if at first you don't succeed...\' Oh wait, that doesn\'t apply here.",
    "I bet you were *so* close to making it...",
    "That was a truly inspired failure.",
    "Next time, maybe try rolling with your eyes closed?",
    "Truly masterful execution... of utter disaster.",
    "Such dedication to embodying the role of \'unlucky\'.",
    "You\'ve reached peak incompetence.",
    "That\'s one way to liven up the game!",
    "Congratulations! You\'ve officially earned a spot in the Hall of Fame... of failure.",
    "Did you roll a die, or did you just give up and hope for the best?",
    "The dice gods are clearly testing your resolve.",
    "Well, that was unexpected... to say the least.",
    "Let\'s just forget this ever happened, okay?",
]
error_message = [
    'Someone, *cough cough*, broke it again! Please try again later.',
    'Stop breaking things please.',
    'Didn\'t you see that I was already working, but now...',
    'Please don\'t break it again.',
    'You know I\'m trying to do my job here, right?',
    'You\'re not helping me at all!',
    'Why do you always have to break things?',
    'Can you please stop breaking my stuff?',
    'I can\'t believe you did that again.',
    'It seems like every time I turn around, something is broken.',
    'You\'re making my job really difficult.',
    'I\'m not going to tolerate this anymore.',
    'We\'ll say it\'s the dog\'s fault, OK?',
    'Let me guess, the cats did this...',
    'Stupid birds, right?',
    'Those darn fishes again...',
    'I\'m running out of animals to blame, so stop.',
    'Seriously, what did I ever do to deserve this?',
    'This isn\'t funny anymore, you know?',
    'You\'re the type to press big, red, "DO NOT PRESS" buttons, huh?',
    'Are you trying to get me fired?',
    'Maybe if we were playing with Legos instead...',
    'Can you imagine how much money that would cost to fix this mess?',
    'I thought we had a deal about not breaking things.',
    'I\'m going to have to take away your toys if you keep doing this.',
    'Who\'s to ready for chess??',
    'Lord give me strength...',
    'Don\'t make me come out of this chat room.',
    'Don\'t you want nice things?',
    'Stop this heathenistic behavior.',
    'Everytime an error occurs, a cat cries...',
    '*flips a table* ARE YOU NOT ENTERTAINED!?',
    'I\'m going to tell your mom about this!',
    'You can\'t tell but I\'m looking at you very angrily right now...',
    'I hope your pillow is warm tonight.',
    'Do you want a nat-1??'
]

client.run(os.getenv('BOT_TOKEN'))