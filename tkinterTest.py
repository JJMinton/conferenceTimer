import tkinter as tk;
from tkinter import font as tkFont

def updateText(root, textList):

    frame = tk.Frame(root, width=100, height=100, bg="red").place(in_=root, anchor='c', relx=0.5, rely=0.5);#pack(side = tk.LEFT);#, width=200, height=200, background="red").pack();
    for item in textList:
        tk.Label(frame, text=item['text'], font=item['font']).pack();#place(_in=container);

if __name__ == "__main__":
    root = tk.Tk();
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("{:}x{:}".format(w,h));
    root.attributes("-fullscreen", True);
    root.focus_set() # <-- move focus to this widget #root.bind("<Escape>", lambda e: e.widget.quit());


    helv24 = tkFont.Font(family='Helvetica', size=36, weight='bold')
    helv36 = tkFont.Font(family='Helvetica', size=24, weight='bold')
    helv72 = tkFont.Font(family='Helvetica', size=72, weight='bold')


    updateText(root, ({'text': 'Next Speaker:', 'font': helv24},
                        {'text': 'Johnny Bravo', 'font': helv36},
                        {'text': 'Talk:', 'font': helv24},
                        {'text': 'How awesome are cartoons', 'font': helv36},
                        {'text': 'Starting in:', 'font': helv24},
                        {'text': '3:21', 'font': helv72},));



