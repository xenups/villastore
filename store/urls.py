from store import views
from django.urls import path

urlpatterns = [

    path('usersProfile/', views.UserProfileList.as_view()),
    path('usersProfile/<int:pk>/', views.UserProfileDetail.as_view()),

    path('units/', views.UnitsList.as_view()),

]
