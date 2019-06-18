from store import views
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('usersProfile/', cache_page(1 * 1)(views.UserProfileViewSet.as_view())),
    path('usersProfile/<int:pk>/', views.UserProfileDetail.as_view()),

    path('units/', (views.UnitsList.as_view())),
    path('units/<int:pk>/', views.UnitsDetail.as_view()),
    path('location/', (views.LocationList.as_view())),
    path('uploadUnitImage/', views.ImagesUnitViewSet.as_view()),
    path('uploadProfileImage/', cache_page(60 * 60)(views.ProfileImageViewSet.as_view())),

]
