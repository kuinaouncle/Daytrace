from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import re, json
from daytraceuser.models import UserInfo, PlanInfo, PlanRemindInfo, MemoryDayInfo, StatisticsInfo, MessagesInfo, FriendsInfo
from datetime import datetime, date, timedelta
# Create your views here.


# -----------功能函数部分--------------
# 检测用户名有没有被注册过
def username_registerd(username):
    if UserInfo.objects.filter(name=username).count() > 0:
        return True
    else:
        return False


# 把负数变成0
def negativeint_to_zero(i):
    if i < 0:
        return 0
    else:
        return i


# ----------------视图函数部分-------------
# /register/
def register(request):
    return render(request, 'register.html', {'code': 'fail'})


# /register_handle/
def register_handle(request):

    # 获取POST数据
    post = request.POST
    username = post.get('usname')
    email = post.get('mail')
    password = post.get('pwd')
    confirm_password = post.get('pwdc')

    # 校验获取的数据
    if not all([username, email, password, confirm_password]):
        return render(request, 'register.html', {'errmsg': '上面信息还没填写完整哦', 'code': 'fail'})

    if username_registerd(username):
        return render(request, 'register.html', {'errmsg': '用户名已经注册过了哦', 'code': 'fail'})

    if len(username) >= 20:
        return render(request, 'register.html', {'errmsg': '用户名的长度必须小于20', 'code': 'fail'})

    if not re.match(r'^\w{6,16}$', password):
        return render(request, 'register.html', {'errmsg': '密码必须由6-16位数字、字母和下划线组成', 'code': 'fail'})

    if not password == confirm_password:
        return render(request, 'register.html', {'errmsg': '两次密码不一样哦', 'code': 'fail'})

    if not re.match(r'^([\w_\-]+)@([\w\-]+[.]?)*[\w]+\.[a-zA-Z]{2,10}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱地址格式不正确哦', 'code': 'fail'})

    # 添加用户记录
    user = UserInfo()
    user.name = username
    user.password = password
    user.email = email
    user.save()

    # 添加用户数据
    statistics = StatisticsInfo()
    statistics.planamount = 0
    statistics.friends_amount = 0
    statistics.compamount = 0
    statistics.friends_plan_amount = 0
    statistics.message_amount = 0
    statistics.which_user = user
    statistics.save()

    # 返回应答
    return render(request, 'register.html', {'code': 'success'})


# /index/
def index(request):
    return render(request, 'index.html')


def login_ajax_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username_registerd(username):
        return JsonResponse({'res': 0, 'username': username, 'password': password})
    elif UserInfo.objects.get(name=username).password == password:
        response = JsonResponse({'res': 1, 'username': username, 'password': password})
        response.set_cookie('username', json.dumps(username))
        return response
    else:
        return JsonResponse({'res': 2, 'username': username, 'password': password})


