from .models import Company
from rest_framework import serializers
from menus.serializers.page_serializers import PageListSerializer
from parts.serializers import CarouselSerializer, CollaborationsSerializer
from posts.serializers import PostManageListSerializer
from menus.serializers.menu_serializers import MenuReadSerializer
from menus.serializers.scientific_direction_serializers import ScientificDirectionListSerializer
from menus.serializers.postgraduate_education_serializers import PostgraduateEducationListSerializer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class HomePageSerializer(serializers.Serializer):
    menu = MenuReadSerializer(many=True)
    company = CompanySerializer(allow_null=True)
    carousels = CarouselSerializer(many=True)
    latest_posts = PostManageListSerializer(many=True)
    latest_news = PostManageListSerializer(many=True)
    latest_announcements = PostManageListSerializer(many=True)
    scientific_directions = ScientificDirectionListSerializer(many=True)
    postgraduate_education = PostgraduateEducationListSerializer(many=True)
    collaborations = CollaborationsSerializer(many=True)

class DashboardItems(serializers.Serializer):
    name = serializers.CharField()
    total_count = serializers.IntegerField()
    active_count = serializers.IntegerField()
    inactive_count = serializers.IntegerField()
    images_count = serializers.IntegerField(required=False)

class DashboardSerializer(serializers.Serializer):
    dashboard = DashboardItems(many=True)