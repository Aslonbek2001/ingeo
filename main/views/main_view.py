from main.models import Company
from posts.models import Post
from posts.serializers import PostManageListSerializer
from drf_spectacular.utils import extend_schema
from main.service import HomePageService
from main.serializers import HomePageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from menus.serializers.menu_serializers import MenuReadSerializer


class HomePageView(APIView):
    @extend_schema(
        tags=["Home Page"],
        description="Bosh sahifa uchun ma'lumotlar",
        responses={200: HomePageSerializer},
    )
    def get(self, request, *args, **kwargs):
        menu = HomePageService.get_navbar()
        company = HomePageService.get_company_info()
        carousels = HomePageService.get_carousels()
        latest_posts = HomePageService.get_latest_posts()
        latest_news = HomePageService.get_latest_posts(type="news")
        latest_announcements = HomePageService.get_latest_posts(type="announcement")
        scientific_directions = HomePageService.scientific_directions()
        postgraduate_education = HomePageService.postgraduate_education()
        collaborations = HomePageService.collaborations()

        data = {
            "menu": menu,
            "company": company,
            "carousels": carousels,
            "latest_posts": latest_posts,
            "latest_news": latest_news,
            "latest_announcements": latest_announcements,
            "scientific_directions": scientific_directions,
            "postgraduate_education": postgraduate_education,
            "collaborations": collaborations,
        }

        serializer = HomePageSerializer(data)
        return Response(serializer.data)

        
    


        









