import discord
from datetime import datetime
import os
import reminder

client = discord.Client()

target_timing = [
    'day', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
    'saturday', 'weekday', 'weekend'
]
weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
weekend = ['sunday', 'saturday']


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
        await message.channel.send('$every (day|weekday) HH:mm message\n' +
                                   '$list-reminder\n' + '$del-reminder {id}')

    if message.content.startswith('$list-reminder'):
        try:
            reminders = reminder.list_reminder(message.channel.id)
            msg = ''
            for r in reminders:
                msg += '({}) {} {} {}\n'.format(r.id, r.date, r.time,
                                                r.message)
            if msg:
                await message.channel.send(msg)
            else:
                await message.channel.send('reminder is not exist')
        except Exception as e:
            print("Unexpected error:", e)
            await message.channel.send('internal server error')

    if message.content.startswith('$del-reminder'):
        ss = message.content.split()
        if len(ss) < 2:
            await message.content.send("message id is empty")
            return
        try:
            reminder.del_reminder(message.channel.id, int(ss[1]))
            await message.channel.send("reminder is deleted")
        except Exception as e:
            print("Unexpected error:", e)
            await message.channel.send('internal server error')

    if message.content.startswith('$every'):
        ss = message.content.split()
        if len(ss) < 4:
            await message.channel.send(
                'syntax \n$every (day|weekday) HH:mm message')
            return
        date, timing, msg = ss[1].lower(), ss[2], ss[3]
        if date not in target_timing:
            await message.channel.send('allow timing are ' +
                                       ', '.join(target_timing))
            return
        try:
            d = datetime.strptime(timing, "%H:%M").strftime('%H:%M')
            reminder.push_reminder(
                reminder.Reminder(msg, d, message.channel.id, date))
            await message.channel.send('reminder is set')
        except ValueError:
            await message.channel.send('{} is bad date syntax'.format(timing))
        except Exception as e:
            print("Unexpected error:", e)
            await message.channel.send('internal server error')


if __name__ == '__main__':

    now = datetime.now(reminder.jp)

    rs = reminder.fetch_reminders('date', '=', 'day')
    for r in rs:
        if r.time > now.strftime('%H:%M'):
            reminder.reminders[r.channel].append(r)

    day_week = now.strftime('%A').lower()
    rs = reminder.fetch_reminders('date', '=', day_week)
    for r in rs:
        if r.time > now.strftime('%H:%M'):
            reminder.reminders[r.channel].append(r)

    if day_week in weekday:
        rs = reminder.fetch_reminders('date', '=', 'weekday')
        for r in rs:
            if r.time > now.strftime('%H:%M'):
                reminder.reminders[r.channel].append(r)

    if day_week in weekend:
        rs = reminder.fetch_reminders('date', '=', 'weekend')
        for r in rs:
            if r.time > now.strftime('%H:%M'):
                reminder.reminders[r.channel].append(r)

    client.loop.create_task(reminder.check_reminder(client))
    token = os.environ.get("TOKEN")
    if not token:
        print("'TOKEN' is empty")
        exit(1)
    client.run(token)
