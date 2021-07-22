from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post
# Create your views here.


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user.username
        instance.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    #instance = Post.objects.get(id=2)
    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish>timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        'content_type': instance.get_content_type,
        'object_id':instance.id
    }
    print(instance.get_content_type)
    #####To Addd comments functionality here!!!!
    comments = Comment.objects.filter_by_instance(instance)
    comment_form = CommentForm(request.POST or None,initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated:
        content_data = comment_form.cleaned_data.get('content')
        new_comment, created = Comment.objects.get_or_create(user=request.user,content_type=instance.get_content_type,object_id=instance.id,content=content_data)
        if created:
            print('Yaye! created...')
    comp_url = 'http://127.0.0.1:8000' + request.get_full_path()
    context = {
        'post_detail': instance,
        'share_string': share_string,
        'comp_url': comp_url,
        'comments': comments,
        'comment_form':comment_form,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    context = {
        'obj_list': queryset,
        'today':today,
    }
    return render(request, "post_list.html", context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('posts:list')


