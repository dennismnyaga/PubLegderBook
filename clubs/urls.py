from django.urls import path
from . import views


urlpatterns = [
    path('club/<int:pk>', views.ClubsOperations.as_view()),
    path('club/', views.ClubsOperations.as_view()),
    path('clubGetPost/', views.ClubGetOperations.as_view()),
]
