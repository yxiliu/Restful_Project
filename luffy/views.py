from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse,HttpResponse
from rest_framework.viewsets import ModelViewSet,generics
from luffy import models
from luffy import utils
from django.db import transaction
from django.db.models import F
import datetime
import redis
import json
class Login(APIView):
    '''
    code:    1000 正确
             1010 错误
    '''
    authentication_classes = [utils.LoginAuthentication,]
    def post(self,request):
        self.dispatch()
        data={'code':1000,'detail':'登录成功'}
        if not request.user:
            data['code']=1010
            data['detail'] = '登录失败，账号或密码有误！'
            return JsonResponse(data)
        data["token"]=request.auth.userauthtoken.token
        data["username"]=request.user
        return JsonResponse(data)


class News(APIView):
    def get(self,request,*args,**kwargs):
        self.dispatch
        ret={'code':1000,"detail":"News",'newslist':None}
        article_list = models.Article.objects.all()
        ser = utils.ArticleSerializer(instance=article_list, many=True, context={'request': request})
        ser.is_valid()
        ret['newslist']= ser.data
        return JsonResponse(ret)


class CoursesView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj=models.Course.objects.filter(id=pk).first()
            title=obj.name
            brief=obj.brief
            period=obj.period
            level=obj.get_level_display()
            price_policy=obj.price_policy.all()

            price_policy_list=[]
            for i in price_policy:
                price_policy_list.append({"周期":i.get_valid_period_display(),"价格":i.price})

            coursesection=obj.coursechapters.all()
            coursesection_list=[]
            for i in coursesection:
                coursesection_list.append(i.name)
            if not coursesection_list:
                coursesection_list="此课程还没有设置章节"
            #评论
            # recommend_courses= obj.recommend_by.all()
            # recommend_courses_list=[]
            # for i in recommend_courses:
            #     print(i,33333)
            #     recommend_courses_list.append(i.recommend_courses)
            # if not recommend_courses_list:
            #     recommend_courses_list="此课程还没有评论，快来评论吧！"

            #常见问题
            course_id=ContentType.objects.filter(app_label="luffy",model="course").first().id
            question_query=models.OftenAskedQuestion.objects.filter(content_type=course_id,object_id=obj.id,).all()
            question_list = []
            for i in question_query:
                question_list.append(i.question)
            if not question_list:
                question_list="此课程还没有常见问题"


            ret = {
                'title':title,
                'brief':brief,
                'coursesection_list':coursesection_list,
                # 'recommend_courses_list':recommend_courses_list
                'question_list':question_list,
                'period':period,
                'level':level,
                'price_policy_list':price_policy_list,
                'rbac':True,
            }
        else:
            course_list=[]
            course_query=models.Course.objects.all().values_list("id","name","course_img","level").order_by("id")
            for course in course_query:
                course_list.append({"id": course[0], "name": course[1],"course_img":course[2],"level":course[3]})
            ret = {'code':1000,'courseList':None}
            ret["courseList"]=course_list
            ret["rbac"]=True
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response



class NewsDetail(APIView):
    def get(self,request,nid,*args,**kwargs):
        ret={'code':1000,"detail":"NewsDetail",'detaillist':[]}
        article_obj = models.Article.objects.get(pk = nid)
        ser = utils.ArticleSerializer(instance=article_obj, context={'request': request})
        ret['detaillist'].append(ser.data)
        return JsonResponse(ret)

class ArticleCollection(APIView):
    authentication_classes = [utils.TokenAuthentication,]
    def get(self,request,nid,*args,**kwargs):
        ret = {'code': 1010, "detail": "收藏", 'data': None}
        if not request.user:
            return JsonResponse(ret)

        article_obj = models.Article.objects.get(id=nid)
        type_obj = models.ContentType.objects.get(app_label='luffy',model='article')
        collection_obj = models.Collection.objects.filter(content_type=type_obj,object_id=nid,account_id=request.user.user_id)#
        if not collection_obj:
            with transaction.atomic():
                ctime = datetime.datetime.now()
                models.Collection.objects.create(content_object=article_obj,account_id=request.user.user_id,date=ctime)
                article_obj.collect_num +=1
                article_obj.save()

                ret['code']=1000
                ret['detail']='完成收藏'
                ret['data']={'collect_num':article_obj.collect_num}
                return JsonResponse(ret)
        ret['code']=1020
        ret['detail']='已收藏'
        return JsonResponse(ret)




class CartView(APIView):
    authentication_classes = [utils.TokenAuthentication,]
    def get(self,request):
        user_id = request.user.id
        ret = {"code":1000,"msg":"wawa"}
        conn = redis.Connection(pool=utils.pool)
        something = conn.hget("Chart", request.user.id)
        curent=json.loads(something)
        return Response(curent)

    def post(self,request):
        self
        ret = {'code': 1000, 'msg': None}
        course_id = request.data.get('course_id')
        price_policy_id = request.data.get('price_policy_id')
        course_obj = models.Course.objects.filter(pk=course_id).first()
        if course_obj:
            ret["msg"] = "瞎输课程"
            ret["code"] = 1001
        else:
            price_policies = course_obj.price_policy.all()
            policies_id = [i.id for i in price_policies]
            policies_list = [{'id':i.id, 'valid_period':i.get_valid_period_display(),'price':i.price} for i in price_policies]  # 老师的比这个好，少用一个for循环
            if not price_policy_id in policies_id:
                ret["msg"] = "瞎输钱数"
                ret["code"] = 1002
            else:
                # 构造一个表
                course_dict = {
                    'id': course_obj.id,
                    'img': course_obj.course_img,
                    'title': course_obj.name,
                    'price_policy_list': policies_list,
                    'default_policy_id': price_policy_id
                }
                conn = redis.Connection(pool=utils.pool)
                nothing = conn.hget("Chart", request.user.id)
                if not nothing:
                    data = {course_obj.id: course_dict}
                else:
                    data = json.loads(nothing.decode('utf-8'))
                    data[course_obj.id] = course_dict
                conn.hset("Chart", request.user.id, json.dumps(data))
        return ret




class Myorder(APIView):
    authentication_classes = [utils.TokenAuthentication,]
    def get(self,request,*args,**kwargs):
        many_order_data = []
        sending_data = {"code":1000,"data":many_order_data,"msg":"good"}
        if request.user:
            order_obj_list = request.user.order_set.all()
            for ord_obj in order_obj_list:
                # ord_obj.order_number  # 订单号
                # ord_obj.actual_amount  # 实付金额
                # ord_obj.get_status_display() # 订单状态
                set_Of_order_details = ord_obj.orderdetail_set.all()
                detiallist=[{"course_name":order_details.content_object.name,"order_valid_period":order_details.valid_period_display,"course_period":order_details.valid_period,"price_after_discount":order_details.price} for order_details in set_Of_order_details]
                    # order_details.content_object.name  # 关联的课程？
                    # order_details.valid_period_display   # 订单有效日期
                    # order_details.original_price  #
                    # order_details.valid_period  # 课程有效期
                    # order_details.price # 折后价格
                coupons = ord_obj.couponrecord_set.all()
                couponlist=[couponre.coupon.name for couponre in coupons]
                each_order = {"order_number":ord_obj.order_number,"actual_amout":ord_obj.actual_amount,"order_status":ord_obj.get_status_display(),
                                "detaillist":detiallist}
                many_order_data.append(each_order)
                sending_data["data"] = many_order_data
        else:
            sending_data["code"] = 1001
            sending_data["msg"] = "no user was found"
        return Response(sending_data)
