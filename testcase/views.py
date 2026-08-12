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
    Test Case 列表。
    """

    model = TestCase

    template_name = "testcase/index.html"

    context_object_name = "testcases"

    paginate_by = 10


    def get_queryset(self):
        """
        取得 Test Case QuerySet。

        支援：
        - 關鍵字搜尋
        - Category 篩選
        """

        queryset = (
            TestCase.objects
            .all()
            .order_by("case_id")
        )

        # -------------------------------------------------
        # 關鍵字搜尋
        # -------------------------------------------------

        keyword = (
            self.request.GET
            .get("q", "")
            .strip()
        )

        # -------------------------------------------------
        # Category 篩選
        # -------------------------------------------------

        category = (
            self.request.GET
            .get("category", "")
            .strip()
        )

        if keyword:

            queryset = queryset.filter(
                name__icontains=keyword
            )

        if category:

            queryset = queryset.filter(
                category=category
            )

        return queryset


    def get_context_data(self, **kwargs):
        """
        建立 Template Context。
        """

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
# Test Case Create
# 新增測試案例
# =========================================================

class TestCaseCreateView(CreateView):
    """
    建立新的 Test Case。
    """

    model = TestCase

    form_class = TestCaseForm

    template_name = "testcase/form.html"

    success_url = reverse_lazy(
        "testcase:testcase_list"
    )


    def get_context_data(self, **kwargs):
        """
        建立頁面 Context。
        """

        context = super().get_context_data(
            **kwargs
        )

        context["title"] = (
            "新增測試案例（Add Test Case）"
        )

        return context


    def form_valid(self, form):
        """
        Test Case 建立成功後顯示訊息。
        """

        messages.success(
            self.request,
            "測試案例已成功建立。",
        )

        return super().form_valid(form)


# =========================================================
# Test Case Update
# 編輯測試案例
# =========================================================

class TestCaseUpdateView(UpdateView):
    """
    編輯 Test Case。
    """

    model = TestCase

    form_class = TestCaseForm

    template_name = "testcase/form.html"

    success_url = reverse_lazy(
        "testcase:testcase_list"
    )


    def get_context_data(self, **kwargs):
        """
        建立頁面 Context。
        """

        context = super().get_context_data(
            **kwargs
        )

        context["title"] = (
            "編輯測試案例（Edit Test Case）"
        )

        return context


    def form_valid(self, form):
        """
        Test Case 更新成功後顯示訊息。
        """

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
    顯示 Test Case 詳細資料。
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

    success_url = reverse_lazy(
        "testcase:testcase_list"
    )


    def form_valid(self, form):
        """
        Test Case 刪除成功後顯示訊息。
        """

        messages.success(
            self.request,
            "測試案例已成功刪除。",
        )

        return super().form_valid(form)