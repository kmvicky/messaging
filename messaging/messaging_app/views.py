import re
import uuid
import base64
import string
import random
import logging
import difflib
import mimetypes


from messaging.messaging_app.models import *
from messaging.messaging_app.utils import *
from messaging.messaging_app.forms import *
from messaging.messaging_app.send_email import send_email


from django.shortcuts import *
from django.conf import settings
from django.utils import timezone
from django.db.models import Value
from django.contrib import messages
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models.functions import Concat
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static


class EmployeeConversation(TemplateView):

	def get(self, request, employee_id, *args, **kwargs):

		try:
		
			self.template_name = 'messaging_app/conversions.html'

			context = dict()

			employee = Employee.objects.get(employee__id=employee_id)

			can_start_conversion = False
			can_delete_comment = False
			start_new = reverse('messaging_app:add-conversation')

			if employee.is_recruiter:
				can_start_conversion = True
				conversions = Conversation.objects.all()
			else:
				conversions = Conversation.objects.filter(sent_to=employee.employee)

			if employee.recruiter_type == 'R1':
				can_delete_comment = True

			context.update({
				'start_new': start_new,
				'conversions': conversions,
				'can_delete_comment': can_delete_comment,
				'can_start_conversion': can_start_conversion
			})

			return self.render_to_response(context)

		except Exception as e:
			print(e)
			raise Http404()


class Landing(TemplateView):

	def get(self, request, *args, **kwargs):

		self.template_name = 'messaging_app/homepage.html'

		context = dict()

		try:
			if request.user.is_authenticated:
				return redirect(reverse('messaging_app:employee', args=(request.user.id, )))
			else:
				print('redirect')
				return redirect(reverse('messaging_app:login'))

		except Exception as e:
			print(e)
			raise Http404()



class Login(TemplateView):

	form_class = LoginForm
	template_name = 'messaging_app/login.html'
	warning = ''

	def get(self, request, *args, **kwargs):

		self.template_name = 'messaging_app/login.html'

		action = reverse('messaging_app:login')

		context = {
			'action': action
		}

		storage = messages.get_messages(request)
		storage.used = True
		
		if request.user.is_authenticated:
			return redirect(reverse('messaging_app:landing'))

		return self.render_to_response(context)


	def post(self, request, *args, **kwargs):

		data = request.POST.dict()

		username = data.get('username')
		password = data.get('password')

		user = authenticate(request, username=username, password=password)

		context = dict()

		if user is not None:
			login(request, user)

			employee = Employee.objects.get(employee=user)
			
			return redirect(reverse('messaging_app:employee', args=(employee.id, )))
		else:
			return HttpResponse('Username or password is incorrect')



class Logout(View):

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		
		user = request.user

		if request.user.is_authenticated:
			logout(request)
		
		return redirect(reverse('messaging_app:login'))		



class RegisterUser(TemplateView):

	def get(self, request, *args, **kwargs):

		context = {
			'action': reverse('messaging_app:register-user')
		}

		self.template_name = 'messaging_app/signup.html'

		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):

		try:

			data = request.POST.dict()

			context = dict()

			email = data.get('email')
			password = data.get('password')
			last_name = data.get('lastname')
			first_name = data.get('firstname')
			employee_type = data.get('employeeType')

			if not employee_type:
				return HttpResponse('Please select employee type')

			if not email:
				return HttpResponse('Please provide email address')

			if not first_name:
				return HttpResponse('Please provide first name')

			if not last_name:
				return HttpResponse('Please provide last name')

			if not password:
				return HttpResponse('Please provide password for the user')

			is_recruiter = False
			is_candidate = False
			recruiter_type = None

			if employee_type in ['R1', 'R2']:
				is_recruiter = True
				recruiter_type = employee_type
			else:
				is_candidate = True

			data = {
				'email': email,
				'username': email,
				'last_name': last_name,
				'first_name': first_name
			}

			if not User.objects.filter(email=email).exists():
				user = User.objects.create(**data)

				user.set_password(password)
				user.save()

				employee_data = {
					'employee': user,
					'is_recruiter': is_recruiter,
					'is_candidate': is_candidate,
					'recruiter_type': recruiter_type
				}

				employee = Employee.objects.create(**employee_data)

				return redirect(reverse('messaging_app:employee', args=(employee.id, )))

			else:
				return HttpResponse('Provided email address is already registered, Please provide a different email address')

			return redirect(reverse('hostel:landing'))

		except Exception as e:
			print(e)
			return HttpResponseNotFound('User could not be registered')



