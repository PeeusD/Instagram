from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import get_user_model
from core.models import Comment, Follow, Post, Like, SavedPost
from core.forms import PostCreateForm
from django.contrib import messages
from django.db.models import Count
from django.core import serializers
import json
# Create your views here.
User = get_user_model()


class HomeView(View):
    # This is the Home Feed....
    def get(self, request, *args, **kwargs):
        form = PostCreateForm()
        #post objs-- this is modified in post model 
        all_posts = Post.objects.all()[:10]  #alt. use this for ordering post--> .order_by('-created_on')
        
        return render(request,'core/feed.html', context={'form':form, 'all_posts':all_posts} )

class PostCreateView(View):
    # This section creats User's post...
    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved')
            return redirect('home_feed')
        else:
            messages.error(request, 'Error')
            return render(request, 'core/feed.html', context={'form':form})
  
class PostDetailView(View):
    # This section shows the users all post details
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:    # retrieving specific post details using pk
            post_obj = Post.objects.get(pk=post_id)
             #retrieving all comments obj using pk
            comments = Comment.objects.filter(post=post_id)
        except:
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            Like.objects.get(user=request.user, post_id=post_id)
            liked_this_post = True
        except:
            liked_this_post = False


        try:
            SavedPost.objects.get(user=request.user, post_id=post_id)
            post_saved = True
        except:
            post_saved = False
        context =  {'post':post_obj, 
                    'liked_this_post':liked_this_post,
                     'comments':comments,
                     'post_saved':post_saved,
                     }
        return render(request, 'core/post_detail.html', context=context)


class PostDeleteView(View):
    # This section deletes User's Posts
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            post_obj = Post.objects.get(pk=post_id)
        except:
            pass

        if request.user == post_obj.user :
            post_obj.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))

class PostSaveView(View):
    # This section saves User's posts
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            SavedPost.objects.get(pk=post_id)
        except: 
            SavedPost.objects.create(post_id=post_id)  #can also pass instance
         
        return redirect(request.META.get('HTTP_REFERER'))


class PostUnsaveView(View):
    # This section unsaves User's posts
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try: # if exists we delete required savedpost 
            savedpost_obj =  SavedPost.objects.get(user=request.user, post_id=post_id)
            savedpost_obj.delete()
        except: # if not user id then we create id in db
            pass 
        return redirect(request.META.get('HTTP_REFERER'))

class PostLikeView(View):
    # This section adds likes to User's posts
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
         
        try: # if exists
            Like.objects.get(user=request.user, post_id=post_id)
            print("---postliked---")
            return JsonResponse({'Exists':1}, safe=False)
        except: # if not user id then we create id in db
            Like.objects.create(post_id=post_id)
            tot_lik = Like.objects.filter(user=request.user, post_id=post_id).count()  #counting total likes
            print("---postcreated---", tot_lik)
            return JsonResponse({'Created':tot_lik}, safe=False)
        # return redirect(request.META.get('HTTP_REFERER'))

class PostUnlikeView(View):
    # This section deletes Unlikes User's posts
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try: # if exists we delete required post 
            like_obj =  Like.objects.get(user=request.user, post_id=post_id)
            like_obj.delete()
            return JsonResponse({'like_delete':1}, safe=False)
        except: # if not then reload page
            return JsonResponse({'like_delete':0}, safe=False)
        # return redirect(request.META.get('HTTP_REFERER'))


class PostCommentView(View):
    # This section creates & saves User's Comments
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pid')
        # print("postid>>",post_id)
        try:
            comment_text = request.POST.get('myData')
            if comment_text:
                # print(comment_text)
                Comment.objects.create(post_id=post_id, text=comment_text)
            comments = Comment.objects.filter(post=post_id)[:5]  # getting last 5 records
          
                #serializing means- converting queryset obj to json str
            comments = serializers.serialize('json', comments)
            return JsonResponse(comments, safe=False)
        except Exception as e:
            comments ={'error':e}
            return JsonResponse(comments, safe=False)
       

class LikedPostView(View):
    # This section renders User's all-liked posts page
    template_name = 'core/liked_posts.html'
    def get(self, request, *args, **kwargs):

        #Accessing all liked post from post model using current user
        liked_posts = Like.objects.filter(user=request.user)
        context = {'liked_posts':liked_posts}
        return render(request, self.template_name, context)
        
class ExplorePostView(View):
    # This section renders all the user's top posts (order by desc of likes) 
    template_name = 'core/explore_posts.html'
    def get(self, request, *args, **kwargs):
        all_posts = Post.objects.annotate(count=Count('like')).order_by('-count')
        context = {'all_posts':all_posts}
        return render(request, self.template_name, context)



class FollowDoneView(View):
    # This section creates/increase User's follwed users
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)
        
        try:
            Follow.objects.get(user=request.user, followed=followed_user_obj)
        
        except:
            Follow.objects.create(followed=followed_user_obj)
        return redirect(request.META.get('HTTP_REFERER'))

class UnfollowDoneView(View):
    # This section unfollws/decrease current followed users
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)
        
        try:
            follow_obj=Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except:
           pass
        return redirect(request.META.get('HTTP_REFERER'))

