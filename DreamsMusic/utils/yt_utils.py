# utils/yt_utils.py
import yt_dlp
import requests
from io import BytesIO
from PIL import Image, ImageFilter

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': 'in_playlist',
    'default_search': 'ytsearch',
    'skip_download': True,
}

def yt_search(query):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            video = info['entries'][0]
        else:
            video = info
        return {
            'title': video.get('title'),
            'url': video.get('url'),
            'webpage_url': video.get('webpage_url'),
            'duration': video.get('duration'),
            'thumbnail': video.get('thumbnail'),
        }

def download_and_blur_thumbnail(url, blur_radius=10):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))
    bio = BytesIO()
    bio.name = "thumb.png"
    blurred.save(bio, "PNG")
    bio.seek(0)
    return bio
