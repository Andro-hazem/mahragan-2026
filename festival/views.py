from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Work, Vote, Comment
from django.db.models import Count
from .forms import RegisterForm, CommentForm

def home(request):
    categories = Category.objects.all()
    works = Work.objects.all()

    # Filter by category if the user selected one
    category_id = request.GET.get('category')
    if category_id:
        works = works.filter(category__id=category_id)

    # Sort based on user selection
    sort = request.GET.get('sort', 'newest')
    if sort == 'newest':
        works = works.order_by('-submitted_at')
    elif sort == 'oldest':
        works = works.order_by('submitted_at')
    elif sort == 'most_voted':
        works = works.annotate(total_votes=Count('votes')).order_by('-total_votes')
    elif sort == 'least_voted':
        works = works.annotate(total_votes=Count('votes')).order_by('total_votes')

    return render(request, 'festival/home.html', {
        'categories': categories,
        'works': works,
        'selected_category': category_id,
        'selected_sort': sort,
    })


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    works = category.works.all().order_by('-submitted_at')
    return render(request, 'festival/category_detail.html', {
        'category': category,
        'works': works,
    })


def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    comments = work.comments.all().order_by('-created_at')
    user_has_voted = False
    comment_form = CommentForm()

    if request.user.is_authenticated:
        user_has_voted = Vote.objects.filter(user=request.user, work=work).exists()

    return render(request, 'festival/work_detail.html', {
        'work': work,
        'comments': comments,
        'user_has_voted': user_has_voted,
        'comment_form': comment_form,
    })


@login_required
def vote(request, pk):
    work = get_object_or_404(Work, pk=pk)

    if Vote.objects.filter(user=request.user, work=work).exists():
        messages.warning(request, 'You have already voted for this work.')
    else:
        Vote.objects.create(user=request.user, work=work)
        messages.success(request, 'Your vote has been recorded!')

    return redirect('work_detail', pk=pk)


@login_required
def add_comment(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # don't save to DB yet
            comment.user = request.user        # attach the logged in user
            comment.work = work                # attach the work
            comment.save()                     # now save to DB
            messages.success(request, 'Comment added!')
        else:
            messages.warning(request, 'Comment cannot be empty.')
    return redirect('work_detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
