from django.contrib import admin
from .models import Post, Category


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","date_posted", "author"]
    search_fields = ["title"]
    class Meta:
        model = Post

class CategoryAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Post,PostModelAdmin)
admin.site.register(Category, CategoryAdmin)

