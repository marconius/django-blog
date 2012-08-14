from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings

from blog.managers import PublicManager

import datetime
import tagging
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


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(_('body'), )
    tease = models.TextField(
        _('tease'),
        blank=True, 
        help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    status = models.IntegerField(_('status'), 
                                 choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = TagField()
    # i18n
    language = models.CharField(_('language'), choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE, max_length=10)
    translations = models.ManyToManyField('self', blank=True, null=True)
    #TODO limit to one translation per language?
    objects = PublicManager()
    #TODO i18n_objects = BlogI18nManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table  = 'blog_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

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
    
    def _get_adjacent_post(self, next):
        kwargs = {"status__gte":2}
        method = self.get_previous_by_publish
        if next:
            method = self.get_next_by_publish
        if settings.USE_I18N:
            kwargs.update({"language":self.language,})
        return method(**kwargs)
        
    def get_previous_post(self):
        return self._get_adjacent_post(next=False)

    def get_next_post(self):
        return self._get_adjacent_post(next=True)


class BlogRoll(models.Model):
    """Other blogs you follow."""
    name = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'name',)
        verbose_name = _('blog roll')
        verbose_name_plural = _('blog roll')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
