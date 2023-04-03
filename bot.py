import discord
from discord import app_commands
from discord.app_commands import Choice
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

@bot.tree.command(name = "join", description = "joins ur vc")                                                   # /join command
async def join(interaction: discord.Interaction):
    user_voice_channel = interaction.user.voice
    if user_voice_channel != None:
        try:
            await (user_voice_channel.channel).connect()
            await interaction.response.send_message("omw", ephemeral = True)
        except Exception as err:
            await interaction.response.send_message(f"unable to join voice", ephemeral=True)
            print(f"bot was unable to join voice with exception: {err}")
    else:
        await interaction.response.send_message("u have to be in a voice call to use this command")

@bot.tree.command(name = "leave", description = "leaves voice")                                                 # /leave command
async def leave(interaction: discord.Interaction):
    bot_voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if bot_voice_client != None:
        try:
            await (bot_voice_client).disconnect()
            await interaction.response.send_message("byeee", ephemeral = True)
        except Exception as err:
            print(f"bot was unable to leave voice with the exception: {err}")
            await interaction.response.send_message(f"something went wrong while attempting to leave the vc", ephemeral = True)
    else:
        await interaction.response.send_message(f"im not in vc", ephemeral = True)

@bot.tree.command(name = "tts", description = "reads text in a funny tiktok voice")                             # /tts command
@app_commands.describe(voice = "the voice to be used", text = "text to be converted to to speech")
@app_commands.choices(voice = [                                                                                 # values for the choices are passed to
    Choice(name = "Classic", value = "en_us_001"),                                                              # json_request.py and sent in an HTTP request
    Choice(name = "American Man 1", value = "en_us_006"),
    Choice(name = "American Man 2", value = "en_us_007"),
    Choice(name = "American Man 3", value = "en_us_008"),
    Choice(name = "American Man 4", value = "en_us_010"),
    Choice(name = "British Man 1", value = "en_uk_001"),
    Choice(name = "British Man 2", value = "en_uk_003"),
    Choice(name = "Australian Woman", value = "en_au_001"),
    Choice(name = "Australian Man", value = "en_au_002"),
    Choice(name = "German Man", value = "de_002"),
    Choice(name = "Spanish Man", value = "es_002"),
    Choice(name = "Spanish (MX) Man", value = "es_mx_002"),
    Choice(name = "Indonesian Woman", value = "id_001"),
    Choice(name = "Japanese Woman 1", value = "jp_001"),
    Choice(name = "Japanese Woman 2", value = "jp_003"),
    Choice(name = "Japanese Woman 3", value = "jp_005"),
    Choice(name = "Japanese Man", value = "jp_006"),
    Choice(name = "Korean Man", value = "kr_004"),
    Choice(name = "Korean Woman", value = "kr_003"),
    Choice(name = "Ghostface", value = "en_us_ghostface"),
    Choice(name = "Chewbacca", value = "en_us_chewbacca"),
    Choice(name = "C3PO", value = "en_us_c3po"),
    Choice(name = "Stitch", value = "en_us_stitch"),
    Choice(name = "Stormtrooper", value = "en_us_stormtrooper"),
    Choice(name = "Rocket", value = "en_us_rocket"),
])
async def tts(interaction: discord.Interaction, voice: str, text: str):
    bot_voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if bot_voice_client != None:                                                                                # triggers if the bot is already connected to 
        try:                                                                                                    # a voice channel in the current server
            converted_text = request_tts_conversion(text, voice)
            vc = interaction.guild.voice_client
            player = discord.FFmpegPCMAudio(source= converted_text)

            vc.play(player)

            await interaction.response.send_message(f"successfully converted: `\"{text}\"`", ephemeral = True)

        except Exception as err:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            print(f"Exception: {err}")
    else:                                                                                                      # if the bot isn't in a voice call, it attempts
        try:                                                                                                   # to join before playing TTS
            await (interaction.user.voice.channel).connect()
        except Exception as err:
            await interaction.response.send_message(f"attempt to join voice failed", ephemeral= True)
            print(err)
        try:
            converted_text = request_tts_conversion(text, voice)
            vc = interaction.guild.voice_client
            player = discord.FFmpegPCMAudio(source= converted_text)

            vc.play(player)

            await interaction.response.send_message(f"successfully converted: `\"{text}\"`", ephemeral= True)

        except Exception as err:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            print(f"Exception: {err}")


if __name__ == "__main__":
    bot.run(TOKEN)