from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import TestPlan
from .forms import TestPlanForm


# =========================================================
# Test Plan List
# 測試計畫列表
# =========================================================

class TestPlanListView(ListView):
    """
    Test Plan 列表。
    """

    model = TestPlan

    template_name = "testplan/index.html"

    context_object_name = "plans"


    def get_queryset(self):
        """
        取得 Test Plan QuerySet。

        支援名稱搜尋。
        """

        keyword = (
            self.request.GET
            .get("q", "")
            .strip()
        )

        if keyword:

            return TestPlan.objects.filter(
                name__icontains=keyword
            )

        return TestPlan.objects.all()


# =========================================================
# Test Plan Create
# 新增測試計畫
# =========================================================

class TestPlanCreateView(CreateView):
    """
    建立新的 Test Plan。
    """

    model = TestPlan

    form_class = TestPlanForm

    template_name = "testplan/form.html"

    success_url = reverse_lazy(
        "testplan:testplan_list"
    )


    def get_context_data(self, **kwargs):
        """
        建立頁面 Context。
        """

        context = super().get_context_data(
            **kwargs
        )

        context["title"] = (
            "新增測試計畫（Add Test Plan）"
        )

        return context


# =========================================================
# Test Plan Detail
# 測試計畫詳細資料
# =========================================================

class TestPlanDetailView(DetailView):
    """
    顯示 Test Plan 詳細資料。
    """

    model = TestPlan

    template_name = "testplan/detail.html"

    context_object_name = "plan"


# =========================================================
# Test Plan Update
# 編輯測試計畫
# =========================================================

class TestPlanUpdateView(UpdateView):
    """
    編輯 Test Plan。
    """

    model = TestPlan

    form_class = TestPlanForm

    template_name = "testplan/form.html"


    def get_success_url(self):
        """
        更新成功後回到 Test Plan Detail。
        """

        return reverse_lazy(
            "testplan:testplan_detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


    def get_context_data(self, **kwargs):
        """
        建立頁面 Context。
        """

        context = super().get_context_data(
            **kwargs
        )

        context["title"] = (
            "編輯測試計畫（Edit Test Plan）"
        )

        return context


class TestPlanDeleteView(DeleteView):
    """刪除測試計畫，先顯示確認頁以避免誤刪。"""

    model = TestPlan
    template_name = "testplan/delete.html"
    context_object_name = "plan"
    success_url = reverse_lazy("testplan:testplan_list")

    def form_valid(self, form):
        messages.success(self.request, "測試計畫已成功刪除。")
        return super().form_valid(form)
