from google import genai

# Inga rendu arguments (viewed_items_list, available_list) irukanum
def get_ai_recommendations(viewed_items_list, available_list):
    client = genai.Client(api_key="AIzaSyDpiQyhHNYuc7-4tzdsVYbvmwE-c34fqKs")
    
    # Variable names-a sariyaa match panniyachu
    prompt = f"""
    User history: {viewed_items_list}.
    Available products in my shop: {available_list}.
    
    TASK: Suggest 2 or 3 products ONLY from the 'Available products' list above.
    Do NOT suggest brands like Rolex or Gucci if they are not in the list.
    Return ONLY product names exactly as given, separated by commas.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=prompt
        )
        
        if response and response.text:
            cleaned_text = response.text.replace("\n", "").strip()
            print(f"CLEANED AI NAMES: {cleaned_text}")
            return cleaned_text
            
        # Fallback-la unga real product name onnu kuduppom (Rolex-a thookittu)
        return "Ergo-Pro Business Chair, Ambient Studio Light" 

    except Exception as e:
        print(f"AI ERROR: {str(e)}")
        return "Ergo-Pro Business Chair, Ambient Studio Light"