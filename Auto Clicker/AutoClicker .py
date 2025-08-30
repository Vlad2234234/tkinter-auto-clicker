import pyautogui
from keyboard import *
from webbrowser import open_new_tab
from tkinter import *
from tkinter import ttk

class AutoClickerApp(Tk):
    def __init__(self):
        super().__init__()

        self.title('Auto Clicker')
        self.geometry('500x400')
        self.resizable(False, False)
        self.call('tk', 'scaling', 1.388)
        self.iconbitmap('\\Auto Clicker\\icon.ico')
        pyautogui.FAILSAFE = False
        
        self.unpack_control = ControlFrame(self)
        self.unpack_control.place(x=0, y=287)
        self.unpack_position = PositionCanvas(self)
        self.unpack_position.place(x=25, y=215)
        self.unpack_time = TimeCanvas(self)
        self.unpack_time.place(x=25, y=15)
        self.unpack_repeat = RepeatCanvas(self)
        self.unpack_repeat.place(x=258, y=90)
        self.unpack_click_options = ClickOptionsCanvas(self)
        self.unpack_click_options.place(x=25, y=90)        

        self.unpack_decor = DecorMixin(self)      

        self.values = (self.unpack_position.xValue,
                       self.unpack_position.yValue,
                       self.unpack_time.millisecsValue,
                       self.unpack_time.secsValue,
                       self.unpack_time.minsValue,
                       self.unpack_time.hrsValue,
                       self.unpack_repeat.times
                       )
        
        self.entries = (self.unpack_position.x_entry,
                        self.unpack_position.y_entry,
                        self.unpack_time.millisecs_entry,
                        self.unpack_time.secs_entry,
                        self.unpack_time.mins_entry,
                        self.unpack_time.hrs_entry,
                        self.unpack_repeat.times_to_click_entry
                        )
        
        for value in self.values:
            value.trace_add("write", self.validator)

        for entry in self.entries:
            entry.bind("<FocusIn>", lambda event: event.widget.delete(0, END))

        for entry in self.entries:
            entry.bind("<FocusOut>", self.is_empty)             

    def validator(self, var_name, index, mode):
        for entry in self.entries:
            for i, val in enumerate(entry.get()):
                if not val.isdigit():
                    entry.delete(i, i+1)
    
    def is_empty(self, event):
        for entry in self.entries:
            if not entry.get():             
                if event.widget == self.unpack_time.millisecs_entry:
                    if not entry.get():
                        entry.insert(0, 100)
                elif event.widget == self.unpack_repeat.times_to_click_entry:
                    if not entry.get():
                        entry.insert(0, 1)
                else:
                    if not entry.get():
                        entry.insert(0, 0)    

    def clicking(self):

        self.milliseconds = int(self.unpack_time.millisecsValue.get())
        self.seconds = int(self.unpack_time.secsValue.get()) * 1000
        self.minutes = int(self.unpack_time.minsValue.get()) * 60000
        self.hours = int(self.unpack_time.hrsValue.get()) * 3600000

        if self.state() == 'iconic':
            if self.unpack_repeat.repetition.get():
                self.unpack_control.times_clicked += 1

            if self.unpack_click_options.selected_click_type_option.get() == 'Single':
                self.click_type = 1
            elif self.unpack_click_options.selected_click_type_option.get() == 'Double':
                self.click_type = 2

            if self.unpack_position.position_status.get():
                pyautogui.moveTo(int(self.unpack_position.x_entry.get()), int(self.unpack_position.y_entry.get()))

            pyautogui.click(button=self.unpack_click_options.selected_mouse_button_option.get().lower(), clicks=self.click_type)
        
        if self.unpack_control.times_clicked != int(self.unpack_repeat.times.get()) or not self.unpack_repeat.repetition.get():
            self.id = self.after(self.hours+self.minutes+self.seconds+self.milliseconds, self.clicking)
    
