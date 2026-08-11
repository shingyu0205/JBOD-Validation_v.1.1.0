import subprocess
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScriptResult:
    """
    Test script execution result.

    Stores the execution result returned by the operating system.
    """

    success: bool
    return_code: Optional[int]
    stdout: str
    stderr: str
    duration: float
    timed_out: bool = False


class ScriptRunner:
    """
    Test script execution service.

    Responsible for executing the command defined in TestCase.command.
    """

    def run(
        self,
        command: str,
        timeout: int = 60,
    ) -> ScriptResult:
        """
        Execute a test command.

        Parameters
        ----------
        command:
            Command or script defined by the TestCase.

        timeout:
            Maximum execution time in seconds.

        Returns
        -------
        ScriptResult
            Execution result containing stdout, stderr, return code,
            execution duration, and timeout information.
        """

        start_time = time.perf_counter()

        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            duration = time.perf_counter() - start_time

            return ScriptResult(
                success=process.returncode == 0,
                return_code=process.returncode,
                stdout=process.stdout.strip(),
                stderr=process.stderr.strip(),
                duration=duration,
                timed_out=False,
            )

        except subprocess.TimeoutExpired as exc:
            duration = time.perf_counter() - start_time

            stdout = ""

            stderr = ""

            if exc.stdout:
                stdout = (
                    exc.stdout.decode(errors="replace")
                    if isinstance(exc.stdout, bytes)
                    else str(exc.stdout)
                ).strip()

            if exc.stderr:
                stderr = (
                    exc.stderr.decode(errors="replace")
                    if isinstance(exc.stderr, bytes)
                    else str(exc.stderr)
                ).strip()

            return ScriptResult(
                success=False,
                return_code=None,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                timed_out=True,
            )

        except Exception as exc:
            duration = time.perf_counter() - start_time

            return ScriptResult(
                success=False,
                return_code=None,
                stdout="",
                stderr=str(exc),
                duration=duration,
                timed_out=False,
            )