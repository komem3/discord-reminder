from datetime import datetime
import discord
from typing import List
import asyncio

class Reminder:
    def __init__(self, message: str, date: datetime, channel: int) -> None:
        self.message = message
        self.date = date
        self.channel = channel

reminders: List[Reminder] = []

async def check_reminder(client: discord.Client):
    await client.wait_until_ready()
    while not client.is_closed():
        for i, r in enumerate(reminders):
            if r.date < datetime.now():
                channel = client.get_channel(r.channel)
                await channel.send(r.message)
                reminders.pop(i)
        await asyncio.sleep(30)

def push_reminder(reminder: Reminder):
    print('push reminder {} {}'.format(reminder.date, reminder.message))
    reminders.append(reminder)
