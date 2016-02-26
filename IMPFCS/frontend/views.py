# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from frontend.models import UserInfo
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
from django import forms
import pymongo
import datetime
from ctypes import*
import struct
#import mongo
import json
from django import forms
import ctypes
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
#from somewhere import handle_uploader_file
#client = mongo.MongoClient()
class Post(Structure):
    _fields_ = (
        ("x", c_void_p),
        ("length", c_int),
    )

class UserForm(forms.Form):
	username=forms.CharField()

class PassForm(forms.Form):
	password=forms.CharField()

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def loginUser(request):
    if request.method == 'GET':
        if request.user.is_authenticated() and request.user.is_active:
            return HttpResponseRedirect(reverse('frontend:foyer'))
        return render(request, 'frontend/login.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_active:
                    return HttpResponseRedirect(reverse('frontend:foyer'))
                else:
                    return render(request, 'frontend/completeInfo.html', {'user' : user})
            else:
                return render(request, 'frontend/login.html', {'errorMsg' : u'学号或密码错误'})
        except KeyError:
            raise Http404
    else:
        pass
    return HttpResponse('Try to login with:\n username=%s, password=%s' % (username, password))


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('frontend:login'))


def completeInfo(request):
    user = request.user
    if user.is_active:
        user.userinfo.name = request.POST['name']
        user.userinfo.gender = request.POST['gender']
        user.userinfo.department = request.POST['department']
        user.userinfo.studentClass = request.POST['studentClass']
    else:
        user.userinfo = UserInfo(
            name=request.POST['name'],
            gender=request.POST['gender'],
            department=request.POST['department'],
            studentClass=request.POST['studentClass'],
        )
        user.is_active = True
    user.userinfo.save()
    user.save()
    return HttpResponseRedirect(reverse('frontend:profile'))


@user_passes_test(lambda user: user.is_active)
def profile(request):
    return render(request, 'frontend/profile.html', {'user': request.user})


@user_passes_test(lambda user: user.is_active)
def foyer(request):
    resources = client.get_resource('resource')
    for i in range(len(resources)):
            resources[i]['id'] = str(resources[i]['_id'])
    if request.user.is_superuser:
        applications = client.get_application('application')
        app = []
        for i in range(len(applications)):
            applications[i]['id'] = str(applications[i]['_id'])
            if applications[i]['state'] == 'suspending':
                app.append(applications[i])
        teamApplications = client.get_teamApplication('teamApplication')
        teamApp = []
        for i in range(len(teamApplications)):
            teamApplications[i]['id'] = str(teamApplications[i]['_id'])
            if teamApplications[i]['state'] == 'suspending':
                teamApp.append(teamApplications[i]) 
        return render(request, 'frontend/adminFoyer.html', 
            {
                'user': request.user,
                'resources': resources, 
                'applications': app,
                'teamApplications': teamApp,
                'sidebar_select': 0})
    else:
        applications = client.get_user_application('application', request.user.username)
        app = []
        for i in range(len(applications)):
            app.append(applications[i])
            app[-1]['loc'] = client.get_resource_by_id('resource', app[-1]['resource_id'])['loc']
        teamApplications = {'teamApplications': [{'teamName': u'游泳队', 'year': 2014, 'month': 1, 'day': 1, 'state': 'rejected'}]}
        resourceApplications = {'resourceApplications': [{'loc': 'loc1', 'date': '20140102', 'state': 'accpeted'}]}
        return render(request, 'frontend/foyer.html', 
            {   'user': request.user,
                'teamApplications': teamApplications['teamApplications'], 
                'resourceApplications': app,
                'resources': resources, 
                'sidebar_select': 0})
        

@user_passes_test(lambda user: user.is_active)
def message(request):
    return HttpResponse('message')


@user_passes_test(lambda user: user.is_active)
def resources(request):
    if request.method == 'GET':
        return render(request, 'frontend/resources.html', {'user':
            request.user, 'sidebar_select': 3, 'superuser':
            request.user.is_superuser})
    else:
        raise Http404


@user_passes_test(lambda user: user.is_active)
def scores(request):
    scores = {'scores': [{'category': '射击', 'name': '奥运会', 'competition': '男子50米步枪3X40', 'rank': '1', 'score': '80', 'time': '0.01s', 'dist': '2m', 'state': 'rejected'}]}
    return render(request, 'frontend/scores.html', 
        {   'user': request.user,
            'scores': scores['scores'],
            'sidebar_select': 2
        })


@user_passes_test(lambda user: user.is_active)
def competitions(request):
      return render(request, 'frontend/competitions.html', {'user':
          request.user, 'sidebar_select': 1})


