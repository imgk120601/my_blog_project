from django import forms
from first_app.models import Post , Comment
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo

class PostForm(forms.ModelForm):
	class Meta:
		model=Post #choose our model
		fields=('author','title','text') #choosing fields which we can edit here

		widgets={   #adding  widgets to fields,css styling ,css class eg..('class':'textinputclass')
			'title':forms.TextInput(attrs={'class':'textinputclass'}),  #here we are using only one css class 'textinputclass' respective of widget TextInput
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})#we have use 3 css class editable(we can edit it), medium-editor-textarea(special--when you hover over some text it display basic editing option like bold,italic etc..) ,postcontent(i don't know)
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=('author','text')

		widgets={   #adding  widgets to fields,css styling ,css class eg..('class':'textinputclass')
			'author':forms.TextInput(attrs={'class':'textinputclass'}),  #here we are using only one css class 'textinputclass' respective of widget TextInput
			'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})#we have use 3 css class editable(we can edit it), medium-editor-textarea(special--when you hover over some text it display basic editing option like bold,italic etc..) ,postcontent(i don't know)
		}
		
class UserForm(forms.ModelForm):      #thsi is must in forms.ModelForm 
	password=forms.CharField(widget=forms.PasswordInput)#we have added password field in user's built-in field

	class Meta:      #use meta class in forms.ModelForm
		model=User 		#use model=User  and use in-built fields of User
		fields=('username','email','password')

class UserProfileInfoForm(forms.ModelForm):       #this is using models.py's class
	#already in herited
	class Meta:                      #in this use model='classname'(in models.py)
		model=UserProfileInfo			#field=('extra field created by us in')
		fields=('portfolio_site','profile_pic')