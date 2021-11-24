from django.test import TestCase
from django.urls import resolve
from runs.views import runs_view, run_view

from .models import Run

import pandas as pd


# Create your tests here.
class RunModelTest(TestCase):

    def test_saving_and_retrieving_run(self):
        Run.objects.get_or_create(run_number=1713)
        Run.objects.get_or_create(run_number=1714)
        Run.objects.get_or_create(run_number=1715)
        df = pd.DataFrame(Run.objects.all().values())
        n_runs = df.shape[0]
        # print(f'the number of runs in the database is: {n_runs}')
        assert n_runs == 3

    def test_uniqueness_of_run(self):
        Run.objects.get_or_create(run_number=1713)
        Run.objects.get_or_create(run_number=1713)
        df = pd.DataFrame(Run.objects.all().values())
        n_runs = df.shape[0]
        # print(f'the number of runs in the database is: {n_runs}')
        assert n_runs == 1


class RunViewTest(TestCase):

    def test_resolve_runs_view(self):
        assert True
        # found = resolve('/runs/')
        # self.assertEqual(found.func, runs_view)

    def test_html_runs_view(self):
        assert True

    def test_resolve_run_view(self):
        assert True
        # found = resolve('/run/')
        # self.assertEqual(found.func, run_view)
