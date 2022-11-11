from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow
from .utils import get_page_obj


def index(request):
    """View main page"""
    template = 'posts/index.html'
    context = {}
    get_page_obj(
        Post.objects.select_related('author', 'group').all(), request, context
    )
    return render(request, template, context)


def group_list(request, slug):
    """view group information"""
    group = get_object_or_404(Group, slug=slug)
    context = {'group': group}
    get_page_obj(group.posts.select_related('author'), request, context)
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """view profile information"""
    author = get_object_or_404(User, username=username)
    following = (
        author.following.filter(user_id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )
    context = {'author': author, 'following': following}
    get_page_obj(author.posts.select_related('group'), request, context)
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """view a post detail page"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'), pk=post_id
    )
    context = {
        'post': post,
        'comments': post.comments.select_related('author'),
        'form': CommentForm(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Create a new post"""
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)
    template = 'posts/create_post.html'
    context = {'form': form, 'is_edit': False}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """editing an existing post"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'), pk=post_id
    )
    post_url = reverse('posts:post_detail', kwargs={'post_id': post.id})
    if request.user != post.author:
        return redirect(post_url)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(post_url)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'post_url': reverse('posts:post_edit', kwargs={'post_id': post.id}),
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(reverse('posts:post_detail', kwargs={'post_id': post.id}))


@login_required
def follow_index(request):
    """Сколько же времени похоронено здесь.
    Писать запросы с хвоста - особый путь"""
    queryset = Post.objects.select_related('author', 'group').filter(
        author__following__user=request.user
    )

    template = 'posts/follow.html'
    context = {}

    get_page_obj(queryset, request, context)
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Подписаться на автора"""
    author = get_object_or_404(User, username=username)

    if (
        request.user != author
        and not author.following.filter(user_id=request.user.id).exists()
    ):
        Follow.objects.create(user=request.user, author=author)

    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """# Дизлайк, отписка"""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        following = author.following.filter(user_id=request.user.id)
        if following.exists():
            following.delete()

    return redirect('posts:profile', username)
