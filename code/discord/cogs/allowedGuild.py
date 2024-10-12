from functools import wraps
from discord.ext import commands

def is_allowed_guild(func):
    @wraps(func)
    async def wrapper(self, ctx:commands.Context, *args, **kwargs):
        if ctx.guild and ctx.guild.id == self.guild.id:
            return await func(self, ctx, *args, **kwargs)
        else:
            await ctx.send("This command cannot be used in this guild.")
            return None
    return wrapper
