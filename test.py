import yt_dlp

#use yt_dlp to download pornhub's video
# get formats with --list-formats
ydl_opts = {'listformats': True}



ydl_opts = {'format': '720p'}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.pornhub.com/view_video.php?viewkey=676e8afcacf1a'])   