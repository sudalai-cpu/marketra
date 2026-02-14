import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Product, ViewHistory

def get_hybrid_recommendations(user, num_rec=10):
    products = Product.objects.all()
    if not products.exists(): return []

    # Content Processing
    df = pd.DataFrame(list(products.values('id', 'name', 'description')))
    df['content'] = df['name'].fillna('') + " " + df['description'].fillna('')
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])
    
    # User History Analysis
    user_history = ViewHistory.objects.filter(user=user).order_by('-viewed_at')[:5]
    
    if not user_history.exists():
        return [{'product': p, 'score': 0} for p in products.order_by('-ai_rank')[:num_rec]]

    # Logic: Last 3 items vachu average similarity edukka porom (Advanced Pro level)
    results = []
    seen_ids = set()
    
    for history in user_history:
        try:
            idx = df[df['id'] == history.product.id].index[0]
            sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix)[0]))
            
            for i, score in sim_scores:
                prod_id = df.iloc[i]['id']
                match_percentage = round(score * 100)
                
                if prod_id not in seen_ids and match_percentage > 10 and prod_id != history.product.id:
                    prod = Product.objects.get(id=prod_id)
                    results.append({'product': prod, 'score': match_percentage})
                    seen_ids.add(prod_id)
        except: continue

    # Top scores-ah sort panni anuppalam
    return sorted(results, key=lambda x: x['score'], reverse=True)[:num_rec]