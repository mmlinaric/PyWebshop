from .models import Category

# Used to list all categories on the navigation bar
def categories(request):
    return {
        'categories': Category.objects.all()
    }