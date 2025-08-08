from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Profile
from .forms import LoginForm, ProfileForm


def mask_name(name: str) -> str:

    length = len(name)
    if length == 1:
        return "Ｏ"
    if length == 2:
        return name[0] + "Ｏ"
    return name[0] + "Ｏ" * (length - 2) + name[-1]


@login_required(login_url="users:login")
def index(request):
    """用於顯示 user 首頁的視圖函數。"""
    return render(request, "users/index.html", {})


def login(request):
    """用於處理用戶登錄操作的視圖函數。"""
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.login(request)
            Profile.objects.get_or_create(user=request.user)[0]
            return redirect("users:index")
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)


def logout(request):
    """用於處理用戶登出操作的視圖函數。"""
    auth_logout(request)
    return redirect("users:login")


def profile(request, slug=None):
    """
    顯示用戶個人資料的視圖函數。

    如果 Profile 不存在，則創建一個新的 Profile。

    顯示 Profile 的基本資料，並顯示 Profile 的 slug。
    """

    profile = get_object_or_404(Profile, slug=slug)

    if not profile.is_public and request.user != profile.user:
        raise Http404

    is_owner = (request.user == profile.user)
    raw_name = profile.full_name or profile.user.username
    display_name = raw_name if is_owner else mask_name(raw_name)
    full_url = request.build_absolute_uri(request.path)

    content = {
        "profile": profile,
        "is_owner": is_owner,
        "display_name": display_name,
        "full_url": full_url,
    }

    return render(request, "users/profile_detail.html", content)


@login_required(login_url="users:login")
def profile_edit(request):
    """
    用於編輯用戶個人資料的視圖函數。

    如果請求方法為 POST，則驗證並保存表單數據。
    如果表單有效，重定向到用戶個人資料頁面。
    否則，顯示編輯表單。

    返回包含 ProfileForm 的上下文以渲染 'profile_edit.html' 模板。
    """

    if not hasattr(request.user, "profile"):
        raise Http404
    else:
        profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=profile)

    content = {
        "form": form,
    }
    return render(request, "users/profile_edit.html", content)
