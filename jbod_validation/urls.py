"""
jbod_validation/urls.py

JBOD Validation Platform
Project URL Configuration
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import (
    include,
    path,
)


urlpatterns = [

    # =========================================================
    # Django Administration
    # =========================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =========================================================
    # Authentication
    # 登入 / 登出
    # =========================================================

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # =========================================================
    # Dashboard
    # =========================================================

    path(
        "",
        include("dashboard.urls"),
    ),


    # =========================================================
    # Models
    # =========================================================

    path(
        "models/",
        include("models_app.urls"),
    ),


    # =========================================================
    # Firmware
    # =========================================================

    path(
        "firmware/",
        include("firmware.urls"),
    ),


    # =========================================================
    # Test Cases
    # =========================================================

    path(
        "testcase/",
        include("testcase.urls"),
    ),


    # =========================================================
    # Test Plans
    # =========================================================

    path(
        "testplan/",
        include("testplan.urls"),
    ),


    # =========================================================
    # Validation
    # =========================================================

    path(
        "validation/",
        include("validation.urls"),
    ),


    # =========================================================
    # Executor
    # =========================================================

    path(
        "executor/",
        include("executor.urls"),
    ),

]