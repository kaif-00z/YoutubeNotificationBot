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


import asyncio
import os
import sys
from logging import INFO, basicConfig, getLogger

import feedparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from googleapiclient.discovery import build
from telethon import Button, TelegramClient, events
from yt_dlp import YoutubeDL

from .config import *

sch = AsyncIOScheduler()
MEMORY = []

basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO)
LOGS = getLogger(__name__)

try:
    YT = build("youtube", "v3", developerKey=YT_API_KEY)
    LOGS.info("Successfully Connected With YouTube...")
except BaseException:
    LOGS.info(str(er))
    exit()

CH_IDS = CH_ID.split(" ")

try:
    bot = TelegramClient(None, APP_ID, API_HASH)
    LOGS.info("successfully connected to telegram")
except Exception as e:
    LOGS.info("Environment vars are missing")
    LOGS.info(str(e))
    exit()
