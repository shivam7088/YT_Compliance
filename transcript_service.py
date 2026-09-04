import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif parsed.hostname and "youtube.com" in parsed.hostname:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/")[2]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[2]
        else:
            video_id = None
    else:
        video_id = None

    if not video_id or not re.fullmatch(r"[\w-]{11}", video_id):
        raise ValueError("Invalid YouTube URL.")
    return video_id

def fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en", "hi"])

    items = []
    for item in transcript:
        text = item.text if hasattr(item, "text") else item["text"]
        start = item.start if hasattr(item, "start") else item["start"]
        duration = item.duration if hasattr(item, "duration") else item["duration"]
        items.append({
            "text": text.strip(),
            "start": float(start),
            "duration": float(duration),
        })
    return items
