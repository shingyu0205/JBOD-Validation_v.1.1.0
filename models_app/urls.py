"""
models_app/urls.py

Model URL Configuration
JBOD Model URL 設定。
"""

from django.urls import path

from . import views


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Model List
    # =====================================================

    path(
        "",
        views.index,
        name="model_list",
    ),


    # =====================================================
    # Model Add
    # =====================================================

    path(
        "add/",
        views.add_model,
        name="model_add",
    ),


    # =====================================================
    # Model Detail
    # =====================================================

    path(
        "<int:pk>/",
        views.detail_model,
        name="model_detail",
    ),


    # =====================================================
    # Model Edit
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_model,
        name="model_edit",
    ),


    # =====================================================
    # Model Delete
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_model,
        name="model_delete",
    ),

]