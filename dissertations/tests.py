from django.test import TestCase
from models import Dissertation


class DisertationModelTests(TestCase):
    def test_dissertation_instance_creation(self):
        dissertation_starting_count = Dissertation.objects.count()
        # Test object creation with required fields only
        Dissertation.objects.create(
            author_last_name="Test",
            author_given_names="Ima",
            contact_email="imatest@someplace.edu",
            title="I Founda Cool Fossil And Said Somthing About It",
            year=2014,
        )
        self.assertEqual(Dissertation.objects.count(), dissertation_starting_count+1)
