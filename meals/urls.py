from django.urls import path
from . import views
from .views import meals,summary,delete_meal,trends

from django.db.models.functions import TruncDate

urlpatterns = [

    path('', meals, name='meals'),
    path( "summary/", summary, name="summary"),
    path( "<int:id>/", delete_meal,name="delete_meal"),
    path("trends/", trends, name="trends"),
    
]