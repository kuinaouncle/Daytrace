from django.db import models
from db.base_model import BaseModel


# 用户类表

class UserInfo(BaseModel):  # 日迹用户信息表

    GENDER_CHOICES = (
        (0, '男'),
        (1, '女'),
    )

    name = models.CharField(max_length=20)
    password = models.CharField(max_length=16)
    email = models.EmailField()
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0)
    theme_color = models.SmallIntegerField(default=0)
    is_show = models.BooleanField(default=True)  # 是否显示给其他用户
    is_receive = models.BooleanField(default=True)  # 是否接受别人的消息

    class Meta:
        db_table = 'user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class FriendsInfo(BaseModel):  # 用户好友信息表

    friendname = models.CharField(max_length=20)
    is_receive = models.BooleanField(default=True)  # 是否接受别人的消息
    is_showplan = models.BooleanField(default=True)  # 是否向好友展示自己的日程
    which_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # 关联用户

    class Meta:
        db_table = 'friends'
        verbose_name = '用户好友信息'
        verbose_name_plural = verbose_name


class StatisticsInfo(BaseModel):  # 用户数据

    planamount = models.PositiveIntegerField()  # 日程总数
    compamount = models.PositiveIntegerField()  # 完成的日程总数
    message_amount = models.PositiveIntegerField()  # 未读消息数
    friends_amount = models.PositiveIntegerField()  # 好友总数
    friends_plan_amount = models.PositiveIntegerField()  # 好友添加的日程总数
    which_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # 关联用户

    class Meta:
        db_table = 'statistics'
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name


class MessagesInfo(BaseModel):  # 用户接收的消息数据

    messagefrom = models.CharField(max_length=20)  # 来自谁的消息
    messagecontent = models.CharField(max_length=255)  # 消息内容
    is_read = models.BooleanField(default=False)  # 消息是否被阅读
    is_added = models.BooleanField(default=False)  # 好友请求、日程等是否被接受（添加）
    receive_datetime = models.DateTimeField(auto_now_add=True)  # 收到消息的时间
    which_user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)  # 关联用户

    class Meta:
        db_table = 'messages'
        verbose_name = '用户接受消息'
        verbose_name_plural = verbose_name


# 日程类表

class PlanInfo(BaseModel):  # 日程信息

    PRIORITY_CHOICES = (
        (0, '很重要很紧急'),
        (1, '很重要不紧急'),
        (2, '不重要很紧急'),
        (3, '不重要不紧急'),
    )
    PLANTYPE_CHOICES = (
        (0, '日计划'),
        (1, '周计划'),
        (2, '月计划'),
        (3, '自定义计划'),
    )

    title = models.CharField(max_length=80)
    content = models.TextField(default='')
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=3)  # 选择时间象限法则
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    during = models.PositiveIntegerField(null=True, blank=True)
    startdatetime = models.DateTimeField(null=True, blank=True)
    plantype = models.PositiveSmallIntegerField(choices=PLANTYPE_CHOICES, default=0)  # 选择计划模式
    color = models.SmallIntegerField(default=0)  # 用户自行选择颜色加以区分
    is_show_to_friends = models.BooleanField(default=False)  # 是否向用户的好友展示
    is_remind = models.BooleanField(default=False)  # 是否提醒
    is_complicated = models.BooleanField(default=False)  # 是否完成
    comp_datetime = models.DateTimeField(null=True, blank=True)  # 完成时间
    comment = models.TextField(default='')  # 对完成的评价
    which_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # 关联用户

    class Meta:
        db_table = 'plan'
        verbose_name = '日程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '普通计划--' + self.title


class PlanRemindInfo(BaseModel):  # 日程提醒类信息

    is_remind = models.BooleanField(default=False)  # 是否提醒
    remind_datetime = models.DateTimeField()
    remind_from = models.CharField(max_length=20)  # 谁提醒用户
    which_plan = models.ForeignKey('PlanInfo', on_delete=models.CASCADE)  # 关联日程

    class Meta:
        db_table = 'planremind'
        verbose_name = '日程提醒数据'
        verbose_name_plural = verbose_name


class PlanCommentInfo(BaseModel):  # 日程评论信息

    comment_from = models.CharField(max_length=20)  # 谁给的评论
    comment_to = models.CharField(max_length=20)    # 评论谁
    content = models.CharField(max_length=255)                    # 评论内容
    comment_time = models.DateTimeField(null=True, blank=True)           # 评论时间
    which_plan = models.ForeignKey('PlanInfo', on_delete=models.CASCADE)  # 关联日程

    class Meta:
        db_table = 'plancomment'
        verbose_name = '日程评论数据'
        verbose_name_plural = verbose_name


class MemoryDayInfo(BaseModel):  # 纪念日

    anniversary_date = models.DateField()           # 纪念日时间
    during = models.PositiveIntegerField(default=0)  # 还有多少天
    title = models.CharField(max_length=80)         # 标题
    content = models.TextField(default='')          # 内容
    is_remind = models.BooleanField(default=False)  # 是否开启提醒
    remind_datetime = models.DateTimeField(null=True, blank=True)        # 提醒时间
    which_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # 关联用户

    class Meta:
        db_table = 'memoryday'
        verbose_name = '纪念日数据'
        verbose_name_plural = verbose_name
