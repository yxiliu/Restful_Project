from django.contrib import admin
from luffy.models import *
# ==================================================课程相关
admin.site.register(CourseCategory)
admin.site.register(CourseSubCategory)
admin.site.register(DegreeCourse)
admin.site.register(Scholarship)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(PricePolicy)
admin.site.register(Coupon)
admin.site.register(CourseDetail)
admin.site.register(OftenAskedQuestion)
admin.site.register(CourseOutline)
admin.site.register(CourseChapter)
admin.site.register(CourseSection)

# ######################## 深科技 ########################
admin.site.register(ArticleSource)
admin.site.register(Article)
admin.site.register(Collection)
admin.site.register(Comment)

# ######################## 用户 ########################
admin.site.register(Account)
admin.site.register(UserAuthToken)



