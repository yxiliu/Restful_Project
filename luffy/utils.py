from rest_framework.authentication import BaseAuthentication

# class MyAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         from django.contrib.sessions.backends.db import SessionStore
#         # print(request._request.session.get('token'))
#         token = request.COOKIES.get('token',None)
#         print(token)
#         return ('a','')