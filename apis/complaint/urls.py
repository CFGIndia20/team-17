from django.contrib import admin
from django.urls import path,include
from . import views
# from .views import EmployeeViewSet
from rest_framework import routers



# router = routers.DefaultRouter()
# router.register('empData', EmployeeViewSet)

urlpatterns = [

    path('',views.postComplaint, name='complaint-add')
]
