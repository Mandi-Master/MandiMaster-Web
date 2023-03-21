from django.urls import path
from Home.api import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms', views.getrooms),
    path('rooms/<str:room_id>' , views.getroom),

]
