from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserSignupForm, ProfileForm
from .models import Profile
from django.db import transaction


from django.shortcuts import render, redirect
from .forms import UserSignupForm, ProfileForm

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserSignupForm, ProfileForm
from .models import Game,GameAnalytics



def signup(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.preferences = profile_form.cleaned_data.get('preference', [])
            profile.save()

            return redirect('home')
        else:
            # Pass errors back to the template
            return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})

    user_form = UserSignupForm()
    profile_form = ProfileForm()
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})



def home(request):
    games = Game.objects.select_related('gameanalytics').all()

    # Group games by category
    games_by_category = {}
    for game in games:
        game.analytics = getattr(game, 'gameanalytics', None)  # Attach analytics directly
        if game.category not in games_by_category:
            games_by_category[game.category] = []
        games_by_category[game.category].append(game)

    return render(request, 'home.html', {'games_by_category': games_by_category})


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    analytics = get_object_or_404(GameAnalytics, game=game)
    return render(request, 'game_detail.html', {'game': game, 'analytics': analytics})