class ControlFrame(Frame):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent)
        self.parent = parent
        
        self.unpack_hotkey_window = HotkeySettingWindow(self)
        self.unpack_hotkey_window.destroy()

        self.unpack_decor = DecorMixin(self)
        
        self.was_started = BooleanVar(value=False)

        self.start_button = ttk.Button(self,
                                       text=f"Start ({self.unpack_hotkey_window.unpack_hotkey_frame.currently_binded.get()})",
                                       style="CustomMain.TButton",
                                       command=self.start_clicking
                                       )
        self.start_button.grid(ipadx=20, 
                               ipady=2.5, 
                               column=0, 
                               row=0, 
                               padx=32.5
                               )
   
        self.stop_button = ttk.Button(self,
                                      text=f"Stop ({self.unpack_hotkey_window.unpack_hotkey_frame.currently_binded.get()})",
                                      style="CustomMain.TButton",
                                      command=self.stop_clicking
                                      )
        self.stop_button.grid(ipadx=20, 
                              ipady=2.5, 
                              column=1, 
                              row=0, 
                              padx=60
                              )
        
        self.github_button = ttk.Button(self,
                                        text='GitHub',
                                        style="CustomMain.TButton",
                                        command=lambda:open_new_tab('https://github.com/Vlad2234234/')
                                        )
        self.github_button.grid(ipadx=20, 
                                ipady=2.5, 
                                column=1, 
                                row=1, 
                                padx=60,
                                pady=10
                                )
        
        self.keybind_button = ttk.Button(self,
                                         text='Keybind',
                                         style="CustomMain.TButton",
                                         command=lambda: HotkeySettingWindow(self)
                                         )
        self.keybind_button.grid(ipadx=20, 
                                 ipady=2.5, 
                                 column=0, 
                                 row=1, 
                                 padx=32.5,
                                 pady=10
                                 )

        self.hotkey_id = add_hotkey(f'{self.unpack_hotkey_window.unpack_hotkey_frame.currently_binded.get()}', self.start_clicking)  

    def start_clicking(self):

        self.times_clicked = 0

        if not self.was_started.get():
            self.parent.iconify()
            remove_hotkey(self.hotkey_id)
            self.hotkey_id = add_hotkey(f'{self.unpack_hotkey_window.unpack_hotkey_frame.currently_binded.get()}', self.stop_clicking)
            self.was_started.set(True)
            self.parent.clicking()
        else:
            self.was_started.set(False)
            self.after_cancel(self.parent.id)
            self.start_clicking()

    def stop_clicking(self):
        if self.was_started.get():
            remove_hotkey(self.hotkey_id)
            self.hotkey_id = add_hotkey(f'{self.unpack_hotkey_window.unpack_hotkey_frame.currently_binded.get()}', self.start_clicking)
            self.was_started.set(False)
            self.parent.after_cancel(self.parent.id)

class HotkeySettingWindow(Toplevel):
    def __init__(self, parent: AutoClickerApp | ControlFrame):
        super().__init__(parent)
        self.parent = parent
        
        self.title('Setting')
        self.geometry('300x150')
        self.resizable(False, False)
        self.iconbitmap('\\Auto Clicker\\icon.ico')

        self.unpack_hotkey_frame = HotkeySettingFrame(self)
        self.unpack_hotkey_frame.place(x=0, y=0)

        self.KEYMAP = {65: "a", 66: "b", 67: "c", 68: "d", 69: "e",
                       70: "f", 71: "g", 72: "h", 73: "i", 74: "j",
                       75: "k", 76: "l", 77: "m", 78: "n", 79: "o",
                       80: "p", 81: "q", 82: "r", 83: "s", 84: "t",
                       85: "u", 86: "v", 87: "w", 88: "x", 89: "y",
                       90: "z",
                       }

