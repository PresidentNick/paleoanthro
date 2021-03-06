from django.shortcuts import render
from django.views import generic
from fiber.views import FiberPageMixin
from django.core.urlresolvers import reverse
from dissertations.models import Dissertation



#####################
# Class Based Views #
#####################

class DissertationIndexView(FiberPageMixin, generic.ListView):
    # default template name is 'dissertations/dissertation_list.html'
    model = Dissertation

    def get_fiber_page_url(self):
        return reverse('dissertations:download')