from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Treasure
from .forms import TreasureForm,LoginForm
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    treasures = Treasure.objects.all()
    form = TreasureForm()
    return render(request,'index.html',
                  {'treasures':treasures,'form':form})

def detail(request,treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    return render(request,'detail.html',{'treasure':treasure})

def post_treasure(request):
    form=TreasureForm(request.POST,request.FILES)
    if form.is_valid():
       treasure = form.save(commit = False)
       treasure.user = request.user
       treasure.save()
#        form.save(commit=True)
#        treasure=Treasure(   name=form.cleaned_data['name'],
#	                     value =form.cleaned_data['value'],
#	                     material =form.cleaned_data['material'],	
#	                     location =form.cleaned_data['location'],
#	                     img_url =form.cleaned_data['img_url'])
 #       treasure.save()
    return HttpResponseRedirect('/')

def profile(request,username):
    user = User.objects.get(username=username)
    treasures = Treasure.objects.filter(user=user)
    return render(request,'profile.html',
                  {'username':username,
		   'treasures':treasures})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("the account has been disabled!")
            else:
                print("the username and password were incorrect.")
    else:
        form = LoginForm()
        return render(request,'login.html',
	             {'form':form})

def register(request):
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          form.save()
          return HttpResponseRedirect('/login/')

    else:
       form = UserCreationForm()
       return render(request,'registration.html',
                    {'form':form})

def logout_view(request):
    logout(request) 
    return HttpResponseRedirect('/')

def like_treasure(request):
    treasure_id = request.POST.get('treasure_id',None)

    likes = 0
    if(treasure_id):
       treasure = Treasure.objects.get(id=int(treasure_id))
       if treasure is not None:
           likes = treasure.likes + 1
           treasure.likes = likes
           treasure.save()
    return HttpResponse(likes)

def search(request):
    search_val = request.GET.get('search',None)

    if(search_val != None):
       results=[]
       treasures = Treasure.objects.filter(name__icontains=search_val)
       for treasure in treasures:
           json={}
           json['name']=treasure.name
           json['link']='/' + str(treasure.id)+'/'
           results.append(json)
       return JsonResponse({'results':results})
    else:
       return render(request,'search.html')
# context = {'treasures':treasures}
   # return render(request,'index.html',context)
						
#class Treasure:
#    def __init__(self,name,value,material,location):
#        self.name = name
#        self.value = value
#        self.material = material
#        self.location = location

#treasures = [
#    Treasure('Gold Nugget',500.00,'gold',"NY"),
#    Treasure('fools',0,'zine',"JP"),
#    Treasure('coffe can', 33.0,'tin','CA'),
#    Treasure('box', 111111,'paper','AU')
#]
 #return HttpResponse('<h1>2nd yeah!!you did it! Finish 1st important step</h1>')
