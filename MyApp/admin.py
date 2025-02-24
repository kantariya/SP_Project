from django.contrib import admin
from .models import Profile, Game, Review, GameAnalytics


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'preferences')  # Shows these fields in the admin list view
    list_filter = ('user_type',)  # Filter by user type
    search_fields = ('user__username',)  # Allow searching by username


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'developer', 'image_url')  # Important fields to show
    list_filter = ('category',)  # Filter by category
    search_fields = ('title', 'developer__username')  # Search by game title and developer’s username


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'rating', 'created_at')  # Useful review details
    list_filter = ('rating', 'created_at')  # Filter by rating and creation date
    search_fields = ('game__title', 'user__username')  # Search reviews by game title or reviewer username


@admin.register(GameAnalytics)
class GameAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('game', 'total_downloads', 'last_updated')  # Key analytics data
    search_fields = ('game__title',)  # Search analytics by game title
