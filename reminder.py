from datetime import datetime
from google.cloud.datastore import entity
import pytz
from typing import Dict, List
import discord
from collections import defaultdict
import asyncio
from google.cloud import datastore

datastore_client = datastore.Client()
kind = 'Reminder'

jp = pytz.timezone('Asia/Tokyo')

weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
weekend = ['sunday', 'saturday']

class Reminder:
    def __init__(self,
                 message: str,
                 time: str,
                 channel: int,
                 date: str,
                 id: int = 0) -> None:
        self.message = message
        self.time = time
        self.date = date
        self.channel = channel
        self.id = id


reminders: Dict[int, List[Reminder]] = defaultdict(list)


async def check_reminder(client: discord.Client):
    await client.wait_until_ready()
    while not client.is_closed():
        now = now_time()
        for ch, l in reminders.items():
            for i, r in enumerate(l):
                if r.time <= now:
                    channel = client.get_channel(ch)
                    await channel.send(r.message)
                    l.pop(i)
        await asyncio.sleep(30)


def push_reminder(reminder: Reminder) -> None:
    save_datastore(reminder)
    week = now_week()
    if (reminder.date == 'date' or
        reminder.date == week) and reminder.time > now_time():
        reminders[reminder.channel].append(reminder)


def list_reminder(channel: int) -> List[Reminder]:
    return fetch_reminders('channel', '=', channel)


def del_reminder(channel: int, id: int) -> None:
    key = datastore_client.key('Channel', channel, kind, id)
    datastore_client.delete(key)
    for i, r in enumerate(reminders[channel]):
        if r.id == id:
            reminders[channel].pop(i)
            return


def save_datastore(reminder: Reminder) -> None:
    key = datastore_client.key('Channel', reminder.channel, kind)
    entity = datastore.Entity(key=key)
    entity['message'] = reminder.message
    entity['time'] = reminder.time
    entity['date'] = reminder.date
    entity['channel'] = reminder.channel
    datastore_client.put(entity)


def fetch_reminders(prop: str, operator: str, value) -> List[Reminder]:
    query = datastore_client.query(kind=kind)
    query.add_filter(prop, operator, value)
    query_iter = query.fetch()
    rs: List[Reminder] = []
    for entity in query_iter:
        rs.append(
            Reminder(entity["message"], entity['time'], entity['channel'],
                     entity['date'], entity.id))
    return rs


def now_time() -> str:
    return datetime.now(jp).strftime('%H:%M')

def now_week() -> str:
    return datetime.now(jp).strftime('%A').lower()
