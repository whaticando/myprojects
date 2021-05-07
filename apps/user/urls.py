from django.conf.urls import url
from django.urls import path

from .views import Login_view, get_valid_img,index,profile_view,\
    logout_view,change_profile_view,register_view,change_pwd_view,change_email_view

urlpatterns = [

    url(r'^login/$', Login_view.as_view(), name='login'),
    url(r'^index/$', index, name='index'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^register/$', register_view, name='register'),
    url(r'^profile/$', profile_view, name='profile'),
    # path('profile/',profile_view,name='profile'),
    url(r'^profile/change/$', change_profile_view, name='change_profile'),
    url(r'^get_valid_img/$', get_valid_img, name='get_valid_img'),
    # url(r'^user_register/$',User_Register.as_view(),name='user_register'),
    url(r'^change_pwd/$',change_pwd_view,name='change_pwd'),
    url(r'^change_email/$',change_email_view,name='change_email'),


]