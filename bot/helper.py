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
from . import YT
from .FastTelethon import upload_file


def dur_parser(_time):
    if not _time:
        return "Not Found!"
    xx = _time.replace("PT", "")
    return xx.lower()


async def channel_info(ch_id):
    return (
        YT.channels().list(part="statistics,snippet,contentDetails", id=ch_id).execute()
    )


def video_info(_id):
    return YT.videos().list(part="snippet,contentDetails,statistics", id=_id).execute()


def yt_dl(yt_link, quality=None):
    opts = {
        "format": quality,
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "postprocessors": [{"key": "FFmpegMetadata"}],
    }
    try:
        return YoutubeDL(opts).extract_info(url=yt_link, download=True)
    except Exception as er:
        LOGS.info(er)
        return None


async def proper_info_msg(client, to_id, yt_id):
    dl_yt = ""
    info = video_info(yt_id)["items"][0]
    channel_name = info["snippet"]["channelTitle"]
    video_title = info["snippet"]["title"]
    try:
        desc = info["snippet"]["description"]
        if len(desc) > 300:
            desc = desc[:200] + "..."
    except BaseException:
        desc = "Not Found!"
    pub_time = info["snippet"]["publishedAt"].replace("T", " ").replace("Z", " ")
    try:
        thumb = info["snippet"]["thumbnails"]["maxres"]["url"]
    except BaseException:
        thumb = info["snippet"]["thumbnails"]["high"]["url"]
    os.system(f"wget {thumb} -O {thumb.split('/')[-2]}.jpg")
    try:
        dur = dur_parser(info["contentDetails"]["duration"])
    except BaseException:
        dur = "Not Found!"
    text = ""
    if info["snippet"]["liveBroadcastContent"] == "live":
        text += f"**{channel_name} is Live 🔴**\n\n"
        dur = "♾"
    else:
        text += f"**{channel_name} Just Uploaded A Video**\n\n"
        if DOWNLOAD_VIDEO:
            dl_yt = yt_dl(yt_id, "135")  # 480p
    text += f"```Title - {video_title}\n\n"
    text += f"Description - {desc}\n"
    text += f"Duration - {dur}\n"
    text += f"Published At - {pub_time}```\n"
    if dl_yt:
        with open(f"{yt_id}.mp4", "rb") as f:
            ok = await upload_file(
                client=client,
                file=f,
                name=f"{yt_id}.mp4",
            )
        await client.send_file(
            to_id,
            file=ok,
            caption=text,
            attributes=[
                DocumentAttributeVideo(
                    duration=dl_yt["duration"],
                    w=dl_yt["width"],
                    h=dl_yt["height"],
                    supports_streaming=True,
                )
            ],
            thumb=f"{thumb.split('/')[-2]}.jpg",
            buttons=[
                [Button.url("Watch", url=f"https://www.youtube.com/watch?v={yt_id}")]
            ],
        )
    else:
        await client.send_file(
            to_id,
            file=f"{thumb.split('/')[-2]}.jpg",
            caption=text,
            buttons=[
                [Button.url("Watch", url=f"https://www.youtube.com/watch?v={yt_id}")]
            ],
        )
    os.remove(f"{thumb.split('/')[-2]}.jpg")
    os.remove(f"{yt_id}.mp4")
