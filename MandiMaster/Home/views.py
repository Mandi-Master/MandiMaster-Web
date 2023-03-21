from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from Home.models import Room,Topic,Message,User
from Home.forms import TopicForm,RoomForm,MyUserCreationForm,UserForm 
# Create your views here.

@login_required(login_url='/login')    
def index(request):
    if request.user.is_authenticated:
        loged_user = request.user
        loged_user.is_online = True
        loged_user.save()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()
    room_list = Room.objects.filter(
        Q(Title__icontains=q) |
        Q(City__icontains=q) |
        Q(Category__name__icontains=q) |
        Q(Description__icontains=q) |
        Q(Type__name__icontains=q) 
    )
    room_messages = Message.objects.filter(Q(room__Title__icontains=q))
    room_count = room_list.count()
    context = {'topics':topics,'room_list':room_list,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'index.html',context)



@login_required(login_url='/login')
def list_details(request,id):
    room = Room.objects.get(id=id)
    participants = room.participants.all()
    context = {'room':room,'participants':participants}
    return render(request, 'list_details.html',context)



@login_required(login_url='/login')
def create_list(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            messages.success(request, "List was created successfully")
            return redirect('/home')

    context = {'form':form}
    return render(request, 'list_add.html',context)


@login_required(login_url='/login')
def create_topic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic was Added successfully")
            return redirect('/home')
    context = {'form':form}
    return render(request, 'topic_add.html',context)





def signup_user(request):
    page = 'signup'
    form = MyUserCreationForm()
    if request.user.is_authenticated:
        messages.success(request, "you have already signup!")
        return redirect('/home')    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            messages.success(request, "Registeration Successful!")
            return redirect("/")
        else:
            messages.success(request, "There was error in signing up , try again...")  
            return redirect('/signup')
    return render(request, 'login_signup.html',{'form':form ,'page':page})



def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.success(request, "you have already login!")
        return redirect('/home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "login Successfully!")
            return redirect("/")
        else:
            messages.success(request, "There was error in logging In , try again...")  
            return redirect('/login')
    context = {'page':page}
    return render(request, 'login_signup.html',context)


@login_required(login_url='/login')
def logout_user(request):
    if request.user.is_authenticated:
        loged_user = request.user
        loged_user.is_online = False
        loged_user.save()
        logout(request)
        messages.success(request, "Logout sucessfully...") 
        return redirect("/home")
    else:
        messages.success(request, "You are not login...")  
        return redirect('/login')

@login_required(login_url='/login')
def user_profile(request,id):
    user = User.objects.get(id=id)
    room_messages = user.message_set.all()
    room_list = user.room_set.all()
    context = {'room_list':room_list,'room_messages':room_messages,'user':user}
    return render(request, 'user_profile.html',context)

@login_required(login_url='/login')
def my_profile(request):
    user = request.user
    room_messages = user.message_set.all()
    room_list = user.room_set.all()
    context = {'room_list':room_list,'room_messages':room_messages,'user':user}
    return render(request, 'my_profile.html',context)


@login_required(login_url='/login')
def update_user_profile(request):
    user = request.user
    form = UserForm(instance = user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance = user)
        try:
            if form.is_valid:
                form.save()
                messages.success(request, "Profile has been updated sucessfully...")
                return redirect('/home')
            else:
                messages.success(request, 'There was a error in updating your profile!')
                return redirect('/update_profile') 
        except:
            messages.success(request, 'There was a error in updating your profile!')
            return redirect('/update_profile') 

    return render(request, 'user_profile_update.html',{'form':form,'user':user})

@login_required(login_url='/login')
def update_user_password(request):   
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home')
        else:
            messages.success(request, 'There was a error in changing password!')
            return redirect('/update_user_password')  
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_password.html',{'form':form})




@login_required(login_url='/login')
def update_list(request, room_id):
    room = Room.objects.get(id=room_id)
    form = RoomForm(instance=room)
    if request.user !=room.host:
        return HttpResponse('you are not allowed here')
    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES,instance = room)   
        if form.is_valid():
            form.save()
            messages.success(request, "Listing has been updated sucessfully...")
            return redirect('list_details',id= room.id)
    return render(request,'list_update.html',{'room':room,'form':form})


@login_required(login_url='/login')
def delete_list(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user !=room.host:
        return HttpResponse('you are not allowed here')
    if request.method == "POST":
        room.delete()
        messages.success(request, "Listing has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'delete.html',{'room':room})

@login_required(login_url='/login')
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == "POST":
        topic.delete()
        messages.success(request, "Topic has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'delete_by_super.html',{'topic':topic})


@login_required(login_url='/login')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    if request.user != message.user :
        return HttpResponse('you are not allowed here')
    if request.method == "POST":
        message.delete()
        messages.success(request, "message has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'delete.html',{'message':message})







