import time
import re
from rich.console import Console

console = Console()

def clean_string(text):
    if isinstance(text, str):
        return text.encode('utf-8', 'replace').decode('utf-8')
    return text

def record_turn(history, speaker, text, stage, turn_type="speech"):
    history.append({
        "speaker": clean_string(speaker),
        "text": clean_string(text),
        "stage": clean_string(stage),
        "type": turn_type,
        "timestamp": time.time()
    })

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.replace(" ", "_")[:100]
