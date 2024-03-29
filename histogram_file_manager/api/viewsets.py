import logging
import threading
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from histogram_file_manager.models import HistogramDataFile, HistogramDataFileContents
from histogram_file_manager.api.serializers import HistogramDataFileSerializer
from histogram_file_manager.api.filters import HistogramDataFileFilter
from histograms.models import (
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)
from histogram_file_manager.forms import HistogramDataFileStartParsingForm
from django.core.management import call_command

logger = logging.getLogger(__name__)

HISTOGRAM_PARSING_FUNCTIONS_MAP = {
    HistogramDataFile.FILETYPE_CSV: {
        HistogramDataFileContents.DIMENSIONALITY_1D: {
            # HistogramDataFile.GRANULARITY_RUN:            RunHistogram.from_csv,  # Not implemented yet
            HistogramDataFileContents.GRANULARITY_LUMISECTION: LumisectionHistogram1D.from_csv
        },
        HistogramDataFileContents.DIMENSIONALITY_2D: {
            HistogramDataFileContents.GRANULARITY_LUMISECTION: LumisectionHistogram2D.from_csv
        },
    },
    HistogramDataFile.FILETYPE_NANODQM: {
        HistogramDataFileContents.DIMENSIONALITY_1D: {
            # HistogramDataFile.GRANULARITY_RUN:            RunHistogram.from_csv,  # Not implemented yet
            HistogramDataFileContents.GRANULARITY_LUMISECTION: LumisectionHistogram1D.from_nanodqm
        },
        HistogramDataFileContents.DIMENSIONALITY_2D: {
            HistogramDataFileContents.GRANULARITY_LUMISECTION: LumisectionHistogram2D.from_nanodqm
        },
    },
}


class HistogramDataFileViewset(viewsets.ModelViewSet):
    queryset = HistogramDataFile.objects.all().order_by("id")
    serializer_class = HistogramDataFileSerializer
    filterset_class = HistogramDataFileFilter

    # Cache results for 60 seconds
    # @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def start_parsing(self, request, pk=None):
        """
        Start parsing a specific HistogramDataFile, identified by pk
        """
        required_params = ["granularity", "data_dimensionality", "file_format"]
        hdf = self.get_object()  # Get specific HistogramDataFile

        if hdf.percentage_processed >= 100.0:
            return Response(
                f"HistogramDataFile with pk {pk} is already parsed",
                status=status.HTTP_400_BAD_REQUEST,
            )
        # elif any(param not in request.data for param in required_params):
        # return Response(f"Required param(s) missing ({required_params})",
        # status=status.HTTP_400_BAD_REQUEST)

        form = HistogramDataFileStartParsingForm(request.data)

        if form.is_valid():
            file_format = request.data["file_format"].lower()
            granularity = request.data["granularity"]
            data_dimensionality = int(request.data["data_dimensionality"])
            # Use the HISTOGRAM_PARSING_FUNCTIONS_MAP to find the appropriate parsing method
            try:
                logger.info(self.get_object().filepath)
                # Start as a separate thread, might take a long time
                threading.Thread(
                    target=HISTOGRAM_PARSING_FUNCTIONS_MAP[file_format][
                        data_dimensionality
                    ][granularity],
                    args=(self.get_object().filepath,),
                ).start()  # Comma is intentional
            except KeyError as e:
                return Response(
                    f"Something possibly missing from HISTOGRAM_DIMENSIONS_CHOICES ({e})",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                logger.exception(e)
                return Response(
                    f"Error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                f"Required param(s) missing ({required_params})",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # logger.info(
        # f"Requested parsing of {self.get_object()} as {file_format}")

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False, permission_classes=[IsAdminUser])
    def discover(self, request):
        """
        Action which starts the management command responsible for discovering DQMIO files.
        TODO: Do not run if an already running request is underway.
        TODO: Add unit test for this.
        """

        logger.info(
            f"Received command to start DQMIO files discovery by {request.user}."
        )
        try:
            threading.Thread(
                target=call_command,
                args=("discover_dqm_files",),  # Comma is intentional
            ).start()
        except Exception as e:
            logger.error(f"Error when launching DQMIO file discovery: {repr(e)}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_202_ACCEPTED)

    class Meta:
        ordering = ["-id"]
        fields = "__all__"
