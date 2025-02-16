from django.urls import path
from user.views import MyObtainTokenPairView, RegisterView, Logout, get_groups_users
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', Logout.as_view(), name='auth_logout'),
    path('get_groups_user/', get_groups_users, name='get_groups_users'),
]
