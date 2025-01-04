#---------------------------------------------------
# TODO
# [] Display results more concisely
# [/] Allow for stacked rolls
# [/] Display both dice results for advantage and disadvantage
# [/] Modifiers to allow positive and negative numbers
# [] Allow for previous rolls to be specific to the user that requested them
# [] Build docker container for deployment
# [] Comment code blocks for future reference
# ---------------------------------------------------

import traceback
import discord
import random
import re
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

user_rolls = {} # Dictionary to store user rolls, keyed by user ID
roll_history = {} # Dictionary to store roll history for each die type, keyed by die type (e.g., 'D6')

# ---------------------------------------------------
# D4 die
class D4():
    def __init__(self):
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll
    
    def Average(self):
        if user_id not in user_rolls or 'D4' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D4']) / len(user_rolls[user_id]['D4'])
            except ZeroDivisionError:
                self.avg_roll = 0

        return self.avg_roll
        # if len(self.roll_tracker) == 0:
        #     self.avg_roll = 0
        # else:
        #     self.avg_roll = sum(self.roll_tracker) / len(self.roll_tracker)
        # return self.avg_roll
        
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 2:
            roll = random.choice(self.high())
        elif 2 < self.avg_roll >= 3:
            roll = random.choice(self.weighted())
        elif 3 < self.avg_roll >= 4:
            roll = random.choice(self.low())
            
        user_rolls[user_id] = {} if user_id not in user_rolls else user_rolls[user_id]
        user_rolls[user_id]['D4'] = [] if 'D4' not in user_rolls[user_id] else user_rolls[user_id]['D4'] 
        
        if len(user_rolls[user_id]['D4']) < 4:
            user_rolls[user_id]['D4'].append(roll) 
        else:
            user_rolls[user_id]['D4'] = []

        return roll


        
    def standard(self):
        return list(range(1, 5))

    def weighted(self):
        return list(range(1, 5)) + list(range(3, 5))

    def high(self):
        return list(range(1, 5)) + list(range(3, 5))* 2

    def low(self):
        return list(range(1, 5)) + list(range(1, 3))* 2

