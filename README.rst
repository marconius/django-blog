===========
django-blog
===========

This is a blog for Django projects.

Requirements:

* django-tiny_mce: http://django-tinymce.googlecode.com/svn/tags/release-1.5/docs/.build/html/installation.html
* filebrowser-no-grappelli or filebrowser: http://readthedocs.org/docs/django-filebrowser/en/latest/quickstart.html
* django comments (django.contrib.comments in INSTALLED_APPS)
* django markup (django.contrib.marup in INSTALLED_APPS)

Requirements TODO:

* Remove commenting and markup from project. These should be added only as they are needed

Principal Ideas/Goals Behind Project:

I like how easy and simple the simple-apps blog is, but because it has been abandonned long ago, I just tweak this thing for use in my projects.

* Very quick installation with TinyMCE and filebrowser already set to go
* Very little or no logic in templates

Installation:

* install django-blog (https://github.com/marconius/django-blog)
* put `blog` in INSTALLED_APPS
* ./manage.py syncdb or ./manage.py migrate
* ./manage.py collectstatic