class HotkeySettingFrame(Frame):
    def __init__(self, parent: HotkeySettingWindow):
        super().__init__(parent, width=300, height=150)
        self.parent = parent

        with open("\\Auto Clicker\\config.txt", '+r', encoding='utf-8') as config:
            self.currently_binded = StringVar(value=config.readline()[17:29].strip())
        
        self.unpack_decor = DecorMixin(self)

        self.start_stop_label = ttk.Label(self,
                                          text='Start / Stop:',
                                          font=('Segoe UI', 15)
                                          )
        self.start_stop_label.place(x=20, y=30)

        self.binding_entry = ttk.Entry(self,
                                       font=('Segoe UI', 15, 'bold'),
                                       width=11,
                                       state='readonly',
                                       textvariable=self.currently_binded
                                       )
        self.binding_entry.place(x=145, y=30)
        
        self.choose_button = ttk.Button(self,
                                        text='Choose',
                                        style='CustomMain.TButton',
                                        command=self.start_choosing_hotkey
                                        )
        self.choose_button.place(x=75, y=85)
        
    def start_choosing_hotkey(self):
        self.parent.parent.stop_clicking()
        remove_hotkey(self.parent.parent.hotkey_id)
        self.hotkey_selector = Toplevel(bg='#262625')
        self.hotkey_selector.title('Select Coordinates')
        self.hotkey_selector.iconbitmap('\\Auto Clicker\\icon.ico')
        self.hotkey_selector.focus_set()
        for k, v in {'-alpha': 0.7, '-fullscreen': True}.items():
            self.hotkey_selector.attributes(k, v)
        
        self.hotkey_selector.bind('<Key>', self.finish_choosing)
    
    def finish_choosing(self, event):
        self.binding_entry.delete(0, END)
        with open("\\Auto Clicker\\config.txt", '+r', encoding='utf-8') as config:
            lines = config.readlines()
        
        for i in range(len(lines)):
            if lines[i].startswith("currently_binded="):
                if event.keycode in self.parent.KEYMAP.keys():
                    lines[i] = f"currently_binded={self.parent.KEYMAP[event.keycode]}\n"
                    self.currently_binded.set(self.parent.KEYMAP[event.keycode])
                    self.parent.parent.hotkey_id = add_hotkey(f'{self.currently_binded.get()}', self.parent.parent.start_clicking)
                    self.parent.parent.start_button.config(text=f"Start ({self.currently_binded.get()})")
                    self.parent.parent.stop_button.config(text=f"Stop ({self.currently_binded.get()})") 
                else:
                    lines[i] = f"currently_binded={event.keysym}"
                    self.currently_binded.set(event.keysym) 
                    self.parent.parent.hotkey_id = add_hotkey(f'{self.currently_binded.get()}', self.parent.parent.start_clicking)
                    self.parent.parent.start_button.config(text=f"Start ({self.currently_binded.get()})")
                    self.parent.parent.stop_button.config(text=f"Stop ({self.currently_binded.get()})")      

        with open("\\Auto Clicker\\config.txt", '+w', encoding='utf-8') as config:
            config.writelines(lines)

        self.hotkey_selector.destroy()

class PositionCanvas(Canvas):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent, highlightthickness=0)
        self.parent = parent

        self.unpack_decor = DecorMixin(self)
        self.unpack_decor.create_wide_rectangle()
        ttk.Label(self.parent, text="Cursor position").place(x=35, y=206)


        self.position_status = BooleanVar(value=True)

        self.current_position = ttk.Radiobutton(self,
                                                text="Current location",
                                                variable=self.position_status,
                                                value=False,
                                                command=self.which_option
                                                )
        self.current_position.place(x=20, y=20)

        self.choose_position = ttk.Radiobutton(self,
                                               text="Choose location",
                                               variable=self.position_status,
                                               value=True,
                                               command=self.which_option
                                               )
        self.choose_position.place(x=150, y=20)
        
        self.pick_button = ttk.Button(self,
                                      text="Pick",
                                      style="Custom.TButton",
                                      width=6,
                                      command=self.start_picking
                                      )
        self.pick_button.place(x=270, y=15)


        self.xValue = IntVar()

        self.x_label = ttk.Label(self,
                                 text="X",
                                 style="Custom.TLabel"
                                 )
        self.x_label.place(x=340, y=18.5)
        
        self.x_entry = ttk.Entry(self,
                                 width=4,
                                 textvariable=self.xValue
                                 )
        self.x_entry.place(x=355, y=20)

        self.yValue = IntVar()

        self.y_label = ttk.Label(self,
                                 text="Y",
                                 style="Custom.TLabel"
                                 )
        self.y_label.place(x=390, y=18.5)
        
        self.y_entry = ttk.Entry(self,
                                 width=4,
                                 textvariable=self.yValue
                                 )
        self.y_entry.place(x=405, y=20)


        for variable in (self.xValue, self.yValue):
            variable.trace_add('write', self.limit)

    def start_picking(self):
        self.coordinate_selector = Toplevel(bg='#262625')
        self.coordinate_selector.title('Select Coordinates')
        self.coordinate_selector.iconbitmap('\\Auto Clicker\\icon.ico')
        self.coordinate_selector.focus_set()
        for k, v in {'-alpha': 0.7, '-fullscreen': True}.items():
            self.coordinate_selector.attributes(k, v)

        self.coordinate_selector.bind('<Escape>', self.stop_picking)
        self.coordinate_selector.bind('<Button-1>', self.finish_picking)   
    
    def stop_picking(self, event):
        self.coordinate_selector.unbind('<Escape>')
        self.coordinate_selector.unbind('<Button-1>')
        self.coordinate_selector.destroy()

    def finish_picking(self, event):
        self.x_entry.delete(0, END), self.y_entry.delete(0, END)
        x, y = self.coordinate_selector.winfo_pointerx(), self.coordinate_selector.winfo_pointery()
        self.x_entry.insert(0, str(x)), self.y_entry.insert(0, str(y))
        self.coordinate_selector.destroy()

    def which_option(self):
        for widget in (self.pick_button, self.x_entry, self.y_entry):
            if self.position_status.get():
                widget.config(state='normal')
            else:
                widget.config(state='disabled')
    
    def limit(self, var_name, index, mode):        
        for entry in (self.x_entry, self.y_entry):
            if len(entry.get()) > 4:
                entry.delete(len(entry.get()) - 1, END)
                                               
