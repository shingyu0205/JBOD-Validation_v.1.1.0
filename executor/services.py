"""
executor/services.py

Execution Service / Validation Engine

負責：

1. 執行 TestPlan
2. 逐一執行 TestCase
3. 判斷 PASS / FAIL / TIMEOUT
4. 建立 ExecuteLog
5. 更新 ExecuteJob Progress
6. 更新 ExecuteJob 最終狀態
"""

import os
import signal
import subprocess
import time

from django.utils import timezone

from .models import ExecuteJob
from .models import ExecuteLog


# =========================================================
# Execution Service
# =========================================================

class ExecutionService:
    """
    Execute Validation Engine。

    負責實際執行 TestPlan 裡面的 TestCase。
    """

    # =====================================================
    # Terminate Process Tree
    # =====================================================

    @staticmethod
    def terminate_process_tree(process):
        """
        終止 Process 以及其子 Process。

        Windows：
            使用 taskkill /T /F 終止整個 Process Tree。

        Linux / macOS：
            使用 Process Group 終止整個 Process Tree。
        """

        if process is None:
            return

        # -------------------------------------------------
        # Process 已經結束
        # -------------------------------------------------

        if process.poll() is not None:
            return

        # -------------------------------------------------
        # Windows
        # -------------------------------------------------

        if os.name == "nt":

            try:

                subprocess.run(
                    [
                        "taskkill",
                        "/PID",
                        str(process.pid),
                        "/T",
                        "/F",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=2,
                    check=False,
                )

            except Exception:

                try:
                    process.kill()
                except Exception:
                    pass

        # -------------------------------------------------
        # Linux / macOS
        # -------------------------------------------------

        else:

            try:

                os.killpg(
                    os.getpgid(process.pid),
                    signal.SIGKILL,
                )

            except Exception:

                try:
                    process.kill()

                except Exception:
                    pass

        # -------------------------------------------------
        # 確認 Process 結束
        # -------------------------------------------------

        try:

            process.wait(
                timeout=1
            )

        except subprocess.TimeoutExpired:

            try:
                process.kill()
            except Exception:
                pass

    # =====================================================
    # Execute Job
    # =====================================================

    @staticmethod
    def execute_job(job):
        """
        執行一個 ExecuteJob。

        Parameters
        ----------
        job : ExecuteJob
            要執行的 ExecuteJob。

        Returns
        -------
        ExecuteJob
            執行完成後的 Job。
        """

        # -------------------------------------------------
        # 防止重複執行
        # -------------------------------------------------

        if job.status == ExecuteJob.Status.RUNNING:
            return job

        # -------------------------------------------------
        # 取得 Active Test Cases
        # -------------------------------------------------

        testcases = list(
            job.testplan.testcases.filter(
                status="Active",
            )
        )

        # -------------------------------------------------
        # 沒有 Test Case
        # -------------------------------------------------

        if not testcases:

            now = timezone.now()

            job.status = ExecuteJob.Status.FAIL
            job.progress = 100
            job.start_time = now
            job.end_time = now

            job.save(
                update_fields=[
                    "status",
                    "progress",
                    "start_time",
                    "end_time",
                ]
            )

            return job

        # -------------------------------------------------
        # 初始化 Job
        # -------------------------------------------------

        job.status = ExecuteJob.Status.RUNNING
        job.progress = 0
        job.start_time = timezone.now()
        job.end_time = None

        job.save(
            update_fields=[
                "status",
                "progress",
                "start_time",
                "end_time",
            ]
        )

        # -------------------------------------------------
        # Validation Start Log
        # -------------------------------------------------

        ExecuteLog.objects.create(
            job=job,
            testcase=testcases[0],
            level=ExecuteLog.Level.INFO,
            message="Validation started.",
        )

        # -------------------------------------------------
        # 執行 Test Cases
        # -------------------------------------------------

        total = len(testcases)

        all_passed = True

        for index, testcase in enumerate(
            testcases,
            start=1,
        ):

            # ---------------------------------------------
            # 檢查是否被 Stop
            # ---------------------------------------------

            job.refresh_from_db(
                fields=[
                    "status",
                ]
            )

            if job.status == ExecuteJob.Status.STOP:

                ExecuteLog.objects.create(
                    job=job,
                    testcase=testcase,
                    level=ExecuteLog.Level.WARNING,
                    message="Validation stopped by user.",
                )

                break

            # ---------------------------------------------
            # 執行 TestCase
            # ---------------------------------------------

            result = ExecutionService.execute_testcase(
                job=job,
                testcase=testcase,
            )

            # ---------------------------------------------
            # 判斷結果
            # ---------------------------------------------

            if not result["passed"]:

                all_passed = False

            # ---------------------------------------------
            # 更新 Progress
            # ---------------------------------------------

            progress = int(
                index / total * 100
            )

            job.progress = progress

            job.save(
                update_fields=[
                    "progress",
                ]
            )

        # -------------------------------------------------
        # Final Status
        # -------------------------------------------------

        job.refresh_from_db()

        if job.status == ExecuteJob.Status.STOP:

            final_status = ExecuteJob.Status.STOP

        elif all_passed:

            final_status = ExecuteJob.Status.PASS

        else:

            final_status = ExecuteJob.Status.FAIL

        # -------------------------------------------------
        # 完成 Job
        # -------------------------------------------------

        job.status = final_status
        job.progress = 100
        job.end_time = timezone.now()

        job.save(
            update_fields=[
                "status",
                "progress",
                "end_time",
            ]
        )

        return job

    # =====================================================
    # Execute TestCase
    # =====================================================

    @staticmethod
    def execute_testcase(job, testcase):
        """
        執行單一 TestCase。

        使用 process.wait(timeout)
        判斷 TestCase 是否 Timeout。

        流程：

        Popen
          ↓
        process.wait(timeout)
          ↓
        ┌───────────────┬─────────────────┐
        │               │                 │
        │ 正常結束       │ Timeout         │
        │               │                 │
        ↓               ↓
        取得 Output      terminate tree
        ↓               ↓
        PASS / FAIL      FAIL / TIMEOUT
        """

        # -------------------------------------------------
        # 開始時間
        # -------------------------------------------------

        start_time = time.monotonic()

        process = None

        # -------------------------------------------------
        # Test Case Start Log
        # -------------------------------------------------

        ExecuteLog.objects.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.INFO,
            message=(
                f"Test Case started: "
                f"{testcase.case_id} - "
                f"{testcase.name}"
            ),
        )

        try:

            # -------------------------------------------------
            # Windows Process Group
            # -------------------------------------------------

            creationflags = 0

            if os.name == "nt":

                creationflags = (
                    subprocess.CREATE_NEW_PROCESS_GROUP
                )

            # -------------------------------------------------
            # 建立 Process
            # -------------------------------------------------

            process = subprocess.Popen(
                testcase.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creationflags,
            )

            # =================================================
            # 關鍵：
            #
            # 不使用 communicate(timeout)
            #
            # 改使用 process.wait(timeout)
            # =================================================

            try:

                process.wait(
                    timeout=testcase.timeout
                )

            except subprocess.TimeoutExpired:

                # =================================================
                # TIMEOUT
                # =================================================

                timeout_duration = (
                    time.monotonic()
                    - start_time
                )

                # -------------------------------------------------
                # 終止整個 Process Tree
                # -------------------------------------------------

                ExecutionService.terminate_process_tree(
                    process
                )

                # -------------------------------------------------
                # 嘗試取得 Process 已產生的 Output
                # -------------------------------------------------

                stdout = ""
                stderr = ""

                try:

                    stdout, stderr = process.communicate(
                        timeout=1
                    )

                except Exception:

                    stdout = ""
                    stderr = ""

                # -------------------------------------------------
                # 建立 Timeout Message
                # -------------------------------------------------

                message = (
                    f"Test Case timeout: "
                    f"{testcase.case_id} - "
                    f"{testcase.name}\n"
                    f"Timeout: "
                    f"{testcase.timeout} seconds"
                )

                # -------------------------------------------------
                # stdout
                # -------------------------------------------------

                if stdout:

                    message += (
                        f"\nOutput before timeout:\n"
                        f"{stdout.strip()}"
                    )

                # -------------------------------------------------
                # stderr
                # -------------------------------------------------

                if stderr:

                    message += (
                        f"\nError before timeout:\n"
                        f"{stderr.strip()}"
                    )

                # -------------------------------------------------
                # Timeout = FAIL
                # -------------------------------------------------

                ExecuteLog.objects.create(
                    job=job,
                    testcase=testcase,
                    level=ExecuteLog.Level.FAIL,
                    message=message,
                    duration=timeout_duration,
                )

                return {
                    "passed": False,
                    "status": "TIMEOUT",
                    "duration": timeout_duration,
                }

            # =================================================
            # Process 正常結束
            # =================================================

            stdout = ""
            stderr = ""

            try:

                stdout, stderr = process.communicate(
                    timeout=1
                )

            except subprocess.TimeoutExpired:

                # -------------------------------------------------
                # 理論上不應該發生。
                # 如果發生，代表子 Process 還持有 Pipe。
                # -------------------------------------------------

                ExecutionService.terminate_process_tree(
                    process
                )

                try:

                    stdout, stderr = process.communicate(
                        timeout=1
                    )

                except Exception:

                    stdout = ""
                    stderr = ""

            # -------------------------------------------------
            # 計算執行時間
            # -------------------------------------------------

            duration = (
                time.monotonic()
                - start_time
            )

            returncode = process.returncode

            # =================================================
            # PASS
            # =================================================

            if returncode == 0:

                message = (
                    f"Test Case passed: "
                    f"{testcase.case_id} - "
                    f"{testcase.name}"
                )

                if stdout:

                    message += (
                        f"\nOutput:\n"
                        f"{stdout.strip()}"
                    )

                ExecuteLog.objects.create(
                    job=job,
                    testcase=testcase,
                    level=ExecuteLog.Level.PASS,
                    message=message,
                    duration=duration,
                )

                return {
                    "passed": True,
                    "status": "PASS",
                    "duration": duration,
                }

            # =================================================
            # FAIL
            # =================================================

            else:

                message = (
                    f"Test Case failed: "
                    f"{testcase.case_id} - "
                    f"{testcase.name}\n"
                    f"Return Code: "
                    f"{returncode}"
                )

                if stderr:

                    message += (
                        f"\nError:\n"
                        f"{stderr.strip()}"
                    )

                if stdout:

                    message += (
                        f"\nOutput:\n"
                        f"{stdout.strip()}"
                    )

                ExecuteLog.objects.create(
                    job=job,
                    testcase=testcase,
                    level=ExecuteLog.Level.FAIL,
                    message=message,
                    duration=duration,
                )

                return {
                    "passed": False,
                    "status": "FAIL",
                    "duration": duration,
                }

        # =====================================================
        # Unexpected Error
        # =====================================================

        except Exception as exc:

            # -------------------------------------------------
            # 確保 Process 被終止
            # -------------------------------------------------

            if process is not None:

                try:

                    if process.poll() is None:

                        ExecutionService.terminate_process_tree(
                            process
                        )

                except Exception:
                    pass

            # -------------------------------------------------
            # 計算執行時間
            # -------------------------------------------------

            duration = (
                time.monotonic()
                - start_time
            )

            # -------------------------------------------------
            # 建立 ERROR Log
            # -------------------------------------------------

            ExecuteLog.objects.create(
                job=job,
                testcase=testcase,
                level=ExecuteLog.Level.ERROR,
                message=(
                    f"Execution error: "
                    f"{testcase.case_id} - "
                    f"{testcase.name}\n"
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
                duration=duration,
            )

            return {
                "passed": False,
                "status": "ERROR",
                "duration": duration,
            }