import subprocess
import time


print("=" * 60)
print("Windows subprocess timeout test")
print("=" * 60)

# ---------------------------------------------------------
# 測試 Command
# ---------------------------------------------------------

command = 'python -c "import time; time.sleep(10)"'

print("Command:")
print(command)

print()
print("Timeout:")
print("3 seconds")

print()
print("Starting process...")

# ---------------------------------------------------------
# 記錄開始時間
# ---------------------------------------------------------

start_time = time.monotonic()

# ---------------------------------------------------------
# 建立 Process
#
# shell=True：
# 模擬目前 ExecutionService 的執行方式。
# ---------------------------------------------------------

process = subprocess.Popen(
    command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

print("PID:", process.pid)

# ---------------------------------------------------------
# 測試 process.wait(timeout)
# ---------------------------------------------------------

try:

    process.wait(
        timeout=3
    )

    elapsed = (
        time.monotonic()
        - start_time
    )

    print()
    print("Process finished normally.")

    print(
        "Elapsed:",
        elapsed,
        "seconds",
    )

except subprocess.TimeoutExpired:

    elapsed = (
        time.monotonic()
        - start_time
    )

    print()
    print("TIMEOUT!")

    print(
        "Elapsed:",
        elapsed,
        "seconds",
    )

    print(
        "Expected:",
        "approximately 3 seconds",
    )

    # -----------------------------------------------------
    # 終止 Process Tree
    # -----------------------------------------------------

    print()
    print("Terminating process tree...")

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

    # -----------------------------------------------------
    # 等待 Process 結束
    # -----------------------------------------------------

    try:

        process.wait(
            timeout=2
        )

    except subprocess.TimeoutExpired:

        print(
            "Process did not terminate within 2 seconds."
        )

        try:
            process.kill()
        except Exception:
            pass

# ---------------------------------------------------------
# 最終狀態
# ---------------------------------------------------------

print()
print("=" * 60)

print(
    "Final return code:",
    process.returncode,
)

print("=" * 60)