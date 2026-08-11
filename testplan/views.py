"""
testplan/views.py

Test Plan Views
測試計畫相關 View。
"""

from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from .models import TestPlan
from .forms import TestPlanForm


# =========================================================
# Test Plan List
# 測試計畫列表
# =========================================================

class TestPlanListView(ListView):
    """
    顯示所有 Test Plan。
    """

    model = TestPlan

    template_name = "testplan/index.html"

    context_object_name = "plans"


    # =====================================================
    # QuerySet
    # =====================================================

    def get_queryset(self):

        keyword = (
            self.request.GET
            .get("q", "")
            .strip()
        )


        # -------------------------------------------------
        # 關鍵字搜尋
        # -------------------------------------------------

        if keyword:

            return TestPlan.objects.filter(
                name__icontains=keyword
            )


        # -------------------------------------------------
        # 無搜尋條件
        # -------------------------------------------------

        return TestPlan.objects.all()


# =========================================================
# Test Plan Add
# 新增測試計畫
# =========================================================

class TestPlanCreateView(CreateView):
    """
    建立新的 Test Plan。
    """

    model = TestPlan

    form_class = TestPlanForm

    template_name = "testplan/form.html"


    # -----------------------------------------------------
    # 建立成功後回到 Test Plan List
    # -----------------------------------------------------

    success_url = reverse_lazy(
        "testplan_list"
    )


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )


        context["title"] = (
            "Add Test Plan"
        )


        return context


# =========================================================
# Test Plan Detail
# 測試計畫詳細資料
# =========================================================

class TestPlanDetailView(DetailView):
    """
    顯示單一 Test Plan 詳細資料。
    """

    model = TestPlan

    template_name = "testplan/detail.html"

    context_object_name = "plan"


# =========================================================
# Test Plan Edit
# 編輯測試計畫
# =========================================================

class TestPlanUpdateView(UpdateView):
    """
    編輯既有 Test Plan。
    """

    model = TestPlan

    form_class = TestPlanForm

    template_name = "testplan/form.html"


    # =====================================================
    # Update Success URL
    # =====================================================

    def get_success_url(self):

        return reverse_lazy(
            "testplan_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )


        context["title"] = (
            "Edit Test Plan"
        )


        return context