from django.urls import path,include
from . import views

urlpatterns = [
    path("import-data/",views.import_data , name = 'import_data'),
]