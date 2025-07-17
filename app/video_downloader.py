import os, uuid
import yt_dlp
def download_video(url,quality):
    download_folder=os.path.join(os.path.expanduser("~"),"Downloads")
    os.makedirs(download_folder,exist_ok=True)
    filename=f"downloaded_video_{uuid.uuid4().hex}.mp4" 
    video_path=os.path.join(download_folder,filename)
    quality_formats={
        "1080": "bestvideo[height<=1080]+bestaudio/best",
        "720": "bestvideo[height<=720]+bestaudio/best",
        "480": "bestvideo[height<=480]+bestaudio/best",
        "best": "bestvideo+bestaudio/best"
    }
    video_format=quality_formats.get(quality,"bestvideo+bestaudio/best",)
    ydl_opts={
        "format":video_format,
        "outtmpl":video_path,
        "merge_output_format":"mp4",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists:
            
            return video_path
    except Exception as e:
        print(f"Video download failed:{e}")
    return None