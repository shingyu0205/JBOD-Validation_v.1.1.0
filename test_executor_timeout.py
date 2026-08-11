import os
import subprocess
import time


# =========================================================
# Test Command
# =========================================================

command = 'python -c "import time; time.sleep(10)"'

timeout = 3


print("=" * 70)
print("ExecutionService Timeout Diagnostic")
print("=" * 70)

print()
print("OS:", os.name)
print("Command:", command)
print("Timeout:", timeout)


# =========================================================
# Windows Process Group
# =========================================================

creationflags = 0

if os.name == "nt":

    creationflags = (
        subprocess.CREATE_NEW_PROCESS_GROUP
    )


print(
    "Creation Flags:",
    creationflags,
)


# =========================================================
# 建立 Process
# =========================================================

start_time = time.monotonic()

print()
print("[1] Starting Popen...")


process = subprocess.Popen(
    command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    creationflags=creationflags,
)


popen_duration = (
    time.monotonic()
    - start_time
)


print(
    "[2] Popen completed:",
    f"{popen_duration:.3f}s",
)

print(
    "[3] PID:",
    process.pid,
)


# =========================================================
# process.wait()
# =========================================================

wait_start = time.monotonic()

print()
print(
    "[4] Calling process.wait(timeout=3)..."
)


try:

    process.wait(
        timeout=timeout
    )

    wait_duration = (
        time.monotonic()
        - wait_start
    )

    print()
    print(
        "[5] PROCESS FINISHED"
    )

    print(
        "Wait Duration:",
        f"{wait_duration:.3f}s",
    )

    print(
        "Return Code:",
        process.returncode,
    )


except subprocess.TimeoutExpired:

    wait_duration = (
        time.monotonic()
        - wait_start
    )

    total_duration = (
        time.monotonic()
        - start_time
    )

    print()
    print(
        "[5] TIMEOUT EXPIRED"
    )

    print(
        "Wait Duration:",
        f"{wait_duration:.3f}s",
    )

    print(
        "Total Duration:",
        f"{total_duration:.3f}s",
    )


    # =====================================================
    # Terminate Process Tree
    # =====================================================

    terminate_start = time.monotonic()

    print()
    print(
        "[6] Terminating Process Tree..."
    )

    if os.name == "nt":

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
            check=False,
        )

    else:

        process.kill()


    terminate_duration = (
        time.monotonic()
        - terminate_start
    )


    print(
        "Terminate Duration:",
        f"{terminate_duration:.3f}s",
    )


# =========================================================
# 最終結果
# =========================================================

print()
print("=" * 70)

print(
    "FINAL ELAPSED:",
    f"{time.monotonic() - start_time:.3f}s",
)

print(
    "FINAL RETURN CODE:",
    process.poll(),
)

print("=" * 70)