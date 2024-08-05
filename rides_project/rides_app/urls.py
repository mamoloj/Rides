from django.urls import path, include
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RideEventViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ride-events', RideEventViewSet)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
