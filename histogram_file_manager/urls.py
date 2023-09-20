from django.urls import path
from . import views

app_name = "histogram_file_manager"

urlpatterns = [
    path("", views.histogram_file_manager, name="file_manager"),
    path("<int:fileid>", views.individual_file_viewer, name="file_viewer"),
]
