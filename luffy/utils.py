from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException
from rest_framework import serializers
from luffy import models
import os
import binascii
import datetime

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token',None)
        obj = models.UserAuthToken.objects.get(token=token)
        if obj:
            return (obj,obj.user.username)
        return (None,None)


class LoginAuthentication(BaseAuthentication):
    '''
    登录验证
    code = 1010 # 错误
    '''
    def authenticate(self, request):
        if request._request.method =='POST':
            user = request.data.get('username', None)
            pwd = request.data.get('password', None)
            obj = models.Account.objects.filter(username=user, password=pwd).first()
            print(user,pwd,obj)
            if obj :
                if not models.UserAuthToken.objects.filter(user=obj):
                    token_obj=models.UserAuthToken.objects.create(user=obj)
                return (obj.username,obj)
            return (None,None)
            # raise APIException('登录失败，账号或密码有误！',code=1010)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={'required': '账号不能为空'})
    password = serializers.CharField(error_messages={'required': '密码不能为空'})


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields =[ 'id', 'title', 'brief', 'head_img','view_num', 'date','comment_num', 'collect_num','agree_num', 'content','source']
        depth = 2
