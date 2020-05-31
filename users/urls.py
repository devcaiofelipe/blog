from django.urls import path
from .views import user_register, user_login, user_index, user_logout, user_profile, user_update, user_delete, user_update_email, user_update_password

urlpatterns = [
    path('', user_index, name='user_index'),
    path('register/', user_register, name='user_register'),
    path('delete/<int:user_id>', user_delete, name='user_delete'),
    path('profile/<int:user_id>', user_profile, name='user_profile'),
    path('update/<int:user_id>', user_update, name='user_update'),
    path('update_email/<int:user_id>', user_update_email, name='user_update_email'),
    path('update_password/<int:user_id>', user_update_password, name='user_update_password'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