class ConversationDetail(TemplateView):

	def get(self, request, conversation_id, *args, **kwargs):
		
		try:
			self.template_name = 'messaging_app/conversation-detail.html'

			conversation = Conversation.objects.get(id=conversation_id)

			messages  = Comments.objects.filter(conversation=conversation)

			employee = Employee.objects.get(employee__id=request.user.id)

			can_start_conversion = False
			can_delete_comment = False
			start_new = reverse('messaging_app:add-conversation')

			if employee.is_recruiter:
				can_start_conversion = True
				conversions = Conversation.objects.all()
			else:
				conversions = Conversation.objects.filter(sent_to=employee.employee)

			if employee.recruiter_type == 'R1':
				can_delete_comment = True

			action = reverse('messaging_app:add-comment', args=(conversation.id, ))

			context = {
				'action': action,
				'messages': messages,
				'start_new': start_new,
				'conversions': conversions,
				'conversation': conversation,
				'can_delete_comment': can_delete_comment,
				'can_start_conversion': can_start_conversion
			}

			return self.render_to_response(context)

		except Exception as e:
			print(e)
			return HttpResponseNotFound('Comments could not fetched')



class AddConvesation(TemplateView):

	def get(self, request, *args, **kwargs):
		try:
			self.template_name = 'messaging_app/add-conversation.html'

			employees = Employee.objects.filter(is_candidate=True)

			context = {
				'employees': employees,
				'action': reverse('messaging_app:add-conversation')
			}

			return self.render_to_response(context)

		except Exception as e:
			return HttpResponseNotFound('New conversion could not be started')


	def post(self, request, *args, **kwargs):
		
		try:

			data = request.POST.dict()

			employee_id = int(data.get('employeeId'))
			description = data.get('description')

			sent_to = User.objects.get(id=employee_id)
			sent_by = request.user

			conversion_data = {
				'sent_to': sent_to,
				'sent_by': sent_by,
				'created_by': sent_by,
				'modified_by': sent_by,
				'description': description
			}

			conversion = Conversation.objects.create(**conversion_data)

			return redirect(reverse('messaging_app:conversation-detail', args=(conversion.id, )))

		except Exception as e:
			print(e)
			return HttpResponseNotFound('New conversion could not be started')



class AddComment(TemplateView):

	def get(self, request, conversation_id, comment_id=None, *args, **kwargs):

		try:
			self.template_name = 'messaging_app/update-comment.html'

			if comment_id:
				comment = Comments.objects.get(id=comment_id)
				action = reverse('messaging_app:update-comment', args=(comment.conversation.id, comment.id, ))
			else:
				comment = None
				action = reverse('messaging_app:add-comment', args=(comment.conversation.id, ))


			context = {
				'action': action,
				'comment': comment
			}

			return self.render_to_response(context)

		except Exception as e:
			print(e)
			return HttpResponseNotFound('Comment could not be added')

	
	def post(self, request, conversation_id, comment_id=None, *args, **kwargs):

		try:
			data = request.POST.dict()

			conversation = Conversation.objects.get(id=conversation_id)

			comment_text = data.get('comment')

			comment_data = {
				'comment': comment_text,
				'conversation': conversation,
				'created_by': request.user,
				'modified_by': request.user
			}

			if comment_id:
				comment = Comments.objects.get(id=comment_id)
				comment.comment = comment_text
				comment.modified_by = request.user
				comment.save()

			else:
				comment = Comments.objects.create(**comment_data)

			if not request.user == conversation.created_by:
				# This is not working
				sender = request.user.get_full_name()
				send_to = conversation.created_by.get_full_name()

				email_data = {
					'sender': sender,
					'send_to': send_to,
					'comment': comment,
					'sender_email':request.user.email,
					'receiver_email': conversation.created_by.email
				}

				try:
					send_email(email_data)
				except Exception as e:
					print(e)

			return redirect(reverse('messaging_app:conversation-detail', args=(conversation.id, )))

		except Exception as e:
			print(e)
			return HttpResponseNotFound('Comment could not be added')



class DeleteComment(View):

	def get(self, request, comment_id, *args, **kwargs):

		try:
			data = request.GET.dict()

			comment = Comments.objects.get(id=comment_id)

			conversation = comment.conversation

			comment.is_deleted = True
			comment.deleted_by = request.user
			comment.deleted_on = timezone.now()
			comment.save()

			return redirect(reverse('messaging_app:conversation-detail', args=(conversation.id, )))

		except Exception as e:
			print(e)
			return HttpResponseNotFound('Comment could not be added')
