from rest_framework import serializers

from ad.models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ad"""

    class Meta:
        model = Ad
        fields = ["id", "title", "price", "description", "author"]
        read_only_fields = ["author"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    class Meta:
        model = Review
        fields = ["id", "text", "ad", "author", "created_at"]
        read_only_fields = ["ad", "author"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["text"]
