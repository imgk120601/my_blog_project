from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



class UserProfileInfo(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE) #in this usename,first name,last name etc...is already in included
	
	#Additional
	portfolio_site=models.URLField(blank=True)
	profile_pic=models.ImageField(upload_to='profile_pic',blank=True) #Upload_to -- profile_pics--is a folder in media
																		#for the ImageField pip install pillow
	def __str__(self):
		return self.user.username



class Post(models.Model):
	author=models.ForeignKey('auth.User',on_delete=models.CASCADE) #someone who can author some post(superuser type)
	title=models.CharField(max_length=250)
	text=models.TextField()
	create_date=models.DateTimeField(default=timezone.now)
	published_date=models.DateTimeField(default=timezone.now) #not wanna publish now

	def publish(self): #when click publish button
		self.published_date=timezone.now()
		self.save()	

	def get_absolute_url(self): #after clicking publish(self.save()) it will redirect us
		return reverse('first_app:post_detail',kwargs={'pk':self.pk}) #here 'post_detail' is template page of DetailView with need a pk value

	def approve_comments(self): # after clicking it.it will filter all approved comment and post it along with the post
		return self.comments.filter(approved_comments=True)

	def	__str__(self):
		return self.title

class Comment(models.Model):
	post=models.ForeignKey('first_app.Post',on_delete=models.CASCADE,related_name='comments') #we have join two classes with ForeignKey()
	author=models.CharField(max_length=200) #any one can comment
	text=models.TextField()
	create_date=models.DateTimeField(default=timezone.now)
	approved_comments=models.BooleanField(default=False) #default it is not approved
	
	def approve(self): #it will approve it
		self.approved_comments=True
		self.save()  #just after approval by superuser it will be posted on page(self.save())

	def get_absolute_url(self):
		return reverse('post_list') #here post_list is a html template page of ListView

	def __str__(self):
		return self.text	