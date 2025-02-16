from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # For PostgreSQL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = ArrayField(models.CharField(max_length=100), blank=True, default=list)  # Preferred categories
    wishlist = models.ManyToManyField('Game', blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True)

    def __str__(self):
        return self.user.username

class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)  # Storing category as text
    developer = models.ForeignKey(DeveloperProfile, on_delete=models.CASCADE)
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
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    total_downloads = models.IntegerField(default=0)
    system_requirements = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.game.title}"
