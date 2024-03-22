import subprocess
import time
import os


def stop_process(proc):
    if proc.poll() is None:
        proc.terminate()  # 发送终止信号
        try:
            proc.wait(timeout=10)  # 等待进程结束
        except subprocess.TimeoutExpired:
            proc.kill()  # 如果进程没有在规定时间内结束，强制杀死


def start_flask_app():
    # 启动 Flask 应用程序
    return subprocess.Popen(["python", "sadtalker_flask.py"])


def start_web_ui(script):
    # 启动 web UI 应用程序
    return subprocess.Popen(["python", "src/agentscope/web_ui/app.py", "--script", script])


# 脚本主体
if __name__ == "__main__":
    script = "examples/conversation/multimodal_conversation.py"

    while True:
        # 清理 runs 目录（谨慎操作，确保不会误删重要文件）
        if os.path.exists("./examples/conversation/runs/"):
            os.system("rm -rf ./examples/conversation/runs/")
        if os.path.exists("./examples/conversation/results/"):
            os.system("rm -rf ./examples/conversation/results/")

        # # 启动 Flask 应用程序
        # flask_process = start_flask_app()

        # 在后台启动 Web UI，不阻塞主线程
        web_ui_process = start_web_ui(script)

        try:
            # 等待指定时间，这里设置为60分钟
            time.sleep(3600)

        finally:
            # 优雅地关闭 Flask 应用程序
            # stop_process(flask_process)
            stop_process(web_ui_process)

        # 短暂休眠，确保进程完全结束，可根据需要调整
        time.sleep(5)
