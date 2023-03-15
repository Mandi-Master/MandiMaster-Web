from django.contrib import admin
from django.urls import path
from Home import views

admin.site.site_header = "Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Bug Tracker"

urlpatterns = [
    path("",views.index,name='home'),
    path("home/",views.index,name='home'),
    path("list_details/<str:id>",views.list_details,name='list_details'),
    path("create_list/",views.create_list,name='create_list'),
    path("create_topic/",views.create_topic,name='create_topic'),
    path("update_list/<room_id>",views.update_list,name='update_list'),
    path("delete_list/<room_id>",views.delete_list,name='delete_list'),
    path("delete_topic/<topic_id>",views.delete_topic,name='delete_topic'),
    path("delete_message/<str:id>",views.delete_message,name='delete_message'),
    path("signup/",views.signup_user,name='signup'),
    path("login/",views.login_user,name='login'),
    path("logout/",views.logout_user,name='logout'),
    path("my_profile/",views.my_profile,name='my_profile'),
    path("profile/<str:id>",views.user_profile,name='profile'),
    path("update_profile/",views.update_user_profile,name='update_profile'),
    path("update_user_password/",views.update_user_password,name='update_user_password'),

]

