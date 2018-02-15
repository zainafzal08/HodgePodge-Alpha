# Hodge Podge Documentation!

A small discord bot to be sweet, keep track of Dnd rescoures, send memes and help you search spells.
Inspired by TAZ! Hodge podge by default doesn't do anything but keep track of it's users and their
access levels. But when you start adding in modules he becomes very fun!

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

## Game

The Game module is a little module to roll dice and keep track of points, Lots of fun!
Check out the commands:

| Command                                  | Description | Example |
| ---------------------------------------- | ----------- | ------- |
| hodge podge roll a d<X>                  | Have hodge podge roll a dice! supports d1 to d1000 | `hodge podge roll a d20`
| hodge podge roll <Y> d<X>s               | Have hodge podge roll a dice Y times! supports up to 1000 d1000 | `hodge podge roll 3 d8's`
| hodge podge give <U> <X> <T> points      | Gives a user <U> (should be a @ tag) <X> points of <T> | `hodge podge give @AAA 10 xp points`
| hodge podge take <X> <T> points from <U> | Same as above but substracts points | `hodge podge take 10 xp points from @AAA`
| hodge podge list all score points | List all score types (such as xp or goof points) in the current channel | `N/A` |
| hodge podge summerise <T> points | List all users and their scores (if they have scores) for score type <T> | `hodge podge summerise xp points`
