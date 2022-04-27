#    This file is part of the Youtube Notification  distribution.
#    Copyright (c) 2022 kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/YoutubeNotificationBot/blob/main/License> .


from . import *
from .helper import *

LOGS.info("• Starting Bot... •")

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as exc:
    LOGS.info(str(exc))


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`\nThis is A YouTube Notification Bot.\n I Notified You Wen Your Subscribed Youtubers Post A Video or Start A Live Streams",
        buttons=[
            [
                Button.url("SOURCE CODE", url="github.com/Kaif-00z/"),
                Button.url("DEVELOPER", url="t.me/kaif_00z"),
            ],
        ],
    )


@bot.on(events.NewMessage(incoming=True, pattern="/subsinfo"))
async def sub_info(event):
    if str(events.sender_id) not in OWNER:
        return
    text = "**List Of Subscribed Channel**\n\n"
    for id in CH_IDS:
        info = await channel_info(id)
        text += f"`• {info['items'][0]['snippet']['title']}`\n"
    await event.reply(text)


async def save_it():
    for id in CH_IDS:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={id}"
        feed = feedparser.parse(feed_url)
        yt_link = feed.entries[0].yt_videoid
        if yt_link not in MEMORY:
            MEMORY.append(yt_link)


async def forever_check():
    for id in CH_IDS:
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={id}"
        feed = feedparser.parse(feed_url)
        yt_link = feed.entries[0].yt_videoid
        if yt_link not in MEMORY:
            await proper_info_msg(bot, CHAT, yt_link)
            MEMORY.append(yt_link)
        await asyncio.sleep(0.5)


sch.add_job(forever_check, "interval", seconds=30)

LOGS.info("Bot has started...")
bot.loop.run_until_complete(save_it())
sch.start()
bot.loop.run_forever()
