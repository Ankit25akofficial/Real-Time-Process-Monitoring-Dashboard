import psutil
import platform
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import pandas as pd
from tkinter import font as tkfont
import os
import sys
import numpy as np
from collections import deque
# process_monitor.py
import sys
import os
import psutil
# ... [keep all your existing imports] ...

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ProcessMonitorDashboard:
    def __init__(self, root):
        self.root = root
        # ... [rest of your existing __init__ code] ...
        
        # Set window icon (for executable)
        try:
            self.root.iconbitmap(resource_path('monitor.ico'))
        except:
            pass  # Icon not found, continue without it

def main():
    # Handle frozen executable (PyInstaller)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    root = tk.Tk()
    app = ProcessMonitorDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()

class ProcessMonitorDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Process Monitoring Dashboard")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Custom styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Data structures for monitoring
        self.cpu_history = deque(maxlen=60)
        self.mem_history = deque(maxlen=60)
        self.process_history = deque(maxlen=60)
        self.alert_history = []
        
        # Queue for thread-safe GUI updates
        self.update_queue = queue.Queue()
        
        # Initialize UI
        self.create_widgets()
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitor_thread.start()
        
        # Start periodic GUI updates
        self.update_gui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        self.style.configure('Critical.TLabel', foreground='red', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Warning.TLabel', foreground='orange', font=('Segoe UI', 10))
        self.style.configure('Normal.TLabel', foreground='green', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
        self.style.map('TButton', background=[('active', '#e6e6e6')])
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.header_frame, text="Real-Time Process Monitor", style='Header.TLabel').pack(side=tk.LEFT)
        
        # System info
        self.system_info_frame = ttk.LabelFrame(self.main_frame, text="System Information")
        self.system_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_system_info_widgets()
        
        # Metrics frame
        self.metrics_frame = ttk.Frame(self.main_frame)
        self.metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # CPU and Memory graphs
        self.create_performance_graphs()
        
        # Process control frame
        self.process_control_frame = ttk.LabelFrame(self.main_frame, text="Process Management")
        self.process_control_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_process_control_widgets()
        
        # Status bar
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
    def create_system_info_widgets(self):
        """Create widgets for displaying system information"""
        # System information labels
        info_frame = ttk.Frame(self.system_info_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # System info
        self.os_label = ttk.Label(info_frame, text=f"OS: {platform.system()} {platform.release()}")
        self.os_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.cpu_label = ttk.Label(info_frame, text="CPU: Loading...")
        self.cpu_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.memory_label = ttk.Label(info_frame, text="Memory: Loading...")
        self.memory_label.grid(row=0, column=2, sticky=tk.W, padx=5)
        
        self.uptime_label = ttk.Label(info_frame, text="Uptime: Loading...")
        self.uptime_label.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Real-time metrics
        metrics_frame = ttk.Frame(self.system_info_frame)
        metrics_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(metrics_frame, text="Current Metrics:").grid(row=0, column=0, sticky=tk.W)
        
        self.cpu_usage_label = ttk.Label(metrics_frame, text="CPU: 0%")
        self.cpu_usage_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        self.mem_usage_label = ttk.Label(metrics_frame, text="Memory: 0%")
        self.mem_usage_label.grid(row=0, column=2, sticky=tk.W, padx=10)
        
        self.process_count_label = ttk.Label(metrics_frame, text="Processes: 0")
        self.process_count_label.grid(row=0, column=3, sticky=tk.W, padx=10)
        
        # Alert indicator
        self.alert_indicator = ttk.Label(metrics_frame, text="Status: Normal", style='Normal.TLabel')
        self.alert_indicator.grid(row=0, column=4, sticky=tk.W, padx=10)
        
    def create_performance_graphs(self):
        """Create CPU and Memory usage graphs"""
        # CPU Usage Graph
        cpu_frame = ttk.LabelFrame(self.metrics_frame, text="CPU Usage")
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(5, 3), dpi=80)
        self.cpu_ax.set_title('CPU Usage (%)')
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_line, = self.cpu_ax.plot([], [], 'r-')
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=cpu_frame)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Memory Usage Graph
        mem_frame = ttk.LabelFrame(self.metrics_frame, text="Memory Usage")
        mem_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mem_fig, self.mem_ax = plt.subplots(figsize=(5, 3), dpi=80)
        self.mem_ax.set_title('Memory Usage (%)')
        self.mem_ax.set_ylim(0, 100)
        self.mem_line, = self.mem_ax.plot([], [], 'b-')
        self.mem_canvas = FigureCanvasTkAgg(self.mem_fig, master=mem_frame)
        self.mem_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_process_control_widgets(self):
        """Create widgets for process management"""
        # Process Treeview with scrollbars
        tree_frame = ttk.Frame(self.process_control_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Treeview for processes
        self.tree = ttk.Treeview(tree_frame, columns=('pid', 'name', 'status', 'cpu', 'memory', 'user'), selectmode='extended')
        
        # Vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Define columns
        self.tree.heading('#0', text='#')
        self.tree.heading('pid', text='PID')
        self.tree.heading('name', text='Name')
        self.tree.heading('status', text='Status')
        self.tree.heading('cpu', text='CPU %')
        self.tree.heading('memory', text='Memory %')
        self.tree.heading('user', text='User')
        
        # Column configuration
        self.tree.column('#0', width=40, stretch=tk.NO)
        self.tree.column('pid', width=80, anchor=tk.CENTER)
        self.tree.column('name', width=150)
        self.tree.column('status', width=100)
        self.tree.column('cpu', width=80, anchor=tk.CENTER)
        self.tree.column('memory', width=100, anchor=tk.CENTER)
        self.tree.column('user', width=100)
        
        # Control buttons
        button_frame = ttk.Frame(self.process_control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_processes).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="End Process", command=self.end_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="End Tree", command=self.end_process_tree).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Set Priority", command=self.set_priority).pack(side=tk.LEFT, padx=2)
        
        # Search frame
        search_frame = ttk.Frame(self.process_control_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_processes)
        
        # Alert log
        alert_frame = ttk.LabelFrame(self.process_control_frame, text="Alert Log")
        alert_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.alert_log = scrolledtext.ScrolledText(alert_frame, wrap=tk.WORD, height=4)
        self.alert_log.pack(fill=tk.BOTH, expand=True)
        self.alert_log.config(state=tk.DISABLED)
        
    def monitor_system(self):
        """Background thread for monitoring system metrics"""
        while self.running:
            try:
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                mem_percent = psutil.virtual_memory().percent
                process_count = len(psutil.pids())
                
                # Get detailed process info
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'username']):
                    try:
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'status': proc.info['status'],
                            'cpu': proc.info['cpu_percent'],
                            'memory': proc.info['memory_percent'],
                            'user': proc.info['username'] or 'N/A'
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                # Get system info
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                uptime_str = str(uptime).split('.')[0]  # Remove microseconds
                
                # Check for alerts
                alerts = []
                if cpu_percent > 90:
                    alerts.append(f"High CPU Usage: {cpu_percent}%")
                if mem_percent > 90:
                    alerts.append(f"High Memory Usage: {mem_percent}%")
                
                # Put data in queue for GUI update
                self.update_queue.put(('metrics', {
                    'cpu_percent': cpu_percent,
                    'mem_percent': mem_percent,
                    'process_count': process_count,
                    'processes': processes,
                    'uptime': uptime_str,
                    'alerts': alerts
                }))
                
                # Small delay to prevent high CPU usage
                time.sleep(1)
                
            except Exception as e:
                self.update_queue.put(('error', f"Monitoring error: {str(e)}"))
                time.sleep(5)
    
    def update_gui(self):
        """Update GUI elements from the queue"""
        try:
            while True:
                try:
                    # Get data from queue (non-blocking)
                    data_type, data = self.update_queue.get_nowait()
                    
                    if data_type == 'metrics':
                        self.update_metrics(data)
                    elif data_type == 'error':
                        self.status_label.config(text=f"Error: {data}")
                except queue.Empty:
                    break
        except Exception as e:
            self.status_label.config(text=f"Update error: {str(e)}")
        
        # Schedule next update
        self.root.after(500, self.update_gui)
    
    def update_metrics(self, data):
        """Update all metrics display"""
        # Update CPU and memory history
        self.cpu_history.append(data['cpu_percent'])
        self.mem_history.append(data['mem_percent'])
        self.process_history.append(data['process_count'])
        
        # Update real-time labels
        self.cpu_usage_label.config(text=f"CPU: {data['cpu_percent']:.1f}%")
        self.mem_usage_label.config(text=f"Memory: {data['mem_percent']:.1f}%")
        self.process_count_label.config(text=f"Processes: {data['process_count']}")
        self.uptime_label.config(text=f"Uptime: {data['uptime']}")
        
        # Update system info (once)
        if not hasattr(self, 'system_info_updated'):
            self.os_label.config(text=f"OS: {platform.system()} {platform.release()}")
            self.cpu_label.config(text=f"CPU: {platform.processor() or 'Unknown'}")
            self.memory_label.config(text=f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
            self.system_info_updated = True
        
        # Update graphs
        self.update_graphs()
        
        # Update process list
        self.update_process_list(data['processes'])
        
        # Handle alerts
        if data['alerts']:
            for alert in data['alerts']:
                self.add_alert(alert)
            self.alert_indicator.config(text="Status: Critical", style='Critical.TLabel')
        else:
            self.alert_indicator.config(text="Status: Normal", style='Normal.TLabel')
        
        # Update status bar
        self.status_label.config(text="Last update: " + datetime.now().strftime("%H:%M:%S"))
    
    def update_graphs(self):
        """Update CPU and Memory graphs"""
        # CPU Graph
        self.cpu_line.set_data(range(len(self.cpu_history)), self.cpu_history)
        self.cpu_ax.set_xlim(0, len(self.cpu_history))
        self.cpu_ax.relim()
        self.cpu_ax.autoscale_view(scaley=False)
        self.cpu_canvas.draw()
        
        # Memory Graph
        self.mem_line.set_data(range(len(self.mem_history)), self.mem_history)
        self.mem_ax.set_xlim(0, len(self.mem_history))
        self.mem_ax.relim()
        self.mem_ax.autoscale_view(scaley=False)
        self.mem_canvas.draw()
    
    def update_process_list(self, processes):
        """Update the process list in the Treeview"""
        # Store current selection and scroll position
        selected = self.tree.selection()
        scroll_pos = self.tree.yview()
        
        # Clear the tree
        self.tree.delete(*self.tree.get_children())
        
        # Sort processes by CPU usage (descending)
        processes_sorted = sorted(processes, key=lambda p: p['cpu'], reverse=True)
        
        # Add processes to tree
        for i, proc in enumerate(processes_sorted, 1):
            self.tree.insert('', 'end', iid=i, text=str(i),
                            values=(proc['pid'], proc['name'], proc['status'],
                                   f"{proc['cpu']:.1f}", f"{proc['memory']:.1f}",
                                   proc['user']))
        
        # Restore selection and scroll position if possible
        if selected:
            try:
                self.tree.selection_set(selected)
                self.tree.yview_moveto(scroll_pos[0])
            except:
                pass
    
    def add_alert(self, message):
        """Add an alert message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.alert_log.config(state=tk.NORMAL)
        self.alert_log.insert(tk.END, formatted_message)
        self.alert_log.config(state=tk.DISABLED)
        self.alert_log.see(tk.END)
        
        # Keep only the last 100 alerts
        alert_lines = self.alert_log.get("1.0", tk.END).split('\n')
        if len(alert_lines) > 100:
            self.alert_log.config(state=tk.NORMAL)
            self.alert_log.delete("1.0", f"{len(alert_lines)-100}.0")
            self.alert_log.config(state=tk.DISABLED)
        
        # Add to alert history
        self.alert_history.append(formatted_message)
    
    def refresh_processes(self):
        """Manual refresh of process list"""
        self.status_label.config(text="Refreshing process list...")
        self.update_queue.put(('metrics', {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'mem_percent': psutil.virtual_memory().percent,
            'process_count': len(psutil.pids()),
            'processes': [],
            'uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0],
            'alerts': []
        }))
    
    def filter_processes(self, event=None):
        """Filter processes based on search text"""
        search_text = self.search_var.get().lower()
        
        if not search_text:
            # Show all items if search is empty
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
                self.tree.detach(item)
                self.tree.move(item, '', 'end')
            return
        
        # Hide non-matching items
        for item in self.tree.get_children():
            values = [str(v).lower() for v in self.tree.item(item)['values']]
            if any(search_text in v for v in values):
                self.tree.item(item, tags=('match',))
                self.tree.detach(item)
                self.tree.move(item, '', 'end')
            else:
                self.tree.item(item, tags=())
                self.tree.detach(item)
    
    def end_process(self):
        """End selected process"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select one or more processes to end")
            return
        
        pids = [int(self.tree.item(item)['values'][0]) for item in selected]
        names = [self.tree.item(item)['values'][1] for item in selected]
        
        confirm = messagebox.askyesno(
            "Confirm End Process",
            f"Are you sure you want to end these processes?\n\n{', '.join(names)}"
        )
        
        if confirm:
            success = []
            failed = []
            
            for pid in pids:
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    success.append(str(pid))
                except Exception as e:
                    failed.append(f"{pid} ({str(e)})")
            
            message = ""
            if success:
                message += f"Successfully ended processes: {', '.join(success)}\n"
            if failed:
                message += f"Failed to end processes: {', '.join(failed)}"
            
            messagebox.showinfo("Result", message)
            self.refresh_processes()
    
    def end_process_tree(self):
        """End selected process and its children"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process to end with its children")
            return
        
        pid = int(self.tree.item(selected[0])['values'][0])
        name = self.tree.item(selected[0])['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm End Process Tree",
            f"Are you sure you want to end {name} (PID: {pid}) and all its child processes?"
        )
        
        if confirm:
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                
                # First try to terminate children
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                
                # Then terminate parent
                parent.terminate()
                
                # Check if processes are gone
                gone, alive = psutil.wait_procs([parent] + children, timeout=3)
                
                if alive:
                    # Force kill if still alive
                    for p in alive:
                        try:
                            p.kill()
                        except:
                            pass
                
                messagebox.showinfo("Success", f"Successfully ended process tree for {name} (PID: {pid})")
                self.refresh_processes()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to end process tree: {str(e)}")
    
    def set_priority(self):
        """Set priority of selected process"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process to change priority")
            return
        
        if len(selected) > 1:
            messagebox.showwarning("Multiple Selection", "Please select only one process to change priority")
            return
        
        pid = int(self.tree.item(selected[0])['values'][0])
        name = self.tree.item(selected[0])['values'][1]
        
        # Create priority selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Set Priority for {name} (PID: {pid})")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Select new priority for {name} (PID: {pid}):").pack(padx=10, pady=5)
        
        priority_var = tk.StringVar(value='normal')
        
        priorities = [
            ('Realtime', 'realtime'),
            ('High', 'high'),
            ('Above Normal', 'above_normal'),
            ('Normal', 'normal'),
            ('Below Normal', 'below_normal'),
            ('Low', 'low')
        ]
        
        for text, value in priorities:
            ttk.Radiobutton(dialog, text=text, variable=priority_var, value=value).pack(anchor=tk.W, padx=20)
        
        def apply_priority():
            try:
                priority_map = {
                    'realtime': psutil.REALTIME_PRIORITY_CLASS,
                    'high': psutil.HIGH_PRIORITY_CLASS,
                    'above_normal': psutil.ABOVE_NORMAL_PRIORITY_CLASS,
                    'normal': psutil.NORMAL_PRIORITY_CLASS,
                    'below_normal': psutil.BELOW_NORMAL_PRIORITY_CLASS,
                    'low': psutil.IDLE_PRIORITY_CLASS
                }
                
                p = psutil.Process(pid)
                p.nice(priority_map[priority_var.get()])
                
                messagebox.showinfo("Success", f"Priority for {name} set to {priority_var.get().replace('_', ' ')}")
                dialog.destroy()
                self.refresh_processes()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set priority: {str(e)}")
                dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Apply", command=apply_priority).pack(side=tk.LEFT, padx=5)
    
    def on_close(self):
        """Handle window close event"""
        self.running = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ProcessMonitorDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()