# Scheduler Simulator 🖥️⏱️

A GUI application for visualizing CPU scheduling algorithms, built with PyQt5 and Matplotlib.

![Screenshot](./ReadmeImg.png?text=Scheduler+Simulator+Screenshot)

## Features ✨

- Supports 10+ scheduling algorithms:
  - FCFS, SJN, SRT, Priority, Round Robin
  - Multilevel Queues, Minimum Laxity, RMS, EDF
- Interactive process configuration
- Real-time Gantt chart visualization
- Job statistics and analysis
- Cross-platform compatibility (Windows/Linux/macOS)

## Installation 📥

### Windows Users

1. Download the latest release from [Releases page](https://github.com/Eng-Ahmed-Hussien/TaskSchedulerSimulator)
2. Run `SchedulerSimulator.exe`
3. (Optional) Add to PATH for command-line access

**System Requirements:**

- Windows 10 or newer
- .NET Framework 8 (usually pre-installed)

### For Other Platforms

```bash
git clone https://github.com/Eng-Ahmed-Hussien/TaskSchedulerSimulator
pip install -r requirements.txt
python main.py
```

## Usage 🚀

1. **Add Processes**  
   Configure process parameters in the left panel
2. **Select Algorithm**  
   Choose from the dropdown menu
3. **Run Simulation**  
   Click the "Run Simulation" button (▶️) or press F5
4. **Analyze Results**  
   View Gantt charts and statistics in the right panel

![UI Demo](./demoImg.png?text=UI+Walkthrough)

## Build from Source 🔨

1. Install requirements:

```bash
pip install pyinstaller matplotlib pyqt5 numpy
```

or

```bash
pip install requirements.txt
```

2. Create executable:

```bash
pyinstaller --name SchedulerSimulator --windowed --icon=myImg.jpg --add-data="myImg.jpg;." main.py
```

3. Find executable in `dist/` directory

## Requirements 📦

- Python 3.8+
- PyQt5
- Matplotlib
- NumPy

## Contributing 🤝

1. Fork the repository
2. Create your feature branch:

```bash
git checkout -b feature/your-feature
```

3. Commit your changes:

```bash
git commit -m 'Add some feature'
```

4. Push to the branch:

```bash
git push origin feature/your-feature
```

5. Open a pull request

## License 📄

MIT License - See [LICENSE](LICENSE) for details

---

**Note:** The executable may trigger antivirus warnings due to PyInstaller packaging. This is a false positive. [Learn more](https://github.com/pyinstaller/pyinstaller/issues/4629)
