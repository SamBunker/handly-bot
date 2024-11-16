import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import discord.utils
import random

my_secret = os.environ['TOKEN']
my_guild = os.environ['MyGuild']
app_id = os.environ['AppID']
message_channel = os.environ['CommitsUpdatesChannel']
voice_channel = os.environ['CommitsEditChannel']

class aclient(discord.Client):
  def __init__(self):
    super().__init__(
      command_prefix = '$',
      intents=discord.Intents.default(),
      application_id = app_id)
    self.synced = False

    async def setup_hook(self):
      await self.load_extension(f'cogs.gitlab_channel_update.py')
      await self.tree.sync(guild = discord.Object(id = my_guild))

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild = discord.Object(id = my_guild))
      synced = True
    print("Winkle is Synced with the Clouds!")
    change_status.start()
    print(f"☁️ Winkle has connected as {client.user} (ID: {client.user.id})")
    print("Spreading the love!")

client = aclient()
tree = app_commands.CommandTree(client)

# @tree.command(name = "plant", description="Plant a seed, grow it daily.", guild = discord.Object(id = my_guild))
# async def plant_slash(interaction: discord.Interaction, name: str):
#   await interaction.response.send_message(f"{name} has planted a seed. Grow it daily with ``/water``.")

# @tree.command(name = "postjob", description="Post a Job Embed", guild = discord.Object(id = my_guild))
# async def post_job_slash(interaction: discord.Interaction, name: str):
#   await interaction.response("Post_Job Confirmed", ephermal = "true")

# @tree.command(name = "post", description="Post a Embed to a Channel", guild = discord.Object(id = 958409313196605440))
# async def post_slash(interaction: discord.Interaction, color: str, *):

#Updating Commits Channel
@client.event
async def on_message(message):
  if message.author.bot:
    return
  
  if message.channel.id == message_channel:
    guild = message.guild
    voice_channel = guild.get_channel(voice_channel)

    if voice_channel is None or not isinstance(voice_channel, discord.VoiceChannel):
      print("Voice channel not found or is not a VoiceChannel.")
      return
    
    #Update the voice channel's name
    new_name = voice_channel.name
    print(new_name)



# Work in Progress, Join a Voice Chat, Delete after leaving.
temp_channels = []
print(temp_channels)
@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
  possible_channel_name = f"🟣 {member.name}'s Bubble"
  try:
    if after.channel.name == "Create a Voice Channel":
      temp_channel = await after.channel.clone(name=possible_channel_name)
      await member.move_to(temp_channel)  
      temp_channels.append(temp_channel.id)
  except Exception as e:
    pass

  for c in client.guilds:
    for channel in c.channels:
      if str(channel.type) == "voice":
        if channel.id in temp_channels:
          if len(channel.members) == 0:
            try:
              nullID = channel.id
              await channel.delete()
              temp_channels.remove(nullID)
            except Exception as e:
              print(e)
          else:
            return

status = ([
    "Spreading Kindness 🪴", "Sending Love ❤️"
])

@tasks.loop(minutes=15)
async def change_status():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(random.choice(status)))
  
# --- COMMANDS ---
# @client.slash_command(guild_ids = my_guild, description='Spread some love! 🪴')
# async def love(ctx: discord.ApplicationContext):
#   await ctx.respond("🪴 Thank you for spreading some love! Cacti really appreciates it!")

client.run(my_secret)