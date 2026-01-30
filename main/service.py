from main.models import Company
from posts.models import Post, PostImages
from parts.models import Carousel, Collaborations
from menus.models import Page, PageImages
from menus.models import Menu
from main.serializers import DashboardSerializer



class HomePageService:
    
    @staticmethod
    def get_navbar():
        return Menu.objects.filter(parent__isnull=True, status=True).order_by('position')
        

    @staticmethod
    def get_carousels():
        return Carousel.objects.filter(status=True).order_by('position')

    @staticmethod
    def get_company_info():
        return Company.objects.first()
    
    @staticmethod
    def get_latest_posts(type=None):
        if type:
            return Post.objects.filter(status=True, type=type).order_by('-published_date')[:6]
        return Post.objects.filter(status=True).order_by('-published_date')[:6]

    @staticmethod
    def scientific_directions():
        return Page.objects.filter(type="scientific_direction", is_menu_page=False, status=True).order_by("position")

    @staticmethod
    def postgraduate_education():
        return Page.objects.filter(type="postgraduate_education", is_menu_page=False, status=True).order_by("position")
    
    @staticmethod
    def collaborations():
        return Collaborations.objects.filter(status=True).order_by('position')
    


class DashboardService:
    
    @staticmethod
    def get_pages_count():
        total_qs = Page.objects.filter(type="page")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PageImages.objects.filter(page__type="page").count()
        return {
            "name": "Pages",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }
    
    @staticmethod
    def get_labs_count():
        total_qs = Page.objects.filter(type="lab")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PageImages.objects.filter(page__type="lab").count()
        return {
            "name": "Laboratories",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }
    
    @staticmethod
    def get_departments_count():
        total_qs = Page.objects.filter(type="department")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PageImages.objects.filter(page__type="department").count()
        return {
            "name": "Departments",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }
    
    # @staticmethod
    # def get_faculties_count():
    #     total = Page.objects.filter(type="faculty").count()
    #     active = Page.objects.filter(status=True).count()
    #     inactive = total - active
    #     images_count =  PageImages.objects.filter(page__type="faculty").count()
    #     return DashboardItems(name="Faculties", total_count=total, active_count=active, inactive_count=inactive, images_count=images_count)

    @staticmethod
    def get_scientific_directions_count():
        total_qs = Page.objects.filter(type="scientific_direction")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PageImages.objects.filter(page__type="scientific_direction").count()
        return {
            "name": "Scientific Directions",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }

    @staticmethod
    def get_postgraduate_education_count():
        total_qs = Page.objects.filter(type="postgraduate_education")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PageImages.objects.filter(page__type="postgraduate_education").count()
        return {
            "name": "Postgraduate Education",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }
    
    @staticmethod
    def get_carousels_count():
        total = Carousel.objects.count()
        active = Carousel.objects.filter(status=True).count()
        inactive = total - active
        return {
            "name": "Carousels",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": total,
        }

    @staticmethod
    def get_news_count():
        total_qs = Post.objects.filter(type="news")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PostImages.objects.filter(post__type="news").count()
        return {
            "name": "News",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }
    
    @staticmethod
    def get_announcements_count():
        total_qs = Post.objects.filter(type="announcement")
        total = total_qs.count()
        active = total_qs.filter(status=True).count()
        inactive = total - active
        images_count = PostImages.objects.filter(post__type="announcement").count()
        return {
            "name": "Announcements",
            "total_count": total,
            "active_count": active,
            "inactive_count": inactive,
            "images_count": images_count,
        }

    
    @staticmethod
    def get_dashboard_data():
        items = [
            DashboardService.get_pages_count(),
            DashboardService.get_departments_count(),
            DashboardService.get_labs_count(),
            # DashboardService.get_faculties_count(),
            DashboardService.get_scientific_directions_count(),
            DashboardService.get_postgraduate_education_count(),
            DashboardService.get_carousels_count(),
            DashboardService.get_news_count(),
            DashboardService.get_announcements_count(),
        ]
        return DashboardSerializer({"dashboard": items})
