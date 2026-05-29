import discord
from dotenv import load_dotenv
import os


def memory_read(filename="tick.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            text = f.read().strip()
            return int(text) if text.isdigit() else 0
    return 0

def memory(data, filename="tick.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        f.write(str(data))

async def makechannel(message):
    user = message.author
    guild = message.guild
    current_tick = memory_read()

    if guild is None:
        return await message.channel.send("This command must be used in a server.")

    admin_role_name = os.environ.get("ADMIN")
    admin_role = discord.utils.get(guild.roles, name=admin_role_name)
    category = discord.utils.get(guild.categories, name="tickets")

    if category is None:
        return await message.channel.send("No category named `tickets` found.")

    if not admin_role_name:
        return await message.channel.send("The ADMIN role name is not configured in the environment.")

    if admin_role is None:
        return await message.channel.send(f"Role `{admin_role_name}` not found.")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        admin_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    next_tick = current_tick + 1
    channel_name = f"ticket-{next_tick}"

    try:
        memory(next_tick)
        channel = await category.create_text_channel(
            name=channel_name,
            overwrites=overwrites
        )

    except Exception as exc:
        await message.channel.send(f"Failed to create ticket channel: {exc}")
        return

    await channel.send(f'{admin_role.mention}')

