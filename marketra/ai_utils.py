import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

def get_ai_recommendations(viewed_items_list, available_list):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("!!! DEBUG ERROR: API KEY MISSING !!!")
        return ""

    # --- CHANGE THIS NAME ---
    # Unga AI Studio list-la enna peru irukko adha anga podunga.
    # Eg: "gemini-pro" or "gemini-1.0-pro" or "gemini-1.5-pro"
    model_id = "gemini-1.5-flash" 
    
    # Intha URL format thaan ippo working standard
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt = (
        f"User history: {viewed_items_list}. "
        f"Available products: {available_list}. "
        "Recommend 6 products from available list. "
        "Return ONLY product names separated by comma."
    )

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            res_json = response.json()
            ai_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            print(f"--- AI SUCCESS ({selected_model}): {ai_text} ---")
            return ai_text
        else:
            print(f"!!! AI ERROR ({response.status_code}): {response.text} !!!")
            return ""
    except Exception as e:
        print(f"!!! CONNECTION FAILED: {str(e)} !!!")
        return ""