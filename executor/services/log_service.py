from executor.models import ExecuteLog


class LogService:
    """
    Execution log service.

    Provides a centralized interface for creating ExecuteLog records.
    """

    @staticmethod
    def create(
        job,
        testcase,
        level,
        message,
        duration=None,
    ):
        """
        Create an execution log.

        Parameters
        ----------
        job:
            ExecuteJob instance.

        testcase:
            TestCase instance.

        level:
            ExecuteLog.Level value.

        message:
            Log message.

        duration:
            Execution duration in seconds.
        """

        return ExecuteLog.objects.create(
            job=job,
            testcase=testcase,
            level=level,
            message=message,
            duration=duration,
        )

    @staticmethod
    def info(
        job,
        testcase,
        message,
        duration=None,
    ):
        """
        Create an INFO log.
        """

        return LogService.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.INFO,
            message=message,
            duration=duration,
        )

    @staticmethod
    def passed(
        job,
        testcase,
        message,
        duration=None,
    ):
        """
        Create a PASS log.
        """

        return LogService.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.PASS,
            message=message,
            duration=duration,
        )

    @staticmethod
    def failed(
        job,
        testcase,
        message,
        duration=None,
    ):
        """
        Create a FAIL log.
        """

        return LogService.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.FAIL,
            message=message,
            duration=duration,
        )

    @staticmethod
    def warning(
        job,
        testcase,
        message,
        duration=None,
    ):
        """
        Create a WARNING log.
        """

        return LogService.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.WARNING,
            message=message,
            duration=duration,
        )

    @staticmethod
    def error(
        job,
        testcase,
        message,
        duration=None,
    ):
        """
        Create an ERROR log.
        """

        return LogService.create(
            job=job,
            testcase=testcase,
            level=ExecuteLog.Level.ERROR,
            message=message,
            duration=duration,
        )