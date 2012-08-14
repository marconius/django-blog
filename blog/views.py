import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail #deprecated
from django.views.generic import ListView, DateDetailView
from django.db.models import Q
from django.conf import settings
from django.utils.translation import get_language

from blog.models import *
from blog.constants import STOP_WORDS_RE
from blog.settings import *
from tagging.models import Tag, TaggedItem

class PostListView(ListView):
    queryset = Post.objects.published()
    paginate_by = getattr(settings,'BLOG_PAGESIZE', 20)
    # TODO: include the context that was there before
    # `has_next`, `next`, `has_previous`, `previous`
    
    def get_queryset(self):
        """
        Get list of objects with i18n mechanics
        """
        qs = super(PostListView, self).get_queryset()
        if settings.USE_I18N:
            qs = qs.filter(language=get_language())
        return qs
        
def post_archive_year(request, year, **kwargs):
    return date_based.archive_year(
        request,
        year=year,
        date_field='publish',
        queryset=Post.objects.published(),
        make_object_list=True,
        **kwargs
    )
post_archive_year.__doc__ = date_based.archive_year.__doc__


def post_archive_month(request, year, month, **kwargs):
    return date_based.archive_month(
        request,
        year=year,
        month=month,
        date_field='publish',
        queryset=Post.objects.published(),
        **kwargs
    )
post_archive_month.__doc__ = date_based.archive_month.__doc__


def post_archive_day(request, year, month, day, **kwargs):
    return date_based.archive_day(
        request,
        year=year,
        month=month,
        day=day,
        date_field='publish',
        queryset=Post.objects.published(),
        **kwargs
    )
post_archive_day.__doc__ = date_based.archive_day.__doc__

class PostDateDetailView(DateDetailView):
    """
    Displays post detail. If user is superuser, view will display 
    unpublished post detail for previewing purposes.
    
    extra context: comments_enabled
    """
    date_field = 'publish'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.published()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(PostDateDetailView, self).get_context_data(**kwargs)
        context.update({"comments_enabled": COMMENTS_ENABLED})
        return context

def category_list(request, template_name = 'blog/category_list.html', **kwargs):
    """
    Category list

    Template: ``blog/category_list.html``
    Context:
        object_list
            List of categories.
    """
    return list_detail.object_list(
        request,
        queryset=Category.objects.all(),
        template_name=template_name,
        **kwargs
    )


def category_detail(request, slug, template_name = 'blog/category_detail.html', **kwargs):
    """
    Category detail

    Template: ``blog/category_detail.html``
    Context:
        object_list
            List of posts specific to the given category.
        category
            Given category.
        parent_categories
            list of parents and parents of parents until root category
    """
    category = get_object_or_404(Category, slug__iexact=slug)
    parent_cats = category.parents

    return list_detail.object_list(
        request,
        queryset=category.post_set.published(),
        extra_context={'category': category},
        template_name=template_name,
        **kwargs
    )


def tag_detail(request, slug, template_name = 'blog/tag_detail.html', **kwargs):
    """
    Tag detail

    Template: ``blog/tag_detail.html``
    Context:
        object_list
            List of posts specific to the given tag.
        tag
            Given tag.
    """
    tag = get_object_or_404(Tag, name__iexact=slug)

    return list_detail.object_list(
        request,
        queryset=TaggedItem.objects.get_by_model(Post,tag).filter(status=2),
        extra_context={'tag': tag},
        template_name=template_name,
        **kwargs
    )


def search(request, template_name='blog/post_search.html'):
    """
    Search for blog posts.

    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.

    Template: ``blog/post_search.html``
    Context:
        object_list
            List of blog posts that match given search term(s).
        search_term
            Given search term.
    """
    context = {}
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS_RE, re.IGNORECASE)
        search_term = '%s' % request.GET['q']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        if len(cleaned_search_term) != 0:
            post_list = Post.objects.published().filter(Q(title__icontains=cleaned_search_term) | Q(body__icontains=cleaned_search_term) | Q(tags__icontains=cleaned_search_term) | Q(categories__title__icontains=cleaned_search_term))
            context = {'object_list': post_list, 'search_term':search_term}
        else:
            message = 'Search term was too vague. Please try again.'
            context = {'message':message}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