class TimeCanvas(Canvas):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent, highlightthickness=0)
        self.parent = parent
        
        self.unpack_decor = DecorMixin(self)
        self.unpack_decor.create_wide_rectangle()
        ttk.Label(self.parent, text="Click interval").place(x=35, y=6)
        

        self.millisecsValue = IntVar(value=100)

        self.millisecs_label = ttk.Label(self,
                                         text='milliseconds',
                                         )
        self.millisecs_label.place(x=365, y=20)

        self.millisecs_entry = ttk.Entry(self,
                                         style="Custom.TEntry",
                                         width=5,
                                         textvariable=self.millisecsValue
                                         )
        self.millisecs_entry.place(x=320, y=15)
         

        self.secsValue = IntVar()
        
        self.secs_label = ttk.Label(self,
                                    text='seconds',
                                    )
        self.secs_label.place(x=265, y=20)

        self.secs_entry = ttk.Entry(self,
                                    style="Custom.TEntry",
                                    width=5,
                                    textvariable=self.secsValue
                                    )
        self.secs_entry.place(x=220, y=15)


        self.minsValue = IntVar()
        
        self.mins_label = ttk.Label(self,
                                    text='minutes',
                                    )
        self.mins_label.place(x=165, y=20)

        self.mins_entry = ttk.Entry(self,
                                    style="Custom.TEntry",
                                    width=5,
                                    textvariable=self.minsValue
                                    )
        self.mins_entry.place(x=120, y=15)


        self.hrsValue = IntVar()

        self.hrs_label = ttk.Label(self,
                                   text='hours',
                                   )
        self.hrs_label.place(x=72.5, y=20)

        self.hrs_entry = ttk.Entry(self,
                                   style="Custom.TEntry",
                                   width=5,
                                   textvariable=self.hrsValue
                                   )
        self.hrs_entry.place(x=27.5, y=15)

        for variable in (self.millisecsValue, self.secsValue, self.minsValue, self.hrsValue):
            variable.trace_add('write', self.limit_to_digits)

    def limit_to_digits(self, var_name, index, mode):
        try:
            for entry in (self.secs_entry, self.mins_entry):
                if int(entry.get()) >= 60:
                    entry.delete(len(entry.get()) - 1, END)           
            for entry in (self.millisecs_entry, self.hrs_entry):
                if len(entry.get()) > 3:
                    entry.delete(len(entry.get()) - 1, END)                  
        except ValueError:
            pass             

class RepeatCanvas(Canvas):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent, highlightthickness=0)
        self.parent = parent
        
        self.unpack_decor = DecorMixin(self)
        self.unpack_decor.create_small_rectangle()
        ttk.Label(self.parent, text="Click repeat").place(x=268, y=81)


        self.repetition = BooleanVar(value=True)

        self.repeat_until_stopped = ttk.Radiobutton(self,
                                                    text="Repeat until stopped",
                                                    variable=self.repetition,
                                                    value=False,
                                                    command=self.which_option
                                                    )
        self.repeat_until_stopped.place(x=10, y=72.5)

        self.repeat = ttk.Radiobutton(self,
                                      text="Repeat",
                                      variable=self.repetition,
                                      value=True,
                                      command=self.which_option
                                      )
        self.repeat.place(x=10, y=22.5)
        
        self.times = IntVar(value=1)

        self.times_label = ttk.Label(self,
                                     text='times'
                                     )
        self.times_label.place(x=152.5, y=22.5)

        self.times_to_click_entry = ttk.Entry(self,
                                              style="Custom.TEntry",
                                              textvariable=self.times,
                                              width=5
                                              )
        self.times_to_click_entry.place(x=85, y=18)

        self.up_button = ttk.Button(self,
                                    text="▲",
                                    style="CustomArrow.TButton",
                                    width=4,
                                    command=self.increment
                                    )
        self.up_button.place(x=127.5, y=19)

        self.down_button = ttk.Button(self,
                                      text="▼",
                                      style="CustomArrow.TButton",
                                      width=4,
                                      command=self.decrement
                                      )
        self.down_button.place(x=127.5, y=33)
    
    def which_option(self):
        for widget in (self.times_to_click_entry, self.up_button, self.down_button):
            if self.repetition.get():
                widget.config(state='normal')
            else:
                widget.config(state='disabled')

    def increment(self):
        if int(self.times_to_click_entry.get()) >= 0:
            self.times.set(int(self.times.get()) + 1)
        
    def decrement(self):      
        if int(self.times_to_click_entry.get()) > 0:
            self.times.set(int(self.times.get()) - 1)    

