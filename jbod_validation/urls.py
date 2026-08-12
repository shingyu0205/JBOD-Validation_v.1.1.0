"""
jbod_validation/urls.py

JBOD Validation Platform
Main URL Configuration
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path


urlpatterns = [

    # =========================================================
    # Django Administration
    # Django 管理後台
    # =========================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =========================================================
    # Authentication
    # 使用者登入 / 登出
    # =========================================================

    # Login
    # 登入頁面
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="user/login.html",
        ),
        name="login",
    ),

    # Logout
    # 登出
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # =========================================================
    # Dashboard
    # 儀表板
    # =========================================================

    path(
        "",
        include("dashboard.urls"),
    ),


    # =========================================================
    # Models
    # 機型管理
    # =========================================================

    path(
        "models/",
        include("models_app.urls"),
    ),


    # =========================================================
    # Firmware
    # 韌體管理
    # =========================================================

    path(
        "firmware/",
        include("firmware.urls"),
    ),


    # =========================================================
    # Test Case
    # 測試案例
    # =========================================================

    path(
        "testcase/",
        include("testcase.urls"),
    ),


    # =========================================================
    # Test Plan
    # 測試計畫
    # =========================================================

    path(
        "testplan/",
        include("testplan.urls"),
    ),


    # =========================================================
    # Validation
    # 驗證中心
    # =========================================================

    path(
        "validation/",
        include("validation.urls"),
    ),


    # =========================================================
    # Executor
    # 執行驗證
    # =========================================================

    path(
        "executor/",
        include("executor.urls"),
    ),

]