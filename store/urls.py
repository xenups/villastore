from store import views
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('units/', (views.UnitsList.as_view())),
    path('units/<int:pk>/', views.UnitsDetail.as_view()),
    path('location/', (views.LocationList.as_view())),
    path('uploadUnitImage/', views.ImagesUnitViewSet.as_view()),


]
