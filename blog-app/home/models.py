from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from django.core.files import File


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

class BlogPost(models.Model):
    title=models.CharField(max_length=255)
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    slug=models.CharField(max_length=130)
    content=models.TextField()    
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    image_data = models.BinaryField(blank = True, null = True, editable=True)
    dateTime=models.DateTimeField(auto_now_add=True)

    # def get_remote_image(self):
    #     print("inside image convert function")
    #     if self.image_url and not self.image_file:
    #         result = urllib.urlretrieve(self.image_url)
    #         self.image_file.save(
    #                 os.path.basename(self.image_url),
    #                 File(open(result[0]))
    #                 )
    #         self.save()
    
    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    
    def get_absolute_url(self):
        return reverse('blogs')
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    

