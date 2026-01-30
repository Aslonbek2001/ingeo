from rest_framework import serializers
from menus.models import Page, PageImages
from menus.serializers.img_files_serializers import PageImageSerializer
from menus.serializers.page_serializers import PageListSerializer, PageSerializer


class LabSer(PageListSerializer):
    image = serializers.SerializerMethodField()

    class Meta(PageListSerializer.Meta):
        model = Page
        fields = list(PageListSerializer.Meta.fields) + ["position", "image"]

    def get_image(self, obj) -> str | None:
        try:
            first_image = obj.images.first()
            if first_image:
                return first_image.image.url
        except:
            return None


class LabDetailSer(PageSerializer):
    images = PageImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    exists_image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta(PageSerializer.Meta):
        model = Page
        fields = list(PageSerializer.Meta.fields) + [
            "position", "images", "upload_images", "exists_image_ids"
        ]

    def create(self, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        validated_data.pop("exists_image_ids", None)
        page = Page.objects.create(**validated_data)
        self._create_images(page, upload_images)
        return page

    def update(self, instance, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        exists_ids = validated_data.pop("exists_image_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if exists_ids is not None:
            instance.images.exclude(id__in=exists_ids).delete()

        self._create_images(instance, upload_images)
        return instance

    def _create_images(self, page, images):
        for image in images:
            PageImages.objects.create(page=page, image=image)
