from django.contrib.admin.templatetags.admin_list import results
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from recommend.models import User
from recommend.tools.cluster import predict
#from recommend.tools.crawler import getItem
def index(request):
    query = request.GET.get('q')  # 获取搜索查询
    results=[]
    data=[]
    if query:
        usr=User.objects.filter(id=int(query))  # 这里可以根据需要处理查询并返回结果
        for result in usr:
            data.append(result.age)
            data.append(result.genderf)
            data.append(result.genderm)
            data.append(result.size)
            data.append(result.pp)
            data.append(result.pm)
            data.append(result.fp)
        results=predict(data)
        # for item in items:
        #     results=results+getItem(item)
    # if query:
    #     age = User.objects.age.filter(id=int(query))  # 这里可以根据需要处理查询并返回结果
    #     genderf=User.objects.genderf.filter(id=int(query))
    #     genderm=User.objects.genderm.filter(id=int(query))
    #     size=User.objects.size.filter(id=int(query))
    #     pp=User.objects.pp.filter(id=int(query))
    #     pm=User.objects.pm.filter(id=int(query))
    #     fp=User.objects.fp.filter(id=int(query))
    #     data=[age,genderf,genderm,size,pp,pm,fp]
    #     results = tools.predict(data)




    # 假设您有一个模型 MyModel 来查询
    # from .models import MyModel
    # if query:
    #     results = MyModel.objects.filter(name__icontains=query)

    return render(request, 'recommend/index.html', {'query': query, 'results': results})