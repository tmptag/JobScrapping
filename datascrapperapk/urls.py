from django.urls import path
from . import views

urlpatterns = [path("get_jd/", views.job_description, name="getJd")]
