import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_recommendations(viewed_items_list, available_list):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Prompt-a innum strict-a maathiyachu
    prompt = f"""
    User history: {viewed_items_list}.
    Available products in my shop: {available_list}.
    
    TASK: Based on user history, suggest exactly 2 products from the 'Available products' list.
    Return ONLY the product names separated by a comma. 
    Example format: Product Name 1, Product Name 2
    Do not add any explanations or other text.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest', 
            contents=prompt
        )
        
        if response and response.text:
            # AI response-la vara newline characters-a thookittu clean pandrom
            cleaned_text = response.text.strip().replace('\n', '')
            return cleaned_text
            
        return "" 

    except Exception as e:
        print(f"AI ERROR: {str(e)}")
        return ""