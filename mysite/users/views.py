from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import LoginForm


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
            return redirect("users:index")
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)


def logout(request):
    """用於處理用戶登出操作的視圖函數。"""
    auth_logout(request)
    return redirect("users:login")


@login_required(login_url="users:login")
def profile(request):
    """用於顯示和更新用戶個人資料的視圖函數。"""
    """如果用戶沒有 Profile，則創建一個新的 Profile。"""
    user = request.user
    if hasattr(user, "profile"):
        profile = user.profile
    else:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        age = request.POST.get("age")
        education = request.POST.get("education")
        avatar = request.FILES.get("avatar")

        profile.update_profile(
            full_name=full_name, age=age, education=education, avatar=avatar
        )

        return redirect("users:profile")

    content = {
        "profile": profile,
        "education_choices": Profile.EDUCATION_CHOICES,
    }
    return render(request, "users/profile.html", content)
