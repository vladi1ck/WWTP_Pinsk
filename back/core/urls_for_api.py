from django.urls import path
from . import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .logic_for_bbo import (
    PostLabValueView,
    GetLabValueView,
    PostProjValueView,
    GetProjValueView,
)

urlpatterns = [
    path('post_lab_value', PostLabValueView.as_view()),
    path('get_lab_value', GetLabValueView.as_view()),
    path('get_proj_value', GetProjValueView.as_view()),
    path('post_proj_value', PostProjValueView.as_view()),

]