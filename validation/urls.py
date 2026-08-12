"""
validation/urls.py

Validation URL Configuration
驗證管理 URL 設定。
"""

from django.urls import path

from . import views


# =========================================================
# URL Namespace
# =========================================================

app_name = "validation"


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Validation List
    # 驗證列表
    # =====================================================

    path(
        "",
        views.validation_list,
        name="validation_list",
    ),

    # =====================================================
    # Validation Add
    # 新增驗證
    # =====================================================

    path(
        "add/",
        views.add_validation,
        name="validation_add",
    ),

    # =====================================================
    # Validation Detail
    # 驗證詳細資料
    # =====================================================

    path(
        "<int:pk>/",
        views.detail_validation,
        name="validation_detail",
    ),

    # =====================================================
    # Validation Edit
    # 編輯驗證
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_validation,
        name="validation_edit",
    ),

    # =====================================================
    # Validation Delete
    # 刪除驗證
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_validation,
        name="validation_delete",
    ),

]