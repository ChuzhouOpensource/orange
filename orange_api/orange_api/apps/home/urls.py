from django.urls import path,include
from home import views

urlpatterns = [

    path('test', views.TestView.as_view())

]
