from django.shortcuts import render, HttpResponse
from django_redis import get_redis_connection

from utils.tencent.sms import send_sms_single
import random
from django.conf import settings


# Create your views here.


def send_sms(request):
    """ 发送短信
            ?tpl=login  -> 548762
            ?tpl=register -> 548760
        """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')
    code = random.randrange(1000, 9999)
    res = send_sms_single('18306604657', 614245, [code, ])
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])


from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
    # 通过自定义规则，将默认字段里的规则重写
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput())

    # 如果字段名相同就覆盖，不同就添加新字段
    confirm_password = forms.CharField(
        label='重复密码',
        widget=forms.PasswordInput())
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        # 修改展示顺序
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 通过 self.fields 获取上面的所有字段
        # 遍历字段，添加类名
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # 添加提示语句
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


def register(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {'form': form})

