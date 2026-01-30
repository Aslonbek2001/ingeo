from menus.models import PageFiles, PageImages
from rest_framework import serializers



class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImages
        fields = ["id", "page", "image"]


class PageFileSerializer(serializers.ModelSerializer):
    page_slug = serializers.SerializerMethodField()
    class Meta:
        model = PageFiles
        fields = [
                    "id", "page", "page_slug",
                    'title_uz', 'title_ru', 'title_en',
                    "file", "position", "status"
                ]
        
    def get_page_slug(self, obj) -> str | None:
        try:
            return obj.page.slug
        except:
            return None


