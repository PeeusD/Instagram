from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
User = get_user_model()

# Create your models here.


#Handling User Posts..
class Post(models.Model):
    text = models.CharField(max_length=150, blank=True, null=True)  #blank means empty values stored in memory, null means blank with no value allocated in memory
    image = models.ImageField(upload_to='post_images')  #storing to BASE DIR
    #adds _id succesive to fieldname in admin d-board when using foreign key; editable false means uneditable field 
    user = models.ForeignKey(User, on_delete= models.PROTECT, editable=False ) # many to one relationship
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']  #for ordering user's post in desc order using '-'
    
    def __str__(self) -> str:

        return str(self.pk)     #id field holds pk instance

  #current user saving automatically if not in db
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:   #for security issues if we delete db then set user= None
            user = None
        if not self.pk:
            self.user = user
        super(Post, self).save(*args, **kwargs)

    @property
    def likes_count(self):
        count=self.like_set.count()
        return count
    
    @property
    def comments_count(self):
        count=self.comment_set.count()
        return count




#Handling respective User's Comments
class Comment(models.Model):
    text = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)  #realted with user field
    user = models.ForeignKey(User, on_delete= models.CASCADE, editable=False)
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-commented_on']  #for ordering user's comment in desc order using '-'
        
    def __str__(self) -> str:
        return str(self.text)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:   #for security issues if we delete db then set user= None
            user = None
        if not self.pk:
            self.user = user
        super(Comment, self).save(*args, **kwargs)

  


#Handling Users Likes....
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)  #realted with user field
    user = models.ForeignKey(User, on_delete= models.CASCADE, editable=False)
    liked_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
        
    def __str__(self) -> str:
        return str(self.post.id)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:   # Added this snippet: for security issues if we delete db then it sets user= None
            user = None
        if not self.pk:
            self.user = user
        super(Like, self).save(*args, **kwargs)


#Handling Users Follow....
class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(User, related_name='follow_followed', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.user} ---> {self.followed}"
    #current user saving automatically if not in db
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:   #for security issues if we delete db then set user= None
            user = None
        if not self.pk:
            self.user = user
        super(Follow, self).save(*args, **kwargs)


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f" {self.post.id}"

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:   #for security issues if we delete db then set user= None
            user = None
        if not self.pk:
            self.user = user
        super(SavedPost, self).save(*args, **kwargs)
    
    