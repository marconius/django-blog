import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
#from django.views.generic import date_based, list_detail #deprecated
from django.views.generic import ( 
    ListView, DetailView, DateDetailView, YearArchiveView, MonthArchiveView, 
    DayArchiveView )
from django.db.models import Q
from django.conf import settings

from blog.models import *
from blog.constants import STOP_WORDS_RE
from blog.settings import *
from tagging.models import Tag, TaggedItem

class PostListView(ListView):
    queryset = Post.objects.published()
    paginate_by = getattr(settings,'BLOG_PAGESIZE', 1)
    # TODO: include the context that was there before
    # `has_next`, `next`, `has_previous`, `previous`

class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.published()
    date_field = "publish"
    make_object_list = True
    
class PostMonthArchiveView(MonthArchiveView):
    queryset=Post.objects.published()
    date_field="publish"
    make_object_list = True

class PostDayArchiveView(DayArchiveView):
    date_field='publish'
    queryset=Post.objects.published()
    make_object_list = True

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

class CategoryListView(ListView):
    template_name = 'blog/category_list.html'
    queryset=Category.objects.all()
    
class CategoryDetailView(DetailView):
    """
    TODO: This is actualy a ListView of posts.just set the queryste accordingly
    """
    template_name = 'blog/category_detail.html'
    model = Category
    
'''
#the old category detail view
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
'''

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

