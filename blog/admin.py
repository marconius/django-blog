from django.contrib import admin
from django.conf import settings
from blog.models import *
from blog.forms import TinyMCEPostForm

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)

class BasePostAdmin(admin.ModelAdmin):
    form = TinyMCEPostForm;
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    
    class Media:
        js = ('tiny_mce/tiny_mce_src.js','blog/js/CustomAddFileBrowser.js',)
        
class PostAdmin(BasePostAdmin):
    """
    The basic admin options for Post
    """

class I18nPostAdmin(BasePostAdmin):
    """
    Admin options with I18n fields for Post
    """
    list_display  = ('title', 'publish', 'language', 'status')
    list_filter   = ('publish', 'categories', 'status', 'language')
    
if settings.USE_I18N:
    admin.site.register(Post, I18nPostAdmin)
else:
    admin.site.register(Post, PostAdmin)

class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order',)
    list_editable = ('sort_order',)
admin.site.register(BlogRoll)
