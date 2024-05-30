from .models import Category

def category_links(request):
    category=Category.objects.all()
    return dict(cat_list=category)
