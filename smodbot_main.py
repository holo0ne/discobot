import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

with open(".token", 'r') as file_token:
    BOT_TOKEN = file_token.read()

GUILD_ID = discord.Object(id=1165695453732536370)

submission_ideas = []
submission_authors = []
screenshots = []
round_idea : str
round_author : str


intents = discord.Intents.default()
intents.message_content = True


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    synced_commands = []

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        Client.synced_commands = await self.tree.sync(guild=GUILD_ID)


client = Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}, bot latency is {round(client.latency * 1000)}ms')
    print(f'Synced {len(client.synced_commands)} commands to guild {GUILD_ID.id}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

#TODO: refactor to send only one message in case of multiple attachments
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                await message.channel.send(f"Ваш скріншот *{attachment.filename}* зареєстровано")
                screenshots.append(attachment.url)
            else:
                await message.channel.send(f"Невідомий формат файлу *{attachment.filename}*, будь ласка загрузіть "
                                           "скріншоти у форматі **png**, **jpg**, **jpeg** або **gif**")


@client.tree.command(name="submit", description="Відправити свою ідею для челенджу", guild=GUILD_ID)
async def submit_idea(interaction: discord.Interaction, idea: str):
    submission_ideas.append(idea)
    submission_authors.append(interaction.user.display_name)
    await interaction.response.send_message(f"**{interaction.user.name}** запропонував нову ідею для челенджу")


@client.tree.command(name="start", description="Почати челендж", guild=GUILD_ID)
async def start_challenge(interaction: discord.Interaction):
    embed_prefase = discord.Embed(title="🔥 Ви готові почати змагання? 🔥",
                                  description="Натисніть кнопку нижче, щоб запустити челендж",
                                  color=discord.Color.random())

    #TODO: check for len(submission_ideas) to use correct form of word 'ідея'
    #TODO: make unable to guess submission author by list of people who submitted ideas

    embed_prefase.add_field(name=f"Наразі отримано {len(submission_ideas)} ідеї від цих учасників:",
                            value=submission_authors)

    class StartChallengeView(discord.ui.View):
        @discord.ui.button(label="Почати змагання!", style=discord.ButtonStyle.green, emoji="🚀")
        async def button_start(self, interaction: discord.Interaction, button: discord.ui.Button):
            channel = interaction.channel
            button.style = discord.ButtonStyle.red
            button.emoji = "⏳"
            button.label = "Змагання почалось"
            button.disabled = True
            await interaction.response.edit_message(view=self)

            #TODO: add timer with remaining count to button
            #TODO: add button to skip currently selected idea

            global round_idea
            global round_author
            round_idea = random.choice(submission_ideas)
            round_author = submission_authors[submission_ideas.index(round_idea)]
            submission_ideas.remove(round_idea)
            submission_authors.remove(round_author)

            #TODO: remove randomly selected entry from the list of submission_ideas along with submission author

            embed_refs = discord.Embed(title="📢 Увага всім учасникам! 📢",
                                       description="Стартує перший етап підготовки.",
                                       color=discord.Color.random())
            embed_refs.add_field(name="Тема цього раунду:", value=f"***{round_idea}***")
            embed_refs.set_footer(text=f"Зараз саме час пошукати натхнення і референсів\n"
                                       f"Маєте 3 хв, поїхали🚀️")

            await channel.send(embed=embed_refs)

            await asyncio.sleep(10.0)

            await channel.send("🟢️ Увага, переходимо до моделінгу. Час пішов⏳\n")
            await asyncio.sleep(10.0)

            #WARNING about half-time passed for challenge
            await channel.send("🟡️ Увага, половина часу вже пройшла. Залишилося **7.5 хв**, тому покваптеся 🔔️")
            await asyncio.sleep(10.0)

            #STOP challenge
            embed_stop = discord.Embed(title="🛑️ Увага, час вийшов!⌛",
                                       description="Підготуйте свої скріншоти для загрузки 🖼")
            embed_stop.set_footer(text="Xто не встигне загрузити свій скріншот той програв 😵")

            await channel.send("@here", embed=embed_stop)
        #TODO: change client presence during challenge

    if submission_ideas:
        await interaction.response.send_message(embed=embed_prefase, view=StartChallengeView())
    else:
        await interaction.response.send_message("Оу ноу... Ніхто ще не надіслав жодної ідеї для челенджу\n"
                                                "Використовуйте команду **/submit** щоб запропонувати свою ідею 💡️",
                                                ephemeral=True)


@client.tree.command(name="results", description="Показати скріншоти прислані учасниками", guild=GUILD_ID)
async def display_screenshots(interaction: discord.Interaction):
    #global round_idea
    embeds = []

    #embed = discord.Embed(title="Результати раунду", description=f"Тема раунду була: {round_idea}",
    #                      color=discord.Color.random())

    if screenshots:
        i = 1
        for url in screenshots:
            embed = discord.Embed(title=f'Скріншот № **{i}**')
            embed.set_image(url=url)
            embeds.append(embed)
            i += 1
        await interaction.response.send_message(embeds=embeds)
    else:
        await interaction.response.send_message("Нажаль ще ніхто не загрузив своїх скріншотів", ephemeral=True)


#We define this function globally to be able to call it with slash command or context menu
async def cyberbully(bully: str, victim: str):
    def load_bully():
        with open("res/bully_phrases.txt", 'r') as file:
            bully_list = file.readlines()
        bully_list = [line.strip() for line in bully_list]
        return bully_list

    def load_statements():
        with open("res/bully_statements.txt", 'r') as file:
            statement_list = file.readlines()
        statement_list = [line.strip() for line in statement_list]
        return statement_list

    def load_questions():
        with open("res/bully_questions.txt", 'r') as file:
            question_list = file.readlines()
        question_list = [line.strip() for line in question_list]
        return question_list

    bully_phrases = load_bully()
    statement_phrases = load_statements()
    question_phrases = load_questions()

    bully_string = random.choice(bully_phrases)
    statement_string = random.choice(statement_phrases)
    question_string = random.choice(question_phrases)

    #TODO: remove entries from the list of phrases after use and reload from file after list is empty

    # if not statement_phrases:
    #     statement_phrases = load_statements()

    # Here we construct our final bulling sentence.It combines with two parts:
    # if main punch (bully) is question (has ?), then we combine random questions with random bully punch.
    # if not then we combine random statement with random bully punch, and finally
    # we replace our placeholders for <bully> and <victim> with usernames

    if bully_string.find('?') != -1:
        sentence = question_string + ' ' + bully_string
    else:
        sentence = statement_string + ' ' + bully_string

    sentence = sentence.replace("<bully>", bully)
    sentence = sentence.replace("<victim>", victim)

    return sentence


@client.tree.command(name="bully", description="Закібербублити будь-кого", guild=GUILD_ID)
async def cyberbully_slash(interaction: discord.Interaction, target: discord.Member):
    result = await cyberbully(interaction.user.name, target.name)
    await interaction.response.send_message(result)


@client.tree.context_menu(name="Закібербулити цього користувача")
async def cyberbully_context_menu(interaction: discord.Interaction, member: discord.Member):
    result = await cyberbully(interaction.user.name, member.name)
    await interaction.response.send_message(result)


client.run(BOT_TOKEN)