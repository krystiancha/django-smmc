from rest_framework import serializers

from .models import Tag, Entry


class TagSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.name

    class Meta:
        model = Tag


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'year', 'month', 'day', 'title', 'description', 'tags', 'sort', 'file', 'mime_type')
