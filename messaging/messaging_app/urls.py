import messaging_app.views as views

from django.urls import include, path, re_path

app_name = 'messaging_app'

urlpatterns = [

	path('login/', 
		views.Login.as_view(),
		 name='login'),

	path('logout/', 
		views.Logout.as_view(),
		 name='logout'),

	path('register-user/', 
		views.RegisterUser.as_view(),
		 name='register-user'),

	re_path(r'^employee/(?P<employee_id>\d+)/$', 
		views.EmployeeConversation.as_view(),
		 name='employee'),

	re_path(r'^conversation-detail/(?P<conversation_id>\d+)/$', 
		views.ConversationDetail.as_view(),
		 name='conversation-detail'),

	path('add-conversation/',
		views.AddConvesation.as_view(),
		 name='add-conversation'),

	re_path(r'^add-comment/(?P<conversation_id>\d+)/$', 
		views.AddComment.as_view(),
		 name='add-comment'),

	re_path(r'^update-comment/(?P<conversation_id>\d+)/(?P<comment_id>\d+)/$', 
		views.AddComment.as_view(),
		 name='update-comment'),

	re_path(r'^delete-comment/(?P<comment_id>\d+)/$', 
		views.DeleteComment.as_view(),
		 name='delete-comment'),

	path('', 
		views.Landing.as_view(),
		 name='landing'),
]