@user_passes_test(lambda user: user.is_active)
def applyTeam(request):
    user = request.user
    user.userinfo.is_applyingTeam = True
    user.userinfo.teamCategory = request.POST['teamCategory']
    user.userinfo.teamRole = request.POST['teamRole']
    user.userinfo.teamName = request.POST['teamName']
    user.userinfo.coach = request.POST['coach']
    user.userinfo.birth = request.POST['birth']
    user.userinfo.politicalBackground = request.POST['politicalBackground']
    user.userinfo.phoneNum = request.POST['phoneNum']
    user.email = request.POST['email']
    user.userinfo.address = request.POST['address']
    user.userinfo.work = request.POST['work']
    user.userinfo.applyTeamTime = datetime.datetime.now()
    user.userinfo.save()
    user.save()
    client.insert_teamApplication('teamApplication', {
        "s_id" : request.user.username,
        "teamName" : request.POST['teamCategory'],
        "date" : str(datetime.datetime.now())[:10],
        "state" : 'suspending' # rejected \ suspending
    })
    return HttpResponseRedirect(reverse('frontend:profile'))


@user_passes_test(lambda user: user.is_superuser)
def management(request):
    if request.method == 'GET':
        users = [u for u in User.objects.all() if u.is_active and not u.is_superuser and not u.userinfo.is_teamMember]
        athletes = [u for u in User.objects.all() if u.is_active and not u.is_superuser and u.userinfo.is_teamMember]
        return render(request, 'frontend/management.html', {'users': users, 'athletes': athletes, 'sidebar_select': 4 })
    else:
        raise Http404

#用户登录
@csrf_exempt
def login(req):
    req.session.set_expiry(0)
    if req.method == "POST":
        uf = UserForm(req.POST)
        ps = PassForm(req.POST)
	if uf.is_valid():
            username = uf.cleaned_data['username']
            req.session.set_expiry(0)
	    if ps.is_valid():
	    	password = ps.cleaned_data['password']
            #把获取表单的用户名传递给session对象
	    	req.session['password'] = password
            req.session['username'] = username
            return HttpResponseRedirect('/site/index/')
    else:
        uf = UserForm()
        ps = PassForm()
    #return render_to_response('frontend/login.html',{'uf':uf},{'ps':ps})
    return render_to_response('frontend/login.html',{'uf':uf,'ps':ps})

@csrf_exempt
def register(req):
    req.session.set_expiry(0)
    if req.method == "POST":
        uf = UserForm(req.POST)
        ps = PassForm(req.POST)
	if uf.is_valid():
            req.session.set_expiry(0)
            username = uf.cleaned_data['username']
	    if ps.is_valid():
	    	password = ps.cleaned_data['password']
            #把获取表单的用户名传递给session对象
	    	req.session['password'] = password
            req.session['username'] = username
            req.session['login'] = "true"
            vistorid = req.session.get("vistorid",-1)
            if vistorid <=0:   #link
	        conn = pymongo.MongoClient("127.0.0.1",27017)
                db=conn.biocad
                psidq = db.setting.find()
                psids = psidq[0]     #即使只有一条满足条件的记录也要这么取
                curvistorid = int(psids["maxid"])+1
                req.session['vistorid'] = curvistorid
                db.setting.update({},{"$set":{"maxid":curvistorid}})
                db.vistor.insert({"vistorid":curvistorid,"pn":1})
            vistorid = req.session.get("vistorid",-1)
	    if vistorid <=0:
		print "please register again"
	    else:
                conn = pymongo.MongoClient("127.0.0.1",27017)
                db=conn.biocad
                db.register.insert({"vistorid":vistorid,"user":username,"password":password})
            return HttpResponseRedirect('/site/adjust/')
    else:
        uf = UserForm()
        ps = PassForm()
    return render_to_response('frontend/register.html',{'uf':uf,'ps':ps})

@csrf_exempt
def page(req):
    req.session.set_expiry(0)
    if req.method == "POST":
        uf = UserForm(req.POST)
        ps = PassForm(req.POST)
	print "0"
	if uf.is_valid():
            username = uf.cleaned_data['username']
	    if ps.is_valid():
	    	password = ps.cleaned_data['password']
            #把获取表单的用户名传递给session对象
	    #	req.session['password'] = password
            #req.session['username'] = username
            conn = pymongo.MongoClient("127.0.0.1",27017)
            db=conn.biocad
            psidq = db.register.find({"user":username,"password":password})
            #print psidq
	    print "1"
            if psidq.count()!=0:
	        psids = psidq[0]     #即使只有一条满足条件的记录也要这么取
                vistorid = int(psids["vistorid"])
                req.session["login"] = "true"
		print "vistorid"
		print vistorid
		print "vistorid"
                req.session["vistorid"] = vistorid
                return HttpResponseRedirect('/site/adjust/')
            else:
                #return render_to_response('frontend/loginerror.html')
                uf = UserForm()
                ps = PassForm() 
                return render_to_response('frontend/loginfront.html',{'uf':uf,'ps':ps, "info":"wrong answer or username,please try again"})
    else:
        uf = UserForm()
        ps = PassForm()
    return render_to_response('frontend/loginfront.html',{'uf':uf,'ps':ps})

