#import tkinter as tk
from tkinter import tix as tk
import JMScript_Api as jmsca 

root = tk.Tk()
app = jmsca.JMScriptUsrApi(master=root)
app.activForm()
app.mainloop()