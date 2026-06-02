from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI(title="Instagram Reel Downloader")

def get_reel_download_url(instagram_url: str) -> str:
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestvideo+bestaudio/best', # Best quality extract karne ke liye
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(instagram_url, download=False)
            # Video ka direct downloadable CDN link nikalna
            return info.get('url')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting URL: {str(e)}")

# Aapka manga hua endpoint structure: /igvid/url?url=YOUR_URL
@app.get("/igvid/url")
def download_reel(url: str = Query(..., description="Instagram Reel URL")):
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
        
    video_url = get_reel_download_url(url)
    
    if video_url:
        # Option A: Agar aap user ko direct video file par redirect karna chahte hain
        return RedirectResponse(url=video_url)
        
        # Option B: Agar aapko JSON response chahiye (isko use karne ke liye upar wali line comment karein)
        # return {"status": "success", "download_url": video_url}
    
    raise HTTPException(status_code=500, detail="Could not extract download URL")

@app.get("/")
def home():
    return {"message": "Instagram Downloader API is Running!"}
