from django.contrib import admin
from models import Member, Membership
from django.template import loader, RequestContext
from django.contrib.admin import helpers
from django.http import HttpResponse
from django.core.mail import send_mass_mail
import csv


class MembershipInline(admin.TabularInline):
    model = Membership


def create_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PaleoAnthro_directory_info.csv"'
    writer = csv.writer(response)
    for member in queryset.all():
        writer.writerow([unicode(member.first_name).encode("utf-8"), unicode(member.last_name).encode("utf-8"),
                         member.email_address])
    return response

create_csv.short_description = "Download .csv file with selected member info"


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email_address', 'member', 'registered', 'recent_membership',
                    'recent_registration', 'last_modified')
    list_display_links = ['id', 'last_name', 'first_name']
    list_filter = ['member', 'registered']
    list_per_page = 600
    search_fields = ['last_name', 'first_name', 'id', 'email_address', 'country']
    inlines = [MembershipInline, ]
    actions = [create_csv, 'send_emails']

    def send_emails(self, request, queryset):
        return_url = "/admin/paleoanthro/member/"
        if 'apply' in request.POST:  # check if the email form has been completed
            # code to send emails. We use send_mass_email, which requires a four-part tuple
            # containing the subject, message, from_address and a list of to addresses.
            if 'subject' in request.POST:
                if request.POST["subject"] == '':
                    self.message_user(request, "Message is missing a subject", level='error')
                    t = loader.get_template("email.html")
                    c = RequestContext(request, {'return_url': return_url, 'emails': queryset,
                                                 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, })
                    return HttpResponse(t.render(c))
                else:
                    subject = request.POST["subject"]
            if 'message' in request.POST:
                if request.POST["message"] == '':
                    self.message_user(request, "Message is empty", level='error')
                    t = loader.get_template("email.html")
                    c = RequestContext(request,
                                       {'emails': queryset, 'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, })
                    return HttpResponse(t.render(c))
                message = request.POST["message"]
            from_address = 'paleoanthro@paleoanthro.org'
            messages_list = []
            # build the to list by iterating over records in queryset from selected records
            for i in queryset:
                if i.email_address:
                    to_address = [i.email_address]
                    message_tuple = (subject, message, from_address, to_address)
                    messages_list.append(message_tuple)
            messages_tuple = tuple(messages_list)
            send_mass_mail(messages_tuple, fail_silently=False)
            self.message_user(request, "Mail sent successfully ")
        else:
            t = loader.get_template("email.html")
            c = RequestContext(request, {'return_url': return_url, 'emails': queryset,
                                         'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME, })
            return HttpResponse(t.render(c))

    send_emails.short_description = "Send an email to selected members"


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'year', 'payment_type')

admin.site.register(Member, MemberAdmin)
