from django.shortcuts import render
from rest_framework import viewsets
from app1.models import Playstore 
from .serializer import PlayStoreSerializer

class PlaystoreAPI(viewsets.ModelViewSet):
    queryset=Playstore.objects.all()
    serializer_class = [PlayStoreSerializer] 
    http_method_names=['get']

    def get_queryset(self):
        return Playstore.objects.all()
