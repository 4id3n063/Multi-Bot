import yt_dlp

def download_audio(url):
    info = get_video_info(url)
    title = info["title"]
    uploader = info["uploader"]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'export/export', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return title, uploader


def get_video_info(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
        }