# /user/
def user(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userstat = u.statisticsinfo_set.all()[0]
    userplan = u.planinfo_set.all()
    userfnd = u.friendsinfo_set.all()

    if u.messagesinfo_set.filter(is_read=False).exists():
        usermsg = u.messagesinfo_set.filter(is_read=False)[0]
    else:
        usermsg = u.messagesinfo_set.filter(is_read=False)

    userplantoday = userplan.filter(startdate=date.today()).filter(is_delete=False).order_by("startdatetime")[0:4]
    if userplan.filter(is_remind=True).filter(is_delete=False).exists():
        userplanremind = userplan.filter(is_remind=True).filter(is_delete=False).order_by("startdatetime")[0]
    else:
        userplanremind = u.messagesinfo_set.filter(is_read=False)

    useranni = u.memorydayinfo_set.all().order_by("anniversary_date")[0:4]
    useranniexists = u.memorydayinfo_set.all().exists()
    userplantodayexists = userplan.filter(startdate=date.today()).filter(is_delete=False).exists()
    return render(request, 'user.html', {
        'nameofuser': nameofuser,
        'userstat': userstat,
        'userplantoday': userplantoday,
        'userplanremind': userplanremind,
        'userplantodayexists': userplantodayexists,
        'useranni': useranni,
        'useranniexists': useranniexists,
        'usermsg': usermsg,
        'userfnd': userfnd,
    })


# /user/addplan
def addplan(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    return render(request, 'addplan.html', {'nameofuser': nameofuser, 'issuccessful': 'false'})


# /user/addplan/addplan_check
def addplan_check(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    plantitle = request.POST.get('plantitle')
    description = request.POST.get('description')
    priority = request.POST.get('priority')
    plantypeselect = request.POST.get('plantypeselect')

    # 添加日程信息
    u = UserInfo.objects.get(name=nameofuser)
    plan = PlanInfo()
    plan.title = plantitle
    plan.content = description
    plan.priority = int(priority)
    plan.which_user = u
    if request.POST.get('isremindcheckbox'):
        plan.is_remind = True
    if request.POST.get('isshowtofriendscheckbox'):
        plan.is_show_to_friends = True

    userstat = u.statisticsinfo_set.all()[0]
    userstat.planamount += 1
    userstat.save()

    # 添加日程时间信息
    if plantypeselect == 'day':
        plan.plantype = 0
        dateofdateplan = request.POST.get('dateofdateplan')
        timeofdateplan = request.POST.get('timeofdateplan')
        dayyear = int(dateofdateplan[0:4])
        daymonth = int(dateofdateplan[5:7])
        daydate = int(dateofdateplan[8:])
        plan.startdate = date(dayyear, daymonth, daydate)
        if timeofdateplan != '':
            dayhour = int(timeofdateplan[0:2])
            dayminute = int(timeofdateplan[3:5])
            plan.startdatetime = datetime(dayyear, daymonth, daydate, dayhour, dayminute, 0, 0)

    if plantypeselect == 'week':
        plan.plantype = 1
        weekofweekplan = request.POST.get('weekofweekplan')
        weekyear = int(weekofweekplan[0:4])
        weekweek = int(weekofweekplan[6:])
        plan.startdate = date(2018, 1, 1)+timedelta(days=((weekyear-2018)*365+(weekweek-1)*7))   # 有bug

    if plantypeselect == 'month':
        plan.plantype = 2
        monthofmonthplan = request.POST.get('monthofmonthplan')
        monthyear = int(monthofmonthplan[0:4])
        monthmonth = int(monthofmonthplan[5:])
        plan.startdate = date(monthyear, monthmonth, 1)

    if plantypeselect == 'custom':
        plan.plantype = 3
        customdateselect = request.POST.get('customdateselect')
        startmonth = int(customdateselect[0:2])
        startday = int(customdateselect[3:5])                       # 有Bug
        startyear = int(customdateselect[6:8])+2000
        endmonth = int(customdateselect[11:13])
        endday = int(customdateselect[14:16])
        endyear = int(customdateselect[17:19])+2000
        plan.startdate = date(startyear, startmonth, startday)
        plan.enddate = date(endyear, endmonth, endday)

    plan.save()

    # 如果勾选了提醒，添加日程提醒信息
    if request.POST.get('isremindcheckbox'):

        isremindcheckbox = request.POST.get('isremindcheckbox')
        timeofremind = request.POST.get('timeofremind')
        planremind = PlanRemindInfo()
        planremind.is_remind = True
        remindyear = int(timeofremind[0:4])
        remindmonth = int(timeofremind[5:7])
        remindday = int(timeofremind[8:10])
        remindhour = int(timeofremind[11:13])
        remindminute = int(timeofremind[14:16])
        planremind.remind_datetime = datetime(remindyear, remindmonth, remindday, remindhour, remindminute, 0, 0)
        planremind.remind_from = nameofuser
        planremind.which_plan = plan
        planremind.save()

    return render(request, 'addplan.html', {'nameofuser': nameofuser, 'issuccessful': 'true'})


# /user/addanniversary
def addanniversary(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    return render(request, 'addanniversary.html', {'nameofuser': nameofuser, 'issuccessful': 'false'})


# /user/addanniversary/addanni_check/
def addanni_check(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    anni_title = request.POST.get('anni_title')
    description = request.POST.get('description')
    anni_date = request.POST.get('anni_date')
    anni_remind_time = request.POST.get('anni_remind_time')

    u = UserInfo.objects.get(name=nameofuser)
    # 添加纪念日信息
    memoryday = MemoryDayInfo()
    memoryday.title = anni_title
    memoryday.content = description
    dayyear = int(anni_date[0:4])
    daymonth = int(anni_date[5:7])
    daydate = int(anni_date[8:])
    memoryday.anniversary_date = date(dayyear, daymonth, daydate)
    memoryday.during = negativeint_to_zero((date(dayyear, daymonth, daydate)-date.today()).days)
    memoryday.which_user = u

    if request.POST.get('anni_isremind'):
        memoryday.is_remind = True
        remindyear = int(anni_remind_time[0:4])
        remindmonth = int(anni_remind_time[5:7])
        remindday = int(anni_remind_time[8:10])
        remindhour = int(anni_remind_time[11:13])
        remindminute = int(anni_remind_time[14:16])
        memoryday.remind_datetime = datetime(remindyear, remindmonth, remindday, remindhour, remindminute, 0, 0)

    memoryday.save()

    return render(request, 'addanniversary.html', {'nameofuser': nameofuser, 'issuccessful': 'true'})


# /user/recover/
def recover(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    deletedplan = userplan.filter(is_delete=True)
    count = userplan.filter(is_delete=True).count()
    return render(request, 'recover.html', {'nameofuser': nameofuser, 'deletedplan': deletedplan, 'count': count})


# /user/recycle/
def recycle(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    planid = int(request.POST.get('planid'))
    p = PlanInfo.objects.get(id=planid)
    p.is_delete = False
    p.save()
    u = UserInfo.objects.get(name=nameofuser)
    userstat = u.statisticsinfo_set.all()[0]
    userstat.planamount += 1
    userstat.save()
    return JsonResponse({'res': 'OK'})


# /user/del_in_user/
def del_in_user(request):
    deltg = request.POST.get('deletetarget')
    nameofuser = json.loads(request.COOKIES.get('username'))
    planid = int(deltg[4:])
    p = PlanInfo.objects.get(id=planid)
    p.is_delete = True
    p.save()
    u = UserInfo.objects.get(name=nameofuser)
    userstat = u.statisticsinfo_set.all()[0]
    userstat.planamount -= 1
    userstat.save()
    return JsonResponse({'res': 'OK'})


# /user/modify_in_user/
def modify_in_user(request):
    deltg = request.POST.get('deletetarget')
    nameofuser = json.loads(request.COOKIES.get('username'))
    planid = int(deltg[4:])
    p = PlanInfo.objects.get(id=planid)
    return render(request, 'changeplan.html', {'nameofuser': nameofuser, 'plan': p})


# /user/changeplan/
def changeplan(request):
    target = request.GET.get('target')
    nameofuser = json.loads(request.COOKIES.get('username'))
    planid = int(target[4:])
    p = PlanInfo.objects.get(id=planid)
    return render(request, 'changeplan.html', {'nameofuser': nameofuser, 'plan': p})


# /user/map_today/
def map_today(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplantoday = userplan.filter(startdate=date.today()).filter(is_delete=False).order_by("startdatetime")
    userplanp0 = userplantoday.filter(priority=0)
    userplanp1 = userplantoday.filter(priority=1)
    userplanp2 = userplantoday.filter(priority=2)
    userplanp3 = userplantoday.filter(priority=3)
    userplanp0exists = userplanp0.exists()
    userplanp1exists = userplanp1.exists()
    userplanp2exists = userplanp2.exists()
    userplanp3exists = userplanp3.exists()
    return render(request, 'map_today.html', {
        'nameofuser': nameofuser,
        'userplanp0': userplanp0,
        'userplanp1': userplanp1,
        'userplanp2': userplanp2,
        'userplanp3': userplanp3,
        'userplanp0exists': userplanp0exists,
        'userplanp1exists': userplanp1exists,
        'userplanp2exists': userplanp2exists,
        'userplanp3exists': userplanp3exists,
    })


# /user/map_thisweek/
def map_thisweek(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplanthisweek = userplan.filter(startdate__gte=date.today()).filter(startdate__lt=date.today()+timedelta(days=7)).filter(is_delete=False).order_by('startdate')
    userplanp0 = userplanthisweek.filter(priority=0)
    userplanp1 = userplanthisweek.filter(priority=1)
    userplanp2 = userplanthisweek.filter(priority=2)
    userplanp3 = userplanthisweek.filter(priority=3)
    return render(request, 'map_thisweek.html', {
        'nameofuser': nameofuser,
        'userplanp0': userplanp0,
        'userplanp1': userplanp1,
        'userplanp2': userplanp2,
        'userplanp3': userplanp3,
    })


# /user/map_thismonth/
def map_thismonth(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplanthismonth = userplan.filter(startdate__gte=date.today()).filter(
        startdate__lt=date.today() + timedelta(days=31)).filter(is_delete=False).order_by('startdate')
    userplanp0 = userplanthismonth.filter(priority=0)
    userplanp1 = userplanthismonth.filter(priority=1)
    userplanp2 = userplanthismonth.filter(priority=2)
    userplanp3 = userplanthismonth.filter(priority=3)
    return render(request, 'map_thismonth.html', {
        'nameofuser': nameofuser,
        'userplanp0': userplanp0,
        'userplanp1': userplanp1,
        'userplanp2': userplanp2,
        'userplanp3': userplanp3,
    })


# /user/timeline_date/
def timeline_date(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplandate = userplan.filter(plantype=0).order_by("startdatetime")
    return render(request, 'timeline_date.html', {
        'nameofuser': nameofuser,
        'userplandate': userplandate,
    })


# /user/timeline_week/
def timeline_week(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplandate = userplan.filter(plantype=1).order_by("startdate")
    return render(request, 'timeline_week.html', {
        'nameofuser': nameofuser,
        'userplandate': userplandate,
    })


# /user/timeline_month/
def timeline_month(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    userplandate = userplan.filter(plantype=2).order_by("startdate")
    return render(request, 'timeline_month.html', {
        'nameofuser': nameofuser,
        'userplandate': userplandate,
    })


# /user/settings/
def settings(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    return render(request, 'settings.html', {
        'nameofuser': nameofuser,
    })


# /user/calendar/
def calendar(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    u = UserInfo.objects.get(name=nameofuser)
    userplan = u.planinfo_set.all()
    return render(request, 'calendartest.html', {
        'nameofuser': nameofuser,
        'userplan': userplan,
    })


# /user/add_friend_check/
def add_friend_check(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    friendname = request.POST.get('friendname')

    if not UserInfo.objects.filter(name=friendname).exists():
        return JsonResponse({'res': 0, 'nameofuser': nameofuser})
    elif username_registerd(friendname):
        frienduser = UserInfo.objects.get(name=friendname)
        message = MessagesInfo()
        message.messagefrom = nameofuser
        message.messagecontent = nameofuser+' '+'请求添加你为好友'
        message.which_user = frienduser
        message.save()
        return JsonResponse({'res': 1, 'nameofuser': nameofuser})


# /user/add_friend/
def add_friend(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    friendname = request.POST.get('friendname')
    u = UserInfo.objects.get(name=nameofuser)
    f = UserInfo.objects.get(name=friendname)
    # 双方好友列表添加
    uf = FriendsInfo()
    uf.friendname = friendname
    uf.which_user = u
    uf.save()
    ff = FriendsInfo()
    ff.friendname = nameofuser
    ff.which_user = f
    ff.save()
    # 好友数据添加
    ustat = u.statisticsinfo_set.all()[0]
    fstat = f.statisticsinfo_set.all()[0]
    ustat.friends_amount += 1
    ustat.save()
    fstat.friends_amount += 1
    fstat.save()
    return JsonResponse({'res': 1, 'nameofuser': nameofuser})


# /user/friendplan/
def friendplan(request):
    nameofuser = json.loads(request.COOKIES.get('username'))
    friendname = request.GET.get('target')
    u = UserInfo.objects.get(name=friendname)
    userplan = u.planinfo_set.all()
    userplanthismonth = userplan.filter(startdate__gte=date.today()).filter(
        startdate__lt=date.today() + timedelta(days=31)).order_by('startdate')
    userplanp0 = userplanthismonth.filter(priority=0)
    userplanp1 = userplanthismonth.filter(priority=1)
    userplanp2 = userplanthismonth.filter(priority=2)
    userplanp3 = userplanthismonth.filter(priority=3)
    return render(request, 'map_friend.html', {
        'nameofuser': friendname,
        'userplanp0': userplanp0,
        'userplanp1': userplanp1,
        'userplanp2': userplanp2,
        'userplanp3': userplanp3,
    })

