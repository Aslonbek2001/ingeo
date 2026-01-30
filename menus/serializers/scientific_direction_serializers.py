from menus.models import Page
from menus.serializers.page_serializers import PageListSerializer, PageSerializer


class ScientificDirectionListSerializer(PageListSerializer):
    class Meta(PageListSerializer.Meta):
        model = Page
        fields = list(PageListSerializer.Meta.fields) + [
            "logo", "position",
            "sub_title_uz", "sub_title_ru", "sub_title_en"
        ]


class ScientificDirectionSerializer(PageSerializer):
    class Meta(PageSerializer.Meta):
        model = Page
        fields = list(PageSerializer.Meta.fields) + [
            "logo", "position",
            "sub_title_uz", "sub_title_ru", "sub_title_en",
        ]
