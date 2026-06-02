from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(title="Instagram Reel Downloader API")

# CORS Settings (Agar aap is API ko kisi website/frontend se connect karna chahein)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_reel_download_url(instagram_url: str) -> str:
    # Instagram block na kare isliye real browser jaisa user-agent aur headers
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
            'Connection': 'keep-alive',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(instagram_url, download=False)
            
            # Agar multiple formats hain ya playlist jaisa response hai
            if 'entries' in info:
                video_url = info['entries'][0].get('url')
            else:
                video_url = info.get('url')
                
            return video_url
            
    except Exception as e:
        print(f"yt-dlp error: {str(e)}")  # Yeh Render ke logs me dikhega
        return None

# Aapka requested endpoint: /igvid/url?url=...
@app.get("/igvid/url")
def download_reel(url: str = Query(..., description="Instagram Reel URL")):
    if not url:
        return {"success": False, "message": "URL parameter is required"}
        
    # URL ko thoda saaf karna (agar extra tracking parameters hon)
    if "?" in url and "instagram.com" in url:
        url = url.split("?")[0]

    video_url = get_reel_download_url(url)
    
    if video_url:
        # Option A: Direct video download link par redirect karne ke liye
        return RedirectResponse(url=video_url)
        
        # Option B: Agar aapko JSON data chahiye, toh upar wali line ko comment (#) karke 
        # niche wali line ka comment hata dein:
        # return {"success": True, "download_url": video_url}
    
    return {
        "success": False, 
        "message": "Video not found or link is private. Please make sure the account is public."
    }

@app.get("/")
def home():
    return {
        "status": "active", 
        "message": "Instagram Downloader API is running successfully!",
        "usage": "/igvid/url?url=YOUR_INSTAGRAM_URL"
    }