# D6 die
class D6():
    def __init__(self):
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll


        
    def Average(self):
        if user_id not in user_rolls or 'D6' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D6']) / len(user_rolls[user_id]['D6'])
            except ZeroDivisionError:
                self.avg_roll = 0
        return self.avg_roll
        
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 2:
            roll = random.choice(self.high())
        elif 2 < self.avg_roll >= 4:
            roll = random.choice(self.weighted())
        elif 4 < self.avg_roll >= 6:
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
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll
    
        
    def Average(self):
        if user_id not in user_rolls or 'D8' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D8']) / len(user_rolls[user_id]['D8'])
            except ZeroDivisionError:
                self.avg_roll = 0
        return self.avg_roll
        
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 3:
            roll = random.choice(self.high())
        elif 3 < self.avg_roll >= 7:
            roll = random.choice(self.weighted())
        elif 7 < self.avg_roll >= 8:
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
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll

    def Average(self):
        if user_id not in user_rolls or 'D10' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D10']) / len(user_rolls[user_id]['D10'])
            except ZeroDivisionError:
                self.avg_roll = 0

        return self.avg_roll
        
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 4:
            roll = random.choice(self.high())
        elif 4 < self.avg_roll >= 7:
            roll = random.choice(self.weighted())
        elif 7 < self.avg_roll >= 10:
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
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll
    
    def Average(self):
        if user_id not in user_rolls or 'D12' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D12']) / len(user_rolls[user_id]['D12'])
            except ZeroDivisionError:
                self.avg_roll = 0
                
        return self.avg_roll
        
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 4:
            roll = random.choice(self.high())
        elif 4 < self.avg_roll >= 9:
            roll = random.choice(self.weighted())
        elif 9 < self.avg_roll >= 12:
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
        self.previous_rolls = [] # List of all rolls for this die, max of 3
        self.avg_roll = 0 # Average of recent rolls, used for determining what version of die to roll
    
    def Average(self):
        if user_id not in user_rolls or 'D20' not in user_rolls[user_id]:
            self.avg_roll = 0
        else:
            try:
                self.avg_roll = sum(user_rolls[user_id]['D20']) / len(user_rolls[user_id]['D20'])
            except ZeroDivisionError:
                self.avg_roll = 0
        return self.avg_roll
                    
    def roll(self, request):
        roll = 0
        self.Average()
        if self.avg_roll == 0:
            roll = random.choice(self.standard())
        elif 0 < self.avg_roll >= 5:
            roll = random.choice(self.high())
        elif 5 < self.avg_roll >= 15:
            roll = random.choice(self.weighted())
        elif 15 < self.avg_roll >= 20:
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
    elif message.content.startswith('!help'):
        await message.channel.send('''
**Commands:**
~~-----------------------------------------------------~~
**!help** - Displays this help message.
**!roll** <die count><die type> - Rolls a die of the specified type (e.g. !roll 3d4). Multiple rolls can be made by separating the die types with commas (e.g., **!roll** 3d4, 2d6). 
**!roll** <die count><die type> +-<modifier> - Rolls a die of the specified type and applies a modifier (e.g., !roll 3d4 +2, !roll 3d4 -2)
**!roll** d20a - Rolls a D20 with advantage.
**!roll** d20d - Rolls a D20 with disadvantage.
**!info** - Displays information about the bot.
~~------------------------------------------------------~~
                                    ''')
        
    elif message.content.lower().startswith("!roll"):
        user_id = message.author.id
        print(f'user_id: {user_id}') # Debugging line to check user ID
        request = message.content[5:].strip().lower()
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
            total += max(result)
            total += sum(modifiers)
            results.append(f'||(from a D{result[0]} and D{result[1]})||')
        elif 'd20d' in request:
            result = d20.roll_twice(request)
            die_roll = str(min(result))
            results.append(die_roll) if die_roll != '20' or die_roll != '1' else results
            total += min(result)
            total += sum(modifiers)
            results.append(f'||(from a D{result[0]} and D{result[1]})||')
        for roll_str in rolls:
            num_dice, dice_type = map(int, roll_str.split("d"))
            if dice_type == 4:
                for i in range(num_dice):
                    result = d4.roll(request)
                    results.append((str(result)))
                    total += result
                results.append(f'(from {num_dice}D4)')
            elif dice_type == 6:
                for i in range(num_dice):
                    result = d6.roll(request)
                    results.append((str(result)))
                    total += result
                results.append(f'(from {num_dice}D6)')
            elif dice_type == 8:
                for i in range(num_dice):
                    result = d8.roll(request)
                    results.append((str(result)))
                    total += result
                results.append(f'(from {num_dice}D8)')
            elif dice_type == 10:
                for i in range(num_dice):
                    result = d10.roll(request)
                    results.append((str(result)))
                    total += result
                results.append(f'(from {num_dice}D10)')
            elif dice_type == 12:
                for i in range(num_dice):
                    result = d12.roll(request)
                    results.append((str(result)))
                    total += result
                results.append(f'(from {num_dice}D12)')
            elif dice_type == 20:
                for i in range(num_dice):
                    result = d20.roll(request)
                    die_roll = str(result)
                    results.append(str(result))
                    total += result
                results.append(f'(from {num_dice}D20)')
            total += sum(modifiers) # Add modifiers
        print(f'die roll:{die_roll}') # Debugging line to check the initial state of 'die_roll'
        print(f'dice type:{dice_type}')  # Debugging line to check the initial state of 'dice_type'
        print(f'results:{results}') # Debugging line to check the initial state of 'results' list
        print(f'total:{total}') # Debugging line to check the initial state of 'total'
        print(f'user_rolls: {user_rolls}') # Debugging line to check the state of 'user_rolls'
        print(f'D4 Avg: {d4.avg_roll}')
        print(f'D6 Avg: {d6.avg_roll}')
        print(f'D8 Avg: {d8.avg_roll}')
        print(f'D10 Avg: {d10.avg_roll}')
        print(f'D12 Avg: {d12.avg_roll}')
        print(f'D20 Avg: {d20.avg_roll}')
    
        
        if 'd20a' in request or 'd20d' in request or dice_type == 20:
            if die_roll == '20':
                await message.channel.send(f'''
**{message.author.mention}**

**!!CRITICAL SUCCESS!!**
Die Results: **{die_roll}!!**, ({', '.join(results)})
Modifiers: {sum(modifiers)},

How exciting!!
                                ''')
        
            elif die_roll == '1':
                await message.channel.send(f'''
**{message.author.mention}**

**!!CRITICAL FAILURE!!**
Die Results: **{die_roll}!!**, ({', '.join(results)})
Modifiers: {sum(modifiers)},

How unfortunate...
                                ''')
                
            else:
                await message.channel.send(f'''
**{message.author.mention}**

Die Results: {', '.join(results)},
Modifiers: {sum(modifiers)}, 
**Total: {total}**
                                ''')
        else:                               
            await message.channel.send(f'''
**{message.author.mention}**

Die Results {', '.join(results)}, 
Modifiers: {sum(modifiers)}, 
**Total: {total}**
                    ''')

    except Exception as e: # Catch any exceptions that occur during the process and print them for debugging purposes
        traceback.print_exc() # Print detailed information about the exception, including its type, value, and a traceback of the stack where it occurred. This is useful for debugging.
        await message.channel.send('Kadie broke it again! Please try again later.') # Send a message to the channel indicating that there was an error with the request.
        return # Return from the function to stop further execution if an error occurs.

    if message.content.startswith('!info'):
        await message.channel.send('''
This program aims to act as a balanced "weighted die". It skews towards more favorable results while punishing too many of them.  This offers the chance to have passible rolls without breaking the game and still allows for low/nat-1 rolls - those can be fun too!

**Type !help for commands**
                                ''')   

client.run(os.getenv('BOT_TOKEN'))
