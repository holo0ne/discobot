import discord
import random

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

image_urls = []

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!submit'):
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    image_urls.append(attachment.url)
            await message.channel.send('Image(s) received!')
        else:
            await message.channel.send('Please attach image(s) with your submission.')

    if message.content.startswith('!random'):
        if image_urls:
            random_image_url = random.choice(image_urls)
            await message.channel.send(random_image_url)
        else:
            await message.channel.send('No images submitted yet.')

client.run('YOUR_BOT_TOKEN')
