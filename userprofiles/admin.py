from django.contrib import admin

from .models import UserTrack, UserProfile

from sorl.thumbnail import get_thumbnail

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'avatar')

	def imagen_avatar(self, obj):
		return '<img src="%s">' % obj.avatar.url
		# return '<img src="%s">' % get_thumbnail(obj.cover, '50x50').url 
	imagen_avatar.allow_tags = True

admin.site.register(UserProfile)
admin.site.register(UserTrack)
#admin.site.register(UserProfileAdmin)