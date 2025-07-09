from yt_dlp import YoutubeDL
import os
from pathlib import Path
import re
import pathlib as Path


def download_vtt(video_url:str)->str:
    output_dir="downloads"
    os.makedirs(output_dir,exist_ok=True)

    yt_opts = {
        'writesubtitles': True,
        'skip_download': True,
        'writeautomaticsub': True, 
        'subtitleslangs': ['en'],
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
    }

    with YoutubeDL(yt_opts) as ydl:
        info=ydl.extract_info(video_url,download=True)
        video_id=info.get("id")
        vtt_path=f"{output_dir}/{video_id}.en.vtt"
        return vtt_path if os.path.exists(vtt_path) else""          
    



def vtt_to_text(vtt_file):
    lines = Path.Path(vtt_file).read_text(encoding='utf-8').splitlines()
    transcript = []
    
    for line in lines:
        line = line.strip()

        if (
            not line or
            line.startswith("WEBVTT") or
            "-->" in line or
            re.match(r'^\d{2}:\d{2}:\d{2}\.\d+', line)
        ):
            continue

        clean_line = re.sub(r'<[^>]+>', '', line)  
        clean_line = re.sub(r'\d{2}:\d{2}:\d{2}\.\d+>?[a-z]*>?', '', clean_line)  

        if clean_line:
            transcript.append(clean_line)

    full_text = " ".join(transcript)

    full_text = re.sub(r'\b(\w+)( \1\b)+', r'\1', full_text)

    return full_text


 


def get_transcript(video_url:str)->str:
    vtt_file=download_vtt(video_url)
    if not vtt_file:
        raise Exception("Transcript Not Available")
    return vtt_to_text(vtt_file)
