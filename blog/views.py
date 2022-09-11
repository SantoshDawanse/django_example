from re import L
from django.shortcuts import render

from blog.models import Post, Comment, Category
from blog.forms import CommentForm
from django.db.models import Q

def parse_search_phrase(allowed_fields, phrase):
    base_qs = Q()
    for field in allowed_fields:
        st = f"{allowed_fields[field]}__contains={phrase}"
        base_qs.add(Q(st), Q.OR)

    print(base_qs)
    return base_qs
    # return Q(categories__name__contains=phrase)

# Create your views here.
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    allowed_fields = {"name": Post.categories.field.name}
    filter = parse_search_phrase(allowed_fields, category)
    print
    posts = Post.objects.filter(filter).order_by(
        "-created_on"
    )
    print(posts)
    context = {"category": category, "posts": posts}
    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments, "form": form,}

    return render(request, "blog_detail.html", context)

def blog_filter(request, cat):
    # print("here")
    posts = Post.objects.filter(categories__name__contains=cat).order_by(
        "-created_on"
    )
    context = {"category": cat, "posts": posts}
    return render(request, "blog_category.html", context)