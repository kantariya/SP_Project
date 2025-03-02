from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserSignupForm, ProfileForm
from .models import Profile
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Review  


from django.shortcuts import render, redirect
from .forms import UserSignupForm, ProfileForm

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserSignupForm, ProfileForm
from .models import Game,GameAnalytics
from .forms import GameForm, GameAnalyticsForm
from .forms import ReviewForm



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

            return redirect('/login')
        else:
            # Pass errors back to the template
            return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})

    user_form = UserSignupForm()
    profile_form = ProfileForm()
    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Assuming 'home' is the name of your home page URL
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



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


# Game detail view with reviews
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    analytics = GameAnalytics.objects.get(game=game)
    reviews = game.reviews.all()  # <- Make sure you're passing reviews!
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = ReviewForm()

    return render(request, 'game_detail.html', {
        'game': game,
        'analytics': analytics,
        'reviews': reviews,  # <- Don't forget this!
        'form': form
    })


# Add review view
@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
            return redirect('game_detail', game_id=game.id)
    return redirect('game_detail', game_id=game.id)

# Delete review view
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
    return redirect('game_detail', game_id=review.game.id)

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return redirect('game_detail', game_id=review.game.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('game_detail', game_id=review.game.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'games/update_review.html', {'form': form, 'review': review})

@login_required
def add_game(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'developer':
        messages.error(request, "Only developers can add games.")
        return redirect('home')

    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()

            # Save game analytics
            GameAnalytics.objects.create(
                game=game,
                total_downloads=request.POST.get('total_downloads', 0),
                system_requirements=request.POST.get('system_requirements', ''),
                size=request.POST.get('size', '')
            )

            messages.success(request, "Game added successfully!")
            return redirect('home')
    else:
        form = GameForm()

    return render(request, 'add_game.html', {'form': form})



def category_games(request, category):
    games = Game.objects.filter(category__iexact=category)  # Case-insensitive match
    return render(request, 'games/category_games.html', {'games': games, 'category': category})


def action_games(request):
    return category_games(request, 'Action')


def adventure_games(request):
    return category_games(request, 'Adventure')


def racing_games(request):
    return category_games(request, 'Racing')


def sports_games(request):
    return category_games(request, 'Sports')