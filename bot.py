import discord
from discord import app_commands
from discord.ext import commands
from json_request import request_tts_conversion
from sensitive import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix = "`", intents = intents)

@bot.event
async def on_ready():
    print("bot started")
    try:
        synced = await bot.tree.sync()
        print(f"synced properly ({len(synced)} commands)")
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
        await interaction.response.send_message("omw", ephemeral = True)
    except Exception as err:
        await interaction.response.send_message(f"unable to join voice with exception: {err}")

@bot.tree.command(name = "leave", description = "leaves voice")
async def leave(interaction: discord.Interaction):
    bot_voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if bot_voice_client != None:
        try:
            await (bot_voice_client).disconnect()
            await interaction.response.send_message("byeee", ephemeral = True)
        except Exception as err:
            print(f"bot was unable to leave voice with the exception: {err}")
            await interaction.response.send_message(f"something went wrong while attempting to leave the vc, check the console for details", ephemeral = True)
    else:
        await interaction.response.send_message(f"im not in vc", ephemeral = True)

@bot.tree.command(name = "debug", description = "debug tool")
async def debug(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"check console")
        print(f"user: {interaction.user}")
        print(f"user voice channel: {interaction.user.voice.channel}")
        print(f"user voice client: {interaction.guild.voice_client}")
        print(f"user voice state: {interaction.user.voice}")
        print(f"bot channel: {interaction.guild.voice_channels}")
        print(f"bot voice client: {discord.utils.get(bot.voice_clients, guild=interaction.guild)}")
        print(f"current guild id: {interaction.guild_id}")
        print(f"current guild: {interaction.guild}")

        if (interaction.guild.voice_client) == (discord.utils.get(bot.voice_clients, guild=interaction.guild)):
            print("bot and user have same voice client")

    except Exception as err:
        await interaction.response.send_message(f"wow, even the debug has errors... {err}")

@bot.tree.command(name = "sync", description = "syncs commands")
async def sync(interaction: discord.Interaction):
    try:
        await bot.tree.sync(guild=discord.Object(id=1043400553385955350))
        await interaction.response.send_message(f"synced commands properly")
    except Exception as err:
        await interaction.response.send_message(f"unable to sync with exception: {err}")

@bot.tree.command(name = "tts", description = "reads text in the funny tiktok voice", guild=(discord.Object(id=1043400553385955350)))
@app_commands.describe(text = "text to be converted to to speech")
async def tts(interaction: discord.Interaction, text: str):

    try:
        converted_text = request_tts_conversion(text)
        vc = interaction.guild.voice_client
        player = discord.FFmpegPCMAudio(source= converted_text)

        vc.play(player)

        await interaction.response.send_message(f"successfully converted: `\"{text}\"`", ephemeral = True)

    except Exception as err:
        await interaction.response.send_message("something went wrong", ephemeral=True)
        print(f"Exception: {err}")



@bot.tree.command(name = "test", guild=(discord.Object(id=1043400553385955350)))
async def test(interaction: discord.Interaction, param: str):
    #print(f"The state of this interaction is: {interaction.is_expired()}")
    print(f"this interaction expires at: {interaction.expires_at}")

    if param == "1":
        await interaction.response.send_message("send_message")
    elif param == "2":
        await interaction.followup.send("followup message")
    elif param == "3":
        await interaction.delete_original_response()
    elif param == "4":
        await interaction.response.defer()
        await interaction.followup("followed up here !")


if __name__ == "__main__":
    bot.run(TOKEN)