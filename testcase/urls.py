"""
testcase/urls.py

Test Case URL Configuration
測試案例 URL 設定。
"""

from django.urls import path

from .views import (
    TestCaseListView,
    TestCaseCreateView,
    TestCaseDetailView,
    TestCaseUpdateView,
    TestCaseDeleteView,
)


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # =====================================================
    # Test Case List
    # 測試案例列表
    #
    # URL:
    # /testcase/
    #
    # URL Name:
    # testcase_list
    # =====================================================

    path(
        "",
        TestCaseListView.as_view(),
        name="testcase_list",
    ),


    # =====================================================
    # Test Case Add
    # 新增測試案例
    #
    # URL:
    # /testcase/add/
    #
    # URL Name:
    # testcase_add
    # =====================================================

    path(
        "add/",
        TestCaseCreateView.as_view(),
        name="testcase_add",
    ),


    # =====================================================
    # Test Case Detail
    # 測試案例詳細資料
    #
    # URL:
    # /testcase/<pk>/
    #
    # URL Name:
    # testcase_detail
    # =====================================================

    path(
        "<int:pk>/",
        TestCaseDetailView.as_view(),
        name="testcase_detail",
    ),


    # =====================================================
    # Test Case Edit
    # 編輯測試案例
    #
    # URL:
    # /testcase/<pk>/edit/
    #
    # URL Name:
    # testcase_edit
    # =====================================================

    path(
        "<int:pk>/edit/",
        TestCaseUpdateView.as_view(),
        name="testcase_edit",
    ),


    # =====================================================
    # Test Case Delete
    # 刪除測試案例
    #
    # URL:
    # /testcase/<pk>/delete/
    #
    # URL Name:
    # testcase_delete
    # =====================================================

    path(
        "<int:pk>/delete/",
        TestCaseDeleteView.as_view(),
        name="testcase_delete",
    ),

]