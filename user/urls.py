from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import MyObtainTokenPairView, SignUpView

urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', SignUpView.as_view(), name='signup')
]