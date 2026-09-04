import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def find_repository(start_path):
    path = Path(start_path).resolve()
    candidates = [path, *path.parents]
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate
    return None


class AutoCommitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Commit Push")
        self.root.geometry("560x390")
        self.root.minsize(480, 300)

        executable_path = Path(sys.executable if getattr(sys, "frozen", False) else __file__)
        repository = find_repository(executable_path.parent) or find_repository(Path.cwd())
        self.repository = tk.StringVar(value=str(repository) if repository else "")
        self.interval = tk.IntVar(value=30)
        self.running = False
        self.stop_event = threading.Event()
        self.log_queue = queue.Queue()

        self.build_ui()
        self.root.after(100, self.process_log_queue)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

        ttk.Label(frame, text="저장소 폴더").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(frame, textvariable=self.repository).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(frame, text="찾아보기", command=self.choose_repository).grid(row=0, column=2, padx=(8, 0), pady=4)

        ttk.Label(frame, text="실행 간격 (초)").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Spinbox(frame, from_=10, to=86400, textvariable=self.interval, width=10).grid(row=1, column=1, sticky="w", pady=4)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 8))
        self.start_button = ttk.Button(button_frame, text="시작", command=self.start)
        self.start_button.pack(side="left", padx=(0, 6))
        self.stop_button = ttk.Button(button_frame, text="중지", command=self.stop, state="disabled")
        self.stop_button.pack(side="left")

        self.status = ttk.Label(frame, text="대기 중")
        self.status.grid(row=2, column=2, sticky="e", pady=(8, 8))

        self.log = tk.Text(frame, height=12, state="disabled", wrap="word")
        self.log.grid(row=3, column=0, columnspan=3, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log.yview)
        scrollbar.grid(row=3, column=3, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

    def write_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def process_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log.configure(state="normal")
                self.log.insert("end", message + "\n")
                self.log.see("end")
                self.log.configure(state="disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

    def choose_repository(self):
        selected = filedialog.askdirectory(title="Git 저장소 선택")
        if selected:
            repository = find_repository(selected)
            if repository:
                self.repository.set(str(repository))
            else:
                messagebox.showwarning("Git 저장소 아님", ".git 폴더가 있는 저장소를 선택하세요.")

    def git(self, *arguments):
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.repository.get(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip()
            raise RuntimeError(details or f"git {' '.join(arguments)} failed")
        return result.stdout.strip()

    def run_once(self):
        if not self.repository.get() or not Path(self.repository.get(), ".git").exists():
            raise RuntimeError("유효한 Git 저장소를 선택하세요.")

        changes = self.git("status", "--porcelain", "--", ".", ":(exclude,glob)**/*.ps1")
        pending_push = self.git("rev-list", "--count", "@{u}..HEAD")

        if changes:
            self.git("add", "--all", "--", ".", ":(exclude,glob)**/*.ps1")
            self.git("commit", "-m", f"Auto-commit: {datetime.now():%Y-%m-%d %H:%M:%S}")
            self.write_log("커밋 완료")

        if changes or int(pending_push) > 0:
            self.git("pull", "--rebase")
            self.git("push")
            self.write_log("커밋 및 푸시 완료")
        else:
            self.write_log("변경 사항 없음")

    def worker(self):
        while not self.stop_event.is_set():
            try:
                self.run_once()
            except Exception as error:
                self.write_log(f"실패: {error}")
            self.stop_event.wait(self.interval.get())

    def start(self):
        if self.running:
            return
        try:
            interval = int(self.interval.get())
            if interval < 10:
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showwarning("간격 확인", "실행 간격은 10초 이상으로 입력하세요.")
            return

        self.running = True
        self.stop_event.clear()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status.configure(text="실행 중")
        threading.Thread(target=self.worker, daemon=True).start()
        self.write_log("자동 커밋·푸시 시작")

    def stop(self):
        self.running = False
        self.stop_event.set()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status.configure(text="중지됨")
        self.write_log("중지됨")

    def close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    AutoCommitApp(app_root)
    app_root.mainloop()