import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileStartParsingForm
from histogram_file_manager.api.filters import HistogramDataFileFilter
from histogram_file_manager.tables import IndividualFileTable
from histograms.models import LumisectionHistogram1D, LumisectionHistogram2D

logger = logging.getLogger(__name__)


@login_required
def histogram_file_manager(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    # Convert all available choices to a dict so that JS can understand it
    field_choices = {
        field: dict(choices.choices)
        for field, choices in HistogramDataFileStartParsingForm().fields.items()
    }

    # Get filter to render on front-end
    hdf_filter = HistogramDataFileFilter(
        request.GET, queryset=HistogramDataFile.objects.all()
    )

    return render(
        request,
        "histogram_file_manager/histogram_file_manager.html",
        context={"field_choices": field_choices, "filter": hdf_filter},
    )

@login_required
def individual_file_viewer(request, fileid):
    try:
        target_file = HistogramDataFile.objects.get(id=fileid)
        hist1d = LumisectionHistogram1D.objects.filter(source_data_file=target_file)
        hist2d = LumisectionHistogram2D.objects.filter(source_data_file=target_file)

        histall = []
        for hist in hist1d:
            histall.append({
                "run": hist.lumisection.run.run_number,
                "lumisection": hist.lumisection.ls_number,
                "dimension": "1D",
                "title": hist.title
            })
        for hist in hist2d:
            histall.append({
                "run": hist.lumisection.run.run_number,
                "lumisection": hist.lumisection.ls_number,
                "dimension": "2D",
                "title": hist.title
            })

        #histcollection = list(hist1d) + list(hist2d)
        hist_table = IndividualFileTable(histall)

        RequestConfig(request, paginate={"per_page": 25}).configure(hist_table)

        context = {
            "file_id": fileid,
            "fileobj": target_file,
            "filename": target_file.filepath,
            "hist_table": hist_table
        }
        
        return render(
            request, 
            "histogram_file_manager/individual_file_viewer.html",
            context
        )
    except (HistogramDataFile.DoesNotExist):
        return render(
            request, 
            "histogram_file_manager/individual_file_viewer.html",
            {
                "file_id": fileid,
                "errormsg": f"File {fileid} not found in database."
            }
        )

    return render(
        request,
        "histogram_file_manager/individual_file_viewer.html",
        context={"fileid": fileid}
    )