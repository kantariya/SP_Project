from django.contrib import admin
from .models import Profile, DeveloperProfile, Game, Review, GameAnalytics

admin.site.register(Profile)
admin.site.register(DeveloperProfile)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(GameAnalytics)
