from django.shortcuts import render

from rest_framework import viewsets
from .serializers import RunSerializer

from .models import Run

import pandas as pd


# Create your views here.
def runs_view(request):

    error_message = None
    df = None

    # objects.all().values() provides a dictionary
    # while objects.all().values_list() provides a tuple
    runs_df = pd.DataFrame(Run.objects.all().values())

    if runs_df.shape[0] > 0:
        df = runs_df.drop(['id'], axis=1).to_html()

    else:
        error_message = "No runs in the database"

    context = {
        'error_message': error_message,
        'runs': df,
    }
    return render(request, 'runs/main.html', context)


def run_view(request):
    return render(request, 'runs/run.html')


# class based view (to be compared to function based view)
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all().order_by('run_number')
    serializer_class = RunSerializer




