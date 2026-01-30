from menus.models import Page
from menus.serializers.page_serializers import PageListSerializer, PageSerializer


class PostgraduateEducationListSerializer(PageListSerializer):
    class Meta(PageListSerializer.Meta):
        model = Page
        fields = list(PageListSerializer.Meta.fields) + [
            "logo", "position",
            "sub_title_uz", "sub_title_ru", "sub_title_en",
            "direction_uz", "direction_ru", "direction_en",
            "duration_uz", "duration_ru", "duration_en"
        ]


class PostgraduateEducationSerializer(PageSerializer):
    class Meta(PageSerializer.Meta):
        model = Page
        fields = list(PageSerializer.Meta.fields) + [
            "logo", "position",
            "sub_title_uz", "sub_title_ru", "sub_title_en",
            "direction_uz", "direction_ru", "direction_en",
            "duration_uz", "duration_ru", "duration_en"
        ]