#登录之后跳转页
def indexpage(req):
    req.session.set_expiry(0)
    username = req.session.get('username','anybody')+req.session.get('password','123456')
    return render_to_response('frontend/test.html',{'username':username})

#注销动作
def logout(req):
    req.session.set_expiry(0)
    del req.session['username']  #删除session
    return HttpResponse('logout ok!')

@user_passes_test(lambda user: user.is_superuser)
def addResource(request):
    client.insert_resource('resource', 
        {
            'loc': request.POST['loc'],
            'date': request.POST['date'],
            'desc': request.POST['desc']
        })
    return HttpResponseRedirect(reverse('frontend:foyer'))


def applyResource(request, resource_id):
    client.insert_application('application', {
    "s_id" : request.user.username,
    "resource_id" : resource_id,
    "date" : str(datetime.datetime.now())[:10],
    "state" : 'suspending' # rejected \ suspending
    })
    return HttpResponseRedirect(reverse('frontend:foyer'))


def replyResourceApplication(request, reply, application_id):
    assert reply in ['accept', 'reject']
    client.change_application_state('application', reply + 'ed', application_id)
    return HttpResponseRedirect(reverse('frontend:foyer'))

@csrf_exempt
def ccc(request):                          #专门处理json数据的函数
  if request.method == 'POST':
    name=int(request.POST.get("num",None))
    name1=int(request.POST.get("num1",None))
    cr = 0
    msg = ". It belongs to ";
    #connection = pymongo.Connection('localhost', 27017)
    conn = pymongo.MongoClient("127.0.0.1",27017)
    db = connection.python
    collection = db.ps
    psc = collection.find({"xasis":name,"yasis":name1},{"ps"}) 
    for post in psc:
        if post:
            msg = msg+","+str(post["ps"])
            cr = 1
    if cr == 0:
        msg = msg+"no ps"
    else :
        pass
    cr = 0
    msg = str(name) + ','+str(name1)+msg
    return  HttpResponse(json.dumps(msg))
  elif request.method == 'GET':
    request.session.set_expiry(0)
 #   loginstatus = request.session.get('login','false')
    vistorid = int(request.session.get('vistorid',-1))
    print 'vistoraa'
    print vistorid
    print 'vistoraa'
    if vistorid>0 :
    	conn = pymongo.MongoClient("127.0.0.1",27017)
    	db=conn.biocad
    	psidq = db.vistor.find({"vistorid":vistorid})
#	if loginstatus == 'true':
#		psidq = db.register.find({"vistorid":vistorid})
#	else:
#		request.session['login']='false'
 #               psidq = db.register.find({"vistorid":vistorid})
	psids = psidq[0]
    	psid=psids["pn"]
    	collection = db.st1
    	if psid==1: collection=db.st1
    	if psid==2: collection=db.st2
    	if psid==3: collection=db.st3
    	if psid==4: collection=db.st4
    	if psid==5: collection=db.st5
    	if psid==6: collection=db.st6
    	if psid==7: collection=db.st7
    	if psid==8: collection=db.st8
    	if psid==9: collection=db.st9
    	if psid==10: collection=db.st10
    	max_content = collection.find({"vistorid":vistorid}).sort("dataid")
	print psid
    	#max_content = conn.demo.st1.find().sort("_id",pymongo.DESCENDING)
    	#max_content = conn.demo.st1.find().sort({"_id":-1}).limit(1)
   	# content  = conn.demo.st1.find().sort({"_id":1}) 
   	# max_id = max_content['_id']
    	#maxid = conn.demo.st1.find().sort("_id").limit(1)
    	data = []
    #if conn.demo.st1.find({"_id":0}):
    	totaldata = 0
        if max_content:
            for pdata in max_content: 
     	       data.append('(')
               data.append(str(pdata['pos_x']))
               data.append('?')
               data.append(str(pdata['pos_y']))
               data.append('!')
               data.append(str(pdata['pid']))
               data.append(')')
               totaldata = totaldata+1

        print 'numaa'
	print totaldata
        print 'numaa'
    	if totaldata<20:
    	    data=[]
       	    data.append('#')
            data.append('#')
            data.append('#')
    	return  HttpResponse(json.dumps(data))
    else:
    	data=[]
    	data.append('#')
    	data.append('#')
    	data.append('#')
    #	request.session['vistorid']=-1
    #	request.session['login']='false'
    	return  HttpResponse(json.dumps(data))

