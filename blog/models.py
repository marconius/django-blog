from django.db import models
from django.utils.translation import (get_language, get_language_info, 
                                      ugettext_lazy as _)
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings


from blog.managers import PublicManager

import datetime
from tagging.fields import TagField


class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, 
                               related_name='child')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)
    
    def _get_parents(self):
        """
        get all parents and parents of parents until root
        """
        parents = []
        parent = self.parent
        while(parent):
            parents.append(parent)
            parent = parent.parent
        parents.reverse()
        return parents
    parents = property(_get_parents)
        
    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})


class BasePost(models.Model):
    """The base post class (abstract)
    
    To be subclassed in order to customize for your app!
    """
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(_('body'), )
    tease = models.TextField(_('tease'), blank=True, 
                             help_text=_('Concise text suggested'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, 
                                 default=1)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = TagField()
    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering  = ('-publish',)
        get_latest_by = 'publish'
        abstract = True

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)
    

#class Post(BasePost):
#    pass

class MultiLingualPostMixin(models.Model):
    """ Adds language field and translation functions to blog post 
    
    must define 'lang_choices' for this to work
    """
    lang_choices = settings.LANGUAGES

    language = models.CharField(_("Language"), choices=lang_choices,
                                max_length=10)
    
    class Meta:
        abstract = True
    
    @property
    def available_for_lang(self, lang=""):
        if lang == "":
            lang = get_language()
        return lang in self._languages()
    
    def _languages(self):
        '''
        returns a list of language codes that Post object is available in
        '''
        lang_codes = [self.language]
        for trans in self.translations.all():
            if trans.status == 2:
                lang_codes.append(trans.language)
        return lang_codes
    
    @property
    def languages(self):
        '''
        returns a list of language info dicts for templates
        '''
        lang_codes = self._languages()
        langs = []
        for lang in self.lang_choices:
            if lang[0] in lang_codes:
                langs.append(get_language_info(lang[0]))
        return langs
    
    @property
    def language_info(self):
        return get_language_info(self.language)
    
    # TODO: def translated(self):
    

class BlogRoll(models.Model):
    """Other blogs you follow."""
    name = models.CharField(max_length=100)
    url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'name',)
        verbose_name = _('blog roll')
        verbose_name_plural = _('blog roll')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
