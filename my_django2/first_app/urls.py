from django.urls import path
from first_app import views
app_name='first_app'

urlpatterns = [
		path('',views.PostListView.as_view(), name='list'),
		path('<int:pk>',views.PostDetailView.as_view() ,name='post_detail'),
		path('create/',views.CreatePostView.as_view() ,name='create'),
		path('update/<int:pk>',views.UpdatePostView.as_view() ,name='update'),
		path('delete/<int:pk>',views.DeletePostView.as_view(),name='delete'),
		path('draft/',views.DraftListView.as_view() ,name='draft'),
		path('comment/<int:pk>',views.add_comment_to_post,name='add_comment_to_post'),
		path('comment/<int:pk>/approve',views.approve_comment,name='approve_comment'),
		path('comment/<int:pk>/delete',views.delete_comment,name='delete_comment'),
		path('publish/<int:pk>',views.publish_post,name='publish_post'),		

]
