from django.db import models
from base.choices import COUNTRY_CHOICES, PAYMENT_TYPE_CHOICES
from django.forms import ModelForm, EmailInput, Textarea, TextInput
from django.core.urlresolvers import reverse
from captcha.fields import CaptchaField


##########################
# Members Model Classes #
##########################

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, null=True, blank=True, help_text="e.g. Mr. Dr., Prof. etc.")
    first_name = models.CharField(max_length=128, null=True, blank=True, help_text="Given name or names")
    last_name = models.CharField(max_length=128, null=True, blank=True, help_text="Family name")
    address_line1 = models.CharField(max_length=128, null=True, blank=True)
    address_line2 = models.CharField(max_length=128, null=True, blank=True)
    address_line3 = models.CharField(max_length=128, null=True, blank=True)
    address_line4 = models.CharField(max_length=128, null=True, blank=True)
    address_line5 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state_or_province = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True, choices=COUNTRY_CHOICES)
    postal_code = models.CharField(max_length=128, null=True, blank=True)
    email_address = models.EmailField(max_length=128, null=True, blank=True)
    old_email_address = models.EmailField(max_length=128, null=True, blank=True)
    hash = models.CharField(max_length=100, null=True, blank=True)
    member = models.NullBooleanField()
    registered = models.NullBooleanField()
    last_modified = models.DateField(auto_now_add=True, auto_now=True, null=False)
    created = models.DateField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def upper_case_name(self):
        if self.title:
            return ("%s %s %s" % (self.title, self.first_name, self.last_name)).title()
        else:
            return ("%s %s" % (self.first_name, self.last_name)).title()

        upper_case_name.short_description = 'Name'
        upper_case_name.admin_order_field = 'last_name'

    def is_current_member(self):
        membership_years = self.membership_set.filter(payment_type='M').filter(year=2013)

    def recent_membership(self):  # returns the last two years of recorded membership
        membership_objects = self.membership_set.filter(payment_type='M')
        membership_years = []
        for o in membership_objects:
            membership_years.append(o.year)
        if membership_years:
            membership_years.sort()
            membership_years.reverse()  # most recent years first
            return str(membership_years[:2]).strip('[]')  # converts integers to strings and removes braces
        else:
            return 'None'

    def recent_registration(self):  # returns the last two years of recorded registration
        registration_objects = self.membership_set.filter(payment_type='R')
        registration_years = []
        for o in registration_objects:
            registration_years.append(o.year)
        if registration_years:
            registration_years.sort()
            registration_years.reverse()  # most recent years first
            return str(registration_years[:2]).strip('[]')  # converts integers to strings and removes braces
        else:
            return 'None'

    def get_absolute_url(self):
        return reverse('members:member_update', kwargs={'pk': self.pk})


class Membership(models.Model):
    member = models.ForeignKey(Member)  # the member id
    year = models.IntegerField()  # the membership/registration year
    payment_type = models.CharField(max_length=128, choices=PAYMENT_TYPE_CHOICES)  # payment for membership or reg.

    def __unicode__(self):
        return self.year


#######################
# Members Model Forms #
#######################

class MemberForm(ModelForm):
    human_test = CaptchaField(help_text='Enter the solution')
    class Meta:
        model = Member
        fields = ['title', 'first_name', 'last_name', 'email_address',
                  'address_line1', 'address_line2', 'address_line3', 'city',
                  'state_or_province', 'postal_code', 'country', 'human_test']
        widgets = {
            'title': TextInput(attrs={'size': 15}),
            'email_address': EmailInput(attrs={'size': 30}),
            'address_line1': TextInput(attrs={'size': 30}),
            'address_line2': TextInput(attrs={'size': 30}),
            'address_line3': TextInput(attrs={'size': 30}),
        }
