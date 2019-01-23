from django.shortcuts import render, HttpResponse, redirect
from app01.models import *
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app01 import form



def test(requset):

    return render(requset, 'test.html')




from app01.tools.fen_ye import Pagination


def book(request):
    current_page = request.GET.get('page')  # 取哪一页
    all_book_list = Book.objects.all()
    page_obj = Pagination(current_page, all_book_list.count(), request)
    book_list = all_book_list[page_obj.start:page_obj.end]  # 取到该页面的book_list
    return render(request, 'book.html', locals())

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user_obj = auth.authenticate(username=username, password=pwd)

        if user_obj:
            #把权限注入session中
            # init_permission.init_permission(request,user_obj)

            auth.login(request, user_obj)

            print('登录成功')
            return redirect('/customers/')
        else:
            print('用户名或密码错误')
    return render(request, 'login.html')


def logout(request):  #注销
    auth.logout(request)   #django会清除session
    return redirect('/login/')


def reg(request):  # 注册功能
    res = {"user": None, "err_msg": ""}  #先定义一个空字典,如果验证成功,给user赋值,如果验证失败,给err_msg赋值,
    # 前端ajax通过判断user有没有值来判断是否注册成功
    if request.method == 'POST':
        form_obj = UserForm(request.POST)
        if form_obj.is_valid():
            res["user"] = form_obj.cleaned_data.get("user")  # 验证成功给res字典的user赋值,前端通过判断user有值表示新增成功
            user = form_obj.cleaned_data.get("user")  # 取出经过校验的数据,
            gender = form_obj.cleaned_data.get('gender')
            pwd = form_obj.cleaned_data.get("pwd")
            email = form_obj.cleaned_data.get("email")

            # 要用create_user,否则密码明文
            UserInfo.objects.create_user(username=user, password=pwd, email=email)  # 操作数据库,新增到UserInfo表中
            res['user'] = 'yes'

        else:
            res["err_msg"] = form_obj.errors  # 将form的errors赋值给res字典的err_msg
        print('resss', res)
        return JsonResponse(res)  # 字符串要用json格式返回

    else:
        form_obj = UserForm()
        return render(request, 'reg.html', {'form_obj': form_obj})


def class_record(request):
    return render(request, 'class_record.html')

class CustomersView(View):
    def get(self,request):
        if reverse('all_customers') == request.path:  # 所有客户
            # print('*********所有客户')
            all_customers = Customer.objects.all()

        elif reverse('my_customers') == request.path:  # 我的客户
            all_customers = Customer.objects.filter(consultant=request.user)
            # print('**********我的客户')

        else:  # 公户列表
            all_customers = Customer.objects.filter(consultant__isnull=True)
            # print('**********公户列表')


        current_page_num = request.GET.get('page', 1)

        # 处理模糊搜索
        serarch_condition = request.GET.get('search')  # 获取用户输入的搜索条件
        field = request.GET.get('field')   # 获取用户是按照什么搜索,按照姓名,qq还是手机号
        if serarch_condition:
            q = Q()
            q.children.append((field + '__contains', serarch_condition))
            all_customers = all_customers.filter(q)

        # 参数分别表示,显示哪一页,总页数,request,每页几条数据
        pagination = Pagination(current_page_num, all_customers.count(), request, 2)
        #
        # all_customers = all_customers[pagination.start:pagination.end]

        # 处理编辑后的返回路径
        path = request.path
        next = '?next=%s' % path
        return render(request, 'customers/customers.html', {'next':next,'all_customers': all_customers, 'pagination': pagination})

    def post(self,request):   # 处理批量处理
        func_name = request.POST.get('action') #获取select框选中的option的value值,根据这个value值知道要做什么操作
        #前端checkbox给相同的name,后台获取的name对应的value是一个列表
        selected_list = request.POST.getlist('selected_list')
        if not hasattr(self,func_name):  #如果没有这个函数
            return HttpResponse('没有此操作')
        else:
            func = getattr(self,func_name)  #func=batch_delete  ??不明白
            querySet = Customer.objects.filter(pk__in=selected_list)
            func(request,querySet)  # batch_delete(selected_list )


            return redirect(request.path)




    def batch_delete(self,request,querySet):
        querySet.update(sex='female')


    def changeTo_private(self,request,querySet): # 公户转私户:将销售设置为当前登录用户
        # 如果consultant为空才可以修改consultant为当前登录用户,如果不为空说明已经有销售人不可再操作

        querySet.update(consultant=request.user)


    def changeTo_public(self,request,querySet): #私户转公户
        querySet.update(consultant=None)




