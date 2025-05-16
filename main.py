import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QColorDialog, QTableWidget,
    QTableWidgetItem, QGroupBox, QMessageBox, QCheckBox, QSplitter, QTextEdit,
    QHeaderView, QFrame, QSizePolicy, QSlider, QToolTip, QAction, QMenu,QLineEdit, 
    QShortcut, QStyle, QFileDialog, QScrollArea, QToolBar, QStatusBar
)
from PyQt5.QtGui import QColor, QFont, QPalette, QKeySequence, QIcon, QPainter, QBrush,QIntValidator
from PyQt5.QtCore import Qt, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

# Choose a preferred style, falling back gracefully
preferred_styles = ['seaborn-v0_8', 'seaborn', 'ggplot', 'default']
for style in preferred_styles:
    if style in mpl.style.available:
        mpl.style.use(style)
        # print(f"Using matplotlib style: '{style}'")
        break
else:
    print("Warning: No preferred style found. Using default matplotlib style.")

# Custom Colors scheme
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'background': '#f5f5f5',
    'main-title': '#2980b9',
}
# Custom styles Sheet
STYLE_SHEET = f"""
QMainWindow, QDialog, QWidget {{
    background-color: {COLORS['background']};
}}

QGroupBox {{
    font-weight: bold;
    border: 1px solid {COLORS['secondary']};
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 0px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top center;
    color: {COLORS['dark']};
}}

QPushButton {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #2980b9;
}}

QPushButton:pressed {{
    background-color: #1f618d;
}}

QPushButton:disabled {{
    background-color: #bdc3c7;
}}

QComboBox, QSpinBox {{
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 4px;
    background: white;
}}

QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {COLORS['accent']};
}}


QTableWidget {{
    alternate-background-color: #eaeaea;
    gridline-color: #d4d4d4;
    
}}
   
QHeaderView::section {{
    background-color: {COLORS['secondary']};
    padding: 5px;
    font-weight: bold;
    color: white;
}}

QLabel {{
    color: {COLORS['dark']};
}}

QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border: 1px solid {COLORS['accent']};
}}

QTextEdit {{
    border-radius: 4px;
    background-color: white;
    padding: 5px;   
}}

QScrollBar:vertical {{
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: #c0c0c0;
    max-height: 20px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: #a0a0a0;
}}
QScrollBar:horizontal {{
        height: 12px;
    background: #f0f0f0;
   }}

QScrollBar::handle:horizontal {{
        background: #c0c0c0;
      min-width: 20px;
  }}
QStatusBar {{
    background-color: {COLORS['secondary']};
    color: white;
}}
"""
# Set default font for the application
class CustomCanvas(FigureCanvas):
    def __init__(self, parent=None, width=12, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=COLORS['background'])
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor(COLORS['light'])
        super().__init__(fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        fig.tight_layout()

# Custom horizontal line for separation
class HorizontalLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(f"background-color: {COLORS['secondary']};")
class ProcessConfigPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.show_missed = True
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Process Configuration Group
        gb = QGroupBox("Process Configuration")
        gb.setFont(QFont("Arial", 10, QFont.Bold))
        v = QVBoxLayout(gb)
        v.setSpacing(10)

        # Simple mode toggle
        mode_layout = QHBoxLayout()
        self.simple_mode = QCheckBox("Simple Mode (p_i, e_i only)")
        self.simple_mode.setToolTip("Toggle between simple and advanced configuration")
        self.simple_mode.setFont(QFont("Arial", 9))
        mode_layout.addWidget(self.simple_mode)
        mode_layout.addStretch()
        v.addLayout(mode_layout)
        self.simple_mode.stateChanged.connect(self.toggle_simple_mode)

        # Separator line
        v.addWidget(HorizontalLine())

        # Process table setup
        table_label = QLabel("Process Parameters")
        table_label.setFont(QFont("Arial", 9, QFont.Bold))
        v.addWidget(table_label)

        self.table = QTableWidget(0, 7)  
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        headers = ["Process", "r_i", "p_i", "e_i", "d_i", "Priority", "Color"]
        tooltips = [
            "Process ID", "Release/Arrival Time", "Period", 
            "Execution Time", "Deadline", "Priority (1=highest)", "Process Color"
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for i, tip in enumerate(tooltips):
            self.table.horizontalHeaderItem(i).setToolTip(tip)

        hdr = self.table.horizontalHeader()
        for i in range(len(headers)):
            if i == 0 or i == 6:
                hdr.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                hdr.setSectionResizeMode(i, QHeaderView.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(150)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v.addWidget(self.table)

        # Add/Remove buttons
        ctrl = QHBoxLayout()
        add = QPushButton("Add Process")
        add.setStyleSheet(f"background-color: {COLORS['accent']}; color: white;")
        add.setStyleSheet(f""" QPushButton:hover {{
                background-color: #2980b9;
            }}
            """)
        # add.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        add.clicked.connect(self.add_process)
        rem = QPushButton("Remove Process")
        rem.setStyleSheet(f"background-color:{COLORS['danger']}; color: white;")
        # rem.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        rem.clicked.connect(self.remove_process)
        ctrl.addWidget(add)
        ctrl.addWidget(rem)
        ctrl.addStretch()
        v.addLayout(ctrl)

        # Separator and jobs control
        v.addWidget(HorizontalLine())
        jobs_layout = QVBoxLayout()
        jobs_header = QHBoxLayout()
        jobs_header.addWidget(QLabel("Jobs per Process:"))
        jobs_value_label = QLabel("2")
        jobs_value_label.setAlignment(Qt.AlignRight)
        jobs_header.addWidget(jobs_value_label)
        jobs_layout.addLayout(jobs_header)

        jobs_slider_layout = QHBoxLayout()
        self.jobs_spin = QSpinBox()
        self.jobs_spin.setRange(1, 20)
        self.jobs_spin.setValue(2)
        self.jobs_spin.valueChanged.connect(lambda v: jobs_value_label.setText(str(v)))
        jobs_slider = QSlider(Qt.Horizontal)
        jobs_slider.setRange(1, 20)
        jobs_slider.setValue(2)
        jobs_slider.valueChanged.connect(self.jobs_spin.setValue)
        self.jobs_spin.valueChanged.connect(jobs_slider.setValue)
        jobs_slider_layout.addWidget(jobs_slider)
        jobs_slider_layout.addWidget(self.jobs_spin)
        jobs_layout.addLayout(jobs_slider_layout)
        v.addLayout(jobs_layout)

        main_layout.addWidget(gb)
        for _ in range(3): self.add_process()
        self.toggle_simple_mode()

    def toggle_simple_mode(self):
        simple = self.simple_mode.isChecked()
        self.table.setColumnHidden(1, simple)
        self.table.setColumnHidden(4, simple)
        for col in (1, 4):
            item = self.table.horizontalHeaderItem(col)
            if simple:
                item.setForeground(Qt.gray)
                item.setToolTip(f"{item.toolTip()} (disabled in simple mode)")
            else:
                item.setForeground(Qt.white)
                item.setToolTip(item.toolTip().replace(" (disabled in simple mode)", ""))

    def add_process(self):
        r = self.table.rowCount()
        self.table.insertRow(r)

        # Process ID
        pid = QTableWidgetItem(f"P{r+1}")
        pid.setFlags(pid.flags() & ~Qt.ItemIsEditable)
        pid.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(r, 0, pid)

        # Numeric input fields
        def create_input(col, default, max_val=1000):
            le = QLineEdit(str(default))
            le.setValidator(QIntValidator(0, max_val))
            le.setAlignment(Qt.AlignCenter)
            # le.setStyleSheet("background: white; border: 1px solid #bdc3c7;")
            self.table.setCellWidget(r, col, le)

        # Arrival time
        if not self.simple_mode.isChecked():
            create_input(1, 0)

        # Period, Execution, Deadline
        create_input(2, 6)
        create_input(3, 2)
        if not self.simple_mode.isChecked():
            create_input(4, 6)

        # Priority
        create_input(5, r+1, 10)

        # Color picker

        color = QColor(*[np.random.randint(0, 255) for _ in range(3)])
        btn = QPushButton()
        btn.setProperty('color', color)
        btn.setStyleSheet(f"background-color:{color.name()}; border: 1px solid #999;")
        btn.setToolTip("Click to change process color")
        btn.setFixedWidth(40)
        btn.clicked.connect(lambda _, row=r: self.choose_color(row))
        self.table.setCellWidget(r, 6, btn)
        self.table.setRowHeight(r, 30)

    def remove_process(self):
        if self.table.rowCount() > 1:
            self.table.removeRow(self.table.rowCount() - 1)
    # Choose color for process
    def choose_color(self, row):
        btn = self.table.cellWidget(row, 6)
        curr = btn.property('color')
        c = QColorDialog.getColor(curr, self, "Choose Process Color")
        if c.isValid():
            btn.setProperty('color', c)
            btn.setStyleSheet(f"background-color:{c.name()}; border: 1px solid #999;")

    def get_processes(self):
        procs = []
        simple = self.simple_mode.isChecked()
        for r in range(self.table.rowCount()):
            def get_val(col):
                return int(self.table.cellWidget(r, col).text())

            arrival = 0 if simple else get_val(1)
            period = get_val(2)
            execution = get_val(3)
            deadline = period if simple else get_val(4)
            
            procs.append({
                'id': r,
                'name': self.table.item(r, 0).text(),
                'arrival': arrival,
                'period': period,
                'execution': execution,
                'deadline': deadline,
                'priority': get_val(5),
                'color': self.table.cellWidget(r, 6).property('color').name()
            })
        return procs, self.jobs_spin.value()
# Scheduler Algorithm Panel
class AlgorithmPanel(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(10)
        
        gb = QGroupBox("Scheduling Algorithm")
        gb.setFont(QFont("Arial", 10, QFont.Bold))
        g = QVBoxLayout(gb)
        g.setSpacing(10)

        # Algorithm selection
        algo_label = QLabel("Select Algorithm:")
        algo_label.setFont(QFont("Arial", 9))
        g.addWidget(algo_label)

        self.combo = QComboBox()
        self.combo.setFont(QFont("Arial", 9))
        self.combo.setStyleSheet("""
            QComboBox {
                min-width: 200px;
            }
        """)
        self.combo.addItem("-- General Purpose --")
        self.combo.model().item(0).setEnabled(False)
        self.combo.addItems(["FCFS", "SJN", "SRT", "Priority", "Round Robin"])

        self.combo.addItem("-- Multilevel --")
        self.combo.model().item(6).setEnabled(False)
        self.combo.addItem("Multilevel Queues")
        self.combo.addItem("-- Real-Time --")
        self.combo.model().item(8).setEnabled(False)
        self.combo.addItems(["Minimum Laxity", "RMS", "EDF"])
        # coming soon
        self.combo.addItem("-- Coming Soon! --")
        self.combo.model().item(11).setEnabled(False)
        self.combo.addItem("MLFQ")

        # Set tooltips for algorithms
        tooltips = {
            "FCFS": "First Come First Served - Non-preemptive scheduling based on arrival time", # First Come First Served
            "SJN": "Shortest Job Next - Non-preemptive scheduling based on execution time", # Shortest Job Next
            "SRT": "Shortest Remaining Time - Preemptive version of SJN", # Shortest Remaining Time
            "Priority": "Preemptive priority scheduling", # Preemptive priority scheduling
            "Round Robin": "Time-sharing algorithm using time quantum", # Round Robin
            "Multilevel Queues": "Multiple queues with different priorities", # Multilevel Queues
            "Minimum Laxity": "Schedules based on slack time (deadline - remaining execution)", # Minimum Laxity
            "RMS": "Rate Monotonic Scheduling - Static priority based on period", # Rate Monotonic Scheduling
            "EDF": "Earliest Deadline First - Dynamic priority based on absolute deadline" # Earliest Deadline First
        }
        
        for i in range(self.combo.count()):
            item_text = self.combo.itemText(i)
            if item_text in tooltips:
                self.combo.setItemData(i, tooltips[item_text], Qt.ToolTipRole)
                
        g.addWidget(self.combo)

        # Add separator
        g.addWidget(HorizontalLine())

        # Parameters in a clean grid layout
        params_group = QGroupBox("Parameters")
        params_group.setFont(QFont("Arial", 9, QFont.Bold))
        grid = QGridLayout(params_group)
        grid.setSpacing(10)

        # Time Quantum
        self.tq_label = QLabel("Time Quantum:")
        self.tq_label.setFont(QFont("Arial", 9))
        self.tq = QSpinBox()
        self.tq.setRange(1, 50)
        self.tq.setValue(2)
        self.tq.setToolTip("Time slice for Round Robin scheduling")
        grid.addWidget(self.tq_label, 0, 0)
        grid.addWidget(self.tq, 0, 1)

        # Max Time
        self.max_t_label = QLabel("Max Time:")
        self.max_t_label.setFont(QFont("Arial", 9))
        self.max_t = QSpinBox()
        self.max_t.setRange(10, 1000)
        self.max_t.setValue(100) 
        self.max_t.setToolTip("Maximum simulation time")
        grid.addWidget(self.max_t_label, 1, 0)
        grid.addWidget(self.max_t, 1, 1)

        # Show Missed
        self.show_miss = QCheckBox("Show Missed Deadlines")
        self.show_miss.setFont(QFont("Arial", 9))
        self.show_miss.setChecked(True)
        self.show_miss.setToolTip("Highlight missed deadlines on the Gantt chart")
        grid.addWidget(self.show_miss, 2, 0, 1, 2)

        g.addWidget(params_group)

        # Add separator
        g.addWidget(HorizontalLine())

        # Run button with prominent styling
        self.run = QPushButton("Run Simulation")
        self.run.setFont(QFont("Arial", 10, QFont.Bold))
        self.run.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #27ae60;
            }}
            QPushButton:pressed {{
                background-color: #219653;
            }}
        """)
        self.run.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.run.setIconSize(QSize(16, 16))
        g.addWidget(self.run)

        v.addWidget(gb)
        v.addStretch()

        self.combo.currentTextChanged.connect(self.update_fields_visibility)
        self.update_fields_visibility()

    def update_fields_visibility(self):
        alg = self.combo.currentText()
        
        # Skip headers
        if alg.startswith("--"):
            self.combo.setCurrentIndex(self.combo.currentIndex() + 1)
            return
            
        needs_quantum = (alg == "Round Robin")
        needs_maxt = (alg not in ["FCFS", "SJN"])
        
        self.tq.setVisible(needs_quantum)
        self.tq_label.setVisible(needs_quantum)
        
        self.max_t.setVisible(needs_maxt)
        self.max_t_label.setVisible(needs_maxt)

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(0)

        # Gantt Chart Section
        gb = QGroupBox("Gantt Charts")
        gb.setFont(QFont("Arial", 10, QFont.Bold))
        chart_layout = QVBoxLayout(gb)
        # chart_layout.setSpacing(2)
        
        # Main Gantt chart
        self.canvas = CustomCanvas(height=2)
        chart_layout.addWidget(self.canvas , stretch=8)

        # Horizontal line for separation
        chart_layout.addWidget(HorizontalLine())


        # Contiguous Gantt chart
        contig_label = QLabel("Contiguous Timeline:")
        contig_label.setFont(QFont("Arial", 8, QFont.Bold))
        contig_label.setAlignment(Qt.AlignLeft)
        chart_layout.addWidget(contig_label)
    
        # Add a small canvas for the contiguous chart
        self.canvas_contig = CustomCanvas(height=1)
        self.canvas_contig.setStyleSheet("background-color: #ecf0f1;")  # light background
        chart_layout.addWidget(self.canvas_contig, stretch=4)
        
        v.addWidget(gb)

        # Statistics & Analysis Section
        gb2 = QGroupBox("Statistics & Analysis")
        gb2.setFont(QFont("Arial", 10, QFont.Bold))
        stats_layout = QVBoxLayout(gb2)
        stats_layout.setSpacing(10)
        
        # Text summary
        stats_label = QLabel("Summary:")
        stats_label.setFont(QFont("Arial", 9, QFont.Bold))
        stats_layout.addWidget(stats_label)
        
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(QFont("Arial", 9))
        self.text.setMaximumHeight(50)
        stats_layout.addWidget(self.text)
        
        # Job analysis table
        job_label = QLabel("Job Analysis:")
        job_label.setFont(QFont("Arial", 9, QFont.Bold))
        stats_layout.addWidget(job_label)
        
        self.job_table = QTableWidget()
        self.job_table.setFont(QFont("Arial", 9))
        self.job_table.setAlternatingRowColors(True)
        self.job_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.job_table.verticalHeader().setVisible(False)
        stats_layout.addWidget(self.job_table)
        
        v.addWidget(gb2)

    # def update(self, sch, procs, jc, missed, alg, show_missed):
    def update(self, sch, procs, jc, missed, alg, show_missed):
        self.show_missed = show_missed  # Store the flag
        ax = self.canvas.axes
        ax.clear()
        
        # Draw Gantt chart
        for j, s, e, pid in sch:
            y = (len(procs) - pid) * 0.8
            col = procs[pid]['color']
            dl = procs[pid]['arrival'] + j * procs[pid]['period'] + procs[pid]['deadline']
            opts = {}
            if e > dl:
                opts = {'edgecolor': 'red', 'linewidth': 2}
            ax.barh(y, e - s, left=s, height=0.6, color=col, **opts)
            if e - s >= 2:
                ax.text(s + (e - s)/2, y, f"J{pid+1},{j+1}", 
                        ha='center', va='center', color='black', fontweight='bold')

        # Handle missed deadlines display
        if self.show_missed:
            for j, dl, pid in missed:
                y = (len(procs) - pid) * 0.8
                ax.plot([dl, dl], [y-0.4, y+0.4], 'r--', linewidth=2)
                ax.plot(dl, y, 'rx', markersize=8)

        # Chart formatting
        ax.set_yticks([(len(procs)-i)*0.8 for i in range(len(procs))])
        ax.set_yticklabels([p['name'] for p in procs])
        ax.set_xlabel("Time")
        ax.set_title(f"{alg} Gantt Chart",color=COLORS['main-title'], fontsize=10, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas.draw()

        # Statistics calculation
        total_jobs = len(sch)
        missed_jobs = len(missed)
        
        # Prevent division by zero
        missed_percent = 0.0
        if total_jobs > 0:
            missed_percent = (missed_jobs / total_jobs) * 100

        utilization = sum(p['execution']/p['period'] for p in procs) if procs else 0
        
        stats_text = (
            f"👉🏻 Algorithm Used: {alg}\t"
            f"👉🏻 Total Jobs: {total_jobs}\t"
            f"👉🏻 Completed: {total_jobs - missed_jobs}\t"
            f"👉🏻 Missed: {missed_jobs} ({missed_percent:.1f}%)\t"
            f"👉🏻 Utilization: {utilization:.2f} "
            f"({'Schedulable ✅' if utilization <= 1 else 'Overloaded ❌'})"
        )
        self.text.setPlainText(stats_text)
        
        # Update other components
        self.draw_contiguous(sch, procs)
        self.populate_job_table(sch, missed, procs)
    def draw_contiguous(self, sch, procs):
        ax = self.canvas_contig.axes
        ax.clear()
        ax.set_facecolor(COLORS['light'])
        
        y = 0.2
        for j, s, e, pid in sch:
            col = procs[pid]['color']
            ax.barh(y, e - s, left=s, height=0.2, color=col)
            if e - s >= 2:
                ax.text(s + (e - s) / 2, y, f"J{pid+1},{j+1}", ha='center', va='center', 
                        color='black', fontweight='bold')
                        
        ax.set_yticks([y])
        # rotate y-ticks to avoid overlap
        # add margin bottom to y-ticks label
        ax.set_yticklabels(["Timeline"], rotation=90)
        ax.set_xlabel("Time", fontsize=8, fontweight='bold')
        ax.set_title("Contiguous Gantt Chart",color=COLORS['main-title'], fontsize=10, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        self.canvas_contig.draw()

    def populate_job_table(self, sch, missed, procs):
        headers = ["Job", "Start", "End", "Deadline", "Missed", "Response Time", "Waiting Time"]
        self.job_table.clear()
        self.job_table.setColumnCount(len(headers))
        self.job_table.setHorizontalHeaderLabels(headers)
        self.job_table.setRowCount(len(sch))
        
        miss_map = {(j, pid): dl for j, dl, pid in missed}
        
        for i, (j, st, et, pid) in enumerate(sch):
            arrival = procs[pid]['arrival'] + j * procs[pid]['period']
            dl = arrival + procs[pid]['deadline']
            is_miss = (j, pid) in miss_map
            
            response_time = et - arrival
            waiting_time = st - arrival
            
            vals = [
                f"J{pid+1},{j+1}", 
                st, 
                et, 
                dl, 
                "Yes" if is_miss else "No",
                response_time,
                waiting_time
            ]
            
            for c, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Highlight missed deadlines
                if c == 4 and v == "Yes":
                    item.setForeground(QColor(COLORS['danger']))
                    item.setFont(QFont("Arial", 7, QFont.Bold))
                    
                self.job_table.setItem(i, c, item)
                
        # Resize columns to content
        self.job_table.resizeColumnsToContents()

class AboutDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Scheduler Simulator")
        self.setFixedSize(500, 300)
        layout = QVBoxLayout(self)
        
        title = QLabel("Scheduler Simulator")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        version = QLabel("Version 2.0")
        version.setFont(QFont("Arial", 10))
        version.setAlignment(Qt.AlignCenter)
        
        desc = QLabel(
            "An interactive tool for visualizing and comparing\n"
            "various CPU scheduling algorithms.\n\n"
            "Supports both general purpose and real-time scheduling."
        )
        desc.setAlignment(Qt.AlignCenter)
        
        author = QLabel("© 2025 Advanced Scheduling Systems")
        author.setAlignment(Qt.AlignCenter)
        
        close = QPushButton("Close")
        close.clicked.connect(self.close)
        
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addSpacing(20)
        layout.addWidget(desc)
        layout.addSpacing(20)
        layout.addWidget(author)
        layout.addSpacing(10)
        layout.addWidget(close)
        layout.addStretch()

class SchedulerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./icon.jpeg"))
        self.setWindowTitle("Scheduler Simulator")
        # self.resize(1280, 900)
        self.setMinimumSize(800, 600)
        
        # Apply global stylesheet
        self.setStyleSheet(STYLE_SHEET)
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Create menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        # Add menu actions
        new_action = QAction("New Simulation", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_simulation)
        
        save_action = QAction("Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_config)
        
        load_action = QAction("Load Configuration", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_config)
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Create toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        toolbar.addAction(new_action)
        toolbar.addAction(save_action)
        toolbar.addAction(load_action)
        toolbar.addSeparator()
        
        run_action = QAction("Run", self)
        run_action.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        toolbar.addAction(run_action)
        
        # Create main widget and layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create panels
        self.proc_panel = ProcessConfigPanel()
        self.alg_panel = AlgorithmPanel()
        self.result_panel = ResultPanel()
        
        # Create left container with scrolling capability
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.proc_panel)
        left_layout.addWidget(self.alg_panel)
        left_layout.addStretch()
        
        # Make left panel scrollable
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(left_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_scroll)
        splitter.addWidget(self.result_panel)
        
        # Set initial size proportions
        # splitter.setSizes([400, 880])  # Adjust these values as needed
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Connect signals
        self.alg_panel.run.clicked.connect(self.run_sim)
        run_action.triggered.connect(self.run_sim)
        
        # Create keyboard shortcuts
        run_shortcut = QShortcut(QKeySequence("F5"), self)
        run_shortcut.activated.connect(self.run_sim)
    
    def new_simulation(self):
        """Reset all configurations to default."""
        reply = QMessageBox.question(self, "New Simulation", 
                                    "Are you sure you want to reset all configurations?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Reset process panel
            for _ in range(self.proc_panel.table.rowCount()):
                self.proc_panel.remove_process()
            for _ in range(3):
                self.proc_panel.add_process()
            self.proc_panel.simple_mode.setChecked(False)
            self.proc_panel.jobs_spin.setValue(2)
            
            # Reset algorithm panel
            self.alg_panel.combo.setCurrentIndex(1)  
            self.alg_panel.tq.setValue(2)
            self.alg_panel.max_t.setValue(100)
            self.alg_panel.show_miss.setChecked(True)
            
            # Clear results
            self.result_panel.text.clear()
            self.result_panel.job_table.setRowCount(0)
            self.result_panel.canvas.axes.clear()
            self.result_panel.canvas.draw()
            self.result_panel.canvas_contig.axes.clear()
            self.result_panel.canvas_contig.draw()
            
            self.statusBar.showMessage("Created new simulation", 3000)
    
    def save_config(self):
        """Save current configuration to a file."""
        filename, _ = QFileDialog.getSaveFileName(self, "Save Configuration", 
                                                 "", "Config Files (*.cfg)")
        if filename:
            if not filename.endswith('.cfg'):
                filename += '.cfg'
            try:
                # Implement actual save logic here
                # For example, save process settings, algorithm choice, etc.
                self.statusBar.showMessage(f"Configuration saved to {filename}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Save Error ❌", f"Error saving configuration: {str(e)} ")
    
    def load_config(self):
        """Load configuration from a file."""
        filename, _ = QFileDialog.getOpenFileName(self, "Load Configuration", 
                                                 "", "Config Files (*.cfg)")
        if filename:
            try:
                # Implement actual load logic here
                # For example, restore process settings, algorithm choice, etc.
                self.statusBar.showMessage(f"Configuration loaded from {filename}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Load Error ❌", f"Error loading configuration: {str(e)}")
    
    def show_about(self):
        """Show the about dialog."""
        dialog = AboutDialog(self)
        dialog.show()
    
    def run_sim(self):
        """Run the simulation with current settings"""
        try:
            # Get configurations
            procs, jc = self.proc_panel.get_processes()
            alg = self.alg_panel.combo.currentText()
            maxt = self.alg_panel.max_t.value()
            tq = self.alg_panel.tq.value()
            show_missed = self.alg_panel.show_miss.isChecked()
            # Validate input
            if not procs:
                QMessageBox.warning(self, "Error ❌", "Add at least one process!")
                return
            if alg.startswith("--"):
                QMessageBox.warning(self, "Error ❌", "Select a valid algorithm!")
                return

            # Run selected algorithm
            alg_methods = {
                "FCFS": self.run_fcfs,
                "SJN": self.run_sjn,
                "SRT": self.run_srt,
                "Priority": self.run_priority,
                "Round Robin": self.run_round_robin,
                "Multilevel Queues": self.run_multilevel_queues,
                "ML": self.run_minimum_laxity,
                "RMS": self.run_rms,
                "EDF": self.run_edf
            }
            
            if alg not in alg_methods:
                raise ValueError(f"Unsupported algorithm: {alg} ❌❌❌")
                
            schedule, missed_deadlines = alg_methods[alg](procs, jc, maxt, tq)

            # Update results with actual data
            self.result_panel.update(
                schedule, 
                procs, 
                jc, 
                missed_deadlines, 
                alg, 
                show_missed
            )
            self.statusBar.showMessage(f"Simulation completed using {alg}", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Simulation failed: {str(e)}")
            self.statusBar.showMessage("Simulation error", 5000)
    # Job generation
    def _generate_jobs(self, procs, jc, maxt):
        jobs = []
        for p in procs:
            for j in range(jc):
                arr = p['arrival'] + j * p['period']
                if arr < maxt:
                    jobs.append({
                        'job': j,
                        'pid': p['id'],
                        'r': arr,
                        'e': p['execution'],
                        'rem': p['execution'],
                        'dl': arr + p['deadline'],
                        'pr': p['priority']
                    })
        return jobs

    # FCFS
    def run_fcfs(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        jobs.sort(key=lambda x: x['r'])
        t = 0
        sch = []
        miss = []
        
        for job in jobs:
            if t < job['r']:
                t = job['r']
            st = t
            en = st + job['e']
            sch.append((job['job'], st, en, job['pid']))
            if en > job['dl']:
                miss.append((job['job'], job['dl'], job['pid']))
            t = en
            
        return sch, miss

    # SJN
    def run_sjn(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        rem = sorted(jobs, key=lambda x: x['r'])
        ready = []
        t = 0
        sch = []
        miss = []
        
        while rem or ready:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
            if not ready:
                t = rem[0]['r']
                continue
                
            job = min(ready, key=lambda x: x['e'])
            ready.remove(job)
            st = t
            en = st + job['e'] 
            sch.append((job['job'], st, en, job['pid']))
            if en > job['dl']:
                miss.append((job['job'], job['dl'], job['pid']))
            t = en
            
        return sch, miss

    # SRT
    def run_srt(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        rem = sorted(jobs, key=lambda x: x['r'])
        ready = []
        t = 0
        sch = []
        miss = []
        current = None
        start = 0
        
        while rem or ready or current:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
                
            if current and ready and min(ready, key=lambda x: x['rem'])['rem'] < current['rem']:
                sch.append((current['job'], start, t, current['pid']))
                ready.append(current)
                current = None
                
            if not current and ready:
                current = min(ready, key=lambda x: x['rem'])
                ready.remove(current)
                start = t
                
            if not current:
                t = rem[0]['r'] if rem else maxt
                continue
                
            next_arrival = rem[0]['r'] if rem else maxt
            step = min(current['rem'], next_arrival - t if next_arrival > t else maxt)
            current['rem'] -= step
            t += step
            
            if current['rem'] == 0:
                sch.append((current['job'], start, t, current['pid']))
                if t > current['dl']:
                    miss.append((current['job'], current['dl'], current['pid']))
                current = None
                
            if t >= maxt:
                break
                
        return sch, miss

    # Priority (preemptive)
    def run_priority(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        rem = sorted(jobs, key=lambda x: x['r'])
        ready = []
        t = 0
        current = None
        start = 0
        sch = []
        miss = []
        
        while rem or ready or current:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
                
            ready.sort(key=lambda x: -x['pr'])  # Higher priority value = higher priority
            
            if current and ready and ready[0]['pr'] > current['pr']:
                sch.append((current['job'], start, t, current['pid']))
                ready.append(current)
                current = None
                
            if not current and ready:
                current = ready.pop(0)
                start = t
                
            if not current:
                t = rem[0]['r'] if rem else maxt
                continue
                
            next_arrival = rem[0]['r'] if rem else maxt
            step = min(current['rem'], next_arrival - t if next_arrival > t else current['rem'])
            current['rem'] -= step
            t += step
            
            if current['rem'] == 0:
                sch.append((current['job'], start, t, current['pid']))
                if t > current['dl']:
                    miss.append((current['job'], current['dl'], current['pid']))
                current = None
                
            if t >= maxt:
                break
                
        return sch, miss

    # Round Robin
    def run_round_robin(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        ready = []
        rem = sorted(jobs, key=lambda x: x['r'])
        t = 0
        sch = []
        miss = []
        
        while rem or ready:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
                
            if not ready:
                t = rem[0]['r']
                continue
                
            job = ready.pop(0)
            st = t
            run = min(tq, job['rem'])
            job['rem'] -= run
            t += run
            
            sch.append((job['job'], st, t, job['pid']))
            
            if job['rem'] > 0:
                ready.append(job)
            else:
                if t > job['dl']:
                    miss.append((job['job'], job['dl'], job['pid']))
                    
            if t >= maxt:
                break
                
        return sch, miss

    # Multilevel queues
    def run_multilevel_queues(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        
        # Find median priority to split into queues
        priorities = [p['priority'] for p in procs]
        med = np.median(priorities) if priorities else 5
        
        # Split jobs into high and low priority queues
        high = [j for j in jobs if j['pr'] > med]
        low = [j for j in jobs if j['pr'] <= med]
        
        sch = []
        miss = []
        t = 0
        
        # Process high priority queue first, then low priority
        for q in [sorted(high, key=lambda x: x['r']), sorted(low, key=lambda x: x['r'])]:
            for job in q:
                if t < job['r']:
                    t = job['r']
                st = t
                en = st + job['e']
                sch.append((job['job'], st, en, job['pid']))
                if en > job['dl']:
                    miss.append((job['job'], job['dl'], job['pid']))
                t = en
                
        return sch, miss

    # Minimum Laxity
    def run_minimum_laxity(self, procs, jc, maxt, tq):
        jobs = self._generate_jobs(procs, jc, maxt)
        rem = sorted(jobs, key=lambda x: x['r'])
        ready = []
        t = 0
        current = None
        start = 0
        sch = []
        miss = []
        
        while rem or ready or current:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
                
            if current:
                ready.append(current)
                current = None
                
            if ready:
                # Calculate laxity (slack time) for each job
                laxities = [(j['dl'] - (t + j['rem']), j) for j in ready]
                # Select job with minimum laxity
                current = min(laxities, key=lambda x: x[0])[1]
                ready.remove(current)
                start = t
                
            if not current:
                t = rem[0]['r'] if rem else maxt
                continue
                
            next_arrival = rem[0]['r'] if rem else maxt
            step = min(current['rem'], next_arrival - t if next_arrival > t else current['rem'])
            current['rem'] -= step
            t += step
            
            if current['rem'] == 0:
                sch.append((current['job'], start, t, current['pid']))
                if t > current['dl']:
                    miss.append((current['job'], current['dl'], current['pid']))
                current = None
                
            if t >= maxt:
                break
                
        return sch, miss

    # RMS
    def run_rms(self, procs, jc, maxt, tq):
        # Rate Monotonic Scheduling (static priority based on shortest period)
        rms_procs = []
        
        # Assign RMS priorities - lower period = higher priority
        for p in procs:
            p_copy = p.copy()
            p_copy['priority'] = 10000 / p['period']  # Invert for correct priority direction
            rms_procs.append(p_copy)
            
        return self.run_priority(rms_procs, jc, maxt, tq)

    # EDF
    def run_edf(self, procs, jc, maxt, tq):
        # Earliest Deadline First (dynamic priority by nearest deadline)
        jobs = self._generate_jobs(procs, jc, maxt)
        rem = sorted(jobs, key=lambda x: x['r'])
        ready = []
        t = 0
        sch = []
        miss = []
        current = None
        start = 0
        
        while rem or ready or current:
            while rem and rem[0]['r'] <= t:
                ready.append(rem.pop(0))
                
            if current:
                ready.append(current)
                current = None
                
            if ready:
                # Select job with earliest absolute deadline
                current = min(ready, key=lambda x: x['dl'])
                ready.remove(current)
                start = t
                
            if not current:
                t = rem[0]['r'] if rem else maxt
                continue
                
            next_arrival = rem[0]['r'] if rem else maxt
            step = min(current['rem'], next_arrival - t if next_arrival > t else current['rem'])
            current['rem'] -= step
            t += step
            
            if current['rem'] == 0:
                sch.append((current['job'], start, t, current['pid']))
                if t > current['dl']:
                    miss.append((current['job'], current['dl'], current['pid']))
                current = None
                
            if t >= maxt:
                break
                
        return sch, miss
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchedulerGUI()
    window.show()
    sys.exit(app.exec_())