def ajax(request):
    return render_to_response('frontend/ajax.html')
@csrf_exempt
def adjust(request):
    return render_to_response('frontend/adjust.html')
   # if request.method == 'POST':
     # if request.POST.has_key('s_thread'):  
     #   pfile = open('/home/shaohx/ps_data/new_ps1.ps','rb') 
    #    pread = pfile.read()
   #     return  HttpResponse(pread)
  #    else:
 #       return render_to_response('frontend/adjust.html')

@csrf_exempt
def ddd(request):
    if request.method == 'POST':
        name=request.POST.getlist("num",None)
        pfile=open('./frontend/ps_data/new_ps1.ps','a')
        ts = 0
        ls = len(name)
        pid = 1
        while ts<ls:
            if int(name[ts+2])==pid:
                pfile.write('(')
                pfile.write(str(int(name[ts])))
                pfile.write(',')
                pfile.write(str(int(name[ts+1])))
                pfile.write(')')
                ts = ts+3
            else:
                pfile.write('\n')
                pid = pid+1
                ts = ts
                
        pfile.close() 
        print int(name[0])
        return HttpResponse(json.dumps("uploaded successfully!")) 
    elif request.method == 'GET':
        if request.GET.has_key('s_thread'):
            filename = './frontend/ps_data/new_ps1.ps'        #??????????                          
            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='text/plain')
            #response['Content-Length'] = os.path.getsize(filename)
            response['Content-Encoding'] = 'utf-8'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            return response
        return render(request,'frontend/adjust.html',locals())
        #pfile = open('/home/shaohx/ps_data/new_ps1.ps','rb')
        #pread = pfile.read()
        #return  HttpResponse(pread)    
def post(request):
    return render_to_response('frontend/post.html')


@csrf_exempt
def eee(request):
    if request.method == 'POST':
        source_x=int(request.POST.get("num",None))
        source_y=int(request.POST.get("num1",None))
        termin_x=int(request.POST.get("num2",None))
        termin_y=int(request.POST.get("num3",None))
        target_x=int(request.POST.get("num4",None))
        target_y=int(request.POST.get("num5",None))
        obs_point = request.POST.getlist("num6",None)    #存储所有点
        print "hello"
        print str(obs_point[0])
        print str(obs_point[1])
        print str(obs_point[2])+str(obs_point[3])
        print obs_point[4]
        print obs_point[5]
        len1 = len(obs_point)
        #print "hello1"
        #TenIntArrayType = c_int * len1
        #arr = TenIntArrayType()       #存储障碍点
        #obs_id = 0                    
        #n_id = 0
        #print "hello3"
        #while obs_id<len1:
        #    arr[obs_id]=int(obs_point[n_id])
        #    arr[obs_id+1]=int(obs_point[n_id+1])
           # print arr[obs_id]
            #print arr[obs_id+1]
        #    obs_id = obs_id+2
        #    n_id = n_id+3
       # print "hello4"
        #pfile1=open('./frontend/ps_data/new_ps2.ps','a')
        #arr="s"
        #obs_id=0;
        #while obs_id<len1:
        #@      arr= arr+"("+str(obs_point[obs_id])+","+str(obs_point[obs_id+1])+")"
        #      obs_id = obs_id+2;
        #pfile1.write(arr)           #用做调试用，测试点写到文件
        #pfile1.close()
        arr="s"
        obs_id=0
        foolib = CDLL("./maze4.so")
        o = Post()
        #print "hello2"
        foolib.maze(byref(o),120,300,target_x,target_y,source_x,source_y,create_string_buffer(arr))
        #foolib.maze(byref(o),120,300,target_x,target_y,source_x,source_y,pointer(arr),len1);
        a=string_at(o.x,o.length+1)
        o1 = Post()
        foolib.maze(byref(o1),120,300,termin_x,termin_y,target_x,target_y,create_string_buffer(arr))
        #foolib.maze(byref(o1),120,300,termin_x,termin_y,target_x,target_y,pointer(arr),len1);
        a1= string_at(o1.x,o1.length+1)
        new_point=[]
        i = 0
        t=len(a)
        
        while ((i<t) and (a[i]!='s')):
          if a[i]==',':
            new_point.append('?')
            i=i+1
          else :
            new_point.append(a[i])
            i=i+1
        i = 1
        t1=len(a1)
        while ((i<t1) and (a1[i]!='s')):
          if a1[i]==',':
            new_point.append('?')
            i=i+1
          else :
            new_point.append(a1[i])
            i=i+1
        if (t<397) and (t1<397):               #这里的计算长度纯属想象，可以修改
            new_point= new_point
        else:
            new_point=[]
        
        if (t>6) and (t1>6) and (t!=t1):               #这里的计算长度纯属想象，可以修改
            new_point= new_point                       #还有提升空间，可以尝试把初始点不符的都干掉
        else:
            new_point=[]
        print new_point
        print source_x
        print source_y
        print termin_x
        print termin_y
        print target_x
        print target_y
        print a
        print a1
        return HttpResponse(json.dumps(new_point))

