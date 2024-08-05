from django.urls import path, include
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, UserViewSet, RideEventViewSet


router = DefaultRouter()
router.register(r'rides', RideViewSet)
router.register(r'users', UserViewSet)
router.register(r'ride-events', RideEventViewSet)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
