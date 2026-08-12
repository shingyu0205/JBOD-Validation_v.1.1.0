from django.urls import path

from .views import (
    TestPlanListView,
    TestPlanCreateView,
    TestPlanDetailView,
    TestPlanUpdateView,
    TestPlanDeleteView,
)


# =========================================================
# URL Namespace
# =========================================================

app_name = "testplan"


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Test Plan List
    # 測試計畫列表
    # =====================================================

    path(
        "",
        TestPlanListView.as_view(),
        name="testplan_list",
    ),

    # =====================================================
    # Test Plan Add
    # 新增測試計畫
    # =====================================================

    path(
        "add/",
        TestPlanCreateView.as_view(),
        name="testplan_add",
    ),

    # =====================================================
    # Test Plan Detail
    # 測試計畫詳細資料
    # =====================================================

    path(
        "<int:pk>/",
        TestPlanDetailView.as_view(),
        name="testplan_detail",
    ),

    # =====================================================
    # Test Plan Edit
    # 編輯測試計畫
    # =====================================================

    path(
        "<int:pk>/edit/",
        TestPlanUpdateView.as_view(),
        name="testplan_edit",
    ),

    path(
        "<int:pk>/delete/",
        TestPlanDeleteView.as_view(),
        name="testplan_delete",
    ),

]
