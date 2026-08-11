from django.utils import timezone

from executor.models import ExecuteJob


class StatusService:
    """
    ExecuteJob status management service.

    Centralizes status transitions and execution timestamps.
    """

    @staticmethod
    def start(job):
        """
        Change job status to RUNNING.
        """

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

        return job

    @staticmethod
    def complete(job):
        """
        Mark job as PASS.
        """

        job.status = ExecuteJob.Status.PASS
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

    @staticmethod
    def fail(job):
        """
        Mark job as FAIL.
        """

        job.status = ExecuteJob.Status.FAIL
        job.end_time = timezone.now()

        job.save(
            update_fields=[
                "status",
                "end_time",
            ]
        )

        return job

    @staticmethod
    def stop(job):
        """
        Mark job as STOP.
        """

        job.status = ExecuteJob.Status.STOP
        job.end_time = timezone.now()

        job.save(
            update_fields=[
                "status",
                "end_time",
            ]
        )

        return job

    @staticmethod
    def update_progress(job, progress):
        """
        Update job progress.

        Progress is automatically restricted to 0-100.
        """

        progress = max(
            0,
            min(
                100,
                int(progress),
            ),
        )

        job.progress = progress

        job.save(
            update_fields=[
                "progress",
            ]
        )

        return job