# class AddCustomerView(View):  #新增客户
#     def get(self,request):  # 新增页面
#         add_customer_obj = CustomerModelForm()
#         return render(request,'customers/add_customer.html',{'add_customer_obj':add_customer_obj})
#
#     def post(self,request):  # 处理新增
#         form_obj = CustomerModelForm(request.POST)
#         if form_obj.is_valid(): # 新增成功
#             form_obj.save()
#             return redirect(reverse('public_customers'))  #新增成功重定向到公户列表
#         else:   # 新增失败
#             return render(request, 'customers/add_customer.html', {'add_customer_obj': form_obj })
#
# class EditCustomersView(View): #处理编辑客户
#     def get(self,request,id):
#         edit_obj = Customer.objects.get(id=id)  #取到要编辑的对象
#         form_obj = CustomerModelForm(instance=edit_obj)
#         return render(request, 'customers/add_customer.html', {'add_customer_obj': form_obj})
#
#     def post(self,request,id):
#         edit_obj = Customer.objects.get(id=id) #取到要编辑的对象
#         form_obj = CustomerModelForm(request.POST,instance=edit_obj)
#
#         if form_obj.is_valid():  # 编辑成功
#             form_obj.save()
#             return redirect(request.GET.get('next'))  # 编辑成功后返回来源的地址
#
#         else:  # 编辑失败
#             return render(request, 'customers/add_customer.html', {'add_customer_obj': form_obj})

#将新增客户和编辑客户整合到一个视图类中
class AddAndEditCustomersView(View):
    def get(self,request,edit_id=None):
        #默认edit_id为None,如果是新增edit_id为空,edit_obj就为空,instance就为空,就是新增页面
        edit_obj = Customer.objects.filter(id=edit_id).first()  # 取到要编辑的对象
        form_obj = CustomerModelForm(instance=edit_obj)
        return render(request, 'customers/add_edit_customer.html', {'add_customer_obj': form_obj,'edit_obj':edit_obj})

    def post(self,request,edit_id=None):
        # 默认edit_id为None,如果是新增的提交edit_id为空,edit_obj就为空,instance就为空,就是新增的保存
        edit_obj = Customer.objects.filter(id=edit_id).first()  # 取到要编辑的对象
        form_obj = CustomerModelForm(request.POST,instance=edit_obj)

        if form_obj.is_valid():  # 编辑成功
            form_obj.save()
            return redirect(request.GET.get('next'))  # 编辑成功后返回来源的地址

        else:  # 编辑失败
            return render(request, 'customers/add_edit_customer.html', {'add_customer_obj': form_obj,'edit_obj':edit_obj})

class ConsultRecordView(View):
    def get(self,request):
        consult_record_list = ConsultRecord.objects.filter(consultant=request.user)  #只显示当前用户的客户

        customer_id = request.GET.get('customer_id')
        if customer_id:  # 如果有id,显示指定id的跟进记录
            consult_record_list = consult_record_list.filter(customer_id=customer_id) #注意,是customer_id=customer_id,显示这个客户所有的跟进记录
        return render(request,'customers/consult_record.html',{'consult_record_list':consult_record_list})


