from django.views import generic
from models import Member, MemberForm
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin
from django.forms import EmailInput, Textarea


#######################
## Members Page Views ##
#######################


class MembersIndexView(FiberPageMixin, generic.ListView):
    template_name = 'members/members.html'
    context_object_name = 'members_list'

    def get_fiber_page_url(self):
        return reverse('members:members')

    def get_queryset(self):
        if 'query' in self.request.GET:  # check for data
            query = self.request.GET['query']  # if data present get the request
            if query != '':  # Don't do anything if empty query string
                return Member.objects.filter(last_name__icontains=query).order_by('last_name', 'first_name')


class MemberUpdateView(FiberPageMixin, generic.UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/member_update.html'

    def get_fiber_page_url(self):
        return reverse('members:member_update_root')

