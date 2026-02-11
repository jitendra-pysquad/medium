from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.article.models import Article
from core.serializers import ProductHuntSerializer, MyTokenObtainPairSerializer


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class HomePageView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'



class ProductDataAPIView(CreateModelMixin, GenericViewSet):
    serializer_class = ProductHuntSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer