"""
executor/services/execution.py

Execution Service / Validation Engine

負責：

1. 執行 TestPlan
2. 逐一執行 TestCase
3. 判斷 PASS / FAIL / TIMEOUT
4. 建立 ExecuteLog
5. 更新 ExecuteJob Progress
6. 更新目前執行中的 TestCase
7. 更新 ExecuteJob 最終狀態
"""

import os
import signal
import subprocess
import time

from django.utils import timezone

from ..models import ExecuteJob
from ..models import ExecuteLog


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

        # -------------------------------------------------
        # Process 不存在
        # -------------------------------------------------

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

                # -------------------------------------------------
                # taskkill 失敗時，至少嘗試終止 parent process
                # -------------------------------------------------

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
        # 確認 Process 是否結束
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
        # 防止同一個 Job 重複執行
        # -------------------------------------------------

        if job.status == ExecuteJob.Status.RUNNING:

            return job

        # -------------------------------------------------
        # 取得 TestPlan 的 Active Test Cases
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
            job.current_testcase = None
            job.current_test_index = 0
            job.start_time = now
            job.end_time = now

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

            return job

        # -------------------------------------------------
        # 初始化 Job
        # -------------------------------------------------

        job.status = ExecuteJob.Status.RUNNING
        job.progress = 0
        job.current_testcase = None
        job.current_test_index = 0
        job.start_time = timezone.now()
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

        # -------------------------------------------------
        # 建立開始 Log
        #
        # ExecuteLog 需要 testcase，
        # 因此使用第一個 TestCase 作為 Job Start Log
        # 的關聯對象。
        # -------------------------------------------------

        ExecuteLog.objects.create(
            job=job,
            testcase=testcases[0],
            level=ExecuteLog.Level.INFO,
            message="Validation started.",
        )

        total = len(testcases)

        all_passed = True

        # -------------------------------------------------
        # 逐一執行 Test Case
        # -------------------------------------------------

        for index, testcase in enumerate(
            testcases,
            start=1,
        ):

            # -------------------------------------------------
            # 每次執行前重新讀取 Job 狀態
            # -------------------------------------------------

            job.refresh_from_db(
                fields=[
                    "status",
                ]
            )

            # -------------------------------------------------
            # 使用者要求 Stop
            # -------------------------------------------------

            if job.status == ExecuteJob.Status.STOP:

                ExecuteLog.objects.create(
                    job=job,
                    testcase=testcase,
                    level=ExecuteLog.Level.WARNING,
                    message="Validation stopped by user.",
                )

                break

            # -------------------------------------------------
            # 更新目前 TestCase
            #
            # 這裡是 Live Execution Runtime 的核心。
            #
            # UI 可以直接讀：
            #
            # job.current_testcase
            # job.current_test_index
            # -------------------------------------------------

            job.current_testcase = testcase
            job.current_test_index = index

            job.save(
                update_fields=[
                    "current_testcase",
                    "current_test_index",
                ]
            )

            # -------------------------------------------------
            # 執行 Test Case
            # -------------------------------------------------

            result = ExecutionService.execute_testcase(
                job=job,
                testcase=testcase,
            )

            # -------------------------------------------------
            # 只要任何 Test Case 不是 PASS
            # 整個 Job 就不能 PASS
            # -------------------------------------------------

            if not result["passed"]:

                all_passed = False

            # -------------------------------------------------
            # 更新 Progress
            #
            # 例如：
            #
            # 1 / 10 = 10%
            # 5 / 10 = 50%
            # 10 / 10 = 100%
            # -------------------------------------------------

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
        # 重新取得最新 Job 狀態
        # -------------------------------------------------

        job.refresh_from_db()

        # -------------------------------------------------
        # 決定最終結果
        # -------------------------------------------------

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
        job.end_time = timezone.now()

        # -------------------------------------------------
        # STOP 不應該強制變成 100%
        #
        # PASS / FAIL：
        #   100%
        #
        # STOP：
        #   保留實際完成進度
        # -------------------------------------------------

        if final_status in (
            ExecuteJob.Status.PASS,
            ExecuteJob.Status.FAIL,
        ):

            job.progress = 100

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
        執行單一 Test Case。

        Timeout 控制：

            subprocess.Popen()
                    ↓
            process.wait(timeout)
                    ↓
              ┌─────┴─────┐
              ↓           ↓
            正常完成      Timeout
              ↓           ↓
           收集結果     FAIL
                          ↓
                   終止 Process Tree

        注意：
            Timeout 發生的瞬間就計算 duration，
            避免 Process Cleanup 時間被算進測試時間。
        """

        # -------------------------------------------------
        # 開始計時
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

            # =================================================
            # Windows Process Group
            # =================================================

            creationflags = 0

            if os.name == "nt":

                creationflags = (
                    subprocess.CREATE_NEW_PROCESS_GROUP
                )

            # =================================================
            # 建立 Process
            # =================================================

            process = subprocess.Popen(
                testcase.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creationflags,
            )

            # =================================================
            # DEBUG
            # =================================================

            wait_start = time.monotonic()

            print(
                f"[EXECUTOR DEBUG] "
                f"PROCESS START | "
                f"PID={process.pid} | "
                f"CASE={testcase.case_id} | "
                f"TIMEOUT={testcase.timeout}"
            )

            # =================================================
            # 等待 Process
            # =================================================

            try:

                process.wait(
                    timeout=testcase.timeout
                )

                wait_duration = (
                    time.monotonic()
                    - wait_start
                )

                print(
                    f"[EXECUTOR DEBUG] "
                    f"PROCESS FINISHED | "
                    f"PID={process.pid} | "
                    f"WAIT={wait_duration:.3f}s"
                )

            except subprocess.TimeoutExpired:

                # =================================================
                # TIMEOUT
                # =================================================

                wait_duration = (
                    time.monotonic()
                    - wait_start
                )

                # -------------------------------------------------
                # Timeout 發生當下立即計算 Duration
                # -------------------------------------------------

                duration = (
                    time.monotonic()
                    - start_time
                )

                print(
                    f"[EXECUTOR DEBUG] "
                    f"TIMEOUT | "
                    f"PID={process.pid} | "
                    f"WAIT={wait_duration:.3f}s | "
                    f"DURATION={duration:.3f}s"
                )

                # -------------------------------------------------
                # 終止 Process Tree
                # -------------------------------------------------

                terminate_start = time.monotonic()

                print(
                    f"[EXECUTOR DEBUG] "
                    f"TERMINATE START | "
                    f"PID={process.pid}"
                )

                ExecutionService.terminate_process_tree(
                    process
                )

                terminate_duration = (
                    time.monotonic()
                    - terminate_start
                )

                print(
                    f"[EXECUTOR DEBUG] "
                    f"TERMINATE END | "
                    f"PID={process.pid} | "
                    f"TIME={terminate_duration:.3f}s"
                )

                # -------------------------------------------------
                # 取得已經產生的 Output
                # -------------------------------------------------

                stdout = ""
                stderr = ""

                try:

                    stdout, stderr = process.communicate(
                        timeout=1
                    )

                except Exception as exc:

                    print(
                        f"[EXECUTOR DEBUG] "
                        f"COMMUNICATE ERROR | "
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    )

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
                # Timeout 前 stdout
                # -------------------------------------------------

                if stdout:

                    message += (
                        f"\nOutput before timeout:\n"
                        f"{stdout.strip()}"
                    )

                # -------------------------------------------------
                # Timeout 前 stderr
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
                    duration=duration,
                )

                return {
                    "passed": False,
                    "status": "TIMEOUT",
                    "duration": duration,
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
                # 理論上 process.wait() 已經確認 Process 結束。
                # 如果仍然無法收集 Pipe，
                # 就終止 Process Tree。
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
            # 如果 Process 還在執行，
            # 確保將其終止。
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