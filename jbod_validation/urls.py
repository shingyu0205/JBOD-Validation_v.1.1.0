"""
jbod_validation/urls.py

JBOD Validation Platform
Main URL Configuration
"""

from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf.urls.i18n import set_language


urlpatterns = [

    # =========================================================
    # Internationalization
    # 全站語言切換
    # =========================================================

    path(
        "i18n/setlang/",
        set_language,
        name="set_language",
    ),


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
    # 使用者登入 / 註冊 / 登出
    #
    # Login:
    # /login/
    #
    # Register:
    # /register/
    #
    # Logout:
    # /logout/
    # =========================================================

    path(
        "",
        include("user.urls"),
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