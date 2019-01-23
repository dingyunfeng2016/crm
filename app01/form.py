from django.forms import widgets

from app01.models import UserInfo, Customer
from django.core.exceptions import ValidationError
import re
from django import forms
from app01.models import *

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values(): # 初始化的时候就给每个字段都加上form-control样式,就不用给每个字段加widget单独加

            from multiselectfield.forms.fields import MultiSelectFormField
            # 如果是MultiSelectFormField不加form-control,加了form-control会变形
            if isinstance(filed,MultiSelectFormField):
                pass
            else:
                filed.widget.attrs.update({'class': 'form-control'})

class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model=ConsultRecord
        exclude= ('delete_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values(): # 初始化的时候就给每个字段都加上form-control样式,就不用给每个字段加widget单独加
            filed.widget.attrs.update({'class': 'form-control'})





class UserForm(forms.Form):
    user = forms.CharField(min_length=2, label="用户名")
    gender = forms.ChoiceField(choices=((1,'男'),(2,'女')),label='性别',required=False)
    pwd = forms.CharField(min_length=2, widget=widgets.PasswordInput(), label="密码")
    r_pwd = forms.CharField(min_length=2, widget=widgets.PasswordInput(), label="确认密码")
    email = forms.EmailField(min_length=5, label="邮箱")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            # 初始化的时候就给每个字段都加上form-control样式,就不用给每个字段加widget单独加
            filed.widget.attrs.update({'class': 'form-control'})

    def clean_user(self):  #判断用户名是否已存在的钩子
        val = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("用户已存在！")
        else:
            return val

    def clean_pwd(self):  #判断密码不能是纯数字的钩子
        val = self.cleaned_data.get("pwd")
        if val.isdigit():
            raise ValidationError("密码不能是纯数字！")
        else:
            return val

    def clean_email(self):  #判断邮箱必须163邮箱的钩子
        val = self.cleaned_data.get("email")
        if re.search("\w+@163.com$", val):
            return val
        else:
            raise ValidationError("邮箱必须是163邮箱！")

    def clean(self):   #判断2次密码是否一致
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")

        if pwd and r_pwd and r_pwd != pwd:
            self.add_error("r_pwd", ValidationError("两次密码不一致！"))
        else:
            return self.cleaned_data

class TestModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo  #取自哪张表
        # fields = '__all__'  显示UserInfo表中所有字段
        # fields = ['username','gender','last_login']   #显示指定字段
        exclude= ['password'] # 去除哪些字段
        labels = {"title":'书籍','price':'价格'}  #批量设置字段的label

        error_messages = {     #批量设置报错信息
            'title':{'rquired':'书籍不能为空'}   #设置title的不能为空的提示 默认是this field is required
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for filed in self.fields.values():
                # 初始化的时候就给每个字段都加上form-control样式,就不用给每个字段加widget单独加
                filed.widget.attrs.update({'class': 'form-control'})