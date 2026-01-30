from rest_framework import serializers
from menus.models import Page
from menus.serializers.employee_serializers import EmployeeListSerializer
from menus.serializers.img_files_serializers import PageFileSerializer, PageImageSerializer
from menus.serializers.menu_serializers import MenuReadSerializer
from posts.serializers import PostManageListSerializer

# # # # # Default # # # # #

class PageListSerializer(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)
    class Meta:
        model = Page
        fields = [
                    "id", "title_uz", 'title_ru', 'title_en', "status", "type", "slug", "menu"
                ]


class PageSerializer(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)

    class Meta:
        model = Page
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    'description_uz', 'description_ru', 'description_en',
                    "status", "type", "slug", "menu"
                ]
        read_only_fields = ['id']



# # # # # # Users # # # #
class PageDetailSerializerForUsers(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)
    images = PageImageSerializer(many=True, read_only=True)
    employees = EmployeeListSerializer(many=True, read_only=True)
    files = PageFileSerializer(many=True, read_only=True)
    posts = serializers.SerializerMethodField()
    labs = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    scientific_directions = serializers.SerializerMethodField()
    postgraduate_educations = serializers.SerializerMethodField()


    class Meta:
        model = Page
        fields = [
                    "id", "menu", "type",
                    'title_uz', 'title_ru', 'title_en', "logo", "position",
                    "sub_title_uz", "sub_title_ru", "sub_title_en",
                    "direction_uz", "direction_ru", "direction_en",
                    "duration_uz", "duration_ru", "duration_en",
                    'description_uz', 'description_ru', 'description_en',
                    "slug", "status", "images", "employees", "files", "posts",
                    "labs", "departments", "scientific_directions", "postgraduate_educations", 
                ]
    
    def get_scientific_directions(self, obj) -> list:
        try:
            if obj.type == 'scientific_direction':
                sd_qs = Page.objects.filter(type='scientific_direction', status=True, is_menu_page=False).order_by('position')
                from .scientific_direction_serializers import ScientificDirectionListSerializer
                return ScientificDirectionListSerializer(sd_qs, many=True).data
                
            return []
        except:
            return []
    
    def get_postgraduate_educations(self, obj) -> list:
        try:
            if obj.type == 'postgraduate_education':
                pe_qs = Page.objects.filter(type='postgraduate_education', status=True, is_menu_page=False).order_by('position')
                from .postgraduate_education_serializers import PostgraduateEducationListSerializer
                return PostgraduateEducationListSerializer(pe_qs, many=True).data
                
            return []
        except:
            return []

    
    def get_labs(self, obj) -> list:
        try:
            if obj.type == 'lab':
                labs_qs = Page.objects.filter(type='lab', status=True, is_menu_page=False).order_by('position')
                from .labser import LabSer
                return LabSer(labs_qs, many=True).data
                
            return []
        except:
            return []
    
    def get_departments(self, obj) -> list:
        try:
            if obj.type == 'department':
                depts_qs = Page.objects.filter(type='department', status=True, is_menu_page=False).order_by('position')
                # Local import to avoid circular dependency with labser.
                from .departments_serializers import DepartmentListSerializer
                return DepartmentListSerializer(depts_qs, many=True).data
            
            return []
        except:
            return []
    
    def get_posts(self, obj) -> list:
        try:
            if obj.posts.exists():
                posts_qs = obj.posts.filter(status=True)
                return PostManageListSerializer(posts_qs, many=True).data
        except:
            return []
        
    

class PageListSerializerForUsers(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = [ "id", 'title_uz', 'title_ru', 'title_en']
        read_only_fields = ["id", "title_uz", "title_ru", "title_en"]

