from django.urls import path
# from menus.views.menus import MenuListCreateAPIView, MenuDetailAPIView

from menus.views.menu_views import MenuListCreateAPIView, MenuDetailAPIView

from menus.views.pages import PageListCreateAPIView, PageDetailAPIView, PageDetailForUsers, AllPagesForSelection
from menus.views.employees import EmployeeListCreateAPIView, EmployeeDetailAPIView
from menus.views.img_file_views import PageFileDetailAPIView, PageFileListCreateAPIView, PageImageDetailAPIView, PageImageListCreateAPIView
from menus.views.laboratories import LabListCreateAPIView, LabDetailAPIView
from menus.views.departments import DepartmentListCreateAPIView, DepartmentDetailAPIView
from menus.views.postgraduate_education import PostgraduateEducationDetailAPIView, PostgraduateEducationListCreateAPIView
from menus.views.scientific_direction import ScientificDirectionDetailAPIView, ScientificDirectionListCreateAPIView


urlpatterns = [
    # Menus
    path("menus/", MenuListCreateAPIView.as_view(), name="menu-list-create"),
    path("menus/<int:menu_id>/", MenuDetailAPIView.as_view(), name="menu-detail"),


    # Pages
    path("pages-users/<slug:slug>/", PageDetailForUsers.as_view(), name="page-for-users"),
    path("pages/<int:id>/", PageDetailAPIView.as_view(), name="page-detail"),
    path("pages/", PageListCreateAPIView.as_view(), name="page-list-create"),
    path("all-pages/", AllPagesForSelection.as_view(), name="all-pages-for-selection"),
    # Laboratories
    path("laboratories/", LabListCreateAPIView.as_view(), name="laboratory-list-create"),
    path("laboratories/<str:lookup>/", LabDetailAPIView.as_view(), name="laboratory-detail"),
    # Departments
    path("departments/", DepartmentListCreateAPIView.as_view(), name="department-list-create"),
    path("departments/<str:lookup>/", DepartmentDetailAPIView.as_view(), name="department-detail"),
    # Postgraduate-education
    path("postgraduate-education/", PostgraduateEducationListCreateAPIView.as_view(), name="postgraduate-education-list-create"),
    path("postgraduate-education/<str:lookup>/", PostgraduateEducationDetailAPIView.as_view(), name="postgraduate-education-detail"),
    #scientific-direction
    path("scientific-direction/", ScientificDirectionListCreateAPIView.as_view(), name="scientific-direction-list-create"),
    path("scientific-direction/<str:lookup>/", ScientificDirectionDetailAPIView.as_view(), name="scientific-direction-detail"),
    
    # 🗂 Page Files
    path("page-files/", PageFileListCreateAPIView.as_view(), name="page-file-list-create"),
    path("page-files/<int:id>/", PageFileDetailAPIView.as_view(), name="page-file-detail"),
    
    # 🖼 Page Images
    path("page-images/", PageImageListCreateAPIView.as_view(), name="page-image-list-create"),
    path("page-images/<int:id>/", PageImageDetailAPIView.as_view(), name="page-image-detail"),
    
    # Employees
    path("employees/", EmployeeListCreateAPIView.as_view(), name="employee-list-create"),
    path("employees/<int:id>/", EmployeeDetailAPIView.as_view(), name="employee-detail")


]
