===========
django-blog
===========

This is a blog for Django projects.

Requirements:

* filebrowser-no-grappelli or filebrowser: http://readthedocs.org/docs/django-filebrowser/en/latest/quickstart.html
* django comments (django.contrib.comments in INSTALLED_APPS)
* django markup (django.contrib.marup in INSTALLED_APPS)

Requirements TODO:

* Remove commenting and markup from project. These should be added only as they are needed

Mission:

* Allow adding basic blog functionnality very quickly to a Django project

Installation:

* pip install git+https://github.com/marconius/django-blog@<TAG>
* put `blog` in INSTALLED_APPS
* ./manage.py syncdb or ./manage.py migrate
* ./manage.py collectstatic
