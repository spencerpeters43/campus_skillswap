from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import SkillPost, Review, Appointment
from .forms import RegisterForm, SkillPostForm, ReviewForm, AppointmentForm


def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    posts = SkillPost.objects.filter(is_active=True).annotate(avg_rating=Avg('reviews__rating'))

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__username__icontains=query)
        )
    if category:
        posts = posts.filter(category=category)

    categories = SkillPost.CATEGORY_CHOICES
    return render(request, 'home.html', {
        'posts': posts,
        'query': query,
        'selected_category': category,
        'categories': categories,
    })


def skill_detail(request, pk):
    post = get_object_or_404(SkillPost, pk=pk)
    reviews = post.reviews.select_related('reviewer')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    avg_rating = round(avg_rating, 1) if avg_rating else None

    user_review = None
    can_review = False
    can_book = False
    if request.user.is_authenticated:
        user_review = reviews.filter(reviewer=request.user).first()
        can_review = (request.user != post.author) and (user_review is None)
        can_book = request.user != post.author

    return render(request, 'skills/detail.html', {
        'post': post,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
        'can_review': can_review,
        'can_book': can_book,
        'review_form': ReviewForm(),
        'appointment_form': AppointmentForm(),
        'star_range': range(1, 6),
    })


@login_required
def add_review(request, pk):
    post = get_object_or_404(SkillPost, pk=pk)

    if request.user == post.author:
        messages.error(request, "You can't review your own skill.")
        return redirect('skill_detail', pk=pk)

    if post.reviews.filter(reviewer=request.user).exists():
        messages.error(request, "You've already reviewed this skill.")
        return redirect('skill_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.skill_post = post
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Your review has been posted!')

    return redirect('skill_detail', pk=pk)


@login_required
def book_appointment(request, pk):
    post = get_object_or_404(SkillPost, pk=pk)

    if request.user == post.author:
        messages.error(request, "You can't book your own skill.")
        return redirect('skill_detail', pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.skill_post = post
            appointment.requester = request.user
            appointment.save()
            messages.success(request, f'Appointment requested for {appointment.date} at {appointment.time.strftime("%I:%M %p")}!')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    return redirect('skill_detail', pk=pk)


@login_required
def appointments(request):
    my_bookings = Appointment.objects.filter(requester=request.user).select_related('skill_post', 'skill_post__author')
    incoming = Appointment.objects.filter(skill_post__author=request.user).select_related('skill_post', 'requester')
    return render(request, 'appointments.html', {
        'my_bookings': my_bookings,
        'incoming': incoming,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Campus SkillSwap, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    posts = SkillPost.objects.filter(author=request.user)
    return render(request, 'accounts/dashboard.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = SkillPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Skill post created!')
            return redirect('dashboard')
    else:
        form = SkillPostForm()
    return render(request, 'skills/form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(SkillPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = SkillPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill post updated!')
            return redirect('dashboard')
    else:
        form = SkillPostForm(instance=post)
    return render(request, 'skills/form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(SkillPost, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Skill post deleted.')
        return redirect('dashboard')
    return render(request, 'skills/confirm_delete.html', {'post': post})
