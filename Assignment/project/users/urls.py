from django.urls import path
from .views import CustomUserCreate, LoginView, UserView,  GetUserById
app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('create/<int:user_id>/', GetUserById.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name="login_user"),
    path('user/', UserView.as_view(), name="user"),

]
