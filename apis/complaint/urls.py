from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework import routers

urlpatterns = [

    path('',views.postComplaint, name='complaint-add'),
    path('fire/',views.firestore1, name='fire-add')
]
