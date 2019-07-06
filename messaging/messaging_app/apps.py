from django.apps import AppConfig

class MessagingAppConfig(AppConfig):

	name = 'messaging.messaging_app'
	verbose_name = 'messaging_app'

	def ready(self):
		pass