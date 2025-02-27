from django import forms
from django.contrib.auth.models import User
from .models import Profile, Game, Review, GameAnalytics


class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    preference = forms.MultipleChoiceField(
        choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Racing', 'Racing'), ('Sports', 'Sports')],
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, widget=forms.RadioSelect(), required=True)

    class Meta:
        model = Profile
        fields = ['user_type', 'preferences']


CATEGORY_CHOICES = [
    ('Sports', 'Sports'),
    ('Racing', 'Racing'),
    ('Adventure', 'Adventure'),
    ('Action', 'Action'),
]

class GameForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select())
    size = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter size like 2GB or 500MB'}))

    class Meta:
        model = Game
        fields = ['title', 'description', 'category', 'image_url']

# Review Form for users to leave a review and rating for a game
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5')
        return rating

# Game Analytics Form for admins to manage game analytics
class GameAnalyticsForm(forms.ModelForm):
    class Meta:
        model = GameAnalytics
        fields = ['total_downloads', 'system_requirements']

# Custom Admin Form for game validation
from django.contrib import admin

class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'category', 'image_url']

    def clean_title(self):
        title = self.cleaned_data['title']
        if Game.objects.filter(title=title).exists():
            raise forms.ValidationError('This game already exists.')
        return title

class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm
    list_display = ('title', 'developer', 'category', 'image_url')
