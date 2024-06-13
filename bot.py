from main import *
import discord
import json

f = open('parameters.json')
processing = False
queue_len = 0
queue = []
awaiting_queue = []
params = json.load(f)

intents = (
    discord.Intents.default()
) 
intents.message_content = True

client = discord.Client(
    intents=intents
) 

async def eliminate_queue(queue, message):
    global queue_len
    for el in queue:
        params["prompt"] = el
        await message.channel.send("Generating...")
        await generate_image(params)

        await message.channel.send(
            message.author.mention, file=discord.File("pic.jpeg")
        )
    queue_len = 0

@client.event
async def on_ready():
    print(f"Logged in.")

@client.event
async def on_message(message):
    global processing, awaiting_queue, queue, queue_len

    msg = message.content.lower()

    if message.author == client.user:
        return

    if msg.startswith("generate"):
        prompt = msg.split(" ")

        if len(prompt) <= 2:
            await message.channel.send(
                f"{message.author.mention} Prompt shouldn't be empty"
            )

        else:
            if processing:
                awaiting_queue.append(" ".join(prompt[2 : len(prompt)]))
                queue_len += 1

                await message.channel.send(
                    f"You are put in a queue. Your place is... {queue_len}"
                )
                return

            processing = True
            queue.append("".join(prompt[2 : len(prompt)]))
            # await message.channel.send(f"Generating...")
            await eliminate_queue(queue, message)

            if awaiting_queue:
                await message.channel.send("Generating queue requests...")
                await eliminate_queue(awaiting_queue, message)
                awaiting_queue = []

            queue = []
            processing = False


client.run(
    ""
)  # THE BOT TOKEN GOES HERE
