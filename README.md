# Real-Time-Process-Monitoring-Dashboard


# [Dashboard Screenshot] 
![RealTimeProcessMonitoringDashboard](https://github.com/user-attachments/assets/524fba09-08e2-4ca4-a1bf-d0cfc64b4085)


A Python-based GUI application for monitoring system processes, CPU, and memory usage in real-time.  

## Features  

✅ **Real-time Monitoring**  
- Live CPU and memory usage graphs  
- Process list with details (PID, name, status, user)  
- System uptime tracking  

✅ **Process Management**  
- End individual processes  
- Kill entire process trees  
- Adjust process priority  

✅ **Alert System**  
- Notifications for high CPU (>90%) or memory (>90%) usage  
- Alert log with timestamps  

✅ **User-Friendly Interface**  
- Search and filter processes  
- Responsive design  
- Dark/light mode support  

## Installation  

### Method 1: From Source  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/Real-Time-Process-Monitoring-Dashboard.git
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:  
   ```bash
   python process_monitor.py
   ```

### Method 2: Download Executable  
- Windows: `ProcessMonitor.exe`  
- macOS: `ProcessMonitor.app`  
- Linux: `process_monitor`  

## Usage  

1. Launch the application  
2. View real-time system metrics in the graphs  
3. Manage processes using the buttons:  
   - **Refresh**: Update process list  
   - **End Process**: Terminate selected process  
   - **End Tree**: Terminate process and its children  
   - **Set Priority**: Change process priority  

## Building from Source  

To create your own executable:  

1. Install PyInstaller:  
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:  
   ```bash
   pyinstaller --onefile --windowed --icon=assets/icon.ico process_monitor.py
   ```
3. Find the executable in the `dist` folder  

## Requirements  

- Python 3.8+  
- Packages:  
  - psutil  
  - matplotlib  
  - tkinter  

## Contributing  

Contributions welcome! Please:  
1. Fork the repository  
2. Create a new branch  
3. Submit a pull request  

## License  

MIT License  

## Screenshots  

![CPU Monitoring] ![Process Management] ![image](https://github.com/user-attachments/assets/a7991774-2496-4125-b0d4-25b307ab6142)

*Real-time CPU usage graph*  
*Process list with management options*  


This README includes:  
- Clear feature highlights  
- Multiple installation options  
- Usage instructions  
- Build instructions  
- Contribution guidelines  
- Visual examples  
- License information  

You'll want to:  
1. Replace `yourusername` with your GitHub username  
2. Add actual screenshots to the `screenshots` folder  
3. Update the license if you're using something other than MIT  
4. Add your contact info in the Support section  

The markdown formatting uses:  
- Headers for clear section separation  
- Emojis for visual appeal  
- Code blocks for commands  
- Bullet points for easy scanning  
- Links to key resources
