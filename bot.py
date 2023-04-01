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
@app_commands.describe(voice = "the voice to be used", text = "text to be converted to to speech")
@app_commands.choices(voice = [
    Choice(name = "American Woman", value = "en_us_001"),
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

    if bot_voice_client != None:
        try:
            converted_text = request_tts_conversion(text, voice)
            vc = interaction.guild.voice_client
            player = discord.FFmpegPCMAudio(source= converted_text)

            vc.play(player)

            await interaction.response.send_message(f"successfully converted: `\"{text}\"`", ephemeral = True)

        except Exception as err:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            print(f"Exception: {err}")
    else: 
        try:
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

@bot.tree.command(name = "sing", description = "sings given text", guild=(discord.Object(id=1043400553385955350)))
@app_commands.describe(voice = "the voice to be used", text = "text to be sung")
@app_commands.choices(voice = [
    Choice(name = "Alto Singing", value = "en_female_f08_salut_damour"),
    Choice(name = "Tenor Singing", value = "en_male_m03_lobby"),
    Choice(name = "Sunshine Soon", value = "en_male_m03_sunshine_soon"),
    Choice(name = "Warmy Breeze", value = "en_female_f08_warmy_breeze"),
    Choice(name = "Glorious", value = "en_female_ht_f08_glorious"),
    Choice(name = "It Goes Up", value = "en_male_sing_funny_it_goes_up"),
    Choice(name = "Chipmunk", value = "en_male_m2_xhxs_m03_silly"),
    Choice(name = "Dramatic", value = "en_female_ht_f08_wonderful_world"),
])
async def sing(interaction: discord.Interaction, voice: str, text: str):
    bot_voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if bot_voice_client != None:
        try:
            converted_text = request_tts_conversion(text, voice)
            vc = interaction.guild.voice_client
            player = discord.FFmpegPCMAudio(source= converted_text)

            vc.play(player)

            await interaction.response.send_message(f"successfully sung: `\"{text}\"`", ephemeral = True)

        except Exception as err:
            await interaction.response.send_message("something went wrong", ephemeral=True)
            print(f"Exception: {err}")
    else: 
        try:
            await (interaction.user.voice.channel).connect()
        except Exception as err:
            await interaction.response.send_message(f"attempt to join voice failed", ephemeral= True)
            print(err)
        try:
            converted_text = request_tts_conversion(text, voice)
            vc = interaction.guild.voice_client
            player = discord.FFmpegPCMAudio(source= converted_text)

            vc.play(player)

            await interaction.response.send_message(f"successfully sung: `\"{text}\"`", ephemeral= True)

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