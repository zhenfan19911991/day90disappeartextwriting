from tkinter import *
from tkmacosx import Button
import time
from tkinter import filedialog
from tkinter import scrolledtext


writing_start = False

def start_writing():
    global writing, stall_seconds, writing_start, check
    if check:
        window.after_cancel(check)
    writing = None
    stall_seconds = -1
    entry.config(state=NORMAL)
    entry.delete('1.0', END)
    writing_start = True
    check_writing()

def check_writing():
    global writing, stall_seconds, writing_start, check
    if writing_start:
        writing_new = entry.get("1.0", 'end-1c')
        if len(writing_new) == 0:
            writing_new = None
        if writing_new != writing:
            writing = writing_new
            stall_seconds = 0
        elif writing_new == writing:
            stall_seconds +=1
        if stall_seconds<6:
            stall_time_label.config(text=f'Idle Seconds: {stall_seconds}s', fg='#747264')
        elif stall_seconds >=6 and stall_seconds<=10:
            remain_time = 10-stall_seconds
            stall_time_label.config(text = f'Idle Seconds: {stall_seconds}s. Warning: Your writing will be deleted in {remain_time}s!', fg='#e2711d')
        elif stall_seconds >= 11:
            stall_time_label.config(text=f'Idle Seconds: {stall_seconds}s. Your writing was deleted.', fg='#C40C0C')
            entry.delete('1.0', END)
            # stall_seconds = 0
            writing = None
        check = window.after(1000, check_writing)

def resume_writing():
    global writing, stall_seconds, writing_start, check
    if check:
        window.after_cancel(check)
    entry.config(state=NORMAL)
    stall_seconds = -1
    writing_start = True
    check_writing()

def end_writing():
    global writing_start
    writing_start = False
    entry.config(state=DISABLED)

def save_as_text_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file_content = entry.get("1.0", 'end-1c')
                file.write(file_content)
                status_label.config(text=f"File saved as: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")

window = Tk()
window.geometry("1000x900")

bg_color = '#EEEDEB'

window.title('Dangerous Writing App')
window.configure(background= bg_color)
window.grid_columnconfigure((0, 1, 2), weight=1, uniform= 'a')

entry = scrolledtext.ScrolledText(window, wrap=WORD, width=70, height=25,font=("Stencil Std", 20), bg = 'white', fg = 'black')
entry.grid(column=0, row=2, columnspan = 3, pady=10)
entry.config(state=DISABLED)

check = None

start_b = Button(window, text="Start Writing", command=start_writing, width=200, font = ('Birch Std', 20), bg = '#B5C18E', activebackground='#4F6F52', highlightthickness=0, borderless=1)
start_b.grid(column=0, row=0, pady=(40,20))

end_b = Button(window, text="Pause Writing", command=end_writing, width=200, font = 'Ariel 20', bg = '#E1ACAC', activebackground='#704264', highlightthickness=0, borderless=1)
end_b.grid(column=1, row=0, pady=(40,20))

resume_b = Button(window, text="Resume Writing", command=resume_writing, width=200, font = 'Ariel 20', bg = '#FFEBB2',activebackground='#FFAF45', highlightthickness=0, borderless=1)
resume_b.grid(column=2, row=0, pady=(40,20))

stall_time_label = Label(window, text ="Please hit Start Writing to begin typing. Your writing will be deleted after 10 seconds' idle time!", font=("MS Sans Serif", 16),
                         fg = '#747264', bg = bg_color)
stall_time_label.grid(column=0, row=1, columnspan = 3, padx = 50, sticky = 'w', pady=(10,5) )

status_label = Label(window, text="", font=("MS Sans Serif", 16), bg = bg_color, fg = '#747264')
status_label.grid(column=0, row=4, columnspan = 3, pady=10)

save_button = Button(window, text="Save As", command=save_as_text_file, highlightthickness=0, borderless=1, width=150, font = 'Ariel 16', bg = '#9AC8CD')
save_button.grid(column=0, row=3, columnspan = 3, pady=10)

window.mainloop()




