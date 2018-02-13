# HodgePodge

A small discord bot to be sweet, keep track of Dnd rescoures, send memes and help you search spells.
Inspired by TAZ!

Hosted with <3 on Heroku

## shit

Run will forward messages to all bots it knows about
Bots have a list of modules.
Each module has a set of triggers that it registers with the bots parser.
on a message the parser produces a match object which maps the input string to
a function in a module.
the bot then will trigger the module to process the input and then give the module
the client object so it can respond if it needs to.

## Access levels

Every user in every server with the chat has a access level. By default this is `0`
If the user has a known admin/maintence role such as `bot-boys` they will be elevated to
level `1`.
if the user is a super admin, i.e one of the engineering or testing crew,
they will be elevated to level `2`

This is calculated on a per message basis to allow the run system to only trigger
commands that a user is allowed to use.

If you want to have a role added or to become a super admin contact zain.afz@gmail.com

Note that commands that allow you to see information outside of your server i.e
commands that let you change points for a player in another server, should be
level `2` commands. the level `1` status is designed for people to have power over
the bot within the bounds of their server.
Any more power should only be afforded to development teams.

## Module Structure

Modules are independent pieces of logic that ate triggered by input and can respond.
Every module needs to have 3 functions defined

1. connectDb
  - This will pass a instance of the database to the module in case it needs to
   query or update it's own tables
2. getTriggerList
  - This must return a list of trigger request objects that allow the system to
  detect when the module must be notified of a event and what information it needs
3. respond
  - Once the module has been triggered it will be given the client and channel it was triggered in
  so it can respond. You can do this manually but using the formatter helper class is advised

This is the bear minimum, of course you will need to define functions that will be triggered.
See the parser documentation for more info.

## Data base

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
```
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
```
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


## Parser

This is the system which parses input messages against all known triggers and
informs the relevant. Note that the parser by default is case insensitive.
it is also puncuation sensitive but you can ask it to ignore full stops etc.

#### Trigger Request Objects

A sample trigger request may be
```
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

#### Trigger functions

Within the module object you must have functions that match the ones that you put
into the trigger request objects.
They must match the prototype `def <f>(self, trigger)` where `trigger` is the
trigger object.

the trigger object is how the parser tells your module of the context of it's activation.

it contains the following fields

| Field | Type | Description                                                                  |
| ----- | ---- | -----------------------------------------------------------------------------|
| args  | list | The list of matched groups from the request regex                            |
| id    | str  | The id of the trigger request this matched against (None if no id was given) |
