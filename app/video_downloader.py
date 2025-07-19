import os
import uuid
import yt_dlp
import random
def browser_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-M115F) AppleWebKit/537.36 Chrome/103.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.youtube.com/"
    }
def download_video(url, quality="best"):
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(download_folder, exist_ok=True)
    filename = f"downloaded_video_{uuid.uuid4().hex}.mp4"
    video_path = os.path.join(download_folder, filename)
    quality_formats = {
        "1080": "bestvideo[height<=1080] +bestaudio/best",
        "720": "bestvideo[height<=720]+bestaudio/best",
        "480": "bestvideo[height<=480]+bestaudio/best",
        "best": "bestvideo+bestaudio/best"
    }
    video_format = quality_formats.get(quality, "bestvideo+bestaudio/best")
    ydl_opts = {
        "format": video_format,
        "outtmpl": video_path,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "headers": browser_headers(),
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }],
        "geo_bypass": True,
        "age_limit": 99,
        "nocheckcertificate": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(video_path):
            return video_path
        else:
            print("file not saved  properly")
    except Exception as e:
        print(f"Video download failed: {e}")
    return None
