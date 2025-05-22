import tkinter as tk
from tkinter import ttk
import constants
import controller
import time

class app(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        super().__init__(self.root)
        self.root.geometry('494x553')
        self.root.resizable(False, False)
        self.root.configure(background='DarkOliveGreen3')
        self.root.title('SeedSorter Software')
        self.root.bind('<KeyPress-Left>', self.on_press_left)
        self.root.bind('<KeyPress-Right>', self.on_press_right)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self._nsteps_bl = 1
        self._frame = 0
        
        self.port = constants.PORT
        self.widgets('light steel blue')
        self.animate()
        self.mainloop()

    def widgets(self, bg_color):
        self.amplitude_val = tk.IntVar(self.root, constants.AMPLITUDE)
        self.frequency_val = tk.IntVar(self.root, constants.FREQUENCY)
        self.phase_val = tk.IntVar(self.root, constants.PHASE)
        self.delta_val = tk.IntVar(self.root, constants.DELTA)
        self.timestep_val = tk.IntVar(self.root, constants.TIME_STEP)
        self.nsteps_val = tk.IntVar(self.root, constants.N_STEPS)


        self.title = tk.Label(
            self.root,
            text='SeedSorter',
            font=('Segoe UI', 29),
            bg="DarkOliveGreen4",
            fg='black', highlightbackground="darkolivegreen", highlightthickness=2
        )
        self.title.place(x=80, y=0, width=328, height=64)

        self.keys = ttk.Button(self.root, text='Joystick/Keys')
        self.keys.place(x=24, y=432, width=112, height=48)

        self.ext = tk.Button(self.root, text='External', font=('Segoe UI', 9), command=self.ext_Command)
        self.ext.place(x=24, y=488, width=112, height=48)

        self.run = tk.Button(self.root, text='RUN', font=('Segoe UI', 12, 'bold'), bg='green', command=self.run_Command)
        self.run.place(x=352, y=432, width=120, height=48)

        self.stop = tk.Button(self.root, text='STOP', font=('Segoe UI', 12, 'bold'), bg='#cc0000', command=self.stop_Command)
        self.stop.place(x=352, y=480, width=120, height=56)

        self.vibration = tk.Button(self.root, text='Vibration', font=('Segoe UI', 9, 'bold'), bg='Royalblue3', command=self.vibration_Command)
        self.vibration.place(x=360, y=360, width=96, height=40)

        self.delta = tk.Scale(self.root, variable=self.delta_val, from_=-45, to=45, resolution=5, orient='horizontal', command=self.delta_Command, bg=bg_color)
        self.delta.place(x=24, y=176, width=120, height=48)

        self.freq = tk.Scale(self.root, variable=self.frequency_val, from_=35, to=45, resolution=0.1, orient='horizontal', command=self.freq_Command, bg=bg_color)
        self.freq.place(x=24, y=264, width=120, height=48)

        self.phase = tk.Scale(self.root, variable=self.phase_val, from_=0, to=180, orient='horizontal', command=self.phase_Command, bg=bg_color)
        self.phase.place(x=24, y=352, width=120, height=48)

        self.timestep = tk.Scale(self.root, variable=self.timestep_val, from_=10, to=100, command=self.timestep_Command, bg=bg_color)
        self.timestep.place(x=200, y=176, width=64, height=120)

        self.nsteps = tk.Scale(self.root, variable=self.nsteps_val, from_=0, to=200, resolution=10, orient='horizontal', command=self.nsteps_Command, bg=bg_color)
        self.nsteps.place(x=184, y=352, width=120, height=48)

        self.wave1 = tk.Frame(self.root, bg=bg_color, highlightbackground="wheat4", highlightthickness=2)
        self.wave1.place(x=335, y=140, width=120, height=80)

        self.canvas1 = tk.Canvas(self.wave1, bg="#f0f0f0", highlightthickness=0, width=120, height=80)
        self.canvas1.place(x=0, y=0)

        label_kwargs = {'font': ('Arial Rounded MT Bold', 10, "bold"), 'bg': "DarkOliveGreen3", 'anchor': 'center'}
        self.lPORT = tk.Label(self.root, text='PORT', **label_kwargs)
        self.lPORT.place(x=24, y=88, width=48, height=24)

        self.portmenuCV = tk.StringVar()
        self.portmenuCV.set('COM3')
        self.portmenu = ttk.Combobox(
        self.root, 
        textvariable=self.portmenuCV, 
        values=['COM8', 'COM7', 'COM6', 'COM5', 'COM4', 'COM3', 'COM2', 'COM1'], 
        font=('Segoe UI', 9))
                            
        self.portmenu.place(x=88, y=88, width=80, height=24)
        self.portmenu.bind('<<ComboboxSelected>>', lambda event: self.select_port())
        self.arduino = controller.Arduino(self.portmenuCV.get(), baudrate=9600)
        
        
        self.lDELTA1 = tk.Label(self.root, text='DELTA (°)', **label_kwargs)
        self.lDELTA1.place(x=48, y=144, width=79, height=24)

        self.lFREQUENCYkHz = tk.Label(self.root, text='FREQUENCY (kHz)', **label_kwargs)
        self.lFREQUENCYkHz.place(x=24, y=232, width=116, height=24)

        self.lPHASE = tk.Label(self.root, text='PHASE', **label_kwargs)
        self.lPHASE.place(x=56, y=320, width=56, height=24)

        self.lTIMESTEPms = tk.Label(self.root, text='TIMESTEP (ms)', **label_kwargs)
        self.lTIMESTEPms.place(x=184, y=144, width=97, height=24)

        self.lNSTEPS = tk.Label(self.root, text='N STEPS', **label_kwargs)
        self.lNSTEPS.place(x=216, y=320, width=58, height=24)

        self.VELOCITY = tk.Label(self.root, text='Vel. = 0.0 mm/s', font=('Arial Rounded MT Bold', 9, "bold"), bg="cornsilk3", anchor='center', highlightbackground="wheat4", highlightthickness=1)
        self.VELOCITY.place(x=340, y=240, width=110, height=30)

    def draw_square_wave(self, shift=0):
        width = 120
        height = 80
        self.canvas1.delete("all")
        cycles = 2
        pixels_per_cycle = (width / cycles) * float(round((self.frequency_val.get() / 40), 2))
        phase_shift = (self.delta_val.get() / 360) * pixels_per_cycle + shift

        points = []
        half_height = height // 2
        amplitude = height // 4

        for x in range(width):
            pos_in_cycle = ((x + phase_shift) % pixels_per_cycle) / pixels_per_cycle
            value = 1 if pos_in_cycle < 0.5 else -1
            y = half_height + value * amplitude
            points.extend([x, y])

        self.canvas1.create_line(points, fill="#800020", width=2)

    def animate(self):
        if not hasattr(self, "_step_counter"):
            self._step_counter = 0
        self._frame = (self._frame + self._nsteps_bl * self.delta_val.get() / 9) % self.canvas1.winfo_width()
        self.draw_square_wave(shift=self._frame)
        self._step_counter += 1
        nsteps = self.nsteps_val.get()
        if nsteps > 0 and self._step_counter >= nsteps:
            self._nsteps_bl *= -1
            self._step_counter = 0
        self.root.after(self.timestep_val.get(), self.animate)

    def update_velocity(self):
        f = self.freq.get()
        omega = self.delta.get()
        time = self.timestep.get()
        velocity = (omega * 343600) / (time * 360 * f)
        self.VELOCITY.config(text=f"Vel: {velocity:.1f} mm/s")

    def freq_Command(self, value):
        value = self.freq.get()
        self.arduino.send_command(f"FREQUENCY {1000 * value}")
        print(f"FREQUENCY SET {value} kHz")
        self.update_velocity()

    def delta_Command(self, value):
        value = self.delta.get()
        self.arduino.send_command("MODE 2")
        self.arduino.send_command(f"DELTA {-value}")
        print(f"DELTA SET {value} °")
        self.update_velocity()

    def nsteps_Command(self, value):
        value = self.nsteps.get()
        self.arduino.send_command('MODE 2')
        self.arduino.send_command(f'NSTEPS {value}')
        print(f"N steps = {value}")

    def timestep_Command(self, value):
        value = self.timestep.get()
        self.arduino.send_command(f"TIMESTEP {value}")
        print(f"TIMESTEP SET TO {value} ms")
        self.update_velocity()

    def on_press_left(self, event):
        print("30º to left")
        self.arduino.send_command("MODE 2")
        self.arduino.send_command("DELTA 30")
        self.arduino.send_command("PAUSE")



    def on_press_right(self, event):
        print("30º to right")
        
        #self.delta.set(-30)
        #time.sleep(1)
        #self.delta.set(0)
        
        self.arduino.send_command("MODE 2")
        self.arduino.send_command("DELTA -30")
        self.arduino.send_command("PAUSE")

    def phase_Command(self, value):
        value = self.phase.get()
        self.arduino.send_command("MODE 0")
        self.arduino.send_command(f"PHASE {value}")
        print(f"PHASE SET TO {value}")

    def ext_Command(self):
        self.arduino.send_command("MODE 1")

    def run_Command(self):
 #       self.arduino.send_command("MODE 2")
 #       self.arduino.send_command("DELTA 30")
 #       self.arduino.send_command("TIMESTEP 60")
 #       self.arduino.send_command("NSTEPS 50")
 #        self.VELOCITY.config(text="Vel: 14.3 mm/s")
 
         self.arduino.send_command("MODE 2")
         self.delta.set(30)
         self.timestep.set(60)
         self.nsteps.set(50)
         
         
    def stop_Command(self):
 #       self.arduino.send_command("NSTEPS 0")
 #       self.arduino.send_command("PAUSE")
#         self.VELOCITY.config(text="Vel: 0 mm/s")
 
         self.arduino.send_command("PAUSE")
         self.delta.set(0)
         self.nsteps.set(0)
 
 

    def vibration_Command(self):
        self.arduino.send_command("MODE 0")
        i = 0
        while i < 15:
            self.arduino.send_command("PHASE 90")
            self.arduino.send_command("FREQUENCY 41500")
            time.sleep(0.04)
            self.arduino.send_command("FREQUENCY 39000")
            self.arduino.send_command("PHASE 1")
            time.sleep(0.04)
            i += 1
    
    def select_port(self):
        port = self.portmenuCV.get()
        if self.arduino is not None: 
            self.arduino.close()  
        self.arduino = controller.Arduino(port, baudrate=9600)
        print(f"Connected to {port}")
        
    def close_window(self):
        self.arduino.close()
        self.root.destroy()
