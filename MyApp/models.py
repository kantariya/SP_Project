from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # For PostgreSQL

class Profile(models.Model):
    USER_TYPES = [
        ('user', 'Normal User'),
        ('developer', 'Developer'),
    ]   

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')  # Identifies user type
    preferences = models.JSONField(blank=True, default=list)  # Stores user's preferred categories

    def is_developer(self):
        return self.user_type == 'developer'  # Helper method to check if the user is a developer

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)  # Storing category as text
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="developed_games")  # Now links directly to User model
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating})"

class GameAnalytics(models.Model):
    game = models.OneToOneField('Game', on_delete=models.CASCADE)
    total_downloads = models.IntegerField(default=0)
    system_requirements = models.TextField()
    size = models.TextField(blank=True, help_text="Enter game size (e.g., '500 MB' or '2.5 GB')")  # Updated to TextField
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.game.title}"

