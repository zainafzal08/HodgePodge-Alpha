# Bot Party

A wonderful modular system built in python that lets you construct bots which can use databases, respond to inputs, play music and more!

Hosted with <3 on Heroku

## shit

Run will forward messages to all bots it knows about
Bots have a list of modules.
Each module has a set of triggers that it registers with the bots parser.
on a message the parser produces a match object which maps the input string to
a function in a module.
the bot then will trigger the module to process the input and then give the module
the client object so it can respond if it needs to.

## Bots

The rest of this documentation will describe how to build a module for a bot. To build a bot
you just have to have a class with 1 input into the constructor which will be the discord client object, a getHelp method and the talk method.
The talk method will take in a discord message object and do what it pleases with that information, printing out stuff when it's ready to respond. How it does it is up to you but take a look at HodgePodge for some ideas. There is a section in this document on Utility classes provided to help with parsing commands and formatting output.
The getHelp method can just return None if you do not want any help messages for your bots modules.
otherwise it must return a help object with 2 fields. `cmds` which is a list of tuples each with 2 fields+ 1 optional field. the command, a description and a optional example.

## Module Structure

Modules are independent pieces of logic that are triggered by input and can respond.
You _can_ make your own to suit your own bot but this system works well if you choose to use the given utilties.
Just inherent from the BotModule class and read below.

Every module needs to have 3 functions defined

1. connectDb
  - This will pass a instance of the database to the module in case it needs to
   query or update it's own tables
2. getTriggerList
  - This must return a list of trigger request objects that allow the system to
  detect when the module must be notified of a event and what information it needs
3. respond
  - Once the module has been triggered it will be given the client and channel it was triggered in
  so it can respond. It will also be given a context object which gives some info on in what context you are being triggered in (see parser for more info). You can respond manually but using the formatter helper class is advised
  - Should be async because it'll prob be calling asynf send functions in discord

This is the bear minimum, of course you will need to define functions that will be triggered.
See the parser documentation for more info.

You can also add in some optional functions if you so choose

1. getHelp
  - you only need this function if you use the same setup for the reccomended bot getHelp command
  - this must return a help obj with 2 field `docs`, a link to full documentation and `raw` a link to the a markdown file which has a `!!start command list` and `!!end command list` wrapped table of commands
  - if the table exists the bot will extract the list send send it to the request channel. if someone types in "<bot name> help with <module name>"

note with getHelp the table in the raw markdown file must conform to

| Command                                  | Description | Example |
| ---------------------------------------- | ----------- | ------- |
| example command                          | ...         | ...     |

Take a look at Hodge Podge. My pride and joy.

## Utility classes

#### Data base

The database is very generic, It's mostly just a wrapper over the actual sql
statements sent to the server. This does allow any module to use the db without having
to build the relevant functions or statement though.
The object has a couple functions to be used

> edit

This allows you to insert or update information in a tables

| Field  | Type | Description                                                   |
| ------ | ---- | ------------------------------------------------------------- |
| TABLE  | str  | the table to be edited                                        |
| SET    | list | list of fields to update/insert                               |
| VALUE  | list | list of values to insert/update that match the fields in SET  |
| WHERE  | obj  | object with all the search fields to find a row to update     |
| RETURN | str  | return either the old ("OLD") row or updated row ("NEW")      |
| FORCE  | bool | If the row doesn't exist to be updated should it be inserted? |

example:
```python
request = {
    "TABLE": "SCORES"
    "SET": ["SCORE"],
    "VALUE": [score],
    "WHERE": {
        "CHANNEL": message.channel.id,
        "TYPE": scoreType,
        "PERSON": person.id
    },
    "RETURN": "NEW",
    "FORCE": True
}
```

> Get

This allows you to query information in a table

**DO NOT USE THIS WITH USER INPUT, USE SEARCH**

| Field    | Type | Description                                                   |
| -------- | ---- | ------------------------------------------------------------- |
| TABLE    | str  | the table to be edited                                        |
| GET      | list | list of fields to grab                                        |
| WHERE    | obj  | object with all the search fields to find matching rows       |
| DUP      | bool | Should duplicate rows be included?                            |
| CASE_INS | bool | If the search should be case insensitive on the WHERE fields  |

example:
```python
request = {
    "TABLE": "SCORES",
    "GET": ["TYPE"],
    "WHERE": {
        "CHANNEL" : message.channel.id
    },
    "DUP": False,
    "CASE_INS": True
}
```

> Search

This is the same as `get` but sanitises all input and looks for close sub string
matches rather then direct matches so you can pipe user search terms into the
database directly to find matches.

#### Parser

This is the system which parses input messages against all known triggers and
informs the relevant. Note that the parser is case insensitive.
it is also puncuation sensitive but you can ask it to ignore full stops etc.

*Trigger Request Objects*

A sample trigger request may be
```python
{
  "trigger": "hodge podge take (\d+) (.*) points? from (.*)\s*$",
  "function": self.editPoints,
  "accessLevel": self.scoreEditLevel,
  "id": 1,
  "ignore": ['.',',']
})
```

the trigger is a regex statement all messages in a chat are parsed against.
Any groups will be given to the trigger function when called. See the parser
documentation for more info.

accessLevel is what level the message sender must be to activate the command
see access levels for more info on how levels work

id is for the case that 1 function is used with multiple regex inputs. It is also
given to the triggered function to disambiguate between these regexs. This is optional.

ignore is a set of characters to remove from the message before attempting to match it.

this is useful if you would like `hi!` `hi` `hi.` all to trigger a function as you
could set ignore to be `[',','.','!']`

*Trigger functions*

Within the module object you must have functions that match the ones that you put
into the trigger request objects.
They must match the prototype `def <f>(self, trigger)` where `trigger` is the
trigger object.

The trigger object is how the parser tells your module of the context of it's activation.

it contains the following fields

| Field | Type | Description                                                                  |
| ----- | ---- | -----------------------------------------------------------------------------|
| args  | list | The list of matched groups from the request regex                            |
| id    | str  | The id of the trigger request this matched against (None if no id was given) |


*Formatter*

This just lets you put in lists and things to print out into a buffer and flush them out using a default
pattern in your bot's respond object.

The code is very self explantory, the real use of the formatter is consistent response styles from the bot and a clean buffer to work with our output dynamically across functions and locations in call cycles.

note that flush is async because it uses discords async send message functions
