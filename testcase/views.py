"""
testcase/views.py

Test Case Views
測試案例相關 View。
"""

from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import TestCase
from .forms import TestCaseForm


# =========================================================
# Test Case List
# 測試案例列表
# =========================================================

class TestCaseListView(ListView):
    """
    顯示所有 Test Case。
    """

    model = TestCase

    template_name = "testcase/index.html"

    context_object_name = "testcases"

    paginate_by = 10


    # =====================================================
    # QuerySet
    # =====================================================

    def get_queryset(self):
        """
        取得 Test Case QuerySet。

        支援：
            q        → 關鍵字搜尋
            category → Category 篩選
        """

        queryset = (
            TestCase.objects
            .all()
            .order_by("case_id")
        )


        # -------------------------------------------------
        # 關鍵字
        # -------------------------------------------------

        keyword = (
            self.request.GET
            .get("q", "")
            .strip()
        )


        # -------------------------------------------------
        # Category
        # -------------------------------------------------

        category = (
            self.request.GET
            .get("category", "")
            .strip()
        )


        # -------------------------------------------------
        # 關鍵字搜尋
        # -------------------------------------------------

        if keyword:

            queryset = queryset.filter(
                name__icontains=keyword
            )


        # -------------------------------------------------
        # Category 篩選
        # -------------------------------------------------

        if category:

            queryset = queryset.filter(
                category=category
            )


        return queryset


    # =====================================================
    # Context
    # =====================================================

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )


        context["keyword"] = (
            self.request.GET
            .get("q", "")
            .strip()
        )


        context["selected_category"] = (
            self.request.GET
            .get("category", "")
            .strip()
        )


        context["categories"] = (
            TestCase.CATEGORY_CHOICES
        )


        return context


# =========================================================
# Test Case Add
# 新增測試案例
# =========================================================

class TestCaseCreateView(CreateView):
    """
    建立新的 Test Case。
    """

    model = TestCase

    form_class = TestCaseForm

    template_name = "testcase/form.html"


    # -----------------------------------------------------
    # 建立成功後回到 Test Case List
    #
    # 使用專案統一 URL Name：
    # testcase_list
    # -----------------------------------------------------

    success_url = reverse_lazy(
        "testcase_list"
    )


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )


        context["title"] = (
            "新增測試案例（Add Test Case）"
        )


        return context


    def form_valid(self, form):

        messages.success(
            self.request,
            "測試案例已成功建立。",
        )


        return super().form_valid(form)


# =========================================================
# Test Case Edit
# 編輯測試案例
# =========================================================

class TestCaseUpdateView(UpdateView):
    """
    編輯既有 Test Case。
    """

    model = TestCase

    form_class = TestCaseForm

    template_name = "testcase/form.html"


    # -----------------------------------------------------
    # 更新成功後回到 Test Case List
    # -----------------------------------------------------

    success_url = reverse_lazy(
        "testcase_list"
    )


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )


        context["title"] = (
            "編輯測試案例（Edit Test Case）"
        )


        return context


    def form_valid(self, form):

        messages.success(
            self.request,
            "測試案例已成功更新。",
        )


        return super().form_valid(form)


# =========================================================
# Test Case Detail
# 測試案例詳細資料
# =========================================================

class TestCaseDetailView(DetailView):
    """
    顯示單一 Test Case 詳細資料。
    """

    model = TestCase

    template_name = "testcase/detail.html"

    context_object_name = "testcase"


# =========================================================
# Test Case Delete
# 刪除測試案例
# =========================================================

class TestCaseDeleteView(DeleteView):
    """
    刪除 Test Case。
    """

    model = TestCase

    template_name = "testcase/delete.html"


    # -----------------------------------------------------
    # 刪除成功後回到 Test Case List
    # -----------------------------------------------------

    success_url = reverse_lazy(
        "testcase_list"
    )


    def form_valid(self, form):

        messages.success(
            self.request,
            "測試案例已成功刪除。",
        )


        return super().form_valid(form)