"""
executor/models.py

Execute Models
執行作業相關資料模型。

ExecuteJob
負責紀錄整個 TestPlan 的執行狀態、進度，
以及目前正在執行的 TestCase。

ExecuteLog
負責紀錄每一個 TestCase 的實際執行結果。
"""

from django.db import models

from testcase.models import TestCase
from testplan.models import TestPlan


# =========================================================
# Execute Job
# 執行作業
# =========================================================

class ExecuteJob(models.Model):
    """
    測試執行任務模型。

    用於紀錄：

    1. TestPlan
    2. 整體執行狀態
    3. 整體執行進度
    4. 目前執行中的 TestCase
    5. 目前執行到第幾項
    6. 開始 / 結束時間
    """

    # -----------------------------------------------------
    # Execution Status
    # -----------------------------------------------------

    class Status(models.TextChoices):
        """
        Execute Job 狀態。
        """

        PENDING = "PENDING", "Pending"

        RUNNING = "RUNNING", "Running"

        PASS = "PASS", "Pass"

        FAIL = "FAIL", "Fail"

        STOP = "STOP", "Stop"

    # -----------------------------------------------------
    # Test Plan
    # -----------------------------------------------------

    testplan = models.ForeignKey(
        TestPlan,
        on_delete=models.CASCADE,
        related_name="execute_jobs",
    )

    # -----------------------------------------------------
    # Execution Status
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # -----------------------------------------------------
    # Progress
    #
    # 整體 TestPlan 執行進度。
    #
    # 範例：
    #
    # 0   = 尚未開始
    # 50  = 執行 50%
    # 100 = 執行完成
    # -----------------------------------------------------

    progress = models.PositiveIntegerField(
        default=0,
    )

    # -----------------------------------------------------
    # Current TestCase
    #
    # 紀錄目前正在執行的 TestCase。
    #
    # SET_NULL：
    #
    # 如果未來 TestCase 被刪除，
    # 不應該讓歷史 ExecuteJob 一起被刪除。
    # -----------------------------------------------------

    current_testcase = models.ForeignKey(
        TestCase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_execute_jobs",
    )

    # -----------------------------------------------------
    # Current Test Index
    #
    # 紀錄目前執行到第幾個 TestCase。
    #
    # 例如：
    #
    # total = 20
    # current_test_index = 8
    #
    # 代表目前正在處理第 8 項。
    # -----------------------------------------------------

    current_test_index = models.PositiveIntegerField(
        default=0,
    )

    # -----------------------------------------------------
    # Start / End Time
    # -----------------------------------------------------

    start_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    # -----------------------------------------------------
    # Created Time
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # -----------------------------------------------------
    # Meta
    # -----------------------------------------------------

    class Meta:
        ordering = [
            "-created_at",
        ]

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def __str__(self):
        """
        回傳 Execute Job 識別名稱。
        """

        return f"Job #{self.pk}"


# =========================================================
# Execute Log
# 執行日誌
# =========================================================

class ExecuteLog(models.Model):
    """
    測試執行日誌。

    每一筆 ExecuteLog 對應一個 TestCase
    在 ExecuteJob 中的執行事件。
    """

    # -----------------------------------------------------
    # Log Level
    # -----------------------------------------------------

    class Level(models.TextChoices):
        """
        Execution Log Level。
        """

        INFO = "INFO", "Info"

        PASS = "PASS", "Pass"

        FAIL = "FAIL", "Fail"

        WARNING = "WARNING", "Warning"

        ERROR = "ERROR", "Error"

    # -----------------------------------------------------
    # Parent Execute Job
    # -----------------------------------------------------

    job = models.ForeignKey(
        ExecuteJob,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    # -----------------------------------------------------
    # Test Case
    # -----------------------------------------------------

    testcase = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        related_name="execute_logs",
    )

    # -----------------------------------------------------
    # Log Level
    # -----------------------------------------------------

    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.INFO,
    )

    # -----------------------------------------------------
    # Message
    # -----------------------------------------------------

    message = models.TextField()

    # -----------------------------------------------------
    # Execution Duration
    #
    # 單位：秒
    # -----------------------------------------------------

    duration = models.FloatField(
        null=True,
        blank=True,
    )

    # -----------------------------------------------------
    # Created Time
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # -----------------------------------------------------
    # Meta
    # -----------------------------------------------------

    class Meta:
        ordering = [
            "created_at",
        ]

    # -----------------------------------------------------
    # String Representation
    # -----------------------------------------------------

    def __str__(self):
        """
        回傳 Log 識別資訊。
        """

        return (
            f"[{self.level}] "
            f"{self.testcase.case_id} - "
            f"{self.message}"
        )