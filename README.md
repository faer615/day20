#  Django 学习笔记 day20
## 创建于 2018年01月09日

### 1.Django请求生命周期
    路由系统 --> 视图函数（获取模板+数据=》渲染）--> 字符串返回给用户
---
### 2.路由系统
    /index/                 --> 函数或类.as_view()
    /detail/(\d+)           --> 函数（参数）或 类.as_view()(参数)
    /detail/(?P<nid>\d+)    --> 函数（参数）或 类.as_view()(参数)
    /detail/                --> include("app01.urls)
    /detail/name='a1'       --> include("app01.urls)
                            --> 试图中，使用reverse
                            --> 模板中，{% url "a1" %}
---
### 3.视图
    FBV：函数
        def index(request, *args, **kwargs):
            ...
    CBV：类
        class Home(views.View)
            def  get(self,request,*args,**kwargs):
            
    获取用户请求中的数据：
        request.POST.get
        request.GET.get
        request.FILES.get()
        
        # checkbox:
        ......getlist()
        request.path_info
        
        文件对象 = request.FILES.get()
        文件对象.name
        文件对象.size
        文件对象.chunks()
        
        # 上传文件 <form enctype="multipart/form-data"></form>
                                
    给用户返回数据：
        render(request, "",{'k1':[1,2,3,4],"k2": {'name':'小张','age':'27'}})
        redirect("URL")
		HttpResponse(字符串)
---
### 4.模板语言
    render(request, "模板文件的路径",{'k1':[1,2,3,4],"k2": {'name':'小张','age':'27'}})
    
    <html>
        <body>
        <!-- 取单值 -->
            <h1>{{ obj }}</h1>
            <h1>{{ k1.3 }}</h1>
            <h1>{{ k2.name }}</h1>
        
        <!-- 循环 -->    
            {% for i in k1 %}
                <p> {{ i }} </p>
            {% endfor %}
        
        <!-- 循环keys -->
            {% for row in k2.keys %}
                {{ row }}
            {% endfor %}
        
        <!-- 循环values -->
            {% for row in k2.values %}
                {{ row }}
            {% endfor %}
            
        <!-- 循环items -->
            {% for row in k2.items %}
                {{ k }} - {{ v }}
            {% endfor %}
                     
        </body>
    </html>
---
### 5.ORM
    a.创建类和字段
        class User(models.Model):
            age = models.IntergerFiled()
            name = models.CharFiled(max_length=12) # 字符长度
    
    # settings.py 注册 app
            
    b.生成数据库
        python manage.py makemigrations
        python manage.py migrate
        
    c.操作
        增: 
            models.User.objects.create(name='xiao',age='21')
            
            dic = {'name':'xx','age':23}
            models.User.objects.create(**dic)
            
            obj = models.User(name='xiao',age='21')
            obj.save()
        删:
            models.User.objects.filter(id__gt=1).delete()
        改:
            models.User.objects.filter(id__gt=1).update(name='fff',age=26)
            dic = {'name':'xx','age':23}
            models.User.objects.filter(id__gt=1).update(**dic)
        查: 
            models.User.objects.filter(id=1,name='root')    # 等于
            models.User.objects.filter(id__gt=1)            # 大于
            models.User.objects.filter(id__lt=1)            # 小于
            models.User.objects.filter(id__gte=1)           # 大于等于     
            models.User.objects.filter(id__lte=1)           # 小于等于
            
            models.User.objects.filter(id=1,name='root')
            dic = {'name':'xx','age__gt':23}
            models.User.objects.create(**dic)
            
            v1 = models.Business.objects.all()
            # QuerySet 内部元素都是对象

            v2 = models.Business.objects.all().values('id', 'caption')
            # QuerySet 内部元素都是字典

            v3 = models.Business.objects.all().values_list('id', 'caption')
            # QuerySet 内部元素都是元组
            
            # 获取到一个对象,如果不存在就报错
            models.Business.objects.get(id=1)
            对象或者None = models.Business.objects.filter(id=1).first()          
        
        外键：
            v = models.Host.objects.filter(nid_gt=0)
            v[0].b.cation ---> 通过.进行跨表
            
            
            
        外键：
            class UserType(models.Model):
                caption = models.Charfield(max_length=32)
                
             id caption 
            # 1.普通用户
            # 2.VIP用户
            # 3.游客用户
            
            class User(models.Model):
                age = models.IntergerFiled()
                name = models.CharField(max_length=10)      # 字符长度
                user_type_id = models.IntergerFiled()       # 约束
                user_type = models.ForeigenKey("UserType", to_field='id')  # 外键约束
            
            # name age user_type_id
              小A  18   1
              小B  28   2
              小C  18   3
              
    position:fixed absolute relative
    
    Ajax提交
        $.ajax({
            url: '/host',
            type: "POST",
            data: {'k1': 123, 'k2': "root"},
            success: function(data){
            // data是服务器端返回的字符串
            }
        )}

        建议：永远让服务器端返回一个字典
        return HttpResponse(json.dumps(字典))
        
## 创建多对多关系表
 
### 方式1：自定义关系表    
    # 主机信息
    class Host(models.Model):
        nid = models.AutoField(primary_key=True)
        hostname = models.CharField(max_length=32, db_index=True)
        ip = models.GenericIPAddressField(protocol="ipv4", db_index=True) # protocol默认是both
        port = models.IntegerField()
        b = models.ForeignKey("Business", to_field='id')
        
    # 应用信息
    class Application(models.Model):
        name = models.CharField(max_length=32)
        
    # 主机与应用关系
    class HostToApp(models.Model):
        hobj = models.ForeignKey(to='Host', to_field='nid')
        aobj = models.ForeignKey(to='Application', to_field='id')
        
    # 插入数据
    HostToapp.objects.create(hobj_id=1, aobj_id=2)
        
### 方式2：自动创建关系表
    # 主机信息
    class Host(models.Model):
        nid = models.AutoField(primary_key=True)
        hostname = models.CharField(max_length=32, db_index=True)
        ip = models.GenericIPAddressField(protocol="ipv4", db_index=True) # protocol默认是both
        port = models.IntegerField()
        b = models.ForeignKey("Business", to_field='id')
        
    # 应用信息
    class Application(models.Model):
        name = models.CharField(max_length=32)
        r = models.ManyToManyField("Host")
         
    # 无法直接对第三张表进行操作
    obj = Application.objects.get(id=1)
    obj.name
        
    # 第三张表增加操作
    obj.r.add(1) 
    obj.r.add(2) 
    obj.r.add(*[1,2,3,4])
        
    # 第三张表删除操作
    obj.r.remove(1) 
    obj.r.remove(2,4) 
    obj.r.remove(*[1,2,3,4]) 
    
    obj.r.clear()
    
    obj.r.set([3,5,7])
        
    # 所有相关主机对象“列表” QuerySet
    obj.r.all()