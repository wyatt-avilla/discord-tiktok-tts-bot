import discord
from discord import app_commands
from discord.ext import commands
from discord import FFmpegPCMAudio
from sensitive import TOKEN

bot = commands.Bot(command_prefix = "`", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("bot started")
    try:
        synced = await bot.tree.sync()
        print("synced properly")
    except Exception as err:
        print(f"unable to sync properly with exception: {err}")


@bot.tree.command(name = "affirm", description = "<3")
async def affirm(interaction: discord.Interaction):
    await (interaction.user).send("i love u")
    await interaction.response.send_message("check ur dms", ephemeral=True)

@bot.tree.command(name = "join", description = "joins ur vc")
async def join(interaction: discord.Interaction):
    try:
        await (interaction.user.voice.channel).connect()
    except Exception as err:
        await interaction.response.send_message(f"unable to join voice with exception: {err}")

@bot.tree.command(name = "leave", description = "leaves voice")
async def leave(interaction: discord.Interaction):
    try:
        await (interaction.guild.voice_client).disconnect()
    except Exception as err:
        await interaction.response.send_message(f"unable to leave voice with exception: {err}")

@bot.tree.command(name = "debug", description = "debug tool")
async def debug(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"ur voice channel is {interaction.user.voice.channel}, + \
                                                ur voice state is ")
    except Exception as err:
        await interaction.response.send_message(f"wow, even the debug has errors... {err}")

@bot.tree.command(name = "playtest", description = "convertstext")
@app_commands.describe(text = "text to be converted")
async def playtest(interaction: discord.Interaction, text: str):
    testlink = "http://noproblo.dayjo.org/ZeldaSounds/WW_New/WW_MainMenu_Start.wav"

    current_voice = interaction.guild.voice_client
    play_source = discord.FFmpegPCMAudio(source=testlink, executable='ffmpeg')
    await current_voice.play(source=play_source, after=None)
    await interaction.response.send_message(f"attempting to play {text}")





if __name__ == "__main__":
    bot.run(TOKEN)