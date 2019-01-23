from django.contrib import admin

# Register your models here.
from app01.models import *


class CustomerConfig(admin.ModelAdmin):
    #显示哪个字段
    list_display = ['name','qq','sex','phone','consultant'] #consultant是fk字段，m2m字段不能放因为结果有多个不知道要显示哪一个，如果要放，需要自定义

    #默认超链接是第一个字段，指定qq，和name 为超链接进入编辑页
    list_display_links = ['name','qq']

    #分类搜索  一般放fk 或m2m,点consultant搜索和consultant有关的
    list_filter = ['consultant']

    #搜索框 模糊搜索 title 或 name
    search_fields = ['qq','name']


    #批量操作
    def patch_set_zero(self,request,queryset):
        queryset.update(phone=0)

    patch_set_zero.short_description = '将手机号重置为0' #设置下拉框显示的中文
    actions = [patch_set_zero] #将函数名放在列表里




admin.site.register(UserInfo)
admin.site.register(Department)
admin.site.register(Customer,CustomerConfig)
admin.site.register(Campuses)
admin.site.register(ClassList)

admin.site.register(ConsultRecord)
admin.site.register(Enrollment)
admin.site.register(PaymentRecord)
admin.site.register(Student)
admin.site.register(ClassStudyRecord)
admin.site.register(StudentStudyRecord)
