import discord
from discord.ext.commands import Bot

from Meme import Meme

BOT_PREFIX = "!"
TOKEN = ""
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    print('is ready')


@client.event
async def on_member_join(member):
    client.say("Hello")
    role = discord.utils.get(member.server.role, name='DICORD_ROLE')
    await client.add_roles(member, role)


@client.command(channel='')
async def meme():
    try:
        get = Meme().run()
        title = get["title"]
        image = get["image"]

        embed = discord.Embed(title=title, color=discord.Color.dark_blue())
        embed.set_image(url=image)
        await client.send_message(discord.Object(id='CHANNEL_ID'), embed=embed)

    except Exception:
        await client.say('Error')


client.run(TOKEN)
