import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileStartParsingForm
from histogram_file_manager.api.filters import HistogramDataFileFilter
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

        n_hist1d = hist1d.count()
        n_hist2d = hist2d.count()

        context = {
            "file_id": fileid,
            "fileobj": target_file,
            "filename": target_file.filepath,
            "hist1d": hist1d,
            "hist2d": hist2d, 
            "n_hist1d": n_hist1d,
            "n_hist2d": n_hist2d
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