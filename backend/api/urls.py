from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignupView, UserView, JobSeekerViewSet, EmployerViewSet, Logoutview


# Router setup for ViewSets
router = DefaultRouter()
router.register(r'jobseekers', JobSeekerViewSet)
router.register(r'employers', EmployerViewSet)


urlpatterns = [
    # Auth endpoints
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jobs/', include('jobapp.urls')),


    # ViewSets
    path('', include(router.urls)),
]
