from django.test import TestCase
from django.urls import resolve
from runs.views import runs_view, run_view

from .models import Run

# Create your tests here.

class HomePageTest(TestCase):

    def test_resolve_runs_view(self):
        found = resolve('/')
        self.assertEqual(found.func, runs_view)

    def test_resolve_run_view(self):
        found = resolve('/run/')
        self.assertEqual(found.func, run_view)


class RunModelTest(TestCase):

    def test_saving_and_retrieving_run(self):
        run = Run(run_number=1712)
        run.save()
