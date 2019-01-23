from django.shortcuts import HttpResponse,redirect

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import *

class login_authenticate_midware(MiddlewareMixin):

    def process_request(self, request):

        # 白名单,login要放行,不然会死循环,login的时候重定向到login,
        if request.path in ['/login/','/reg/']:
            return None  #return None就相当于pass,继续执行下一个中间件


        # 如果没认证就重定向到登录页面,注意登录认证的中间件要放在AuthenticationMiddleware中间件的下面,
        # 因为要auth.login()后才会有request.user
        if not request.user.is_authenticated:
            return redirect('/login/')


