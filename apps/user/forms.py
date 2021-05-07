import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Ouser
from django.forms import widgets


class UserForm(forms.Form):
    user = forms.CharField(min_length=5, max_length=32,
                               error_messages={
                                   "required": "用户不能为空",
                                   "min_length": "最短长度为5",
                                   "max_length": "最长长度为12"
                               },
                               widget=widgets.TextInput(attrs={ "class": "form-control","placeholder": "用户名"}),
                               )
    pwd = forms.CharField(min_length=5, max_length=32,

                               error_messages={
                                   "required": "密码不能为空",
                                   "min_length": "密码长度太短，至少8位",
                                   "max_length": "最长长度为16"
                               },
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "密码"}),
                               )
    re_pwd = forms.CharField(max_length=32,

                             error_messages={
                                 "required": "确认密码不能为空",
                                 "min_length": "最短长度为5",
                             },
                             widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "确认密码"}),
                             )
    email = forms.EmailField(max_length=32, label="邮箱",
                             error_messages={
                                 'required':'邮箱不能为空','invalid': "邮箱格式错误"
                             },
                             widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "邮箱"}),
                             )
    # tel = forms.CharField(max_length=32,
    #                       label="电话",
    #                       error_messages={
    #                           "required": "不能为空",
    #                       }, )

    def clean_user(self):
        val = self.cleaned_data.get("user")
        if not Ouser.objects.filter(username=val):
            return val
        else:
            raise ValidationError("用户名已存在！")

    def clean_email(self):
        val = self.cleaned_data.get('email')
        email = Ouser.objects.filter(email=val)
        if email:
            raise ValidationError('该邮箱已经注册')
        else:
            return val

    # def clean_tel(self):
    #     val = self.cleaned_data.get('tel')
    #     ret = re.search(r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$", val)
    #     if ret:
    #         return val
    #     else:
    #         raise ValidationError('手机号格式错误')

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('repeat_pwd')

        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码输入不一致')

        else:
            return self.cleaned_data





class PasswordForm(forms.Form):
    """
    更改密码单独校验
    """
    pwd = forms.CharField(max_length=32,
                          min_length=8,
                          label="密码:",
                          error_messages={'required': '密码不能为空', 'min_length': '密码长度太短,至少8位'},
                          widget=widgets.PasswordInput(attrs={'class': 'form-control'}))


class EmailForm(forms.Form):
    """
    更改邮箱单独校验
    """
    email = forms.EmailField(max_length=32,
                             label='邮箱:',
                             error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式不对'},
                             widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        val = self.cleaned_data.get('email')
        email = Ouser.objects.filter(email=val)
        if email:
            raise ValidationError('该邮箱已经注册')
        else:
            return val



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Ouser
        fields = ['link', 'avatar']