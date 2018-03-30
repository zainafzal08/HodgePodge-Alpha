# Hodge Podge

The Best Boy™

A beautiful discord bot built to be expandable, useful and ever so cute.

## User


## Developer

Hi! I assume you are here because you want to either understand how hodge podge works or because you want to maybe help out by building a module!

If you are here to build a module, thanks for dropping in! I hope i can make the process a bit easier by walking you through how the module interface works. Keep reading below. If you want a complete overview of how things works jump down to the explanation section

#### Making a Module

> Intro

So to make a module you must make a class much like the classes in `modules/`.

Make a class that inherits from `Module` and just has a empty `__init__` method that calls the super `__init__` method.

Then import the Trigger decorator from the ModuleDecorator file.

Now within your class you can create functions that are triggered by hodge podge as such

```python
@Trigger(moduleInstance, regex, access)
def roll(self, context):
    print("Doing the Roll")
```

> Trigger decorator

The trigger decorator must take in
1. The module instance (i.e `self`)
2. The regex on which you want this function to be triggered (regex groups will be given to your function via `context`)
3. A access list specifying the roles that people must have to use. If empty everyone is assumed to have access

for example

```python
@Trigger(self, 'hodge podge do me a solid and roll a d(\d+)', [])
def roll(self, context):
    dice = int(context["groups"][1])
    print("Doing the Roll On A d%d dice!"%dice)
```

> context








## TODO

#### code

1. hodge podge processRequest + erroring
2. parser module clash handling
3. formatter/erroring
4. make better paramater checking system (built into parser?)

#### Features
- voice Channel + Google Module
- CostCo Bot For Gold / integrate leonbot
- update personality module to know peoples names and birthdays etc.
- reminders
- have hodge podge respond to "who do you work for"
- have hodge podge respond to "what is love"
- have typo detection / more robust trigger questions
- integrate with DnD Beyond!
- nickname for channels
- override command to just make hodge podge say something
- mini learning algorithm to learn memes by observation (if a gif is sent what triggered it?)
  - Natural Language Processing
- Website for hodge podge command interface (www.zainafzal.com/hpci)
- update documentation to include default values for objects
- Add system to handle database failure connection with a hard restart :D
- Help command for each module (unified help system?? print out from github?)
- Module to have shortcut commands / system in bot
- Massive Change log
- binary translator / encryptor
- clean up heroku to have 2 project, a off test bot (that is on when in dev) and a on hodge podge
- if the database crashes he just spams every channel
- log system
- error message should be DISTRESSED BEEPING
- have spell search work with commas
- math expression evaluator
- quick commands i.e \hp for hodge podge
- give option to validate hodge podge
- let people roll dice with adjectives
- remember command
- markcov chains -> conversations
