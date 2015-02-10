from django.db import models

class UserProfile(models.Model):
	avatar = models.ImageField(upload_to='avatars')
	user = models.OneToOneField(User)

	def __str__(self):
		return self.user.username

class UserTrack(models.Model):
	"""count"""
	count = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User)
	track = models.ForeignKey(Track)