@csrf_exempt
def backdevice(request):
        if request.method == 'GET':
                request.session.set_expiry(0)
		vistorid = int(request.session.get('vistorid',-1))
		if vistorid>0:
                	conn = pymongo.MongoClient("127.0.0.1",27017)
			db = conn.biocad
			psidq = db.vistor.find({"vistorid":vistorid})
			psids = psidq[0]
		        psid=psids["pn"]
        		collection = db.device1
        		if psid==1: collection=db.device1
        		if psid==2: collection=db.device2
        		if psid==3: collection=db.device3
        		if psid==4: collection=db.device4
        		if psid==5: collection=db.device5
        		if psid==6: collection=db.device6
        		if psid==7: collection=db.device7
        		if psid==8: collection=db.device8
        		if psid==9: collection=db.device9
        		if psid==10: collection=db.device10
			max_content = collection.find({"vistorid":vistorid})
                	data = []
			if max_content:
				for pdata in max_content:
					data.append(pdata["p0"])
					data.append(pdata["p1"])
					data.append(pdata["p2"])
					data.append(pdata["p3"])
					data.append(pdata["p4"])
                	return HttpResponse(json.dumps(data))
		else:
			data = []
			return HttpResponse(json.dumps(data))

@csrf_exempt
def backflow(request):
        if request.method == 'GET':
                request.session.set_expiry(0)
                vistorid = int(request.session.get('vistorid',-1))
                if vistorid>0:
                        conn = pymongo.MongoClient("127.0.0.1",27017)
                        db = conn.biocad
                        psidq = db.vistor.find({"vistorid":vistorid})
                        psids = psidq[0]
                        psid=psids["pn"]
                        collection = db.flow1
                        if psid==1: collection=db.flow1
                        if psid==2: collection=db.flow2
                        if psid==3: collection=db.flow3
                        if psid==4: collection=db.flow4
                        if psid==5: collection=db.flow5
                        if psid==6: collection=db.flow6
                        if psid==7: collection=db.flow7
                        if psid==8: collection=db.flow8
                        if psid==9: collection=db.flow9
                        if psid==10: collection=db.flow10
                        max_content = collection.find({"vistorid":vistorid}).sort("order")
                        data = []
                        if max_content:
                                for pdata in max_content:
                                        data.append(pdata["px"])
                                        data.append(pdata["py"])
                                        data.append(pdata["psid"])
                        return HttpResponse(json.dumps(data))
                else:
                        data = []
                        return HttpResponse(json.dumps(data))

@csrf_exempt
def backcontrol(request):
        if request.method == 'GET':
                request.session.set_expiry(0)
                vistorid = int(request.session.get('vistorid',-1))
                if vistorid>0:
                        conn = pymongo.MongoClient("127.0.0.1",27017)
                        db = conn.biocad
                        psidq = db.vistor.find({"vistorid":vistorid})
                        psids = psidq[0]
                        psid=psids["pn"]
                        collection = db.control1
                        if psid==1: collection=db.control1
                        if psid==2: collection=db.control2
                        if psid==3: collection=db.control3
                        if psid==4: collection=db.control4
                        if psid==5: collection=db.control5
                        if psid==6: collection=db.control6
                        if psid==7: collection=db.control7
                        if psid==8: collection=db.control8
                        if psid==9: collection=db.control9
                        if psid==10: collection=db.control10
                        max_content = collection.find({"vistorid":vistorid}).sort("order")
                        data = []
                        if max_content:
                                for pdata in max_content:
                                        data.append(pdata["px"])
                                        data.append(pdata["py"])
                                        data.append(pdata["psid"])

                        return HttpResponse(json.dumps(data))
                else:
                        data = []
                        return HttpResponse(json.dumps(data))