#将新增跟进记录和编辑跟进记录整合到一个视图类中
class AddAndEditConsultRecordView(View):
    def get(self,request,edit_id=None):
        #默认edit_id为None,如果是新增edit_id为空,edit_obj就为空,instance就为空,就是新增页面
        edit_obj = ConsultRecord.objects.filter(id=edit_id).first()  # 取到要编辑的对象
        form_obj = ConsultRecordModelForm(instance=edit_obj)
        return render(request, 'customers/add_edit_consult_record.html', {'add_customer_obj': form_obj,'edit_obj':edit_obj})

    def post(self,request,edit_id=None):
        # 默认edit_id为None,如果是新增的提交edit_id为空,edit_obj就为空,instance就为空,就是新增的保存
        edit_obj = ConsultRecord.objects.filter(id=edit_id).first()  # 取到要编辑的对象
        form_obj = ConsultRecordModelForm(request.POST,instance=edit_obj)

        if form_obj.is_valid():  # 编辑成功
            form_obj.save()
            return redirect('/consult_record/')  # 编辑成功后返回来源的地址

        else:  # 编辑失败
            return render(request, 'customers/add_edit_consult_record.html', {'add_customer_obj': form_obj,'edit_obj':edit_obj})


def study_record(request):
    return render(request, 'students/study_record.html')


def stuff_management(request):
    return render(request, 'stuff_management.html')


def class_study_record_list(request):
    class_record_list = ClassStudyRecord.objects.all()
    return render(request, 'students/class_study_record_list.html', locals())


def all_student_study_record_list(request):
    all_student_study_record_list = StudentStudyRecord.objects.all()

    return render(request, 'students/all_student_study_record_list.html', locals())


from app01.form import *


class RecordScoreView(View):
    msg = ''

    def get(self, request, cls_sud_record_id):  # 传来班级记录的id,用这个id取找这个班级的obj
        # 用传来的班级学习id取到这个班级学习obj
        cls_sud_record_obj = ClassStudyRecord.objects.get(id=cls_sud_record_id)
        score_choices = StudentStudyRecord.score_choices
        # 用这个obj取到他关联的所有学生学习记录.小写表名反查
        stu_sud_record_list = cls_sud_record_obj.studentstudyrecord_set.all()

        return render(request, 'students/record_score.html', locals())

    def post(self, request, class_study_record_id):
        '''
        传来的request.POST是:
       <QueryDict: {'csrfmiddlewaretoken': ['S99mCD5SIW1T0kJWnOZv8fuOck5sZMuBHEjlt7sxbnCqWO4UDbvG7W0QHL7QjYyd'], 
       'score__1': ['60'], 
       'homework_note__1': ['学生1的评语'], 
       'score__2': ['80'], 
       'homework_note__2': ['学生2的评语'], 
       'score__3': ['0'], 
       'homework_note__3': ['学生3的评语']}>
        
        要将上面的request.post构建成下面的字典:
        data_dict = {
        1:{score:76,home_note:123} }
        2:{score:76,home_note:123} }        '''

        data_dict = {}
        for key, val in request.POST.items():  # request.post 是一个字典,循环字典的items
            if key == "csrfmiddlewaretoken":  # 传来的字典里有csrf, 是csrf不用管开始下一次循环
                continue
            # 切割后, 左边是字段名, 右边是pk
            field, pk = key.split("__")  # name="homework_note__{{ studentstudyrecord.pk }}
            # 切割后field是score, pk是1,val是60
            pk = int(pk)
            if pk not in data_dict:  # 如果没有这个pk直接添加
                data_dict[pk] = {
                    field: val
                }
            else:  # 如果有这个pk,那么在这个key的value的字典里添加
                data_dict[pk][field] = val

        # pk=int(pk)

        for pk, data in data_dict.items():  # 处理字典,更新数据库
            StudentStudyRecord.objects.filter(pk=pk).update(**data)

        request.session['msg'] = '保存成功'

        return redirect(request.path)

        # return render(request, 'students/record_score.html', locals())
        # return render(request,,locals())


# 用formset实现批量保存
from django.forms.models import modelformset_factory


class StudentStudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = StudentStudyRecord  # 指定是哪张表的formset
        fields = ["score", "homework_note"]  # files里面的字段,就是formset保存的实时校验的字段


