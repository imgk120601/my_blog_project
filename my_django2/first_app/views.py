from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import ListView,DetailView,UpdateView,CreateView,DeleteView
from first_app.models import Post,Comment
from first_app.forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse  
from first_app import forms 

def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

class PostListView(ListView):
	context_object_name='post'
	model=Post
	template_name='post_list.html'

	def get_queryset(self):# it is basically Pytonish version of SQLite Query
# filter out all query(post)from Post model whose published_date is'less than or equal to'
#(lte) timezone.now() in desecding order by published_date('-published_date')--means reverse
		return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') 


class PostDetailView(DetailView):
	context_object_name='post_detail'
	model=Post
	template_name='post_detail.html'

class CreatePostView( LoginRequiredMixin ,CreateView):
	login_url='/login/' #if a person is not logged in go to '/login/'
	redirect_field_name='post_detail.html' #redirext them to post_detail.html
	form_class=PostForm
	model=Post
	template_name='post_form.html'

class UpdatePostView( LoginRequiredMixin ,UpdateView):
	login_url='/login/' #if a person is not logged in go to '/login/'
	redirect_field_name='post_detail.html ' #redirext them to post_detail.html
	form_class=PostForm
	model=Post
	 
	template_name='post_form.html'

class DeletePostView(LoginRequiredMixin , DeleteView):
	model=Post
	template_name='post_confirm_delete.html'
	success_url=reverse_lazy('first_app:list')


class DraftListView(LoginRequiredMixin,ListView):
	login_url='/login/'
	redirect_field_name='post_draft_list.html'
	model=Post

	def get_queryset(self):#filter out all the query which has published_date=null or not publisher save them in ListView as Draft.
		return Post.objects.filter(published_date__isnull=True).order_by('create_date') 

############################################################
############################################################
def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')				#after submit when you come here name column in input name='username'
		password=request.POST.get('password')  #after submit when you come here name column in input name='password'

		user=authenticate(username=	username,password= password)  #it will authenticate it is valid or not

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('first_app:list'))   #it will redirect it to the index.html
			else:
				return HttpResponse('Account is not active!!!!!')
		else:
			print('Some tried to login and failed')                   #printing in console
			print('Username: {} and Password: {}'.format(username,password))
			return HttpResponse('Invalid login details provided')
	else:
		return	render(request,'login.html')

@login_required        #inbuilt decorator that ensure you are logged in
def user_logout(request):
	logout(	request)
	return HttpResponseRedirect(reverse('index'))

#################################### for the comments
####################################

@login_required
def publish_post(request,pk):
	post=get_object_or_404(Post,pk=pk)
	post.publish()
	return redirect('post_detail',pk=post.pk) 

@login_required
def add_comment_to_post(request,pk): #adding comment to specific post(pk)
	post=get_object_or_404(Post,pk=pk)
	if request.method=='POST': #if sumbody fill the form hit the submit button
		form= CommentForm(request.POST)
		if form.is_valid():
			comment=form.save(commit=False) #filling is not *required
			comment.post=post #connecting comment to specific post ---check Comment model Comment's post field is equal to post itself
			comment.save()
			return redirect('first_app:post_detail',pk=post.pk)
	else:
		form=CommentForm()
	return render(request,'comment_form.html',{'form':form})

@login_required
def approve_comment(request,pk):  #a superuser will approve the comment 
	comment=get_object_or_404(Comment,pk=pk)
	comment.approve()              #in Comment there is def approve() it will approve
	return redirect('first_app:post_detail',pk=comment.post.pk)  #Comment and Post are linked pk is equal to comment.post.pk

@login_required
def delete_comment(request,pk):
	comment=get_object_or_404(Comment,pk=pk)
	post_pk=comment.post.pk#here post in comment it just ----def ():---- so it is called by just--.post--
							# and if is inbuilt function like delete,save they will be called as ---.save()----
	comment.delete()              #it will delete comment permanent(its inbuit function)
	return redirect('first_app:post_detail',pk=post_pk) 
def registration(request):
	registered=False
	if request.method=='POST':
		user_form=forms.UserForm(data=request.POST)
		profile_form=forms.UserProfileInfoForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()#profile_form modelform(UserForm) which has model=User and 
								#field=('username','email','password')

			user.set_password(user.password)#here in user.password user represent
			#this called password hashing go to settings.py#we have created password instance in UserForm (modelform) in form.py
			user.save()

			profile=profile_form.save(commit=False)#profile_form modelform(UserProfileInfoForm) which has model=UserProfileInfo and 
										#field=(portfolio_site,profile_pic)
			profile.user=user         #we have assign profile's user as user(in model.py)

			
			if 'profile_pic'in request.FILES:
				profile.profile_pic=request.FILES['profile_pic']
				print('its image here')
			print(request.FILES)

			profile.save()

			registered=True


		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form=forms.UserForm()
		profile_form=forms.UserProfileInfoForm()

	return render(request,'registration.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})


























