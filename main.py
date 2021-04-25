import discord
from datetime import datetime
import os
import reminder

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send('$every($alarm) HH:mm message')

    if message.content.startswith('$alarm'):
        ss  = message.content.split()
        if len(ss) < 3:
            await message.channel.send('syntax \n$alarm HH:mm message')
            return
        timing, msg = ss[1], ss[2]
        try:
            d = datetime.strptime(timing, "%H:%M")
            reminder.push_reminder(reminder.Reminder(msg, d, message.channel.id))
            await message.channel.send('set alarm {} {}'.format(timing, msg))
        except:
            await message.channel.send('{} is bad date syntax'.format(timing))

    if message.content.startswith('$every'):
        ss  = message.content.split()
        if len(ss) < 3:
            await message.channel.send('syntax \n$every HH:mm message')
            return
        timing, msg = ss[1], ss[2]
        try:
            d = datetime.strptime(timing, "%H:%M")
            reminder.push_reminder(reminder.Reminder(msg, d, message.channel.id))
            await message.channel.send('reminder set every {} {}'.format(timing, msg))
        except:
            await message.channel.send('{} is bad date syntax'.format(timing))

if __name__ == '__main__':
    client.loop.create_task(reminder.check_reminder(client))
    token = os.environ.get("TOKEN")
    if not token:
        print("'TOKEN' is empty")
        exit(1)
    client.run(token)
