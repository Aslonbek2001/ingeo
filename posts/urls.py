from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import PostImageViewSet, PostManageViewSet

router = DefaultRouter()
# router.register(r"posts", PostViewSet, basename="post")
router.register(r"posts", PostManageViewSet, basename="posts")

# Nested router: posts/{post_id}/images
posts_router = NestedDefaultRouter(router, r"posts", lookup="post")
posts_router.register(r"images", PostImageViewSet, basename="post-images")


urlpatterns = router.urls + posts_router.urls
