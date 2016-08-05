import random

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from .settings import RANDOM_ENTRIES_AMOUNT
from .models import Tag, Entry
from .serializers import TagSerializer, EntrySerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.filter(entry__active=True).distinct()
    serializer_class = TagSerializer


class EntryViewSet(viewsets.ViewSet):
    queryset = Entry.objects.filter(active=True).prefetch_related('tags')
    serializer_class = EntrySerializer

    def tag(self, request, tag):
        queryset = self.queryset.filter(tags=tag)
        return Response(self.serializer_class(queryset, many=True).data)

    def random(self, request):
        num = RANDOM_ENTRIES_AMOUNT
        if num > self.queryset.count():
            num = self.queryset.count()
        return Response(self.serializer_class(random.sample(list(self.queryset), num), many=True).data)