@csrf_exempt
def fff(request):
    request.session.set_expiry(0)
    if request.method == 'POST':
    	vistorid=int(request.session.get("vistorid",-1))
	if vistorid<=0:
		print "error"
	else:
		name=request.POST.getlist("num",None)
        	#pfile3=open('./frontend/ps_data/new_ps3.ps','a') 
        	#len1=len(name)/
        	#obs_id=0
        	#arr="s"
        	#while obs_id<len1:
        	#      arr= arr+"("+str(name[obs_id])+","+str(name[obs_id+1])+","+str(name[obs_id+2])+")"
        	#      obs_id = obs_id+3
        	#pfile3.write(arr)           #用做调试用，测试点写到文件
        	#print "tiaoshi2"
        	#pfile3.close()
		print "ok"
        	#for p in name:
		#	print p
        	ts = 0
        	#conn = pymongo.Connection("127.0.0.1",27017)
        	conn = pymongo.MongoClient("127.0.0.1",27017)
		if conn:
			print "ok1"
		db = conn.biocad
		if db:
			print "ok"
        	psid = 1
        	psids = db.vistor.find({"vistorid":vistorid})
        	#psids = db.userinfo
        	psidsq = psids[0]
        	psid = psidsq["pn"]
        	if psid<10:
            		psid =psid+1
        	else: psid = 1
        	collection = db.st1
        	if psid==1: collection=db.st1
        	if psid==2: collection=db.st2
        	if psid==3: collection=db.st3
        	if psid==4: collection=db.st4
        	if psid==5: collection=db.st5
        	if psid==6: collection=db.st6
        	if psid==7: collection=db.st7
        	if psid==8: collection=db.st8
        	if psid==9: collection=db.st9
        	if psid==10: collection=db.st10
        	#db.st1.save({'_id':save_id,'pid':m1,'pos_x':num_tmp1,'pos_y':num_tmp2})
        	print "trr"
        	print psid
		collection.remove({"vistorid":vistorid})
        	while ts<len(name):
        	     collection.insert({'vistorid':vistorid,'dataid':(ts+3)/3,'pid':int(name[ts+2]),'pos_x':int(name[ts]),'pos_y':int(name[ts+1])})
        	     ts=ts+3
		     print "ss"
        	db.vistor.update({"vistorid":vistorid},{"$set":{"pn":psid}})
        	print "s"
		return HttpResponse(json.dumps("okay"))

@csrf_exempt
def ggg(request):
    request.session.set_expiry(0)
    if request.method == 'POST':
      vistorid = int(request.session.get("vistorid",-1))
      if vistorid <=0:
           print "error"
      else:
        name=request.POST.get("num",None)
        #conn = pymongo.Connection("127.0.0.1",27017)
        conn = pymongo.MongoClient("127.0.0.1",27017)
	db=conn.biocad
        psid = 1
        psidq = db.vistor.find({"vistorid":vistorid})
        psids = psidq[0]
        psid = psids["pn"]
        if psid>1:
            psid =psid-1
        else: psid = 10
        #collection_before是当前,会被remove掉，collection是tobe        
        collection = db.st1
        collection_before=db.st1
        if psid==1: 
             collection=db.st1
             collection_before=db.st2
        if psid==2:
             collection=db.st2
             collection_before=db.st3
        if psid==3: 
             collection=db.st3
             collection_before=db.st4
        if psid==4: 
             collection=db.st4
             collection_before=db.st5
        if psid==5: 
             collection=db.st5
             collection_before=db.st6
        if psid==6:
             collection=db.st6
             collection_before=db.st7
        if psid==7: 
             collection=db.st7
             collection_before=db.st8
        if psid==8: 
             collection=db.st8
             collection_before=db.st9
        if psid==9: 
             collection=db.st9
             collection_before=db.st10
        if psid==10:  
             collection=db.st10
             collection_before=db.st1
        #print "3"
        max_content = collection.find().sort("_id")
        totaldata = 0
        data = []
        if max_content:
            for pdata in max_content:
                #if pdata['pid']==25:#当初用做调试用
                #    print "x"
                #    print pdata['pos_x']
                #    print "y"
                #    print pdata['pos_y']
                #    print "ps"
                #    print pdata['pid']
                data.append('(')
                data.append(str(pdata['pos_x']))
                data.append('?')
                data.append(str(pdata['pos_y']))
                data.append('!')
                data.append(str(pdata['pid']))
                data.append(')')
                totaldata = totaldata+1
         #   print "4"
        if totaldata<20:
            data=[]
            data.append('#')
            data.append('#')
            data.append('#')
        else:
            collection_before.remove()
            collection_before.insert({'dataid':0,'pid':0,'pos_x':0,'pos_y':0})
            db.userinfo.update({"vistorid":vistorid},{"$set":{"pn":psid}})
        #print "5"
        return  HttpResponse(json.dumps(data))

