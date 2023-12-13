from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import UsersView


urlpatterns = [
    path('', UsersView.as_view()),
    path('login/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
]
