from .models import Collection

def collection_status(request):
    """
    Context processor to make collection count available globally.
    """
    count = 0
    if request.user.is_authenticated:
        if hasattr(request.user, 'collection'):
            count = request.user.collection.products.count()
    else:
        collection = request.session.get('collection', [])
        count = len(collection)
        
    return {
        'collection_count': count
    }
