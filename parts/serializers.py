from parts.models import Carousel, Application, Collaborations
from rest_framework import serializers


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    'description_uz', 'description_ru', 'description_en',
                    "image", "link", "position", "status"
                ]
        read_only_fields = ["id"]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["id", "submitted_at"]



class CollaborationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborations
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    "image", "link", "position", "status"
                ]
        read_only_fields = ["id"]