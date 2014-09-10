from django.test import TestCase
from members.models import Member, Membership
from fiber.models import Page
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime


# Factory method to create a fiber page tree.
def create_django_page_tree():
    mainmenu=Page(title='mainmenu')
    mainmenu.save()
    home = Page.objects.create(title='home', parent=mainmenu, url='home', template_name='base/home.html')
    detail = Page.objects.create(title='detail', parent=home, url='home/detail', template_name='base/detail.html')
    join = Page.objects.create(title='join', parent=home, url='join', template_name='base/join.html')
    members = Page.objects.create(title='members', parent=home, url='members', template_name='base/members.html')
    meetings = Page.objects.create(title='meetings', parent=mainmenu, url='meetings', template_name='')


class MemberMethodTest(TestCase):

    def test_create_member_method(self):
        m = Member(last_name='Bugglesworth', first_name='Paul', title="Dr.", member=True, registered=False)
        self.assertEqual(m.last_name, 'Bugglesworth')

        member_start_count = Member.objects.count()
        m.save()
        Member.objects.create(last_name="Lennon", first_name="John", member=True, registered=True)
        member_end_count = Member.objects.count()
        self.assertEqual(member_end_count, member_start_count+2)

    def test_uppercase_name_method(self):
        m = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Paul Bugglesworth')

    def test_uppercase_name_method_with_title(self):
        m = Member(title='Dr.', last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Dr. Paul Bugglesworth')

    def test_recent_membership_method(self):
        member_start_count = Member.objects.count()
        membership_start_count = Membership.objects.count()
        member = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(member.recent_membership(), 'None')  # None b/c Membership table is empty
        self.assertEqual(member.recent_registration(), 'None')  # because no registration record
        Membership.objects.create(member=member, year=2013, payment_type="M")  # Add a membership record
        self.assertEqual(member.recent_membership(), '2013')  # True now that there is a membership record
        self.assertEqual(member.recent_registration(), 'None')  # because no registration record
        Membership.objects.create(member=member, year=2013, payment_type="R")  # Add a registration record
        self.assertEqual(member.recent_membership(), '2013')
        self.assertEqual(member.recent_registration(), '2013')
        Membership.objects.create(member=member, year=2014, payment_type="M")  # Add a membership record
        self.assertEqual(member.recent_membership(), '2014, 2013')
        self.assertEqual(member.recent_registration(), '2013')

        membership_end_count = Membership.objects.count()
        self.assertEqual(membership_end_count, membership_start_count+3)
        member_end_count = Member.objects.count()
        self.assertEqual(member_end_count, member_start_count+1)

    def test_get_absolute_url_method(self):
        member = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEquals(member.get_absolute_url(), '/members/'+str(member.id)+'/')


# class MembersPageViewMethods(TestCase):
#     def test_home_page_view_no_members(self):
#         create_django_page_tree()  # create a test fiber page tree
#         self.assertEqual(reverse('members:members'), '/members/')  # sanity check for reverse method
#         response = self.client.get(reverse('members:members'))  # fetch the home page
#         self.assertEqual(response.status_code, 200)  # check home page returns 200
#         self.assertContains(response, "No members match your searching")  # Test no members message
#
#     def test_home_page_view_one_member(self):
#         create_django_page_tree()
#         member = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
#         Membership.objects.create(member=member, year=2013, payment_type="M")  # Add a membership record


