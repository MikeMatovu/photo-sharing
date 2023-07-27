from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from core.models import Post, Profile, LikePost, FollowersCount 

@login_required(login_url='core:signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower= request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for username in user_following_list:
        feed_lists = Post.objects.filter(user = username) 
        feed.append(feed_lists)

    feed_list = list(chain(*feed))  

    #user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)


    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
       


    context ={
      'user_profile' :user_profile,
      'posts' : feed_list,
      'suggestions_username_profile_list': suggestions_username_profile_list[:4],
    }
    return render(request, 'core/index.html', context)

# @login_required(login_url='core:signin')
# def search(request):
#     user_object = User.objects.get(username = request.user.username)
#     user_profile = Profile.objects.get(user=user_object)

#     if request.method == 'POST':
#         username = request.POST['username']
#         username_object = User.objects.filter(username__icontains=username)
        
 

#         username_profile = []
#         username_profile_list = []

#         for users in username_object:
#             username_profile.append(users.id)


#         for id in username_profile:
#             profile_lists = Profile.objects.filter(id_user=id)
#             print("-"*20)
#             print(profile_lists)
#             print("-"*20)
#             username_profile_list.append(profile_lists)

#         username_profile_list = list(chain(*username_profile_list))    




#     context = {
#         'user_profile' : user_profile,
#         'username_profile_list' : username_profile_list
#     }    
#     return render(request, 'core/search.html', context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for id in username_profile:
            profile_lists = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
        
    context = {
            'user_profile': user_profile, 
            'username_profile_list': username_profile_list,
    }    
    return render(request, 'core/search.html', context)

def signup(request):
    

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('core:signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                #create a profile object for the new user

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user= user_model.id)
                new_profile.save()
                return redirect('core:settings')


        else:
            messages.info(request, 'Passwords do not match')
            return redirect('core:signup')


    else:
        context ={ }
        return render(request, 'core/signup.html', context)

def signin(request):



    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('core:signin')

        
    else:
        context = {}
        return render(request, 'core/signin.html', context)
    

@login_required(login_url='core:signin')
def logout(request):
    auth.logout(request)
    return redirect('core:signin')


@login_required(login_url='core:signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            
        else:
            image = user_profile.profileimg        

        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return   redirect('core:settings')       

            
    context = {
        'user_profile' : user_profile
    }
    return render(request, 'core/setting.html', context)

@login_required(login_url='core:signin')
@login_required
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='core:signin')
def like_post(request):
    uname = request.user.username
    post__id = request.GET.get('post_id')
    post = Post.objects.get(id=post__id)

    like_filter = LikePost.objects.filter(post_id = post__id, username=uname).first()

    if like_filter:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')
    else:
        new_like = LikePost.objects.create(post_id = post__id, username=uname)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')

@login_required(login_url='core:signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context ={
        'user_object': user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_posts_length' : user_posts_length,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following,
    }
    return render(request, 'core/profile.html', context)

@login_required(login_url='core:signin')
def follow(request):
    if request.method == 'POST':
        followerr = request.POST['follower']
        userr = request.POST['user']
        if FollowersCount.objects.filter(follower=followerr, user = userr).first():
            delete_follower = FollowersCount.objects.get(follower=followerr, user=userr)
            delete_follower.delete()
            return redirect('/profile/'+ userr)
        else:
            new_follower = FollowersCount.objects.create(follower=followerr, user=userr)
            new_follower.save()
            return redirect('/profile/'+ userr) 

    else:
        return redirect('/')
