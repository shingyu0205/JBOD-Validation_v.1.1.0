"""
executor/views.py

Execute Views
執行作業相關 View。

負責：

1. Execute Dashboard
2. Execute Job Detail
3. Execute Job Status API
4. Start / Retry Execute Job
5. Stop Execute Job
6. Delete Execute Job
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import ExecuteJobForm
from .models import ExecuteJob
from .models import ExecuteLog
from .services import ExecutionService


# =========================================================
# Helper Functions
# 共用資料處理函式
# =========================================================

def _build_testcase_results(job, logs=None):
    """
    建立 TestPlan 所有 TestCase 的目前執行結果。

    每個 TestCase 的最終狀態由 ExecuteLog 最後一筆紀錄決定。

    回傳：

        {
            testcase.pk: {
                "testcase": testcase,
                "status": "PENDING",
                "level": None,
                "message": "",
                "duration": None,
            }
        }
    """

    # -----------------------------------------------------
    # 取得 TestPlan TestCases
    # -----------------------------------------------------

    testcases = list(
        job.testplan.testcases.all()
    )

    # -----------------------------------------------------
    # 如果外部沒有傳入 logs
    # 自動取得 Execute Logs
    # -----------------------------------------------------

    if logs is None:

        logs = list(
            job.logs
            .select_related("testcase")
            .order_by(
                "created_at",
                "id",
            )
        )

    # -----------------------------------------------------
    # 建立初始狀態
    # -----------------------------------------------------

    testcase_results = {}

    for testcase in testcases:

        testcase_results[testcase.pk] = {

            "testcase": testcase,

            "status": "PENDING",

            "level": None,

            "message": "",

            "duration": None,
        }

    # -----------------------------------------------------
    # 套用 ExecuteLog
    #
    # ExecuteLog 按照時間順序套用，
    # 因此最後一筆 Log 會成為目前狀態。
    # -----------------------------------------------------

    for log in logs:

        testcase_id = log.testcase_id

        # -------------------------------------------------
        # 忽略不屬於目前 TestPlan 的 Log
        # -------------------------------------------------

        if testcase_id not in testcase_results:

            continue

        result = testcase_results[testcase_id]

        # -------------------------------------------------
        # 保存最後 Log 資訊
        # -------------------------------------------------

        result["level"] = log.level

        result["message"] = log.message

        # -------------------------------------------------
        # INFO
        #
        # INFO 代表 TestCase 已經開始執行。
        # -------------------------------------------------

        if log.level == ExecuteLog.Level.INFO:

            result["status"] = "RUNNING"

        # -------------------------------------------------
        # PASS
        # -------------------------------------------------

        elif log.level == ExecuteLog.Level.PASS:

            result["status"] = "PASS"

            result["duration"] = log.duration

        # -------------------------------------------------
        # FAIL
        # -------------------------------------------------

        elif log.level == ExecuteLog.Level.FAIL:

            result["status"] = "FAIL"

            result["duration"] = log.duration

        # -------------------------------------------------
        # ERROR
        # -------------------------------------------------

        elif log.level == ExecuteLog.Level.ERROR:

            result["status"] = "ERROR"

            result["duration"] = log.duration

        # -------------------------------------------------
        # WARNING
        #
        # WARNING 不改變目前 TestCase 狀態。
        # -------------------------------------------------

        elif log.level == ExecuteLog.Level.WARNING:

            pass

    return testcases, testcase_results


def _get_current_test(
    job,
    testcases,
    testcase_results,
):
    """
    判斷目前應該顯示的 TestCase。

    優先順序：

    1. ExecuteJob.current_testcase
    2. RUNNING TestCase
    3. PENDING TestCase
    4. 最後一個 TestCase

    同時回傳：

        current_test
        current_test_index
    """

    current_test = None

    current_test_index = 0

    # =====================================================
    # 1. ExecuteJob Runtime State
    # =====================================================

    if job.current_testcase_id:

        for index, testcase in enumerate(testcases):

            if testcase.pk == job.current_testcase_id:

                current_test = testcase_results.get(
                    testcase.pk
                )

                current_test_index = index

                break

    # =====================================================
    # 2. RUNNING TestCase
    # =====================================================

    if current_test is None:

        for index, testcase in enumerate(testcases):

            result = testcase_results.get(
                testcase.pk
            )

            if (
                result
                and result["status"] == "RUNNING"
            ):

                current_test = result

                current_test_index = index

                break

    # =====================================================
    # 3. PENDING TestCase
    # =====================================================

    if current_test is None:

        for index, testcase in enumerate(testcases):

            result = testcase_results.get(
                testcase.pk
            )

            if (
                result
                and result["status"] == "PENDING"
            ):

                current_test = result

                current_test_index = index

                break

    # =====================================================
    # 4. 最後一個 TestCase
    #
    # 適用於：
    #
    # PASS
    # FAIL
    # ERROR
    #
    # 而 ExecuteJob.current_testcase 為 NULL 的舊資料。
    # =====================================================

    if (
        current_test is None
        and testcase_results
    ):

        last_index = len(testcases) - 1

        current_test = testcase_results[
            testcases[last_index].pk
        ]

        current_test_index = last_index

    # =====================================================
    # Job 已完成
    #
    # current_test_index 採用「已完成數量」概念。
    #
    # 例如：
    #
    # 1 個 TestCase 完成
    # → index = 1
    #
    # 3 個 TestCase 完成
    # → index = 3
    #
    # 這與 ExecutionService 的 Runtime State 一致。
    # =====================================================

    completed_count = sum(
        1
        for result in testcase_results.values()
        if result["status"] in (
            "PASS",
            "FAIL",
            "ERROR",
        )
    )

    if job.status in (
        ExecuteJob.Status.PASS,
        ExecuteJob.Status.FAIL,
        ExecuteJob.Status.STOP,
    ):

        if completed_count == len(testcases):

            current_test_index = completed_count

    return current_test, current_test_index


# =========================================================
# Execute Home
# =========================================================

@login_required(login_url="/login/")
def index(request):
    """
    Execute Validation 首頁。

    顯示：

        - 建立 Execute Job
        - Job 列表
        - Running / Pending / PASS / FAIL / STOP 數量
    """

    # -----------------------------------------------------
    # 建立新的 Execute Job
    # -----------------------------------------------------

    if request.method == "POST":

        form = ExecuteJobForm(
            request.POST
        )

        if form.is_valid():

            ExecuteJob.objects.create(
                testplan=form.cleaned_data["testplan"],
                status=ExecuteJob.Status.PENDING,
                progress=0,
            )

            return redirect(
                "executor:index"
            )

    else:

        form = ExecuteJobForm()

    # -----------------------------------------------------
    # 取得 Execute Jobs
    # -----------------------------------------------------

    jobs = (
        ExecuteJob.objects
        .select_related(
            "testplan",
        )
        .order_by(
            "-created_at"
        )
    )

    # -----------------------------------------------------
    # Dashboard Context
    # -----------------------------------------------------

    context = {

        "form": form,

        "jobs": jobs[:10],

        "running_count": jobs.filter(
            status=ExecuteJob.Status.RUNNING
        ).count(),

        "pending_count": jobs.filter(
            status=ExecuteJob.Status.PENDING
        ).count(),

        "pass_count": jobs.filter(
            status=ExecuteJob.Status.PASS
        ).count(),

        "fail_count": jobs.filter(
            status=ExecuteJob.Status.FAIL
        ).count(),

        "stop_count": jobs.filter(
            status=ExecuteJob.Status.STOP
        ).count(),
    }

    return render(
        request,
        "executor/index.html",
        context,
    )


# =========================================================
# Execute Detail
# =========================================================

@login_required(login_url="/login/")
def detail(request, pk):
    """
    Execute Job Detail。

    將：

        ExecuteJob
        TestPlan
        TestCase
        ExecuteLog

    整合後提供給 Executor Detail UI。
    """

    # -----------------------------------------------------
    # 取得 Execute Job
    # -----------------------------------------------------

    job = get_object_or_404(
        ExecuteJob.objects.select_related(
            "testplan",
            "testplan__model",
            "testplan__firmware",
            "current_testcase",
        ),
        pk=pk,
    )

    # -----------------------------------------------------
    # 取得 Execute Logs
    # -----------------------------------------------------

    logs = list(
        job.logs
        .select_related(
            "testcase",
        )
        .order_by(
            "created_at",
            "id",
        )
    )

    # -----------------------------------------------------
    # 建立 TestCase 結果
    # -----------------------------------------------------

    testcases, testcase_results = (
        _build_testcase_results(
            job,
            logs,
        )
    )

    # -----------------------------------------------------
    # 轉換成 List
    #
    # Template 使用 List 比 Dictionary 更方便。
    # -----------------------------------------------------

    testcase_results_list = list(
        testcase_results.values()
    )

    # =====================================================
    # TestCase 統計
    # =====================================================

    total_testcases = len(
        testcase_results_list
    )

    completed_testcases = sum(
        1
        for result in testcase_results_list
        if result["status"] in (
            "PASS",
            "FAIL",
            "ERROR",
        )
    )

    running_testcases = sum(
        1
        for result in testcase_results_list
        if result["status"] == "RUNNING"
    )

    pending_testcases = sum(
        1
        for result in testcase_results_list
        if result["status"] == "PENDING"
    )

    # =====================================================
    # PASS / FAIL 統計
    # =====================================================

    pass_testcases = sum(
        1
        for result in testcase_results_list
        if result["status"] == "PASS"
    )

    fail_testcases = sum(
        1
        for result in testcase_results_list
        if result["status"] in (
            "FAIL",
            "ERROR",
        )
    )

    # =====================================================
    # Current Test
    # =====================================================

    current_test, current_test_index = (
        _get_current_test(
            job,
            testcases,
            testcase_results,
        )
    )

    # =====================================================
    # Remaining TestCases
    # =====================================================

    remaining_testcases = max(
        total_testcases - completed_testcases,
        0,
    )

    # =====================================================
    # Validation / Job 是否完成
    # =====================================================

    execution_completed = job.status in (
        ExecuteJob.Status.PASS,
        ExecuteJob.Status.FAIL,
        ExecuteJob.Status.STOP,
    )

    # =====================================================
    # 是否可以 Start / Retry
    # =====================================================

    can_start = job.status in (
        ExecuteJob.Status.PENDING,
        ExecuteJob.Status.FAIL,
        ExecuteJob.Status.STOP,
    )

    # =====================================================
    # 是否可以 Stop
    # =====================================================

    can_stop = (
        job.status
        == ExecuteJob.Status.RUNNING
    )

    # =====================================================
    # Status 顯示文字
    # =====================================================

    status_display = job.get_status_display()

    # =====================================================
    # Context
    # =====================================================

    context = {

        "job": job,

        "status_display": status_display,

        "testcase_results": testcase_results_list,

        "total_testcases": total_testcases,

        "completed_testcases": completed_testcases,

        "running_testcases": running_testcases,

        "pending_testcases": pending_testcases,

        "remaining_testcases": remaining_testcases,

        "pass_testcases": pass_testcases,

        "fail_testcases": fail_testcases,

        "current_test": current_test,

        "current_test_index": current_test_index,

        "execution_completed": execution_completed,

        "can_start": can_start,

        "can_stop": can_stop,

        "execution_logs": logs,
    }

    return render(
        request,
        "executor/detail.html",
        context,
    )


# =========================================================
# Execute Job Status API
# =========================================================

@login_required(login_url="/login/")
def job_status(request, pk):
    """
    Execute Job Status API。

    Endpoint：

        GET /executor/<pk>/status/

    提供前端 Live Execution UI 使用。
    """

    # -----------------------------------------------------
    # 只允許 GET
    # -----------------------------------------------------

    if request.method != "GET":

        return JsonResponse(
            {
                "success": False,
                "error": "GET method required.",
            },
            status=405,
        )

    # -----------------------------------------------------
    # 取得 Job
    # -----------------------------------------------------

    job = get_object_or_404(
        ExecuteJob.objects.select_related(
            "testplan",
            "current_testcase",
        ),
        pk=pk,
    )

    # -----------------------------------------------------
    # 取得 Execute Logs
    # -----------------------------------------------------

    logs = list(
        job.logs
        .select_related(
            "testcase",
        )
        .order_by(
            "created_at",
            "id",
        )
    )

    # -----------------------------------------------------
    # 建立 TestCase Status
    # -----------------------------------------------------

    testcases, testcase_results = (
        _build_testcase_results(
            job,
            logs,
        )
    )

    testcase_ids = {
        testcase.pk
        for testcase in testcases
    }

    # =====================================================
    # Statistics
    # =====================================================

    completed_testcases = sum(
        1
        for result in testcase_results.values()
        if result["status"] in (
            "PASS",
            "FAIL",
            "ERROR",
        )
    )

    running_testcases = sum(
        1
        for result in testcase_results.values()
        if result["status"] == "RUNNING"
    )

    pending_testcases = sum(
        1
        for result in testcase_results.values()
        if result["status"] == "PENDING"
    )

    pass_testcases = sum(
        1
        for result in testcase_results.values()
        if result["status"] == "PASS"
    )

    fail_testcases = sum(
        1
        for result in testcase_results.values()
        if result["status"] in (
            "FAIL",
            "ERROR",
        )
    )

    total_testcases = len(
        testcases
    )

    remaining_testcases = max(
        total_testcases
        - completed_testcases,
        0,
    )

    # =====================================================
    # Current Test
    #
    # 使用與 Detail Page 完全相同的判斷邏輯。
    # =====================================================

    current_test, current_test_index = (
        _get_current_test(
            job,
            testcases,
            testcase_results,
        )
    )

    # =====================================================
    # Current TestCase JSON
    # =====================================================

    current_testcase_data = None

    if current_test is not None:

        testcase = current_test["testcase"]

        current_testcase_data = {

            "id": testcase.pk,

            "case_id": testcase.case_id,

            "name": testcase.name,

            "status": current_test["status"],

            "duration": current_test["duration"],

            "message": current_test["message"],
        }

    # =====================================================
    # Latest Log
    # =====================================================

    latest_log = None

    if logs:

        log = logs[-1]

        latest_log = {

            "id": log.pk,

            "level": log.level,

            "testcase": (
                log.testcase.case_id
                if log.testcase
                else None
            ),

            "message": log.message,

            "duration": log.duration,

            "created_at": (
                log.created_at.isoformat()
            ),
        }

    # =====================================================
    # Response
    # =====================================================

    data = {

        "success": True,

        # -------------------------------------------------
        # Job
        # -------------------------------------------------

        "job_id": job.pk,

        "status": job.status,

        "status_display": job.get_status_display(),

        "progress": job.progress,

        # -------------------------------------------------
        # Runtime State
        # -------------------------------------------------

        "current_test_index": current_test_index,

        "current_testcase": current_testcase_data,

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        "total_testcases": total_testcases,

        "completed_testcases": completed_testcases,

        "running_testcases": running_testcases,

        "pending_testcases": pending_testcases,

        "remaining_testcases": remaining_testcases,

        "pass_testcases": pass_testcases,

        "fail_testcases": fail_testcases,

        # -------------------------------------------------
        # Execution Time
        # -------------------------------------------------

        "start_time": (
            job.start_time.isoformat()
            if job.start_time
            else None
        ),

        "end_time": (
            job.end_time.isoformat()
            if job.end_time
            else None
        ),

        # -------------------------------------------------
        # Latest Log
        # -------------------------------------------------

        "latest_log": latest_log,
    }

    return JsonResponse(
        data
    )


# =========================================================
# Start / Retry Execute Job
# =========================================================

@login_required(login_url="/login/")
def start_job(request, pk):
    """
    Start / Retry Execute Job。

    PENDING / STOP / FAIL
        ↓
    ExecutionService
        ↓
    TestPlan
        ↓
    TestCase
        ↓
    PASS / FAIL / TIMEOUT
    """

    job = get_object_or_404(
        ExecuteJob,
        pk=pk,
    )

    # -----------------------------------------------------
    # 只允許 POST
    # -----------------------------------------------------

    if request.method != "POST":

        return redirect(
            "executor:detail",
            pk=job.pk,
        )

    # -----------------------------------------------------
    # 可執行狀態
    # -----------------------------------------------------

    if job.status not in (
        ExecuteJob.Status.PENDING,
        ExecuteJob.Status.STOP,
        ExecuteJob.Status.FAIL,
    ):

        return redirect(
            "executor:detail",
            pk=job.pk,
        )

    # =====================================================
    # Retry
    # =====================================================

    # -----------------------------------------------------
    # 清除前一次 Execute Logs
    # -----------------------------------------------------

    job.logs.all().delete()

    # -----------------------------------------------------
    # 重設 Job
    # -----------------------------------------------------

    job.status = ExecuteJob.Status.PENDING

    job.progress = 0

    job.current_testcase = None

    job.current_test_index = 0

    job.start_time = None

    job.end_time = None

    job.save(
        update_fields=[
            "status",
            "progress",
            "current_testcase",
            "current_test_index",
            "start_time",
            "end_time",
        ]
    )

    # =====================================================
    # 執行 Validation Engine
    # =====================================================

    ExecutionService.execute_job(
        job
    )

    # -----------------------------------------------------
    # 回到 Detail Page
    # -----------------------------------------------------

    return redirect(
        "executor:detail",
        pk=job.pk,
    )


# =========================================================
# Stop Execute Job
# =========================================================

@login_required(login_url="/login/")
def stop_job(request, pk):
    """
    Stop Execute Job。
    """

    job = get_object_or_404(
        ExecuteJob,
        pk=pk,
    )

    # -----------------------------------------------------
    # 只允許 POST
    # -----------------------------------------------------

    if request.method == "POST":

        if job.status == ExecuteJob.Status.RUNNING:

            job.status = ExecuteJob.Status.STOP

            job.save(
                update_fields=[
                    "status",
                ]
            )

    return redirect(
        "executor:detail",
        pk=job.pk,
    )


# =========================================================
# Delete Execute Job
# =========================================================

@login_required(login_url="/login/")
def delete_job(request, pk):
    """
    Delete Execute Job。
    """

    job = get_object_or_404(
        ExecuteJob,
        pk=pk,
    )

    # -----------------------------------------------------
    # 只允許 POST
    # -----------------------------------------------------

    if request.method == "POST":

        # -------------------------------------------------
        # 執行中的 Job 不允許刪除
        # -------------------------------------------------

        if job.status != ExecuteJob.Status.RUNNING:

            job.delete()

            return redirect(
                "executor:index"
            )

    return redirect(
        "executor:detail",
        pk=job.pk,
    )