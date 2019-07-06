from django.db import models
from django.utils import timezone


class BaseDatedQuerySet(models.QuerySet):

	def deleted(self, *args, **kwargs):
		kwargs.update({'is_deleted': True})
		return self.filter(**kwargs)



class BaseModelManager(models.Manager):
	
	def get_queryset(self):
		return (
			super(BaseModelManager, self)
				.get_queryset()
				.filter(is_deleted=False)
			)

	def deleted(self, *args, **kwargs):
		return BaseDatedQuerySet(self.model, using=self._db).deleted(*args, **kwargs)