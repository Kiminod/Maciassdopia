from functools import wraps

def is_allowed_guild(func):
    @wraps(func)
    async def wrapper(self, ctx, *args, **kwargs):
        if ctx.guild and ctx.guild.id == self.guild.id:
            return await func(self, ctx, *args, **kwargs)
        else:
            await ctx.send("This command cannot be used in this guild.")
            return None
    return wrapper
