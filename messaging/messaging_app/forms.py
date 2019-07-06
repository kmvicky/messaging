from django import forms
from django.conf import settings
from django.contrib.auth import authenticate



class LoginForm(forms.Form):

	"""Standard username and password authentication form."""

	username = forms.CharField(label="Email address",
		error_messages={'required': "Please enter your username"})
	password = forms.CharField(label="Password", 
		widget=forms.PasswordInput, 
		error_messages={'required': "Please enter your password"})

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)


	def clean(self):
		"""
		Pass the provided username and password to the active
		authentication backends and verify the user account is
		not disabled. If authentication succeeds, the ``User`` object
		is assigned to the form so it can be accessed in the view.
		"""
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		username = username.lower()


		if username and password:
			try:
				self.user = authenticate(username=username, password=password)
			except Exception as e:
				error_msg = 'Internal error while authenticating user'
				raise forms.ValidationError(error_msg)

			if self.user is None:
				error_msg = 'The username or password is not correct'
				raise forms.ValidationError(error_msg)
			else:
				if not self.user.is_active:
					error_msg = 'This user account is disabled'
					raise forms.ValidationError(error_msg)

		return self.cleaned_data