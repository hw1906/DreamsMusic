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
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Try direct URL first
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in info and info['entries']:
                    video = info['entries'][0]
                else:
                    video = info
                    
                duration = video.get('duration', 0)
                if duration > 3600:  # More than 1 hour
                    raise Exception("Song is too long (max 1 hour)")
                    
                return {
                    'title': video.get('title', 'Unknown Title'),
                    'url': video.get('url', None),
                    'webpage_url': video.get('webpage_url', None),
                    'duration': duration,
                    'thumbnail': video.get('thumbnail', None),
                }
            except Exception as e:
                raise Exception(f"Error extracting info: {str(e)}")
    except Exception as e:
        raise Exception(f"Error searching YouTube: {str(e)}")

def download_and_blur_thumbnail(url, blur_radius=10):
    if not url:
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        image = Image.open(BytesIO(response.content)).convert("RGBA")
        blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))
        
        bio = BytesIO()
        bio.name = "thumb.png"
        blurred.save(bio, "PNG")
        bio.seek(0)
        return bio
    except Exception as e:
        print(f"Error processing thumbnail: {str(e)}")
        return None  # Return None if anything goes wrong
