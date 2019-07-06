from django.db import models
from django.contrib.auth.models import User
from messaging.messaging_app.managers import *



class BaseModel(models.Model):

	class Meta:
		abstract = True
	
	objects			= BaseModelManager()
	created_by 		= models.ForeignKey(User, 
						related_name='%(app_label)s_%(class)s_creator',
						on_delete=models.CASCADE)
	created_on 		= models.DateTimeField(auto_now_add=True)
	modified_by 	= models.ForeignKey(User, 
						related_name='%(app_label)s_%(class)s_modifier',
						on_delete=models.CASCADE)
	modified_on		= models.DateTimeField(auto_now=True)
	deleted_by		= models.ForeignKey(User, null=True, blank=True, 
						related_name='%(app_label)s_%(class)s_deleter',
						on_delete=models.CASCADE)
	deleted_on		= models.DateTimeField(null=True, blank=True)
	is_deleted		= models.BooleanField(default=False)

	def save(self, *args, **kwargs):
	
		if not self.id or not self.created_on:
			self.created_on = timezone.now()
	
		return super(BaseModel,	self).save(*args, **kwargs)


class Employee(models.Model):

	RECRUITER_TYPE = (
		('R1', 'Primary Recruiter'),
		('R2', 'Secondary Recruiter')
	)

	employee 		= models.ForeignKey(User, on_delete=models.CASCADE)
	is_recruiter 	= models.BooleanField(default=False)
	is_candidate	= models.BooleanField(default=False)
	recruiter_type 	= models.CharField(max_length=2, choices=RECRUITER_TYPE,
						null=True, blank=True)

	def __str__(self):
		return self.employee.get_full_name()


class Conversation(BaseModel):

	sent_by 	= models.ForeignKey(User, related_name='sent_by',
					on_delete=models.CASCADE)
	sent_to		= models.ForeignKey(User, related_name='sent_to',
					on_delete=models.CASCADE)
	description = models.CharField(max_length=1024)

	def __str__(self):
		return self.sent_by.get_full_name()



class Comments(BaseModel):

	conversation 	= models.ForeignKey(Conversation, on_delete=models.CASCADE)
	comment 		= models.CharField(max_length=1024)

	def __str__(self):
		return self.comment

