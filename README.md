# HodgePodge

A small discord bot to be sweet, keep track of Dnd rescoures, send memes and help you search spells.
Inspired by TAZ!

Hosted with <3 on Heroku

## Objects

Run will forward messages to all bots it knows about
Bots have a list of modules.
Each module has a set of triggers that it registers with the bots parser.
on a message the parser produces a match object which maps the input string to
a function in a module.
the bot then will trigger the module to process the input and then give the module
the client object so it can respond if it needs to.


## ToDo

1. add in voice channel triggers (https://github.com/Rapptz/discord.py/blob/async/examples/playlist.py)
2. Redo all this shit