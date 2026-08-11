from django.db import transaction

from executor.models import ExecuteJob
from executor.services.log_service import LogService
from executor.services.script_runner import ScriptRunner
from executor.services.status_service import StatusService


class JobRunner:
    """
    Validation Job Runner.

    Responsible for executing all TestCases belonging to a TestPlan.
    """

    def __init__(self):
        self.script_runner = ScriptRunner()

    def run(self, job):
        """
        Execute the validation job.

        Execution flow:

        1. Change job status to RUNNING.
        2. Load TestCases from the TestPlan.
        3. Execute TestCases sequentially.
        4. Create ExecuteLog records.
        5. Update execution progress.
        6. Mark the job as PASS or FAIL.
        """

        if job.status not in (
            ExecuteJob.Status.PENDING,
            ExecuteJob.Status.STOP,
            ExecuteJob.Status.FAIL,
        ):
            return job

        # 清除上一輪執行留下的 Log。
        # Clear logs from previous execution attempts.
        job.logs.all().delete()

        StatusService.start(job)

        testcases = list(
            job.testplan.testcases.filter(
                status="Active",
            ).order_by("case_id")
        )

        total = len(testcases)

        # 沒有 Test Case 時，直接判定失敗。
        if total == 0:
            testcase = None

            # ExecuteLog 必須關聯 TestCase，
            # 因此沒有 TestCase 時無法建立 ExecuteLog。
            # 直接將 Job 標記為 FAIL。
            StatusService.fail(job)

            return job

        for index, testcase in enumerate(testcases, start=1):

            # 每次執行前重新取得 Job 狀態。
            # This allows another request to mark the job as STOP.
            job.refresh_from_db()

            if job.status == ExecuteJob.Status.STOP:
                StatusService.stop(job)
                return job

            # 計算目前 TestCase 開始前的進度。
            progress_before = int(
                ((index - 1) / total) * 100
            )

            StatusService.update_progress(
                job,
                progress_before,
            )

            LogService.info(
                job=job,
                testcase=testcase,
                message=(
                    f"Start Test Case: "
                    f"{testcase.case_id} - {testcase.name}"
                ),
            )

            # 執行 TestCase Command。
            result = self.script_runner.run(
                command=testcase.command,
                timeout=testcase.timeout,
            )

            # 組合執行輸出。
            output_parts = []

            if result.stdout:
                output_parts.append(
                    f"STDOUT:\n{result.stdout}"
                )

            if result.stderr:
                output_parts.append(
                    f"STDERR:\n{result.stderr}"
                )

            if result.timed_out:
                output_parts.append(
                    f"TIMEOUT: "
                    f"Execution exceeded "
                    f"{testcase.timeout} seconds."
                )

            if result.return_code is not None:
                output_parts.append(
                    f"RETURN CODE: {result.return_code}"
                )

            message = "\n\n".join(output_parts)

            if not message:
                message = "Command completed without output."

            # 如果有設定 Expected Result，
            # 除了 Return Code == 0 之外，
            # 也要求 stdout 包含 Expected Result。
            expected_result = (
                testcase.expected_result.strip()
            )

            expected_result_failed = False

            if (
                result.success
                and expected_result
                and expected_result not in result.stdout
            ):
                expected_result_failed = True

            test_passed = (
                result.success
                and not result.timed_out
                and not expected_result_failed
            )

            if expected_result_failed:
                message += (
                    "\n\n"
                    f"EXPECTED RESULT NOT FOUND:\n"
                    f"{expected_result}"
                )

            if test_passed:
                LogService.passed(
                    job=job,
                    testcase=testcase,
                    message=message,
                    duration=result.duration,
                )
            else:
                LogService.failed(
                    job=job,
                    testcase=testcase,
                    message=message,
                    duration=result.duration,
                )

                StatusService.fail(job)

                # 失敗時將進度更新到目前 Test Case 完成的位置。
                progress_after = int(
                    (index / total) * 100
                )

                StatusService.update_progress(
                    job,
                    progress_after,
                )

                return job

            # 更新目前 Test Case 完成後的進度。
            progress_after = int(
                (index / total) * 100
            )

            StatusService.update_progress(
                job,
                progress_after,
            )

        # 所有 Test Cases 都 PASS。
        StatusService.complete(job)

        return job