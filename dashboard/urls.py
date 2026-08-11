"""
dashboard/urls.py

Dashboard URL Configuration
儀表板 URL 設定。
"""

from django.urls import path

from . import views


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # -----------------------------------------------------
    # Dashboard
    # -----------------------------------------------------

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

]