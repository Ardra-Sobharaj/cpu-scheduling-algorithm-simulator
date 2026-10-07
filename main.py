import tkinter as tk
from gui.simulator_gui import CPUSchedulerApp

def main():
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()