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
3. A access list specifying the roles that people must have to use. If empty `@everyone` is inserted

for example

```python
@Trigger(self, 'hodge podge do me a solid and roll a d(\d+)', [])
def roll(self, context):
    dice = int(context["groups"][1])
    print("Doing the Roll On A d%d dice!"%dice)
```

> context
