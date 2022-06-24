from .models import *

"""
- You have to add this context processor in settings.py
- Go to settings.py -> TEMPLATES -> OPTIONS
- add 'app_name.file_name.function_name'
- In this case => 'product.context_processors.menu_links'
"""
def menu_links(request) :
    categories = Category.objects.all()
    return dict(categories=categories)


