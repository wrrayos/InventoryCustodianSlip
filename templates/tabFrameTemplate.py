import tkinter as tk

class TabFrameTemplate(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        super().__init__(self.parent)

        self["width"] = 1000
        self["height"] = 500
        self["bg"] = "green"

        self.canvas = tk.Canvas(self,bg="#F3BFB3",width=800,height=500)

        self.view_port = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0,ipadx=10,ipady=10)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas_window = self.canvas.create_window((0, 0),
                                                       window=self.view_port,
                                                       anchor='nw',
                                                       tags="self.view_port")

        self.view_port.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.parent.bind("<MouseWheel>", self._on_mousewheel)
        self.onFrameConfigure(None)
        self.view_port.grid_columnconfigure(0, weight=1)

    def _on_mousewheel(self,event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)