class RecordScoreView2(View):
    def get(self, request, class_study_record_id):
        # 实例化一个formset对象
        model_formset_cls = modelformset_factory(model=StudentStudyRecord, form=StudentStudyRecordModelForm, extra=0)
        # 取到关联这个班级记录的所有学生记录
        queryset = StudentStudyRecord.objects.filter(classstudyrecord=class_study_record_id)
        # 把取到的queryset传给formset对象,把forset对象传给前端
        formset = model_formset_cls(queryset=queryset)
        return render(request, "students/record_score.html", locals())

    def post(self, request, class_study_record_id):
        # 和get方法一样 实例化一个formset对象
        model_formset_cls = modelformset_factory(model=StudentStudyRecord, form=StudentStudyRecordModelForm, extra=0)
        # 和get方法一样 取到关联这个班级记录的所有学生记录
        queryset = StudentStudyRecord.objects.filter(classstudyrecord=class_study_record_id)

        # 把提交来的request.POST全部给formset对象
        formset = model_formset_cls(request.POST)
        if formset.is_valid():  # 校验formset对象, 校验的字段是filds中写的字段
            formset.save()  # 保存更新的formset对象
        return redirect(request.path)


from django.db.models import Count


class TongJiView(View):

    def today(self):
        import datetime
        today = datetime.datetime.now().date()  # 取到今天的年月日

        all_customer_list = Customer.objects.filter(deal_date=today)  # 今天所有的成交量

        # 查询每一个销售的名字以及今天对应的成单量, 查询部门id是4销售部 的用户名和他们的成交的记录数
        tongji_queryset = UserInfo.objects.filter(depart_id=4, customers__deal_date=today).annotate(
            c=Count("customers")).values_list("username", "c")

        # 把查询出来的queryst,先list强转成列表套元组, 在变成列表套列表,因为柱状图接收的格式是列表套列表

        tongji_list = [[item[0], item[1]] for item in list(tongji_queryset)]

        return {"all_customer_list": all_customer_list, "tongji_list": list(tongji_list)}

    def zuotian(self):
        import datetime
        zuotian = datetime.datetime.now().date() - datetime.timedelta(days=1)  # 取到昨天的日期
        customer_list = Customer.objects.filter(deal_date=zuotian)  # 取到queryset

        # 查询每一个销售的名字以及昨天对应的成单量
        ret = UserInfo.objects.filter(depart_id=2, customers__deal_date=zuotian).annotate(
            c=Count("customers")).values_list("username", "c")

        ret = [[item[0], item[1]] for item in list(ret)]

        return {"customer_list": customer_list, "ret": list(ret)}

    def week(self):
        import datetime
        today = datetime.datetime.now().date()
        weekdelta = datetime.datetime.now().date() - datetime.timedelta(weeks=1)
        customer_list = Customer.objects.filter(deal_date__gte=weekdelta, deal_date__lte=today)

        # 查询每一个销售的名字以及昨天对应的成单量
        ret = UserInfo.objects.filter(depart_id=2, customers__deal_date__gte=weekdelta,
                                      customers__deal_date__lte=today).annotate(
            c=Count("customers")).values_list("username", "c")

        ret = [[item[0], item[1]] for item in list(ret)]

        return {"customer_list": customer_list, "ret": list(ret)}

    def recent_month(self):
        import datetime
        today = datetime.datetime.now().date()
        weekdelta = datetime.datetime.now().date() - datetime.timedelta(weeks=4)
        customer_list = Customer.objects.filter(deal_date__gte=weekdelta, deal_date__lte=today)

        # 查询每一个销售的名字以及昨天对应的成单量
        ret = UserInfo.objects.filter(depart_id=2, customers__deal_date__gte=weekdelta,
                                      customers__deal_date__lte=today).annotate(
            c=Count("customers")).values_list("username", "c")

        ret = [[item[0], item[1]] for item in list(ret)]

        return {"customer_list": customer_list, "ret": list(ret)}

    def get(self, request):
        date = request.GET.get("date", "today")  # 获取data的参数,如果没有获取到默认显示今天

        if hasattr(self, date):
            ret = getattr(self, date)()  # 如果data=today, 反射执行的是self.today()
            # self.today()执行返回的是{"all_customer_list":all_customer_list,"tongji_list":list(tongji_list)}

        return render(request, "students/tongji.html", ret)

    def post(self): pass


from django import forms


class BookForm(forms.Form):
    title = forms.CharField(max_length=16)
    price = forms.IntegerField()
    emil = forms.EmailField()
