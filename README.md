# Adaptive Dice Roller - ADR

A Discord bot that allows users to roll adaptive dice in a server, intended for table-top games, such (but not limited to) as Dungeons and Dragons, and Pathfinder.

What sets this apart from others is this dice bot adjusts the ratio of each die roll depending on the result(s) of the past rolls.  This aims to enhance gameplay experience by allowing greater probability of successful dice rolls.  Success can be also be boring however and will also adjust to make failure more possible if previous rolls are too high.  This resets after every 4th roll, which will utilize a normal random ratio for each dice roll.

Features:
- Dice support for D2, D4, D6, D8, D10, D12, D20, D50, D100, precentile, and coin flips.
    - Note: Coin flips, D2, D50, and D100 are not adaptive.  They will use a normal random ratio.
- Each dice will have their own average ratio and wont affect the probability of other dice.
- Each player will have their own probablity ratio for each dice and wont affect the probability of other players
- Use of multiples of the same dice.
- Ability to add modifiers (both + and -).
- Use of Advantage and Disadvantage D20 dice rolls (this will affect the probability ratio).
- Concise result layout, showcasing what dice was used, what the total amount for modifiers are, and the total result.
- Ability to utilize multiple different dice and modifiers in the same roll.
- Snarkybot - the dice bot will provide a snarky remark based on natural success (nat20) or natural failures (nat1).  Natural success and failures only apply to D20 dice rolls.  
    - Will also provide a snarky remark when there is an error.

Upcoming features:

~~- Reroll: Ability to reroll of the last roll that the player has sent.  This is per player.~~
- Calculate modifiers per dice type, independent from total modifiers. 
- Anything else requested.




This is a self-project, aimed for my personal use with my discord group.  Currently in beta phase and testing.  A public release is possible, but not expected at the moment.
