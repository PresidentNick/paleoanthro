from django.db import models

CONTENT_TYPE_CHOICES = (
('Annual Meeting Abstracts', 'Annual Meeting Abstracts'),
('Articles', 'Articles'),
('Letters', 'Letters'),
('Data', 'Data'),
('Reviews', 'Reviews'),
)


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    contact_email = models.EmailField(max_length=75, null=True, blank=True)  # lead author contact email
    title = models.TextField(null=True, blank=True)  # abstract title
    authors = models.TextField(null=True, blank=True)  # text string of all authors
    abstract_text = models.TextField(null=True, blank=True)  # abstract text
    article_type = models.CharField(max_length=128, choices=CONTENT_TYPE_CHOICES)  # article type: article, review, letter, data
    acknowledgements = models.TextField(null=True, blank=True)  # article acknowledgements
    references = models.TextField(null=True, blank=True)  # references cited in the article
    comments = models.TextField(null=True, blank=True)
    year = models.IntegerField() # year of publication
    volume = models.IntegerField(null=True, blank=True)  # volumen number, for PaleoAnthro same as year
    start_page = models.CharField(max_length=20, null=True, blank=True)  # starting page as a string, can have leading letters, e.g. L120 for a letter or A4 for an abstract
    end_page = models.CharField(max_length=20, null=True, blank=True)
    start_page_n = models.IntegerField(null=True, blank=True)  # starting page as an integer
    end_page_n = models.IntegerField(null=True, blank=True)
    file_size = models.CharField(max_length=20,null=True, blank=True)
    pdf_link = models.CharField(max_length=200, null=True, blank=True)
    article = models.CharField(max_length=100, null=True, blank=True)
    doi = models.CharField(max_length=128, null=True, blank=True)
    last_modified = models.DateField(null=False, blank=True, auto_now_add=True, auto_now=True)
    created = models.DateField(null=False, blank=True, auto_now_add=True)
    pdf = models.FileField(upload_to = "webapps/static/journal/content/", null=True, blank=True)
    supplement1 = models.CharField(max_length=50, null=True, blank=True)  # string with comma separated file names for supplementary data
    supplement2 = models.CharField(max_length=50, null=True, blank=True)  # string with comma separated file names for supplementary data
    supplement3 = models.CharField(max_length=50, null=True, blank=True)  # string with comma separated file names for supplementary data
    supplement4 = models.CharField(max_length=50, null=True, blank=True)  # string with comma separated file names for supplementary data

    def __unicode__(self):
        return self.title[0:20]


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    book_authors = models.TextField(null=True, blank=True)
    year = models.IntegerField()
    title = models.CharField(max_length=500, null=True, blank=True)
    place = models.CharField(max_length=256, null=True, blank=True)
    publisher = models.CharField(max_length=256, null=True, blank=True)
    pages = models.IntegerField()
    reviewer = models.CharField(max_length=256, null=True, blank=True)
    review_text =  models.TextField(null=True, blank=True)
    review_title = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    last_modified = models.DateField(null=False, blank=True, auto_now_add=True, auto_now=True)
    created = models.DateField(null=False, blank=True, auto_now_add=True)

    def __unicode__(self):
        return self.title[0:20]