@csrf_exempt
def upall(request):
        if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form:
                        handle_upallfile(request.FILES['file'])
			vistorid = request.session.get('vistorid',-1)
            		conn = pymongo.MongoClient("127.0.0.1",27017)
            		db=conn.biocad
            		if vistorid <=0:
                		psidq = db.setting.find()
                		psids = psidq[0]     #即使只有一条满足条件的记录也要>这么取
                		vistorid = int(psids["maxid"])+1
                		db.setting.update({},{"$set":{"maxid":vistorid}})
                		db.vistor.insert({"vistorid":vistorid,"pn":1})
            		else:
                		db.vistor.update({"vistorid":vistorid},{"$set":{"pn":1}})
                		if request.session.get("login","false")!="true":
                   			return HttpResponseRedirect('/site/login/')
            		request.session['vistorid'] = vistorid
                        all_db_setup(vistorid)
			return HttpResponseRedirect('/site/adjust/')
        else:
                form = UploadFileForm()

def all_db_setup(curvistorid):
        up_file = open('all.txt')
        conn = pymongo.MongoClient("127.0.0.1",27017)
        db = conn.biocad
        lines = up_file.readline()
        lines = up_file.readline()
        ss = lines.split(" ")
        num = 0
        if ss[0] =='device':
                num = int(ss[1])
                if num==None    or num<=0:
                        return
        else:
                return
        i=0
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                i=i+1
                db.device1.insert({"vistorid":curvistorid,"p0":int(sss[0]),"p1":int(sss[1]),"p2":int(sss[2]),"p3":int(sss[3]),"p4":int(sss[4])})
        lines = up_file.readline()
        num = 0
	ss = lines.split(" ")
        if ss[0]=='path':
                num = int(ss[1])
                if num==None or num<=0:
                        db.device1.remove()
        else:
                db.device1.remove()
        i = 0
        a=1
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                t = 1
                while t<len(sss)-1:
                        ssss = sss[t].split(",")
                        ssss1 = ssss[0].split("(")
                        ssss2 = ssss[1].split(")")
                        db.flow1.insert({"vistorid":curvistorid,"order":a,"px":int(ssss1[1]),"py":int(ssss2[0]),"psid":i})
                        t=t+1
                        a=a+1
                i = i+1
        lines = up_file.readline()
        num = 0
        ss = lines.split(" ")
        if ss[0]=='control':
         	num = int(ss[1])
                if num==None or num<=0:
                        db.flow1.remove()
                        db.device1.remove()
                        return
        else:
                db.device1.remove()
                db.flow1.remove()
                return
        i = 0
        a=1
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                t = 1
                while t<len(sss)-1:
                        ssss = sss[t].split(",")
                        ssss1 = ssss[0].split("(")
                        ssss2 = ssss[1].split(")")
                        db.control1.insert({"vistorid":curvistorid,"order":a,"px":int(ssss1[1]),"py":int(ssss2[0]),"psid":i})
                        t=t+1
                        a=a+1
                i = i+1
	up_file.close()

def handle_upallfile(f):
        destination = open('all.txt', 'wb')
        for chunk in f.chunks():
                destination.write(chunk)
                #print chunk the next point
        destination.close()

@csrf_exempt
def upflow(request):
        if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form:
                        handle_upflowfile(request.FILES['file'])
                        flow_db_setup()
                return HttpResponse(json.dumps("ok"))
        else:
                form = UploadFileForm()

