from store import views
from django.urls import path

urlpatterns = [

    path('usersProfile/', views.UserProfileViewSet.as_view()),
    path('usersProfile/<int:pk>/', views.UserProfileDetail.as_view()),

    path('units/', views.UnitsList.as_view()),
    path('units/<int:pk>/', views.UnitsDetail.as_view()),

]
