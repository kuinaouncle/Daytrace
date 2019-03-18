from django.contrib import admin
from daytraceuser.models import UserInfo, FriendsInfo, MemoryDayInfo, PlanCommentInfo, PlanInfo, PlanRemindInfo
from daytraceuser.models import StatisticsInfo, MessagesInfo
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'email']


class PlanInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'plantype', 'priority']


class FriendsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'friendname']


class StatisticsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'which_user', 'planamount', 'compamount']


class MemoryDayInfoAdmin(admin.ModelAdmin):
    list_display = ['which_user', 'anniversary_date', 'title', 'is_remind']


class PlanRemindInfoAdmin(admin.ModelAdmin):
    list_display = ['which_plan', 'is_remind', 'remind_from', 'remind_datetime']


class PlanCommentInfoAdmin(admin.ModelAdmin):
    list_display = ['which_plan', 'comment_from', 'comment_to', 'comment_time']


class MessagesInfoAdmin(admin.ModelAdmin):
    list_display = ['which_user', 'messagefrom', 'is_read']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PlanInfo, PlanInfoAdmin)
admin.site.register(FriendsInfo, FriendsInfoAdmin)
admin.site.register(StatisticsInfo, StatisticsInfoAdmin)
admin.site.register(MemoryDayInfo, MemoryDayInfoAdmin)
admin.site.register(PlanRemindInfo, PlanRemindInfoAdmin)
admin.site.register(PlanCommentInfo, PlanCommentInfoAdmin)
admin.site.register(MessagesInfo, MessagesInfoAdmin)

