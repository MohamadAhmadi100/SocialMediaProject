from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from .forms import NewPostForm, EditPostForm, AddCommentForm, AddReplyForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.conf import settings
import redis


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


redis_con = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)


def post_detail(request, slug, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, is_reply=False)
    redis_con.hsetnx('post_views', post.id, 0)
    post_views = redis_con.hincrby('post_views', post.id)
    replies_count = 0
    for comment in comments:
        replies_count += comment.r_comment.count()
    is_liked = []
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user)
    form = AddCommentForm()
    reply_form = AddReplyForm()
    return render(request, 'posts/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'reply': reply_form,
                   'replies_count': replies_count, 'is_liked': is_liked, 'post_views': post_views})


@login_required
def add_comment(request, post_id):
    current_post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = current_post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'نظر شما ثبت شد', 'success')
    return redirect('posts:post_detail', current_post.created.year, current_post.created.month,
                    current_post.created.day, current_post.slug)


@login_required
def add_reply(request, post_id, comment_id):
    current_post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            r1 = form.save(commit=False)
            r1.user = request.user
            r1.post = current_post
            r1.reply = Comment.objects.get(pk=comment_id)
            r1.is_reply = True
            r1.save()
            messages.success(request, 'پاسخ شما ثبت شد', 'success')
    return redirect('posts:post_detail', current_post.created.year, current_post.created.month,
                    current_post.created.day, current_post.slug)


@login_required
def new_post(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = NewPostForm(request.POST)
            if form.is_valid():
                post_body = form.save(commit=False)
                post_body.user = request.user
                post_body.slug = f"{get_random_string(8, '0123456789')}" \
                                 f"-{slugify(form.cleaned_data['body'][:20], allow_unicode=True)}"
                post_body.save()
                messages.success(request, 'پست جدید با موفقیت ایجاد شد', 'success')
                return redirect('account:profile', user_id)

        else:
            form = NewPostForm()
        return render(request, 'posts/new_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def post_delete(request, user_id, post_id):
    if request.user.id == user_id:
        Post.objects.filter(pk=post_id).delete()
        messages.success(request, 'محتوا با موفقیت حذف شد', 'success')
        return redirect('account:profile', user_id)
    else:
        messages.error(request, 'دسترسی مسدود می باشد', 'danger')
        return redirect('posts:all_posts')


@login_required
def post_edit(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                edit_post_body = form.save(commit=False)
                edit_post_body.user = request.user
                edit_post_body.slug = post.slug
                edit_post_body.save()
                messages.success(request, 'ویرایش با موفقیت انجام شد', 'success')
                return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.slug)

        else:
            form = EditPostForm(instance=post)
        return render(request, 'posts/edit_post.html', {'form': form})
    else:
        messages.error(request, 'دسترسی مسدود می باشد', 'danger')
        return redirect('posts:all_posts')


def like_post(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, pk=post_id)
        liked = Like.objects.filter(post=post, user=request.user)
        if liked.exists():
            liked.delete()
            total_likes = post.likes_count()
            return JsonResponse({'status': 'unliked', 'total_likes': total_likes})
        else:
            Like(post=post, user=request.user).save()
            total_likes = post.likes_count()
            return JsonResponse({'status': 'liked', 'total_likes': total_likes})
    else:
        return JsonResponse({'status': 'not_exists'})
