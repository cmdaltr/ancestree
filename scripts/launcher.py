#!/usr/bin/env python3
"""
Ancestree Launcher
A simple graphical launcher for the Ancestree application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import webbrowser
import threading
import time
import signal
from pathlib import Path

class AncestreeLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ancestree Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Track processes
        self.backend_process = None
        self.frontend_process = None
        self.docker_mode = False

        # Set window icon if available
        icon_path = Path(__file__).parent.parent / "assets" / "ancestree.png"
        if icon_path.exists():
            try:
                # Try to set icon (works on some platforms)
                self.root.iconphoto(True, tk.PhotoImage(file=str(icon_path)))
            except:
                pass  # Icon setting may not be supported on all platforms

        # Setup UI
        self.setup_ui()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=100)
        header.pack(fill=tk.X)

        # Try to add logo to header
        icon_path = Path(__file__).parent.parent / "assets" / "ancestree.png"
        if icon_path.exists():
            try:
                logo_img = tk.PhotoImage(file=str(icon_path))
                # Subsample to make it smaller (1024x1024 -> ~60x60)
                logo_img = logo_img.subsample(17, 17)
                logo_label = tk.Label(header, image=logo_img, bg="#2c3e50")
                logo_label.image = logo_img  # Keep a reference
                logo_label.pack(pady=(10, 5))
            except:
                pass  # If logo fails to load, just show text

        title = tk.Label(
            header,
            text="🌳 Ancestree",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=(5, 10))

        # Main content
        content = tk.Frame(self.root, padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Welcome message
        welcome = tk.Label(
            content,
            text="Build and explore your family tree",
            font=("Arial", 12),
            fg="#555"
        )
        welcome.pack(pady=(0, 20))

        # Mode selection
        mode_frame = tk.LabelFrame(content, text="Launch Mode", padx=10, pady=10)
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        self.mode_var = tk.StringVar(value="docker")

        tk.Radiobutton(
            mode_frame,
            text="🐳 Docker (Recommended - Easy setup)",
            variable=self.mode_var,
            value="docker",
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        tk.Radiobutton(
            mode_frame,
            text="💻 Manual (Development mode)",
            variable=self.mode_var,
            value="manual",
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        # Buttons
        btn_frame = tk.Frame(content)
        btn_frame.pack(fill=tk.X, pady=(0, 15))

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start Ancestree",
            command=self.start_app,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.stop_btn = tk.Button(
            btn_frame,
            text="⬛ Stop",
            command=self.stop_app,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Open browser button
        self.browser_btn = tk.Button(
            content,
            text="🌐 Open in Browser",
            command=self.open_browser,
            bg="#3498db",
            fg="white",
            font=("Arial", 11),
            padx=20,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.browser_btn.pack(fill=tk.X, pady=(0, 15))

        # Status log
        log_frame = tk.LabelFrame(content, text="Status", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.log.pack(fill=tk.BOTH, expand=True)

        # Initial log message
        self.log_message("Welcome to Ancestree! Click 'Start' to begin.")
        self.log_message(f"Working directory: {os.getcwd()}")

    def log_message(self, message):
        """Add a message to the log"""
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"{message}\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def check_docker(self):
        """Check if Docker is installed and running"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                return False

            # Check if Docker daemon is running
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def start_app(self):
        """Start the application"""
        mode = self.mode_var.get()

        if mode == "docker":
            if not self.check_docker():
                messagebox.showerror(
                    "Docker Not Available",
                    "Docker is not installed or not running.\n\n"
                    "Please install Docker Desktop from:\n"
                    "https://www.docker.com/products/docker-desktop\n\n"
                    "Or use 'Manual' mode instead."
                )
                return
            self.start_docker()
        else:
            self.start_manual()

    def start_docker(self):
        """Start using Docker Compose"""
        self.docker_mode = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.log_message("\n🐳 Starting Ancestree with Docker...")
        self.log_message("This may take a few minutes on first run...")

        def run_docker():
            try:
                # Check if docker-compose.yml exists
                if not os.path.exists("docker-compose.yml"):
                    self.log_message("❌ Error: docker-compose.yml not found")
                    self.reset_buttons()
                    return

                # Start Docker Compose
                self.log_message("📦 Building and starting containers...")
                process = subprocess.Popen(
                    ["docker-compose", "up", "--build"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                self.backend_process = process

                # Wait for services to be ready
                time.sleep(10)

                self.log_message("✅ Ancestree is starting!")
                self.log_message("⏳ Waiting for services to be ready...")

                # Check if services are up
                time.sleep(5)
                self.log_message("✅ Backend ready at http://localhost:8000")
                self.log_message("✅ Frontend ready at http://localhost:3000")
                self.log_message("\n🎉 Click 'Open in Browser' to start using Ancestree!")

                self.browser_btn.config(state=tk.NORMAL)

                # Auto-open browser
                time.sleep(2)
                self.open_browser()

            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.reset_buttons()

        thread = threading.Thread(target=run_docker, daemon=True)
        thread.start()

    def start_manual(self):
        """Start using manual mode (direct Python/Node)"""
        self.docker_mode = False
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.log_message("\n💻 Starting Ancestree in manual mode...")

        # Check if backend exists
        if not os.path.exists("backend"):
            messagebox.showerror(
                "Backend Not Found",
                "Backend directory not found.\n"
                "Please ensure you're in the Ancestree directory."
            )
            self.reset_buttons()
            return

        def run_manual():
            try:
                # Start backend
                self.log_message("🔧 Starting backend...")

                backend_cmd = [sys.executable, "run.py"]
                if os.path.exists("backend/run.py"):
                    backend_cmd = [sys.executable, "backend/run.py"]

                self.backend_process = subprocess.Popen(
                    backend_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd="backend" if os.path.exists("backend/run.py") else "."
                )

                time.sleep(3)
                self.log_message("✅ Backend started")

                # Start frontend
                self.log_message("🔧 Starting frontend...")

                frontend_dir = "frontend"
                if not os.path.exists(frontend_dir):
                    self.log_message("❌ Frontend directory not found")
                    self.reset_buttons()
                    return

                self.frontend_process = subprocess.Popen(
                    ["npm", "run", "dev"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=frontend_dir,
                    shell=True
                )

                time.sleep(5)
                self.log_message("✅ Frontend started")
                self.log_message("\n🎉 Click 'Open in Browser' to start using Ancestree!")

                self.browser_btn.config(state=tk.NORMAL)

                # Auto-open browser
                time.sleep(2)
                self.open_browser()

            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                messagebox.showerror(
                    "Startup Error",
                    f"Failed to start Ancestree:\n{str(e)}\n\n"
                    "Try using Docker mode instead."
                )
                self.reset_buttons()

        thread = threading.Thread(target=run_manual, daemon=True)
        thread.start()

    def stop_app(self):
        """Stop the application"""
        self.log_message("\n⏹ Stopping Ancestree...")

        if self.docker_mode:
            try:
                subprocess.run(["docker-compose", "down"], timeout=30)
                self.log_message("✅ Docker containers stopped")
            except Exception as e:
                self.log_message(f"⚠ Warning: {str(e)}")
        else:
            # Stop manual processes
            if self.backend_process:
                try:
                    self.backend_process.terminate()
                    self.backend_process.wait(timeout=5)
                except:
                    self.backend_process.kill()

            if self.frontend_process:
                try:
                    self.frontend_process.terminate()
                    self.frontend_process.wait(timeout=5)
                except:
                    self.frontend_process.kill()

            self.log_message("✅ Services stopped")

        self.reset_buttons()

    def reset_buttons(self):
        """Reset button states"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.browser_btn.config(state=tk.DISABLED)

    def open_browser(self):
        """Open the application in the default browser"""
        webbrowser.open("http://localhost:3000")
        self.log_message("🌐 Opened in browser")

    def on_closing(self):
        """Handle window closing"""
        if self.backend_process or self.frontend_process:
            if messagebox.askokcancel("Quit", "Ancestree is running. Stop and quit?"):
                self.stop_app()
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Change to the project root directory (parent of scripts/)
    os.chdir(Path(__file__).parent.parent)

    app = AncestreeLauncher()
    app.run()
