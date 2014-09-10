from django.db import models
from ckeditor.fields import RichTextField


THESIS_TYPE_CHOICES = (
    ('PhD', 'PhD'),
    ('MA', 'MA')
)


class Dissertation(models.Model):
    author_last_name = models.CharField(max_length=200, null=False, blank=False)  # REQUIRED
    author_given_names = models.CharField(max_length=200, null=False, blank=False)  # REQUIRED
    contact_email = models.EmailField(max_length=128, null=True, blank=True)  # REQUIRED
    title = RichTextField(max_length=200, null=False, blank=False)  # REQUIRED
    abstract_text = RichTextField(null=True, blank=True)  # REQUIRED
    comments = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=False, blank=False)  # REQUIRED.
    pages = models.IntegerField(null=True, blank=True, help_text="The page length of the thesis")
    publisher = models.CharField(max_length=200, null=True, blank=True, help_text="The publishing institution")
    thesis_type = models.CharField(max_length=50, null=True, blank=True, choices=THESIS_TYPE_CHOICES)
    location = models.CharField(max_length=200, null=True, blank=True, help_text="The publishing location")
    last_modified = models.DateField(null=False, blank=True, auto_now_add=True, auto_now=True)  # REQUIRED BUT AUTOMATIC
    created = models.DateField(null=False, blank=True, auto_now_add=True)  # REQUIRED BUT AUTOMATIC
    abstract_media = models.FileField(upload_to="dissertations/", null=True, blank=True)
    thesis_media = models.FileField(upload_to="dissertations/", null=True, blank=True)

    def __unicode__(self):
        return self.title[0:20]