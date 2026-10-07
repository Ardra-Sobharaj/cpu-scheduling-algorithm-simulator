import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from algorithms import run_fcfs, run_sjf, run_priority, run_round_robin
from calculations import compute_metrics
from visualization import render_gantt_chart


class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithm Simulator")
        self.root.geometry("1180x820")
        self.root.minsize(1000, 700)

        # Black & Beige Theme Colors
        self.BG_MAIN = "#121212"
        self.BG_CARD = "#1E1E1E"
        self.BG_ENTRY = "#2A2A2A"
        self.ACCENT_BEIGE = "#F5F5DC"
        self.ACCENT_GOLD = "#D4AF37"
        self.TEXT_MAIN = "#F5F5DC"
        self.TEXT_MUTED = "#AAAAAA"
        self.BORDER_COLOR = "#333333"

        self.processes = []
        self.last_results = {}  # Store results for Run All switching

        self._apply_global_styles()
        self._build_ui()

    def _apply_global_styles(self):
        self.root.configure(bg=self.BG_MAIN)
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Treeview styling
        style.configure("Treeview",
                        background=self.BG_CARD,
                        foreground=self.TEXT_MAIN,
                        fieldbackground=self.BG_CARD,
                        rowheight=28,
                        bordercolor=self.BORDER_COLOR,
                        font=('Helvetica', 10))
        style.map("Treeview", background=[('selected', self.ACCENT_GOLD)],
                              foreground=[('selected', '#000000')])

        style.configure("Treeview.Heading",
                        background="#2D2D2D",
                        foreground=self.ACCENT_BEIGE,
                        font=('Helvetica', 10, 'bold'),
                        bordercolor=self.BORDER_COLOR)
        style.map("Treeview.Heading", background=[('active', '#3D3D3D')])

    def _build_ui(self):
        # 1. HEADER
        header_frame = tk.Frame(self.root, bg=self.BG_CARD, pady=15, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))

        title = tk.Label(header_frame, text="CPU Scheduling Algorithm Simulator", font=("Helvetica", 20, "bold"),
                         bg=self.BG_CARD, fg=self.ACCENT_BEIGE)
        title.pack()
        subtitle = tk.Label(header_frame, text="Visualizing and Comparing CPU Scheduling Techniques",
                            font=("Helvetica", 10, "italic"), bg=self.BG_CARD, fg=self.TEXT_MUTED)
        subtitle.pack(pady=(2, 0))

        # 2. MAIN LAYOUT CONTAINER
        main_container = tk.Frame(self.root, bg=self.BG_MAIN)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # LEFT PANEL: Controls & Input Table
        left_panel = tk.Frame(main_container, bg=self.BG_MAIN)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))

        self._build_input_section(left_panel)
        self._build_table_section(left_panel)
        self._build_controls_section(left_panel)

        # RIGHT PANEL: Output Metrics, Comparison & Gantt Chart
        right_panel = tk.Frame(main_container, bg=self.BG_MAIN)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_output_section(right_panel)
        self._build_gantt_section(right_panel)

    def _build_input_section(self, parent):
        frame = tk.LabelFrame(parent, text=" Process Input ", bg=self.BG_CARD, fg=self.ACCENT_BEIGE,
                              font=("Helvetica", 11, "bold"), padx=10, pady=10, bd=1, relief="solid")
        frame.pack(fill=tk.X, pady=(0, 10))

        fields = [("Process ID:", "pid_entry"), ("Arrival Time:", "arr_entry"),
                  ("Burst Time:", "burst_entry"), ("Priority:", "prio_entry")]

        for idx, (label_text, attr_name) in enumerate(fields):
            lbl = tk.Label(frame, text=label_text, bg=self.BG_CARD, fg=self.TEXT_MAIN, anchor="w", font=("Helvetica", 9))
            lbl.grid(row=idx // 2, column=(idx % 2) * 2, sticky="w", padx=5, pady=5)
            
            entry = tk.Entry(frame, bg=self.BG_ENTRY, fg=self.TEXT_MAIN, insertbackground=self.TEXT_MAIN,
                             bd=1, relief="solid", width=12, font=("Helvetica", 10))
            entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
            setattr(self, attr_name, entry)

        # Action Buttons
        btn_frame = tk.Frame(frame, bg=self.BG_CARD)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        self._create_btn(btn_frame, "Add Process", self.add_process, self.ACCENT_GOLD, "#000000").pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_frame, "Update", self.update_process, "#3A3A3A", self.TEXT_MAIN).pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_frame, "Delete", self.delete_process, "#3A3A3A", self.TEXT_MAIN).pack(side=tk.LEFT, padx=3)
        self._create_btn(btn_frame, "Clear All", self.clear_all, "#8B0000", "#FFFFFF").pack(side=tk.LEFT, padx=3)

    def _build_table_section(self, parent):
        frame = tk.LabelFrame(parent, text=" Process List (Starts Empty) ", bg=self.BG_CARD, fg=self.ACCENT_BEIGE,
                              font=("Helvetica", 11, "bold"), padx=10, pady=10, bd=1, relief="solid")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("PID", "Arrival", "Burst", "Priority")
        self.process_tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=70, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscroll=scrollbar.set)

        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.process_tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _build_controls_section(self, parent):
        frame = tk.LabelFrame(parent, text=" Algorithm Selection & Controls ", bg=self.BG_CARD, fg=self.ACCENT_BEIGE,
                              font=("Helvetica", 11, "bold"), padx=10, pady=10, bd=1, relief="solid")
        frame.pack(fill=tk.X)

        # Radio Selection
        self.algo_var = tk.StringVar(value="FCFS")
        algos = [("FCFS", "FCFS"), ("SJF", "SJF"), ("Priority", "Priority"), ("Round Robin", "RR")]

        radio_frame = tk.Frame(frame, bg=self.BG_CARD)
        radio_frame.pack(fill=tk.X, pady=(0, 5))

        for text, mode in algos:
            rb = tk.Radiobutton(radio_frame, text=text, variable=self.algo_var, value=mode,
                                bg=self.BG_CARD, fg=self.TEXT_MAIN, selectcolor=self.BG_ENTRY,
                                activebackground=self.BG_CARD, activeforeground=self.ACCENT_BEIGE,
                                command=self._toggle_quantum_state)
            rb.pack(side=tk.LEFT, expand=True)

        # Quantum Entry
        q_frame = tk.Frame(frame, bg=self.BG_CARD)
        q_frame.pack(fill=tk.X, pady=5)

        tk.Label(q_frame, text="Time Quantum (RR):", bg=self.BG_CARD, fg=self.TEXT_MAIN,
                 font=("Helvetica", 9)).pack(side=tk.LEFT, padx=(5, 10))
        self.quantum_entry = tk.Entry(q_frame, bg=self.BG_ENTRY, fg=self.TEXT_MAIN, insertbackground=self.TEXT_MAIN,
                                      bd=1, relief="solid", width=8, state=tk.DISABLED)
        self.quantum_entry.pack(side=tk.LEFT)

        # Trigger Buttons
        btn_frame = tk.Frame(frame, bg=self.BG_CARD)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        self._create_btn(btn_frame, "Run Selected Algorithm", self.run_selected, self.ACCENT_GOLD, "#000000").pack(fill=tk.X, pady=2)
        self._create_btn(btn_frame, "Run All & Compare", self.run_all_compare, "#4A5D4E", self.TEXT_MAIN).pack(fill=tk.X, pady=2)
        self._create_btn(btn_frame, "Reset Simulator", self.reset_all, "#3A3A3A", self.TEXT_MAIN).pack(fill=tk.X, pady=2)

    def _build_output_section(self, parent):
        self.output_notebook = ttk.Notebook(parent)
        self.output_notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Tab 1: Execution Details
        self.single_tab = tk.Frame(self.output_notebook, bg=self.BG_CARD)
        self.output_notebook.add(self.single_tab, text=" Execution Results ")

        columns = ("PID", "Arrival", "Burst", "Priority", "CT", "TAT", "WT")
        self.results_tree = ttk.Treeview(self.single_tab, columns=columns, show="headings", height=5)
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=65, anchor="center")

        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Metrics display bar
        metrics_bar = tk.Frame(self.single_tab, bg=self.BG_CARD)
        metrics_bar.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.lbl_avg_wt = tk.Label(metrics_bar, text="Average WT: -", bg=self.BG_CARD, fg=self.ACCENT_BEIGE, font=("Helvetica", 10, "bold"))
        self.lbl_avg_wt.pack(side=tk.LEFT, padx=15)

        self.lbl_avg_tat = tk.Label(metrics_bar, text="Average TAT: -", bg=self.BG_CARD, fg=self.ACCENT_BEIGE, font=("Helvetica", 10, "bold"))
        self.lbl_avg_tat.pack(side=tk.LEFT, padx=15)

        # Tab 2: Comparison View
        self.compare_tab = tk.Frame(self.output_notebook, bg=self.BG_CARD)
        self.output_notebook.add(self.compare_tab, text=" Algorithm Comparison ")

        comp_cols = ("Algorithm", "Average Waiting Time", "Average Turnaround Time")
        self.compare_tree = ttk.Treeview(self.compare_tab, columns=comp_cols, show="headings", height=5)
        for col in comp_cols:
            self.compare_tree.heading(col, text=col)
            self.compare_tree.column(col, width=150, anchor="center")

        self.compare_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.compare_tree.bind("<<TreeviewSelect>>", self._on_comparison_select)

    def _build_gantt_section(self, parent):
        frame = tk.LabelFrame(parent, text=" Gantt Chart ", bg=self.BG_CARD, fg=self.ACCENT_BEIGE,
                              font=("Helvetica", 11, "bold"), padx=5, pady=5, bd=1, relief="solid")
        frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 2.5), dpi=100)
        self.fig.patch.set_facecolor(self.BG_CARD)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        render_gantt_chart([], self.fig)

    def _create_btn(self, parent, text, command, bg, fg):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=self.ACCENT_BEIGE, activeforeground="#000000",
                         font=("Helvetica", 9, "bold"), bd=0, relief="flat", cursor="hand2", padx=8, pady=4)

    def _toggle_quantum_state(self):
        if self.algo_var.get() == "RR":
            self.quantum_entry.config(state=tk.NORMAL, bg=self.BG_ENTRY)
        else:
            self.quantum_entry.config(state=tk.DISABLED, bg="#202020")

    # --- VALIDATION & HELPERS ---
    def _validate_inputs(self, check_quantum=False):
        pid = self.pid_entry.get().strip()
        arr_str = self.arr_entry.get().strip()
        burst_str = self.burst_entry.get().strip()
        prio_str = self.prio_entry.get().strip()

        if not pid:
            messagebox.showerror("Validation Error", "Process ID cannot be empty.")
            return None

        try:
            arrival = int(arr_str)
            if arrival < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Arrival Time must be a non-negative integer.")
            return None

        try:
            burst = int(burst_str)
            if burst <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Burst Time must be a positive integer (> 0).")
            return None

        try:
            priority = int(prio_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Priority must be a valid integer.")
            return None

        quantum = None
        if check_quantum:
            q_str = self.quantum_entry.get().strip()
            try:
                quantum = int(q_str)
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation Error", "Time Quantum must be a positive integer (> 0).")
                return None

        return {"pid": pid, "arrival": arrival, "burst": burst, "priority": priority, "quantum": quantum}

    # --- PROCESS MANAGEMENT HANDLERS ---
    def add_process(self):
        data = self._validate_inputs()
        if not data:
            return

        # Check Duplicate Process ID
        if any(str(p['pid']) == str(data['pid']) for p in self.processes):
            messagebox.showerror("Validation Error", f"Process ID '{data['pid']}' already exists.")
            return

        proc = {'pid': data['pid'], 'arrival': data['arrival'], 'burst': data['burst'], 'priority': data['priority']}
        self.processes.append(proc)
        self._refresh_tree()
        self._clear_input_fields()

    def update_process(self):
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a process from the table to update.")
            return

        data = self._validate_inputs()
        if not data:
            return

        item = self.process_tree.item(selected[0])
        old_pid = str(item['values'][0])

        # If PID changed, check for collision
        if str(data['pid']) != old_pid and any(str(p['pid']) == str(data['pid']) for p in self.processes):
            messagebox.showerror("Validation Error", f"Process ID '{data['pid']}' already exists.")
            return

        for p in self.processes:
            if str(p['pid']) == old_pid:
                p['pid'] = data['pid']
                p['arrival'] = data['arrival']
                p['burst'] = data['burst']
                p['priority'] = data['priority']
                break

        self._refresh_tree()
        self._clear_input_fields()

    def delete_process(self):
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a process to delete.")
            return

        item = self.process_tree.item(selected[0])
        target_pid = str(item['values'][0])

        self.processes = [p for p in self.processes if str(p['pid']) != target_pid]
        self._refresh_tree()
        self._clear_input_fields()

    def clear_all(self):
        self.processes.clear()
        self._refresh_tree()
        self._clear_input_fields()
        self.reset_all()

    def _clear_input_fields(self):
        self.pid_entry.delete(0, tk.END)
        self.arr_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.prio_entry.delete(0, tk.END)

    def _refresh_tree(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        for p in sorted(self.processes, key=lambda x: str(x['pid'])):
            self.process_tree.insert("", tk.END, values=(p['pid'], p['arrival'], p['burst'], p['priority']))

    def _on_tree_select(self, event):
        selected = self.process_tree.selection()
        if selected:
            item = self.process_tree.item(selected[0])
            vals = item['values']
            self._clear_input_fields()
            self.pid_entry.insert(0, vals[0])
            self.arr_entry.insert(0, vals[1])
            self.burst_entry.insert(0, vals[2])
            self.prio_entry.insert(0, vals[3])

    # --- EXECUTION & SIMULATION HANDLERS ---
    def _execute_algo(self, algo_key, quantum=None):
        if algo_key == "FCFS":
            return run_fcfs(self.processes)
        elif algo_key == "SJF":
            return run_sjf(self.processes)
        elif algo_key == "Priority":
            return run_priority(self.processes)
        elif algo_key == "RR":
            return run_round_robin(self.processes, quantum)

    def run_selected(self):
        if not self.processes:
            messagebox.showerror("Execution Error", "No processes entered! Please add at least one process.")
            return

        algo = self.algo_var.get()
        quantum = None

        if algo == "RR":
            q_str = self.quantum_entry.get().strip()
            try:
                quantum = int(q_str)
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Validation Error", "Please provide a valid Time Quantum (> 0) for Round Robin.")
                return

        gantt, process_metrics = self._execute_algo(algo, quantum)
        detailed, avg_wt, avg_tat = compute_metrics(process_metrics)

        self._display_single_results(detailed, avg_wt, avg_tat)
        render_gantt_chart(gantt, self.fig)
        self.canvas.draw()

        self.output_notebook.select(self.single_tab)

    def run_all_compare(self):
        if not self.processes:
            messagebox.showerror("Execution Error", "No processes entered! Please add at least one process.")
            return

        quantum = 2  # Default fallback if quantum not provided
        q_str = self.quantum_entry.get().strip()
        if q_str:
            try:
                q_val = int(q_str)
                if q_val > 0:
                    quantum = q_val
            except ValueError:
                pass

        algos = [("FCFS", "FCFS", None),
                 ("SJF", "SJF", None),
                 ("Priority", "Priority", None),
                 ("Round Robin", "RR", quantum)]

        for item in self.compare_tree.get_children():
            self.compare_tree.delete(item)

        self.last_results.clear()

        for display_name, algo_key, q in algos:
            gantt, process_metrics = self._execute_algo(algo_key, q)
            detailed, avg_wt, avg_tat = compute_metrics(process_metrics)

            self.last_results[display_name] = {
                'gantt': gantt,
                'detailed': detailed,
                'avg_wt': avg_wt,
                'avg_tat': avg_tat
            }

            self.compare_tree.insert("", tk.END, values=(display_name, f"{avg_wt:.2f}", f"{avg_tat:.2f}"))

        self.output_notebook.select(self.compare_tab)
        
        # Default select FCFS to show chart
        first_item = self.compare_tree.get_children()[0]
        self.compare_tree.selection_set(first_item)

    def _on_comparison_select(self, event):
        selected = self.compare_tree.selection()
        if selected:
            item = self.compare_tree.item(selected[0])
            algo_name = item['values'][0]

            if algo_name in self.last_results:
                res = self.last_results[algo_name]
                render_gantt_chart(res['gantt'], self.fig)
                self.canvas.draw()
                self._display_single_results(res['detailed'], res['avg_wt'], res['avg_tat'])

    def _display_single_results(self, detailed_results, avg_wt, avg_tat):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for p in detailed_results:
            self.results_tree.insert("", tk.END, values=(
                p['pid'], p['arrival'], p['burst'], p['priority'],
                p['completion'], p['tat'], p['wt']
            ))

        self.lbl_avg_wt.config(text=f"Average WT: {avg_wt:.2f}")
        self.lbl_avg_tat.config(text=f"Average TAT: {avg_tat:.2f}")

    def reset_all(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        for item in self.compare_tree.get_children():
            self.compare_tree.delete(item)

        self.lbl_avg_wt.config(text="Average WT: -")
        self.lbl_avg_tat.config(text="Average TAT: -")
        self.last_results.clear()

        render_gantt_chart([], self.fig)
        self.canvas.draw()