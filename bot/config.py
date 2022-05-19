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


from decouple import config
from dotenv import load_dotenv

from .helpers import LOGS

load_dotenv()

try:
    APP_ID = config("APP_ID", default=6, cast=int)
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    BOT_TOKEN = config("BOT_TOKEN")
    YT_API_KEY = config("YT_API_KEY")
    OWNER = config("OWNER")
    CHAT = config("CHAT", cast=int)
    CH_ID = config("YT_CHANNEL_ID")
    DELAY_TIME = config("DELAY_TIME", default=5, cast=int)
    DOWNLOAD_VIDEO = config("DOWNLOAD_VIDEO", default=False, cast=bool)
except Exception as e:
    LOGS.info("Environment vars Missing")
    LOGS.info("something went wrong")
    LOGS.info(str(e))
    exit()
