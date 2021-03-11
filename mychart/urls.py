from . import views
from django.urls import path

urlpatterns = [
    path('',views.AddPost.as_view(),name="chart"),
]