from django.urls import path
from rest_framework import routers

from core.views import IndexView, HomePageView, ProductDataAPIView

router = routers.DefaultRouter()
router.register('product', ProductDataAPIView, basename='create')

urlpatterns = [
 path('home/', HomePageView.as_view(), name='home'),
]
urlpatterns += router.urls
