
from django.urls import path, include
from daytraceuser import views


urlpatterns = [
    path('', views.user, name='user'),
    path('addplan/', views.addplan, name='addplan'),
    path('addplan/addplan_check/', views.addplan_check, name='addplancheck'),
    path('addanniversary/', views.addanniversary, name='addanniversary'),
    path('addanniversary/addanni_check/', views.addanni_check, name='addanni_check'),
    path('map_today/', views.map_today, name='map_today'),
    path('map_thisweek/', views.map_thisweek, name='map_thisweek'),
    path('map_thismonth/', views.map_thismonth, name='map_thismonth'),
    path('timeline_date/', views.timeline_date, name='timeline_date'),
    path('timeline_week/', views.timeline_week, name='timeline_week'),
    path('timeline_month/', views.timeline_month, name='timeline_month'),
    path('del_in_user/', views.del_in_user, name='del_in_user'),
    path('modify_in_user/', views.modify_in_user, name='modify_in_user'),
    path('changeplan/', views.changeplan, name='changeplan'),
    path('recover/', views.recover, name='recover'),
    path('recycle/', views.recycle, name='recycle'),
    path('settings/', views.settings, name='settings'),
    path('calendar/', views.calendar, name='calendar'),
    path('add_friend_check/', views.add_friend_check, name='add_friend_check'),
    path('friendplan/', views.friendplan, name='friendplan'),
    path('add_friend/', views.add_friend, name='add_friend'),
]
