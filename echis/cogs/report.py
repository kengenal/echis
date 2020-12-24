import discord

from echis.main.settings import ADMIN_CHANNEL
from echis.modules import mixins
from discord.ext.commands import has_permissions, command


class Report(mixins.BaseCog):
    @command(pass_context=True)
    async def report(self, ctx, user_id: int = None, description: str = None):
        """  send report user, pattern accepts user_id and description like '!report 55555 "this guy is toxic"' """
        if user_id is not None and description is not None:
            description = str(description)
            author = ctx.message.author.name
            name = self.client.get_user(user_id)
            channel = ADMIN_CHANNEL
            chan = discord.utils.get(self.client.get_all_channels(), name=channel)
            embed = discord.Embed(olour=discord.Color.red())
            embed.set_author(name="Report")
            embed.add_field(name=f"User {author}: send report to {name} : {user_id}",
                            value=description, inline=True
                            )
            await ctx.send("Report has been sended")
            chan = self.client.get_channel(int(chan.id))
            await chan.send(embed=embed)
        else:
            await ctx.send("The variabe can not be empty")

    @command()
    @has_permissions(administrator=True)
    async def find(self, ctx, user_id: int):
        """ you can find user if have admin permission, takes user id  """
        current_channel = ctx.message.channel.name
        channel_name = ADMIN_CHANNEL
        if str(current_channel) == str(channel_name):
            if id:
                name = self.client.get_user(user_id)
                await ctx.send(f"Name: {name}")
            else:
                await ctx.send("Admin channel not found")


def setup(client):
    client.add_cog(Report(client))
