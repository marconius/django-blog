===========
django-wall
===========

This is a blog for Django projects.

Requirements:

* django-tiny_mce: http://django-tinymce.googlecode.com/svn/tags/release-1.5/docs/.build/html/installation.html
* filebrowser-no-grappelli or filebrowser: http://readthedocs.org/docs/django-filebrowser/en/latest/quickstart.html

Principal Ideas/Goals Behind Project:

* Takes basic-apps' blog a little closer to Wordpress, without overbloat
* Easy installation ( installs with TinyMce and filebrowser already configured
* Very little or no logic in templates
* Makes easy to use and intuitive sites that can be used as substitutes for walls and spaces on the popular social networking sites  

Installation:

* install django-wall (https://github.com/marconius/django-wall)
* put `blog` in INSTALLED_APPS
* ./manage.py syncdb or ./manage.py migrate
* ./manage.py collectstatic
