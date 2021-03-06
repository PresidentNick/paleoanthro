from django.views import generic
from models import Content
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext
import string
import re


# ############################
# class based journal views #
# ############################

class JournalHome(FiberPageMixin, generic.ListView):
    model = Content
    template_name = 'journal/journal_home.html'

    def get_context_data(self, **kwargs):
        context = super(JournalHome, self).get_context_data(**kwargs)

        # Get a unique list of all volume years in the content db
        def get_content_years():
            years = []  # initialize the list
            for c in Content.objects.all():  # get all content items
                if c.year not in years:  # add a year if not there
                    years.append(c.year)
                    years.sort()  # sort latest to earliest
            return years

        context['years'] = get_content_years()

        return context

    def get_fiber_page_url(self):
        return reverse('journal:journal')


class JournalIndex(FiberPageMixin, generic.ListView):
    model = Content
    template_name = 'journal/journal_index.html'

    def get_context_data(self, **kwargs):
        context = super(JournalIndex, self).get_context_data(**kwargs)

        # Get a unique list of all volume years in the content db
        def get_content_years():
            years = []  # initialize the list
            for c in Content.objects.all():  # get all content items
                if c.year not in years:  # add a year if not there
                    years.append(c.year)
                    years.sort()  # sort latest to earliest
            return years

        context['years'] = get_content_years()

        return context

    def get_fiber_page_url(self):
        return reverse('journal:journal_index')


class JournalVolumes(FiberPageMixin, generic.ListView):
    template_name = 'journal/journal_volumes.html'
    context_object_name = 'content_list'

    def get_queryset(self):
        queryset = Content.objects.filter(year__exact=self.kwargs['year'])
        return queryset

    def get_context_data(self, **kwargs):
        year = self.kwargs['year']
        context = super(JournalVolumes, self).get_context_data(**kwargs)
        context['abstracts'] = Content.objects.filter(year=year,
                                                      article_type="Annual Meeting Abstracts").order_by('start_page_n')
        context['articles'] = Content.objects.filter(year=year, article_type="Articles").order_by('start_page_n')
        context['data'] = Content.objects.filter(year=year, article_type="Data").order_by('start_page_n')
        context['reviews'] = Content.objects.filter(year=year, article_type="Reviews").order_by('start_page_n')

        # Get a unique list of all volume years in the content db
        def get_content_years():
            years = []  # initialize the list
            for c in Content.objects.all():  # get all content items
                if c.year not in years:  # add a year if not there
                    years.append(c.year)
                    years.sort()  # sort latest to earliest
            return years

        context['years'] = get_content_years()

        return context

    def get_fiber_page_url(self):
        return reverse('journal:volumes', kwargs={'year': self.kwargs['year']})


class JournalSearch(FiberPageMixin, generic.ListView):
    template_name = 'journal/search_results.html'
    model = Content
    # context_object_name = 'content_list'

    def get_fiber_page_url(self):
        return reverse('journal:search')

        # def get_queryset(self, request):
        # queryset = Content.objects.filter()
        #     if request.method == 'POST':
        #         if request.POST['query'] and request.POST['query'].strip():
        #             query_string = request.POST['query']
        #             entry_query = get_query(['title'], query_string)
        #             queryset = queryset.filter(entry_query)
        #             return queryset
        # return render_to_response('journal/search_results.html', {'results': queryset}, RequestContext(request))

    # return render_to_response('journal/search_results.html', RequestContext(request))


    def get_context_data(self, request, **kwargs):
        # year = 2014
        #year = self.kwargs['year']
        queryset = self.queryset
        context = super(JournalSearch, self).get_context_data(**kwargs)
        if request.method == 'GET':
            if request.GET['query'] and request.GET['query'].strip():
                query_string = request.GET['query']
                entry_query = get_query(['title'], query_string)
                queryset = queryset.filter(entry_query)

        context['abstracts'] = queryset.filter(article_type="Annual Meeting Abstracts").order_by('start_page_n')
        context['articles'] = Content.objects.filter(article_type="Articles").order_by('start_page_n')
        context['data'] = Content.objects.filter(article_type="Data").order_by('start_page_n')
        context['reviews'] = Content.objects.filter(article_type="Reviews").order_by('start_page_n')

        # Get a unique list of all volume years in the content db
        def get_content_years():
            years = []  # initialize the list
            for c in Content.objects.all():  # get all content items
                if c.year not in years:  # add a year if not there
                    years.append(c.year)
                    years.sort()  # sort latest to earliest
            return years

        context['years'] = get_content_years()

        return context


# #################################
# definition based journal views #
# #################################

def static_redirect(request, resource):
    """
    Redirect to a static url. This function captures legacy urls registered with CrossRef for doi lookups
    :param request:
    :param resource:
    :return:
    """
    static_resource = '/static/journal/content/' + resource  # resource is passed from url, points to a pdf
    return redirect(to=static_resource)  # redirect to a new url


def journal_current(request):
    """
    Redirct to the most recent (and hopefully current) volume of the journal
    :param request:
    :return:
    """

    def get_current_volume():
        # Return the most recent (max) year for any content item
        return Content.objects.aggregate(Max('year'))['year__max']

    current_volume = get_current_volume()
    return redirect(reverse('journal:volumes', kwargs={'year': current_volume}))


def journal_citation(request, content_id, **kwargs):
    c = get_object_or_404(Content, pk=content_id)
    return HttpResponse('%s (%s) "%s" <i>PaleoAnthropology</i> %s:%s-%s' % (
        c.authors, c.year, c.title, c.year, c.start_page, c.end_page))


def journal_bibtex(request, content_id, **kwargs):
    c = get_object_or_404(Content, pk=content_id)
    return HttpResponse(
        '@article{%s, <br>author="%s",<br>title="%s",<br>journal="PaleoAnthropology",<br>year="%s",<br>volume="%s",<br>pages="%s-%s"<br>}' % (
            c.pdf_link, c.authors, c.title, c.year, c.year, c.start_page, c.end_page))


def journal_ris(request, content_id, **kwargs):
    c = get_object_or_404(Content, pk=content_id)
    authors = c.authors
    author_string = "AU - " + string.replace(authors, ",", "<br>AU - ")
    author_string2 = string.replace(author_string, " and ", "<br>AU - ")
    ris_string = 'TY - JOUR<br>%s<br>T1 - %s<br>JO - PaleoAnthropology<br>Y1 - %s<br>VL - %s<br>SP - %s<br>EP - %s<br>ER - ' % \
                 (author_string2, c.title, c.year, c.year, c.start_page, c.end_page)
    return HttpResponse(ris_string)


####################################FOR QUERY PURPOSES###########################################

#Credit: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/

#Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


#Returns a query, that is a combination of Q objects. That combination aims to search keywords within a model by
#testing the given search fields.


def get_query(fields, query_string):
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field in fields:
            q = Q(**{'%s__icontains' % field: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query