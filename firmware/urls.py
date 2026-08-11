"""
firmware/urls.py

Firmware URL Configuration
韌體 URL 設定。
"""

from django.urls import path

from . import views


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Firmware List
    # =====================================================

    path(
        "",
        views.index,
        name="firmware_list",
    ),


    # =====================================================
    # Firmware Add
    # =====================================================

    path(
        "add/",
        views.add_firmware,
        name="firmware_add",
    ),


    # =====================================================
    # Firmware Detail
    # =====================================================

    path(
        "<int:pk>/",
        views.detail_firmware,
        name="firmware_detail",
    ),


    # =====================================================
    # Firmware Edit
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_firmware,
        name="firmware_edit",
    ),


    # =====================================================
    # Firmware Delete
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_firmware,
        name="firmware_delete",
    ),

]