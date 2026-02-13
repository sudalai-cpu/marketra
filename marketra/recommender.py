from marketra.models import Product
from .models import Collection

def get_ai_recommendations(product_string, available_products_str, user):
    from marketra.models import Product, Collection
    
    # 1. User kitta munnadiye irukkara products-ah kandupidi
    user_collections = Collection.objects.filter(user=user)
    owned_ids = user_collections.values_list('products__id', flat=True)

    # 2. User paatha items-oda names-ah vachu filter panna keywords edukkalam
    # (e.g., 'iPhone, Samsung' nu product_string irundha, 'iPhone' kulla irukkara vera models-ah kaatum)
    keywords = [k.strip() for k in product_string.split(',') if k.strip()]
    
    # 3. Database-la check pannu
    recommended_qs = Product.objects.exclude(id__in=owned_ids)
    
    final_picks = []
    for word in keywords:
        # User paatha word product name-la irundha adhai pick pannu
        matches = recommended_qs.filter(name__icontains=word).exclude(id__in=[p.id for p in final_picks])
        final_picks.extend(list(matches[:2])) # Oru keyword-ku 2 products max

    # 4. Oru vela matches illana, general-ah konjam products pick pannu
    if len(final_picks) < 4:
        extras = recommended_qs.exclude(id__in=[p.id for p in final_picks]).order_by('?')[:4]
        final_picks.extend(list(extras))

    # String-ah thiruppi anupu (Home view split panna)
    return ", ".join([p.name for p in final_picks[:8]])