from django.forms import ModelForm
from models import Abstract, Author, Meeting
from django.forms.models import inlineformset_factory
from django.forms.widgets import Textarea, TextInput, HiddenInput
from django import forms
from captcha.fields import CaptchaField


# Abstract Model Form
class AbstractForm(ModelForm):
    confirm_email = forms.EmailField(widget=TextInput(attrs={'size': 60}))
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.filter(year__exact=2015), empty_label=None)
    year = forms.IntegerField(widget=HiddenInput, initial=2015)
    # human_test = CaptchaField(help_text='Enter the solution') # only for testing

    class Meta:
        model = Abstract
        fields = (
            'year',
            'meeting',
            'presentation_type',
            'title',
            'abstract_text',
            'acknowledgements',
            'references',
            'funding',
            'comments',
            'contact_email',
            'confirm_email',
            # 'human_test' # Only for testing purposes
        )

        widgets = {
            'contact_email': TextInput(attrs={'size': 60, }),

            'title': Textarea(attrs={'cols': 60, 'rows': 2}),
            'abstract_text': Textarea(attrs={'cols': 60, 'rows': 20}),
            'acknowledgements': Textarea(attrs={'cols': 60, 'rows': 5}),
            'references': Textarea(attrs={'cols': 60, 'rows': 5}),
            'comments': Textarea(attrs={'cols': 60, 'rows': 10}),
        }


# Author Model Form
class AuthorForm(ModelForm):
    class Meta:
        model = Author

    def __init__(self, *arg, **kwarg):
        super(AuthorForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

# generate an inline formset for authors, exclude author rank field,
# which the view will add automatically. Show three blank author forms
# and don't show delete buttons
AuthorInlineFormSet = inlineformset_factory(Abstract, Author,
                                            form=AuthorForm,
                                            extra=1,
                                            exclude=('author_rank',),
                                            can_delete=False
                                            )

