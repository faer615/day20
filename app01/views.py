from django.shortcuts import render, HttpResponse, redirect

from app01 import models


# Create your views here.

def business(request):
    v1 = models.Business.objects.all()
    # QuerySet 内部元素都是对象
    #[obj(id,caption,code),obj(id,caption,code),obj(id,caption,code)]

    v2 = models.Business.objects.all().values('id', 'caption')
    # QuerySet 内部元素都是字典
    #[{'id':1, 'caption':'运维部'},{'id':1, 'caption':'运维部'}]

    v3 = models.Business.objects.all().values_list('id', 'caption')
    # QuerySet 内部元素都是元组
    # [(1,'运维部'),(2,'开发部')]

    return render(request, 'business.html', {'v1':v1, 'v2':v2, 'v3':v3})

# def host(request):
#
#     v1 = models.Host.objects.filter(nid__gt=0)
#     # QuerySet
#     # for row in v1:
#     #     print(row.nid,row.hostname,row.ip,row.port,row.b_id,row.b.caption,row.b.code,row.b.id, sep='\t')
#
#     # return HttpResponse('Host')
#     v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'b_id', 'b__caption')
#
#     # print(v2)
#
#     # for row in v2:
#     #     print(row['nid'],row['hostname'],row['b_id'],row['b__caption'])
#
#     v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'b_id', 'b__caption')
#
#     return render(request, 'host.html', {'v1': v1, 'v2':v2, 'v3':v3})

def host(request):
    if request.method == "GET":
        v1 = models.Host.objects.filter(nid__gt=0)
        v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'b_id', 'b__caption')
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'b_id', 'b__caption')

        b_list = models.Business.objects.all()

        return render(request, 'host.html', {'v1': v1, 'v2':v2, 'v3':v3, 'b_list':b_list})

    elif request.method == "POST":
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        # models.Host.objects.create(hostname=h,
        #                            ip=i,
        #                            prot=p,
        #                            b=models.Business.objects.get(id=b))
        models.Host.objects.create(hostname=h,
                                    ip=i,
                                    port=p,
                                    b_id=b
                                   )
        return redirect('/host')

def test_ajax(request):
    import json
    ret = {'status': True, 'error': None, 'data': None}
    try:
        # print(request.method, request.GET.get('user'), request.GET.get('pwd'),sep='\t')
        # print(request.method, request.POST,sep='\t')
        # import time
        # time.sleep(5)
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                       ip=i,
                                       port=p,
                                       b_id=b
                                       )
        # return HttpResponse('OK')
        else:
            ret['status'] = False
            ret['error'] = "输入错误"
    except Exception as e:
        ret['status'] = False
        ret['error'] = "请求错误"
    return HttpResponse(json.dumps(ret))


def app(request):
    app_list = models.Application.objects.all()
    # for row in app_list:
    #     print(row.name,row.r.all())
    return render(request, 'app.html', {"app_list": app_list})