class ClickOptionsCanvas(Canvas):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent, highlightthickness=0)
        self.parent = parent
        
        self.unpack_decor = DecorMixin(self)
        self.unpack_decor.create_small_rectangle()
        ttk.Label(self.parent, text="Click options").place(x=35, y=81)

        
        self.mouse_button_options = ['Left', 'Right', 'Middle']

        self.selected_mouse_button_option = StringVar(value=self.mouse_button_options[0])

        self.choose_mouse_button_label = ttk.Label(self,
                                                   text='Mouse button :'
                                                   )
        self.choose_mouse_button_label.place(x=10, y=22.5) 

        self.choose_mouse_button_combobox = ttk.Combobox(self,
                                                         textvariable=self.selected_mouse_button_option,
                                                         values=self.mouse_button_options,
                                                         font=('Segoe UI', 11),
                                                         state='readonly',
                                                         width=8
                                                         )
        self.choose_mouse_button_combobox.place(x=110, y=20)
        

        self.click_type_options = ['Single', 'Double']

        self.selected_click_type_option = StringVar(value=self.click_type_options[0])

        self.choose_click_type_label = ttk.Label(self,
                                                 text='Click type :'
                                                 )
        self.choose_click_type_label.place(x=10, y=72.5)

        self.choose_click_type_combobox = ttk.Combobox(self,
                                                       textvariable=self.selected_click_type_option,
                                                       values=self.click_type_options,
                                                       font=('Segoe UI', 11),
                                                       state='readonly',
                                                       width=8
                                                       )
        self.choose_click_type_combobox.place(x=110, y=70)

class DecorMixin:
    def __init__(self, parent: ControlFrame | HotkeySettingFrame | PositionCanvas | TimeCanvas | RepeatCanvas | ClickOptionsCanvas):
        self.parent = parent

        self.setup_style()

    def setup_style(self):

        control_button_style = ttk.Style()
        
        control_button_style.configure("CustomMain.TButton",
                                       foreground='black',
                                       background='white',
                                       font=('Segoe UI', 15),
                                       )
         
        button_style = ttk.Style()
        
        button_style.configure("Custom.TButton",
                               foreground='black',
                               background='white',
                               font=('Segoe UI', 11),
                               )
        
        arrow_button_style = ttk.Style()

        arrow_button_style.configure("CustomArrow.TButton",
                                     foreground='black',
                                     background='white',
                                     padding=(0, 0, 0, 0),
                                     font=('Segoe UI', 3)
                                     )
        
        entry_style = ttk.Style()

        entry_style.configure("Custom.TEntry",
                              padding=(5, 5, 5, 5),
                              font=('Segoe UI', 5)
                              )
        
        label_style = ttk.Style()
        
        label_style.configure("Custom.TLabel",
                              font=('Segoe UI', 11)
                              )

    def create_wide_rectangle(self):

        self.parent.config(width=450, height=60)
    
        self.parent.create_rectangle(0, 0, 
                                     450, 60, 
                                     outline='#b5b5b5', 
                                     width=3.5
                                     )
        
    def create_small_rectangle(self):

        self.parent.config(width=216.5, height=110)

        self.parent.create_rectangle(0, 0, 
                                     216.5, 110, 
                                     outline='#b5b5b5', 
                                     width=3.5
                                     )
         
if __name__ == '__main__':
    root = AutoClickerApp()
    root.mainloop()