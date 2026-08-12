from django.urls import path

from .views import (
    TestCaseListView,
    TestCaseCreateView,
    TestCaseUpdateView,
    TestCaseDetailView,
    TestCaseDeleteView,
)


# =========================================================
# URL Namespace
# =========================================================

app_name = "testcase"


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Test Case List
    # 測試案例列表
    # =====================================================

    path(
        "",
        TestCaseListView.as_view(),
        name="testcase_list",
    ),

    # =====================================================
    # Test Case Add
    # 新增測試案例
    # =====================================================

    path(
        "add/",
        TestCaseCreateView.as_view(),
        name="testcase_add",
    ),

    # =====================================================
    # Test Case Detail
    # 測試案例詳細資料
    # =====================================================

    path(
        "<int:pk>/",
        TestCaseDetailView.as_view(),
        name="testcase_detail",
    ),

    # =====================================================
    # Test Case Edit
    # 編輯測試案例
    # =====================================================

    path(
        "<int:pk>/edit/",
        TestCaseUpdateView.as_view(),
        name="testcase_edit",
    ),

    # =====================================================
    # Test Case Delete
    # 刪除測試案例
    # =====================================================

    path(
        "<int:pk>/delete/",
        TestCaseDeleteView.as_view(),
        name="testcase_delete",
    ),

]