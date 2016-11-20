from discord.ext import commands
from cogs.utils.dataIO import dataIO
import discord
from __main__ import send_cmd_help


class companycog:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.db = dataIO.load_json("data/company.json")  # load company db
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        dataIO.save_json("data/company.json", self.db)

    @commands.group(no_pm=True, invoke_without_command=True, pass_context=True)
    async def company(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @company.command(pass_context=True)
    async def create(self, ctx):
        """Creates a company!"""
        if ctx.message.server.id not in self.db:
            self.db[ctx.message.server.id] = {}  # if the server isnt in db it will add server
        if ctx.message.author.id not in self.db[ctx.message.server.id]:
            self.db[ctx.message.server.id][ctx.message.author.id] = 5  # starting balance of 5
            self.save_db()  # save
            await self.bot.say("You're company is now registered.")
        else:
            await self.bot.say("You can't have two companies yet!")
            
    @company.command(pass_context=True)
    async def balance(self, ctx, *, user: discord.Member= None):
        """Checks how much money you've invested in your company!"""
        if user is None:  # if there is no user being mentioned it willview your balance
            user = ctx.message.author
        if user.id in self.db[ctx.message.server.id]:
            userdb = self.db[ctx.message.server.id][user.id]
            await self.bot.say('The Company owned by User {}  Has: {} funds.'.format(user.name, userdb))
        else:
            await self.bot.say('Create a company with [prefix]company create')  # says you need a account

    @company.command(pass_context=True) # puts money into your company bank
    async def invest(self, ctx, *, amount: int, user: discord.Member= None):
        bank = self.bot.get_cog('Economy').bank
        if amount > 0:
                    if bank.can_spend(user, amount):
                        bank.withdraw_credits(user, amount)
                        self.db[ctx.message.server.id][ctx.message.author.id] += amount
                        dataIO.save_json(self.file_path, self.system)
                    else:
                        await self.bot.say('Get more money or get a company with [prefix]company create')
                        
    @company.command(pass_context=True) # takes money out of your company bank
    async def unvest(self, ctx, *, amount: int, user: discord.Member= None):
        bank = self.bot.get_cog('Economy').bank
        if amount > 0 and self.db[ctx.message.server.id][ctx.message.author.id] > 0:
                        bank.deposit_credits(user, amount)
                        self.db[ctx.message.server.id][ctx.message.author.id] -= amount
                        dataIO.save_json(self.file_path, self.system)
        else:
                        await self.bot.say('Get more money or get a company with [prefix]company create')

def setup(bot):
    bot.add_cog(companycog(bot))
