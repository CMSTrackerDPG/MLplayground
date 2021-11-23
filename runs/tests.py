from django.test import TestCase
from .models import Run

# Create your tests here.
class RunModelTest(TestCase):

    def test_saving_and_retrieving_run(self):
        run = Run(run_number=1712)
        run.save()
