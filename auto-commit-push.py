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
        self.root.geometry("620x470")
        self.root.minsize(520, 380)
        self.root.configure(bg="#111827")

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
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.TFrame", background="#111827")
        style.configure("Panel.TFrame", background="#1f2937")
        style.configure("Title.TLabel", background="#111827", foreground="#f9fafb", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#111827", foreground="#9ca3af", font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background="#1f2937", foreground="#d1d5db", font=("Segoe UI", 10))
        style.configure("PanelHeading.TLabel", background="#1f2937", foreground="#f9fafb", font=("Segoe UI", 11, "bold"))
        style.configure("Status.TLabel", background="#1f2937", foreground="#34d399", font=("Segoe UI", 10, "bold"))
        style.configure("Primary.TButton", background="#10b981", foreground="#06281f", font=("Segoe UI", 10, "bold"), padding=(18, 9), borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#34d399"), ("disabled", "#36514b")])
        style.configure("Stop.TButton", background="#f97316", foreground="#321506", font=("Segoe UI", 10, "bold"), padding=(18, 9), borderwidth=0)
        style.map("Stop.TButton", background=[("active", "#fb923c"), ("disabled", "#594236")])
        style.configure("Browse.TButton", background="#374151", foreground="#f9fafb", padding=(12, 6), borderwidth=0)
        style.map("Browse.TButton", background=[("active", "#4b5563")])
        style.configure("App.TEntry", fieldbackground="#111827", foreground="#f9fafb", insertcolor="#f9fafb", bordercolor="#4b5563", padding=8)
        style.configure("App.TSpinbox", fieldbackground="#111827", foreground="#f9fafb", insertcolor="#f9fafb", bordercolor="#4b5563", padding=6)

        frame = ttk.Frame(self.root, padding=22, style="App.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(4, weight=1)

        ttk.Label(frame, text="Auto Commit Push", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, text="변경 사항을 감지해 GitHub에 자동으로 동기화합니다.", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 18))

        settings = ttk.Frame(frame, padding=16, style="Panel.TFrame")
        settings.grid(row=2, column=0, sticky="ew")
        settings.columnconfigure(1, weight=1)
        ttk.Label(settings, text="저장소 설정", style="PanelHeading.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        ttk.Label(settings, text="Git 저장소", style="Panel.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 12))
        ttk.Entry(settings, textvariable=self.repository, style="App.TEntry").grid(row=1, column=1, sticky="ew")
        ttk.Button(settings, text="찾아보기", command=self.choose_repository, style="Browse.TButton").grid(row=1, column=2, padx=(8, 0))
        ttk.Label(settings, text="확인 주기", style="Panel.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=(12, 0))
        ttk.Spinbox(settings, from_=10, to=86400, textvariable=self.interval, width=10, style="App.TSpinbox").grid(row=2, column=1, sticky="w", pady=(12, 0))
        ttk.Label(settings, text="초마다 확인", style="Panel.TLabel").grid(row=2, column=2, sticky="w", padx=(8, 0), pady=(12, 0))

        controls = ttk.Frame(frame, style="App.TFrame")
        controls.grid(row=3, column=0, sticky="ew", pady=(16, 12))
        self.start_button = ttk.Button(controls, text="▶  시작", command=self.start, style="Primary.TButton")
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(controls, text="■  중지", command=self.stop, state="disabled", style="Stop.TButton")
        self.stop_button.pack(side="left", padx=(8, 0))
        self.status = ttk.Label(controls, text="●  대기 중", style="Status.TLabel")
        self.status.pack(side="right", pady=8)

        log_panel = ttk.Frame(frame, padding=12, style="Panel.TFrame")
        log_panel.grid(row=4, column=0, sticky="nsew")
        log_panel.columnconfigure(0, weight=1)
        log_panel.rowconfigure(1, weight=1)
        ttk.Label(log_panel, text="활동 로그", style="PanelHeading.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.log = tk.Text(log_panel, height=12, state="disabled", wrap="word", bg="#111827", fg="#d1d5db", insertbackground="#f9fafb", relief="flat", padx=10, pady=8, font=("Consolas", 9))
        self.log.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_panel, orient="vertical", command=self.log.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
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
        startup_info = None
        creation_flags = 0
        if os.name == "nt":
            creation_flags = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(
            ["git", *arguments],
            cwd=self.repository.get(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            creationflags=creation_flags,
            startupinfo=startup_info,
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