import os
import re
from pathlib import Path
from datetime import time

def get_weekly_txt_path():
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    weekly_txt_path = backend_dir / 'weekly.txt'
    return weekly_txt_path

def read_weekly_txt():
    weekly_txt_path = get_weekly_txt_path()
    if not weekly_txt_path.exists():
        return "weekly.txt file not found"
    
    with open(weekly_txt_path, 'r') as file:
        content = file.read()
    
    return content

