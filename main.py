from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.messagebox import showerror

from numerical_methods import fft, sdm
import plots

import tkinter as tk
from tkinter import ttk

# freq = 5
#
# x1 = np.linspace(0.0, 1.0, 256)
# x2 = np.linspace(0.0, 128.0, 128)
# y1 = np.sin(2 * np.pi * freq * x1) + np.sin(2 * np.pi * 70 * x1) + 2 * np.sin(2 * np.pi * 10 * x1)
# y2 = abs(np.array(fft(y1)[:128]))
#
# plots.fft_plots(x1, y1, x2, y2)


LARGE_FONT = ("Verdana", 12)


class NumMet(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "FFT & SDM")
        tk.Tk.report_callback_exception = self.report_callback_exception

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.params = {}

        self.frames = {}

        for F in (StartPage, PlotController, SdmController):
            frame = F(self.container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont, params=None):
        if cont == SdmPlotController:
            frame = cont(self.container, self, params, )
            self.frames[SdmPlotController] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()

    def report_callback_exception(self, exc, val, tb):
        if type(val) is SyntaxError:
            msg = 'There is some problems with syntax. Check it!'
        elif type(val) is ValueError:
            msg = "Couldn't find minimum"
        else:
            msg = str(val)
        showerror("Error", message=msg)


class StartPage(tk.Frame):

    def __init__(self, parent, controller, ):
        tk.Frame.__init__(self, parent,  width=100, height=100, relief='raised')
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PlotController))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(SdmController))
        button2.pack()


class PlotController(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class SdmController(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=100, height=100, relief='raised')

        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_propagate(0)

        function = tk.StringVar(self, value='(-abs(x)+1)**2 + (-abs(y)+1)**2')
        step = tk.StringVar(self, value='0.01')
        gradient_dx = tk.StringVar(self, value='-2*x*(1-abs(x))/abs(x)')
        gradient_dy = tk.StringVar(self, value='-2*y*(1-abs(y))/abs(y)')
        accuracy1 = tk.StringVar(self, value='0.001')
        accuracy2 = tk.StringVar(self, value='0.001')
        accuracy3 = tk.StringVar(self, value='0.001')
        start_x = tk.StringVar(self, value='1')
        start_y = tk.StringVar(self, value='2')

        params = {'fun': function, 'step': step, 'ac1': accuracy1, 'ac2': accuracy2, 'ac3': accuracy3,
                  'start_x': start_x, 'start_y': start_y, 'grad1': gradient_dx, 'grad2': gradient_dy }

        tk.Label(self, text="Method of steepest descent", font=LARGE_FONT).grid(
            row=0, column=2, columnspan=2, sticky='nwse')
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage)).grid(
            row=0, column=1, columnspan=1, sticky='nwse')

        tk.Label(self, text="f(x,y) = ").grid(row=1, column=1, sticky='nwse')
        tk.Entry(self, width=60, textvariable=function).grid(row=1, column=2, columnspan=3, sticky='nws')

        tk.Label(self, text="Gradient:  df/dx = ").grid(row=2, column=1, sticky='nwse')
        tk.Entry(self, width=20, textvariable=gradient_dx).grid(row=2, column=2, sticky='nws')
        tk.Label(self, text="df/dy = ").grid(row=2, column=3)
        tk.Entry(self, width=20, textvariable=gradient_dy).grid(row=2, column=4, sticky='nws')

        tk.Label(self, text="Step: ").grid(row=3, column=1, sticky='nwse')
        tk.Entry(self, width=20, textvariable=step).grid(row=3, column=2, sticky='nwse')

        tk.Label(self, text="Step: ").grid(row=4, column=1, sticky='nwse')
        tk.Entry(self, width=20, textvariable=accuracy1).grid(row=4, column=2, sticky='nws')
        tk.Entry(self, width=20, textvariable=accuracy2).grid(row=4, column=3, sticky='nws')
        tk.Entry(self, width=20, textvariable=accuracy3).grid(row=4, column=4, sticky='nws')

        tk.Label(self, text="Start:  x : ").grid(row=5, column=1, sticky='nwse')
        tk.Entry(self, width=20, textvariable=start_x).grid(row=5, column=2, sticky='nws')
        tk.Label(self, text="Start:  y : ").grid(row=5, column=3)
        tk.Entry(self, width=20, textvariable=start_y).grid(row=5, column=4, sticky='nws')

        button = ttk.Button(self, text="Find Minimum", command=lambda: controller.show_frame(SdmPlotController, params))
        button.grid(row=6, column=3, columnspan=1)


class SdmPlotController(tk.Frame):

    def __init__(self, parent, controller, params):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack()

        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(SdmController))
        button1.pack()

        function = params['fun'].get()
        gradient = (params['grad1'].get(), params['grad2'].get())
        start = (float(params['start_x'].get()), float(params['start_y'].get()))
        step = float(params['step'].get())
        accuracy = (float(params['ac1'].get()), float(params['ac2'].get()), float(params['ac3'].get()))

        minimum = sdm(function, gradient, start, step, accuracy=accuracy)

        scope = (abs(int(start[0])) + 1, abs(int(start[1])) + 1,
                 abs(int(minimum['point'][0])) + 2, abs(int(minimum['point'][1])) + 2)
        scope = -max(scope), max(scope)

        figure = plots.sdm_plot(function, minimum, scope=scope)
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


app = NumMet()
app.mainloop()
