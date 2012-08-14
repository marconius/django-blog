import os
from django.conf import settings

settings.TINYMCE_SPELLCHECKER = True

# Allow comments 
def comments_installed():
    return ('django.contrib.comments' in settings.INSTALLED_APPS or
            'comments' in settings.INSTALLED_APPS)

COMMENTS_ENABLED = getattr(settings, 'BLOG_ENABLE_COMMENTS', 
                           comments_installed())
