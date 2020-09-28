from django.contrib import admin

from .models import (
	Contest,
	Team,
	Member,
	Category,
	Round,
	Grade,
	)

admin.site.register(Contest)
admin.site.register(Team)
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Round)
admin.site.register(Grade)