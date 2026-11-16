import pyperclip
import time
import json
import tkinter as tk
import queue
from pynput import keyboard

lastValue = None
newValue = None
maxItems = 10
maxLength = 5000
clipboardList = []
show_popup_queue = queue.Queue()


def on_activate_v():
    if not clipboardList:
        print("lista ancora vuota")
        return
    show_popup_queue.put(True)

def show_popup():
    finestra = tk.Tk()
    finestra.geometry('400x600')
    finestra.title('finestra')
    listbox = tk.Listbox(finestra) #salvataggio del widget nella variabile e posizionamento
    
    for item in clipboardList:
        listbox.insert(tk.END, item)
    
    def on_select(event):
        index = listbox.curselection()
        pyperclip.copy(listbox.get(index[0]))
        finestra.destroy()
    listbox.pack() #mostro widget
    listbox.bind("<Double-Button-1>", on_select)
    
    finestra.mainloop()

def save_history():
    with open("clipboard_history.json", "w") as f:
        json.dump(clipboardList, f)

#definisco un listener
listener = keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+v' : on_activate_v
})
listener.start()

try:
    with open("clipboard_history.json", "r") as f:
        clipboardList = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    clipboardList = []

while True:
    try: 
        newValue = pyperclip.paste()
    except pyperclip.PyperclipException:
        continue
    if not show_popup_queue.empty():
        show_popup_queue.get()
        show_popup()
    if lastValue != newValue and newValue and len(newValue) <= maxLength:
        if newValue in clipboardList:
            clipboardList.remove(newValue)
        clipboardList.append(newValue)
        if len(clipboardList) > maxItems:
            del clipboardList[0]
        lastValue = newValue
        print(clipboardList)
        save_history()
    time.sleep(1)