def handle_upflowfile(f):
    destination = open('flow.txt', 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def flow_db_setup():
        up_file = open('flow.txt')
        conn = pymongo.MongoClient("127.0.0.1",27017)
        db = conn.demo
        lines = up_file.readline()
        lines = up_file.readline()
        ss = lines.split(" ")
	num = 0
        if ss[0] =='device':
                num = int(ss[1])
                if num==None    or num<=0:
                        return
        else:
                return
        i=0
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                i=i+1
                db.device.insert({"p0":int(sss[0]),"p1":int(sss[1]),"p2":int(sss[2]),"p3":int(sss[3]),"p4":int(sss[4])})
        lines = up_file.readline()
        num = 0
        ss = lines.split(" ")
        if ss[0]=='path':
                num = int(ss[1])
                if num==None or num<=0:
                        db.device.remove()
        else:
                db.device.remove()
        i = 0
        a=1
	while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                t = 1
                while t<len(sss)-1:
                        ssss = sss[t].split(",")
                        ssss1 = ssss[0].split("(")
                        ssss2 = ssss[1].split(")")
                        db.flow.insert({"order":a,"px":int(ssss1[1]),"py":int(ssss2[0]),"psid":i})
                        t=t+1
                        a=a+1
                i = i+1
	up_file.close()

@csrf_exempt 
def upload(request):
    request.session.set_expiry(0)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form:
            handle_uploaded_file(request.FILES['file'])
            vistorid = request.session.get('vistorid',-1)
            conn = pymongo.MongoClient("127.0.0.1",27017)
            db=conn.biocad
            if vistorid <=0:
       	    	psidq = db.setting.find()
            	psids = psidq[0]     #即使只有一条满足条件的记录也要这么取
            	vistorid = int(psids["maxid"])+1
                db.setting.update({},{"$set":{"maxid":vistorid}})
	        db.vistor.insert({"vistorid":vistorid,"pn":1})
	    else:
                db.vistor.update({"vistorid":vistorid},{"$set":{"pn":1}})
                if request.session.get("login","false")!="true":
                   return HttpResponseRedirect('/site/login/')
	    db_setup(vistorid)
	    request.session['vistorid'] = vistorid
            return HttpResponseRedirect('/site/adjust/')
        #return  HttpResponse(json.dumps(data))
    else:
        form = UploadFileForm()
    return render_to_response('frontend/post.html')



def handle_uploaded_file(f):
    destination = open('name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def flow_layer(request):
    print 'Come in flow layer'
    input_file = open('flow_layer')
    conn = pymongo.MongoClient("127.0.0.1",27017)
    if conn:
        print "flow layer ok!"
    db = conn.demo
    lines = input_file.readlines()
    length = len(lines)
   # print lines
    return  HttpResponse(json.dumps(lines))

def control_layer(request):
    print 'Come in control layer'
    input_file = open('control_layer')
    conn = pymongo.MongoClient("127.0.0.1",27017)
    if conn:
        print "control layer ok!"
    db = conn.demo
    lines = input_file.readlines()
    length = len(lines)
    print lines
    return  HttpResponse(json.dumps(lines))


def db_setup(curvistorid):
    up_file = open('name.txt')#调用文件的 readline()方法
    #conn = pymongo.Connection("127.0.0.1",27017)
    conn = pymongo.MongoClient("127.0.0.1",27017)
    db = conn.biocad
    lines = up_file.readline()
    i1 = len(lines)                  #当前行总长度
    t1 = 0                           #标记当前处理到的位置,当前字在该行中的标号
    m1 = 1                           #标记当前对应的ps id   
    wr1 = 0                          #标记开端,有括号才计入数据
    num1 = [0,0,0,0,0]               #存储各个位上的数字
    num_tmp1 = 0                           
    num_tmp2 = 0
    times = 0                        #存储数据位数
    save_id = 1;                     #存储存储顺序
    while lines:
            t1 = 0
            i1 = len(lines)
            while t1<i1:
                if lines[t1]=="(":
                    wr1 = 1
                elif lines[t1]==',':
                    num_tmp_id = 0
                    while num_tmp_id < times:
                         num_tmp1+=num1[num_tmp_id]*10**(times-1-num_tmp_id)
                         num_tmp_id = num_tmp_id+1
                    times = 0                    
                elif lines[t1]==')':             #识别到“）”才整组存入
                    #存入num_tmp1,num_tmp2和ps
                    num_tmp_id = 0
                    while num_tmp_id < times:
                         num_tmp2+=num1[num_tmp_id]*10**(times-1-num_tmp_id)
                         num_tmp_id = num_tmp_id+1
                    db.st1.save({'vistorid': curvistorid , 'dataid':save_id,'pid':m1,'pos_x':num_tmp1,'pos_y':num_tmp2})
                    save_id = save_id+1
                    times = 0
                    num_tmp1 = 0
                    num_tmp2 = 0
                    wr1 = 0
                elif ((lines[t1]>='0') and (lines[t1]<='9')):
                    if wr1==1:
                        num1[times]=int(lines[t1])
                        times = times+1
                else:pass
                t1=t1+1
            m1 = m1+1
            lines =up_file.readline()
    up_file.close()
    db.st2.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st3.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st4.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st5.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st6.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st7.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st8.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st9.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    db.st10.insert({"vistorid": curvistorid , "dataid": 0 ,"pid":0,"pos_x":0,"pos_y":0})
    #db.st4.remove()
    #db.st5.remove()
    #db.st6.remove()
    #db.st7.remove()
    #db.st8.remove()
    #db.st9.remove()
    #db.st10.remove()
    

def replyTeamApplication(request, reply, application_id):
    assert reply in ['accept', 'reject']
    client.change_teamApplication_state('teamApplication', reply + 'ed', application_id)
    app = client.get_teamApplication_by_id('teamApplication', application_id)
    user = User.objects.get(username=app['s_id'])
    if reply == 'accept':
        user.userinfo.is_teamMember = True
    user.userinfo.is_applyingTeam = False
    user.userinfo.save()
    user.save()
    return HttpResponseRedirect(reverse('frontend:foyer'))


@user_passes_test(lambda user: user.is_superuser)
def deleteUser(request, username):
    user.objects.get(username=username).delete()
    return httpresponseredirect(reverse('frontend:management'))
