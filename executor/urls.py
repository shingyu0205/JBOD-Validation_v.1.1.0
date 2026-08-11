"""
executor/urls.py

Execute URL Configuration

負責：

1. Execute List
2. Execute Detail
3. Start Execute Job
4. Stop Execute Job
5. Delete Execute Job
6. Execute Status API
"""

from django.urls import path

from . import views


app_name = "executor"


urlpatterns = [

    # =====================================================
    # Execute Home
    # =====================================================

    path(
        "",
        views.index,
        name="index",
    ),

    # =====================================================
    # Execute Detail
    # =====================================================

    path(
        "<int:pk>/",
        views.detail,
        name="detail",
    ),

    # =====================================================
    # Start Execute Job
    # =====================================================

    path(
        "<int:pk>/start/",
        views.start_job,
        name="start",
    ),

    # =====================================================
    # Stop Execute Job
    # =====================================================

    path(
        "<int:pk>/stop/",
        views.stop_job,
        name="stop",
    ),

    # =====================================================
    # Delete Execute Job
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_job,
        name="delete",
    ),

    # =====================================================
    # Execute Status API
    #
    # GET /executor/<job_id>/status/
    #
    # 提供前端 Live Execution UI 使用。
    # =====================================================

    path(
        "<int:pk>/status/",
        views.job_status,
        name="status",
    ),
]