from menus.models import Menu, Page
from rest_framework import serializers
from menus.services.menu_services import MenuService


class MenuReadSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    page_slug = serializers.SerializerMethodField()
    page_type = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en', "parent",
                    "status", "position", "has_page", "page_slug", "page_type", "children"
                ]
        
    def get_page_type(self, obj) -> str | None:
        if hasattr(obj, 'page') and obj.page:
            return obj.page.type
        return None
    
    

    def get_page_slug(self, obj) -> str | None:
        if hasattr(obj, 'page') and obj.page:
            return obj.page.slug
        return None
    
    
    def get_children(self, obj)-> list:
        try:
            if obj.children.exists():
                return MenuReadSerializer(obj.children.all(), many=True).data
        except:
            return []
        



class MenuWriteSerializer(serializers.ModelSerializer):

    page_slug = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Menu
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en', 'page_type',
                    "status", "position", "parent", "has_page", "page_slug"
                ]
    
    def validate(self, data):
        has_page = data.get('has_page', None)

        if has_page:
            page_slug = data.get('page_slug', None)
            if not page_slug:
                raise serializers.ValidationError("Agar 'has_page' True bo'lsa, 'page_slug' kiritilishi shart.")
          
        return data
    
    def create(self, validated_data):
        return MenuService.create_menu(validated_data)
    
    def update(self, instance, validated_data):
        return MenuService.update_menu(instance, validated_data)
    

        
    
    

