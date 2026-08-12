"""
validation/views.py

Validation Views
驗證作業相關 View。
"""

from django.contrib import messages

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ValidationForm
from .models import Validation
from .services import ValidationService


# =========================================================
# Validation List
# 驗證作業列表
# =========================================================

def validation_list(request):
    """
    Validation List

    顯示所有 Validation 作業，
    並提供 Validation ID 關鍵字搜尋。
    """

    # -----------------------------------------------------
    # 取得搜尋關鍵字
    # -----------------------------------------------------

    keyword = (
        request.GET
        .get("q", "")
        .strip()
    )


    # -----------------------------------------------------
    # 建立 QuerySet
    # -----------------------------------------------------

    queryset = (
        Validation.objects
        .select_related(
            "model",
            "tester",
        )
    )


    # -----------------------------------------------------
    # 關鍵字搜尋
    # -----------------------------------------------------

    if keyword:

        queryset = queryset.filter(
            validation_id__icontains=keyword
        )


    # -----------------------------------------------------
    # Render
    # -----------------------------------------------------

    return render(
        request,
        "validation/index.html",
        {
            "validations": queryset,
            "keyword": keyword,
        },
    )


# =========================================================
# Validation Add
# 新增 Validation
# =========================================================

def add_validation(request):
    """
    建立新的 Validation 作業。
    """

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        form = ValidationForm(
            request.POST
        )


        if form.is_valid():

            ValidationService.create_validation(
                form
            )


            messages.success(
                request,
                "驗證任務已成功建立。",
            )


            # -------------------------------------------------
            # 回到 Validation List
            # -------------------------------------------------

            return redirect(
                "validation:validation_list"
            )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        form = ValidationForm()


    # -----------------------------------------------------
    # Render
    # -----------------------------------------------------

    return render(
        request,
        "validation/form.html",
        {
            "form": form,
            "title": "新增驗證任務（Create Validation）",
        },
    )


# =========================================================
# Validation Edit
# 編輯 Validation
# =========================================================

def edit_validation(request, pk):
    """
    更新指定 Validation。
    """

    # -----------------------------------------------------
    # 取得 Validation
    # -----------------------------------------------------

    validation = get_object_or_404(
        Validation,
        pk=pk,
    )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        form = ValidationForm(
            request.POST,
            instance=validation,
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "驗證任務已成功更新。",
            )


            # -------------------------------------------------
            # 回到 Validation List
            # -------------------------------------------------

            return redirect(
                "validation:validation_list"
            )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        form = ValidationForm(
            instance=validation,
        )


    # -----------------------------------------------------
    # Render
    # -----------------------------------------------------

    return render(
        request,
        "validation/form.html",
        {
            "form": form,
            "title": "編輯驗證任務（Edit Validation）",
        },
    )


# =========================================================
# Validation Detail
# 查看 Validation 詳細資訊
# =========================================================

def detail_validation(request, pk):
    """
    顯示指定 Validation 的詳細資訊。
    """

    # -----------------------------------------------------
    # 取得 Validation
    # -----------------------------------------------------

    validation = get_object_or_404(
        Validation.objects.select_related(
            "model",
            "tester",
        ),
        pk=pk,
    )


    # -----------------------------------------------------
    # Render
    # -----------------------------------------------------

    return render(
        request,
        "validation/detail.html",
        {
            "validation": validation,
        },
    )


# =========================================================
# Validation Delete
# 刪除 Validation
# =========================================================

def delete_validation(request, pk):
    """
    刪除指定 Validation。
    """

    # -----------------------------------------------------
    # 取得 Validation
    # -----------------------------------------------------

    validation = get_object_or_404(
        Validation,
        pk=pk,
    )


    # -----------------------------------------------------
    # POST：確認刪除
    # -----------------------------------------------------

    if request.method == "POST":

        validation.delete()


        messages.success(
            request,
                "驗證任務已成功刪除。",
        )


        # -------------------------------------------------
        # 回到 Validation List
        # -------------------------------------------------

        return redirect(
            "validation:validation_list"
        )


    # -----------------------------------------------------
    # GET：顯示確認頁
    # -----------------------------------------------------

    return render(
        request,
        "validation/delete.html",
        {
            "validation": validation,
        },
    )
