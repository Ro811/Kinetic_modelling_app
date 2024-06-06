# Import necessary libraries

import ttkbootstrap as tk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap import *
from ttkbootstrap import ttk
from tkinter import filedialog
from pathlib import Path
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate as ip
import matplotlib
from scipy.integrate import odeint 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from scipy.optimize import least_squares
from tkinter.filedialog import asksaveasfilename
import math as m
import pickle

# Make use of object oriented programming (OOP)
class MyGui:
    matplotlib.use('TkAgg')
    def __init__(self):
        self.Rg=8.3145 # Gas constant
        self.root=tk.Tk() # Main window

        # Set window dimensions
        width = self.root.winfo_screenwidth() 
        height = self.root.winfo_screenheight()
        self.root.state('zoomed')

        # Customization
        self.root.title('Kinetic modelling app')
        self.menubar=tk.Menu(self.root)
        self.tabControl = ttk.Notebook(self.root,width=2000,height=2000)
        s = ttk.Style()
        s.configure('TButton', font=('Arial',16))
        s.theme_use('clam')
        
        # Making the tabs
        self.data_plots=ttk.Frame(self.tabControl,bootstyle="light")
        self.kinetic_modelling=ttk.Frame(self.tabControl)
        self.Master_plots=ttk.Frame(self.tabControl)
        self.Tga_reconstruct=ttk.Frame(self.tabControl)
        self.Tga_predict=ttk.Frame(self.tabControl)
        self.Optimize=ttk.Frame(self.tabControl)

        # Adding the tabs
        self.tabControl.add(self.data_plots,text='Plots')
        self.tabControl.add(self.kinetic_modelling,text='KAS Modelling')
        self.tabControl.add(self.Master_plots,text='Master-plots')
        self.tabControl.add(self.Tga_reconstruct,text='Reconstruct TGA')
        self.tabControl.add(self.Optimize,text='Optimize model')
        self.tabControl.add(self.Tga_predict,text='Predict TGA')
        

        # Adding the tab bar
        self.tabControl.pack()

        # Adding figures for the tabs
        self.fig,self.ax=plt.subplots(1,2)
        self.fig.set_size_inches(16,6)

        self.fig2,self.ax2=plt.subplots()
        self.fig2.set_size_inches(10,8)

        self.fig3,self.ax3=plt.subplots(2,2)
        self.fig3.set_size_inches(16,8)

        self.fig4,self.ax4=plt.subplots(1,2)
        self.fig4.set_size_inches(16,8)

        self.fig5,self.ax5=plt.subplots()
        self.fig5.set_size_inches(16,8)

        self.fig6,self.ax6=plt.subplots(1,2)
        self.fig6.set_size_inches(16,8)

        # Addings frames for figures
        self.frame=ttk.Frame(self.data_plots)
        self.frame2=ttk.Frame(self.kinetic_modelling)
        self.frame3=ttk.Frame(self.Master_plots)
        self.frame4=ttk.Frame(self.Tga_reconstruct)
        self.frame5=ttk.Frame(self.Tga_predict)
        self.frame6=ttk.Frame(self.Optimize)

        ttk.Style().configure("TButton", font=('Arial', 16))

        # Adding the canvas for Tkinter to display figures of Matplotlib
        self.canvas=FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack()
        self.canvas2=FigureCanvasTkAgg(self.fig2, master=self.frame2)
        self.canvas2.get_tk_widget().pack()
        self.canvas3=FigureCanvasTkAgg(self.fig3,master=self.frame3)
        self.canvas3.get_tk_widget().pack()
        self.canvas4=FigureCanvasTkAgg(self.fig4,master=self.frame4)
        self.canvas4.get_tk_widget().pack()
        self.canvas5=FigureCanvasTkAgg(self.fig5,master=self.frame5)
        self.canvas5.get_tk_widget().pack()
        self.canvas6=FigureCanvasTkAgg(self.fig6,master=self.frame6)
        self.canvas6.get_tk_widget().pack()

        # File menu addition
        self.filemenu=tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=self.on_closing)
        self.filemenu.add_separator()
        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.root.config(menu=self.menubar)

        # Main prompt for 1st tab
        self.label=ttk.Label(self.data_plots,text='Enter the number of heating rates')
        self.label.place(x=10,y=10)

        # Button to perform KAS analysis
        self.analysis=ttk.Button(self.kinetic_modelling, text='Analyze',command=self.KAS)
        self.analysis.pack()

        # Adding shortcut (enter for plotting)
        self.entry=Entry(self.data_plots, font=('Arial', 18))
        self.entry.bind("<KeyPress>", self.shortcut )
        self.entry.focus_set()
        self.entry.place(in_=self.data_plots,x=400,y=10)

        # Adding frames
        self.Userframe=ttk.Frame(self.data_plots)
        self.Userframe.columnconfigure(0,weight=1)
        self.Userframe.columnconfigure(1,weight=1)
        self.Userframe.columnconfigure(2,weight=1)
        self.Userframe.columnconfigure(3,weight=1)

        self.Sheet=ttk.Frame(self.kinetic_modelling)
        self.Sheet.columnconfigure(0,weight=1)
        self.Sheet.columnconfigure(1,weight=1)
        self.Sheet.columnconfigure(2,weight=1)
        self.Sheet.columnconfigure(3,weight=1)

        self.sheet2=ttk.Frame(self.kinetic_modelling)
        self.sheet2.columnconfigure(0,weight=1)
        self.sheet2.columnconfigure(1,weight=1)
        self.sheet2.columnconfigure(2,weight=1)
        self.sheet2.columnconfigure(3,weight=1)

        # Adding closing functionality
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

        # Adding buttons
        self.browse=ttk.Button(self.data_plots,text='Browse file',command=self.click)
        self.go=ttk.Button(self.data_plots,text="Go", command=self.makefileentries)
        self.go.place(x=700,y=5)
        self.savebutton=ttk.Button(self.data_plots,text='save plot',command=lambda: self.save(self.fig))
        self.savebutton.place(x=700,y=100)
        self.plot=ttk.Button(self.data_plots,text='Plot', command=lambda: self.makeplots(self.ax,self.canvas,True))
        self.plot.place(x=700,y=50)

        # Adding masterplot frame
        self.fr3=ttk.Frame(self.Master_plots)
        self.fr3.columnconfigure(0,weight=1)
        self.fr3.columnconfigure(1,weight=1)
        self.fr3.columnconfigure(2,weight=1)

        # Addings buttons, entries, labels, frames
        self.input=Entry(self.fr3,font=('Arial',16))
        self.labinput=ttk.Label(self.fr3,text='Enter Heating Rate')
        self.btn2=ttk.Button(self.fr3,text='Go', command=self.masterplots)
        self.btn3=ttk.Button(self.Master_plots,text='Display RRMSEs',command=self.printerrors)
        self.btn2.grid(row=0,column=2)
        self.input.grid(row=0,column=1)
        self.labinput.grid(row=0,column=0)
        self.fr3.pack()
        self.btn3.place(x=1500,y=20)
        self.clicked=StringVar()
        self.clicked2=StringVar()
        self.clicked2.set(value='Select Model')
        self.clicked.set(value='Select Model')
        self.opfr=ttk.Frame(self.Tga_reconstruct)
        self.opfr.columnconfigure(0,weight=1)
        self.opfr.columnconfigure(1,weight=1)
        self.opfr.pack()
        self.btn4=ttk.Button(self.opfr,text='Plot', command=self.reconstruct)
        self.labelerror=ttk.Label(self.Tga_reconstruct,text='NAN')
        self.labelerror2=ttk.Label(self.Tga_reconstruct, text='NAN')
        
        # Creating drop down menu
        self.options=['Select Model','D1','D2-VB','D2-J','D2-AJ','D3','D-IT','D-TD','D2','D3-J','D3-GB','D3-ZL','A4','A3','A2','A1.5','R0','R1', 'R2','R3','R-CS', 'R-CC', 'P2','P3','P4','E1']
        self.options2=['Select Model','Optimized','D1','D2-VB','D2-J','D2-AJ','D3','D-IT','D-TD','D2','D3-J','D3-GB','D3-ZL','A4','A3','A2','A1.5','R0','R1', 'R2','R3','R-CS', 'R-CC', 'P2','P3','P4','E1']
        self.opfr2=ttk.Frame(self.Tga_predict)
        self.opfr2.columnconfigure(0,weight=1)
        self.opfr2.columnconfigure(1,weight=1)
        self.opfr2.columnconfigure(2,weight=1)
        self.opfr2.columnconfigure(3,weight=1)

        # More Buttons
        self.btn42=ttk.Button(self.opfr2,text='Plot', command=self.predict)
        self.drop=ttk.OptionMenu(self.opfr,self.clicked,*self.options)

        self.drop.grid(row=0,column=0)
        self.btn4.grid(row=0,column=1)

        self.drop2=ttk.OptionMenu(self.opfr2,self.clicked2,*self.options2)
        self.drop2lab=ttk.Label(self.opfr2,text='Heating rate :')
        self.drop2enter=ttk.Entry(self.opfr2)

        self.drop2lab.grid(row=0,column=0)
        self.drop2enter.grid(row=0,column=1)
        self.drop2.grid(row=0,column=2)
        self.btn42.grid(row=0,column=3)

        # Drop down menu for optimization
        self.opfr2.pack()
        self.options2=['Select Model', 'Avrami', 'Chemical Reaction', 'Power law', 'SB model']
        self.opfr3=ttk.Frame(self.Optimize)
        self.opfr3.columnconfigure(0,weight=1)
        self.opfr3.columnconfigure(1,weight=1)
        self.opfr3.columnconfigure(2,weight=1)
        self.opfr3.columnconfigure(3,weight=1)
        self.opfr3.columnconfigure(4,weight=1)
        self.opfr3.columnconfigure(5,weight=1)
        self.opfr3.columnconfigure(6,weight=1)
        self.opfr3.columnconfigure(7,weight=1)
        self.opfr3.columnconfigure(8,weight=1)
        self.opfr3.columnconfigure(9,weight=1)

        # Optimization buttons, option menu, entries, labels
        self.clicked3=StringVar()
        self.clicked3.set(value='Select Model')
        self.btn43=ttk.Button(self.opfr3,text='Optimize and plot', command=self.optimize)
        self.drop3=ttk.OptionMenu(self.opfr3,self.clicked3,*self.options2)
        self.drop3lab=ttk.Label(self.opfr3,text='Heating rate :')
        self.drop3labn=ttk.Label(self.opfr3,text='Initial guess (n) :')
        self.drop3labk=ttk.Label(self.opfr3,text='Initial guess (k) :')
        self.drop3enter=ttk.Entry(self.opfr3)
        self.drop3enter2=ttk.Entry(self.opfr3)
        self.drop3enter3=ttk.Entry(self.opfr3)
        self.drop3enter4=ttk.Entry(self.opfr3)
        self.drop3labn.grid(row=0,column=0)
        self.drop3enter2.grid(row=0,column=1)
        self.drop3labk.grid(row=0,column=2)
        self.drop3enter3.grid(row=0,column=3)
        self.drop3lab.grid(row=0,column=4)
        self.drop3enter.grid(row=0,column=5)
        self.drop3.grid(row=0,column=6)
        self.btn43.grid(row=0,column=7)
        self.opfr3.pack()
        self.order2=ttk.Label(self.Optimize,text='NAN')
        self.order=ttk.Label(self.Optimize,text='NAN')

        # Style customization
        ttk.Style().configure("TNotebook",background='#aeecf4')
        ttk.Style().configure('My.TFrame', background='#aeecf4')
        ttk.Style().configure('TButton',background='#ff6e00')
        ttk.Style().configure("TFrame",background='#aeecf4')
        ttk.Style().configure("TLabel", background='#aeecf4', font=('Arial',18))
        self.data_plots.configure(style='My.TFrame')

        # Updating the toolbar of matplotlib
        toolbar3=NavigationToolbar2Tk(self.canvas2,self.frame2)
        toolbar3.update()

        toolbar=NavigationToolbar2Tk(self.canvas,self.frame)
        toolbar.update()

        toolbar4=NavigationToolbar2Tk(self.canvas3,self.frame3)
        toolbar4.update()

        toolbar2=NavigationToolbar2Tk(self.canvas4,self.frame4)
        toolbar2.update()

        toolbar5=NavigationToolbar2Tk(self.canvas5,self.frame5)
        toolbar5.update()

        # More configuration
        ttk.Style().configure("TMenubutton",background='#ff6e00',font=('Arial',18))
        ttk.Style().configure("TSeparator",background='#000000')

        # The infinite loop aka window
        self.root.mainloop()


        # function for processing TGA data
    def processing(self,TGA_file,Beta,showplots=False): 

        # Read data
        data=pd.read_csv(TGA_file,encoding='latin-1', skipinitialspace=True, sep="\t")
        # Convert decimal separator to . if decimal separator is ,
        if (data.Time.dtype !='float64'):
            data['Time'] = data['Time'].str.replace(',', '.')
            data['Temperature'] = data['Temperature'].str.replace(',', '.')
            data['Weight'] = data['Weight'].str.replace(',', '.')
            data['Weight.1'] = data['Weight.1'].str.replace(',', '.')
            data['Deriv. Weight']=data['Deriv. Weight'].str.replace(',','.')

        # make arrays and remove NaN values (e.g. empty rows)

        t=np.array([float(i) for i in data['Time'].tolist()]) 
        t=t[~np.isnan(t)]
        mass=np.array([float(i) for i in data['Weight'].tolist()])
        mass=mass[~np.isnan(mass)]
        T=np.array([float(i) for i in data['Temperature'].tolist()])
        T=T[~np.isnan(T)]
        mass_centage=np.array([float(i) for i in data['Weight.1'].tolist()])
        mass_centage=mass_centage[~np.isnan(mass_centage)]
        mass_deriv=np.array([float(i) for i in data['Deriv. Weight'].tolist()])
        mass_deriv=mass_deriv[~np.isnan(mass_deriv)]

        # Find smallest rows, make all columns have the same number of rows to allow calculations (Process)

        mini=min(len(T),len(mass_centage),len(mass_deriv))
        mass_centage=mass_centage[100:mini]
        T=T[100:mini]
        t=t[100:mini]
        mass_deriv=mass_deriv[100:mini]
        
        # Normalization

        mass_centage=mass_centage*100/mass_centage[0]

        # Filtering DTG data using median filter of 499 sample size which is roughly equal to 0.165 mins

        mass_deriv=sp.signal.medfilt(mass_deriv, kernel_size=99)
        
        # Calculation of conversion and derivative of conversion

        alpha=(mass_centage[0]-mass_centage)/(mass_centage[0]-mass_centage[-1]) # Conversion alpha = (m0 - m)/(m0-mf)
        dalpha=-mass_deriv/(mass_centage[0]-mass_centage[-1]) # Derivative of conversion dalpha/dT = -(dm/dT)/(m0-mf)
        # Plotting
        if showplots==True:
            plt.subplot(3,1,1)
            plt.plot(T,mass_centage)
            plt.xlabel(r'Temperature ($^{\circ}$ C)')
            plt.ylabel('Mass %')
            plt.title('TGA curve')
            plt.grid()
            plt.subplot(3,1,2)
            plt.plot(T,mass_deriv)
            plt.xlabel(r'Temperature ($^{\circ}$ C)')
            plt.ylabel(r'Deriv Mass %/$^{\circ}$ C')
            plt.title('DTG curve')
            plt.grid()
            plt.tight_layout()
            plt.subplot(3,1,3)
            plt.plot(T,alpha)
            plt.xlabel(r'Temperature ($^{\circ}$ C)')
            plt.ylabel('Alpha')
            plt.title('Conversion vs Temperature')
            plt.grid()
            plt.show()

        # Temperature correction for linear ramping
        Temp=[T[0]+((t[i]-t[0])*Beta) for i in range(len(t))]
        Temp=np.array(Temp)

        # Return everything
        return t,alpha,dalpha,T,mass_centage,mass_deriv,Temp
    
    # d(alpha)/dt of theoretical solid state reaction models

    def funcD1(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(1/(2*y[0])), Beta] 
    def funcD2VB(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(-1/np.log(1-y[0])), Beta]
    def funcD2J(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(((1-y[0])**(1/2))/(1-(1-y[0])**(1/2))), Beta]
    def funcD2AJ(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(((1+y[0])**(1/2))/(-1+(1+y[0])**(1/2))), Beta]
    def funcD3(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*((2*(1-y[0])**(2/3))/(1-(1-y[0])**(1/3))), Beta]
    def funcDIT(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3*(1-y[0])**(4/3)), Beta]
    def funcDTD(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3/((1-y[0])**(-4/3) - (1-y[0])**(-1))), Beta]
    def funcD2(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3/((1-y[0])**(-8/3) - (1-y[0])**(-7/3))), Beta]
    def funcD3J(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*((3*(1-y[0])**(2/3))/(2*(1-(1-y[0])**(1/3)))), Beta]
    def funcD3GB(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3/(2*((1-y[0])**(-1/3) - 1))), Beta]
    def funcD3ZL(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*((3/2)*(1-y[0])**(4/3)*((1-y[0])**(-1/3)-1)**(-1)), Beta]
    def funcA4(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(4*(1-y[0])*(-np.log(1-y[0]))**(3/4)), Beta]
    def funcA3(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3*(1-y[0])*(-np.log(1-y[0]))**(2/3)), Beta]
    def funcA2(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(2*(1-y[0])*(-np.log(1-y[0]))**(1/2)), Beta]
    def funcA1_5(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(1.5*(1-y[0])*(-np.log(1-y[0]))**(0.5/1.5)), Beta]
    def funcR0(self,y,t,Ea,R,A,Beta):
        if (y[0]>=0.99):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1])), Beta]
    def funcR1(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(1-y[0]), Beta]
    def funcR2(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(1-y[0])**2, Beta]
    def funcR3(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(1-y[0])**3, Beta]
    def funcRCC(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*2*((1-y[0])**(1/2)), Beta]
    def funcRCS(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3*(1-y[0])**(2/3)), Beta]
    def funcP2(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(2*y[0]**(1/2)), Beta]
    def funcP3(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(3*y[0]**(2/3)), Beta]
    def funcP4(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*(4*y[0]**(3/4)), Beta]
    def funcE1(self,y,t,Ea,R,A,Beta):
        if (y[0]>=1):
            return [0,Beta]
        return [A*np.exp(-Ea/(R*y[1]))*y[0], Beta]

    # Shortcut function

    def shortcut(self,event):  
        if event.keysym=="Return":
            self.makefileentries()

    # Window closing message

    def on_closing(self):
        if Messagebox.yesnocancel(title="Quit?", message="Do you really want to quit?")=='Yes':
            self.root.destroy()
    
    # Adding browse file capabilities
    def click(self):
        filename=filedialog.askopenfilename(parent=self.data_plots, title='Browse file')
    def clickenteries(self,index):
        filename=filedialog.askopenfilename(parent=self.data_plots, title='Browse file')
        self.entries[index].delete(0,tk.END)
        self.entries[index].insert(0,filename)

    # browse files
    def makefileentries(self):
        self.Userframe.destroy()
        n=int(self.entry.get())
        self.Userframe=ttk.Frame(self.data_plots)
        self.Userframe.columnconfigure(0,weight=1)
        self.Userframe.columnconfigure(1,weight=1)
        self.Userframe.columnconfigure(2,weight=1)
        self.Userframe.columnconfigure(3,weight=1)
        self.entries=[]
        self.texts=[]
        self.betas=[]
        self.browses=[]
        self.upper=ttk.Label(self.Userframe,text='Heating rates')
        self.upperr=ttk.Label(self.Userframe,text='file directory')
        for i in range(1,n+1):
            self.entries.append(ttk.Entry(self.Userframe))
            self.betas.append(ttk.Entry(self.Userframe))
            self.texts.append(ttk.Label(self.Userframe,text=f'Heating rate {i}:'))
            self.texts[i-1].grid(row=i,column=0)
            self.browses.append(ttk.Button(self.Userframe,text='Browse file',command=lambda i=i: self.clickenteries(i-1)))
            self.browses[i-1].grid(row=i,column=3)
            self.betas[i-1].grid(row=i,column=1) 
            self.entries[i-1].grid(row=i,column=2)
        self.upper.grid(row=0,column=1)
        self.upperr.grid(row=0,column=2)
        self.Userframe.place(x=1000,y=10)
    
    # Makes plots in the first tab, must be run to perform analysis
    def makeplots(self,ax,canvas,showplot):
        ax[0].clear()
        ax[1].clear()
        self.frame.place_forget()
        n=int(self.entry.get())
        filenames=[]
        self.Betas=[]
        for i in range(n):
            filenames.append(self.entries[i].get())
            self.Betas.append(self.betas[i].get())
        
        self.T=[]
        self.t=[]
        self.T_actual=[]
        self.dmdt=[]
        self.alpha=[]
        self.dalpha=[]
        self.mass=[]
        self.Betas=[int(i) for i in self.Betas]
        for i in range(n):
            t_l,alpha_l,dalpha_l,T_l,mass_l,dmdt_l,T_actual_l=self.processing(filenames[i],self.Betas[i],False)
            print(mass_l[-1])
            self.t.append(t_l)
            self.alpha.append(alpha_l)
            self.T.append(T_l)
            self.dmdt.append(dmdt_l)
            self.T_actual.append(T_actual_l)
            self.dalpha.append(dalpha_l)
            self.mass.append(mass_l)
            if showplot==True:
                ax[0].plot(T_actual_l,mass_l, label=f'HR-{self.Betas[i]}')
                ax[0].set_xlabel(r'Temperature ($^{\circ}$ C)', fontsize=20)
                ax[0].set_ylabel('Mass %', fontsize=20)
                ax[0].tick_params(axis='both', which='major', labelsize=15)
                ax[0].set_title('TGA curve at different heating rates', fontsize=20)
                ax[0].grid(visible=True)
                ax[1].plot(T_actual_l,abs(dmdt_l)*self.Betas[i], label=f'HR-{self.Betas[i]}')
                ax[1].set_xlabel(r'Temperature ($^{\circ}$ C)', fontsize=20)
                ax[1].set_ylabel(r'Deriv mass $\left(\frac{\%}{\text{min}}\right)$', fontsize=20)
                ax[1].tick_params(axis='both', which='major', labelsize=15)
                ax[1].set_title('DTG curve at different heating rates', fontsize=20)
                ax[1].grid(visible=True)
        if showplot==True:
            self.fig.tight_layout()
            ax[0].legend()
            ax[1].legend()
            self.frame.place(x=240,y=250)
            canvas.draw()

    # Peforms KAS analysis
    def KAS(self):
        self.Sheet.destroy()
        self.sheet2.destroy()
        self.ax2.clear()

        conversions=np.linspace(0.2,0.7,11) # Fitting range
        self.T_alphas=np.zeros((len(conversions),len(self.Betas))) # KAS temperatures which correspond to fitting range conversions
        for i in range(0,len(conversions)):
            for j in range(0,len(self.Betas)):
                self.T_alphas[i,j]=self.T_actual[j][np.isclose(self.alpha[j],conversions[i],atol=0.001)][0] + 273.15
       
        self.Eas=[]
        self.R2s=[]

        for i in range(0,len(conversions)): 
            r=sp.stats.linregress(1/self.T_alphas[i], np.log(self.Betas/(self.T_alphas[i]**2))) # Linear regression
            R2=r.rvalue**2 # R square value calculation
            Ea=r.slope*-self.Rg # Activation energy calculation
            self.Eas.append(Ea)
            self.R2s.append(R2)
        self.Eamean=np.mean(self.Eas)
        self.As=[]
        self.Tps=[]

        # Arrhenius prefactor calculation
        for i in range(len(self.Betas)):
            self.Tps.append(np.mean(self.T_actual[i][abs(self.dmdt[i])==max(abs(self.dmdt[i]))])+273.15)
            self.As.append(self.Betas[i]*self.Eamean*np.exp(self.Eamean/(self.Rg*self.Tps[i]))/(self.Rg*(self.Tps[i]**2))) # calculation of arrhenius pre-factor

        # Putting results in software UI
        self.Sheet=Frame(self.kinetic_modelling)
        self.Sheet.columnconfigure(0,weight=1)
        self.Sheet.columnconfigure(1,weight=1)
        self.Sheet.columnconfigure(2,weight=1)
        self.Sheet.columnconfigure(3,weight=1)

        self.sheet2=Frame(self.kinetic_modelling)
        self.sheet2.columnconfigure(0,weight=1)
        self.sheet2.columnconfigure(1,weight=1)
        self.sheet2.columnconfigure(2,weight=1)
        self.sheet2.columnconfigure(3,weight=1)

        self.Eas=np.array(self.Eas)
        self.R2s=np.array(self.R2s)
        self.EaSE=np.std(self.Eas/1000)/np.sqrt(len(self.Eas))
        self.R2SE=np.std(self.R2s)/np.sqrt(len(self.R2s))

        for i in range(len(conversions)):
            self.e=ttk.Label(self.Sheet,text=f'{self.Eas[i]/1000 :.2f}')
            self.a=ttk.Label(self.Sheet,text=f'{conversions[i] : .2f}')
            self.r=ttk.Label(self.Sheet,text=f'{self.R2s[i] : .3f}')
            self.a.grid(row=i+1,column=1)
            self.e.grid(row=i+1,column=2)
            self.r.grid(row=i+1,column=3)
        self.Ea=ttk.Label(self.Sheet, text=f'{self.Eamean/1000 : .2f}')
        self.Ea.grid(row=len(conversions)+3,column=2)

        self.Rsq=ttk.Label(self.Sheet, text=f'{np.mean(self.R2s) : .3f}')
        self.Rsq.grid(row=len(conversions)+3,column=3)
        separator2 = ttk.Separator(self.Sheet, orient='horizontal')
        separator2.grid(row=len(conversions)+2,columnspan=4,sticky='ew')
        separator2.config(style='primary.Horizontal.TSeparator')

        self.alp=ttk.Label(self.Sheet,text='\u03B1')
        self.Eatit=ttk.Label(self.Sheet,text='Ea (kJ/mol)')
        self.R2tit=ttk.Label(self.Sheet,text='R\u00b2')

        self.EsSEl=ttk.Label(self.Sheet,text=f'\u00b1{self.EaSE: .3f}')
        self.R2SEl=ttk.Label(self.Sheet,text=f'\u00b1{self.R2SE: .3f}')
        self.Esl=ttk.Label(self.Sheet,text='SE')
        self.Esl.grid(row=len(conversions)+4, column=0)

        self.EsSEl.grid(row=len(conversions)+4,column=2)
        self.R2SEl.grid(row=len(conversions)+4,column=3)

        self.alp.grid(row=0,column=1)
        self.Eatit.grid(row=0,column=2)
        self.R2tit.grid(row=0,column=3)

        self.mean=ttk.Label(self.Sheet, text='mean')
        self.mean.grid(row=len(conversions)+3,column=0)
        self.title=ttk.Label(self.kinetic_modelling,text='Activation energy results')
        self.title.place(x=40,y=20)
        self.Sheet.place(x=10,y=75)

        self.Btit=ttk.Label(self.sheet2,text='\u03B2 (C/min)')
        self.Atit=ttk.Label(self.sheet2,text='A (1/min)')
        self.SEtit=ttk.Label(self.sheet2,text='SE (1/min)')
        self.title2=ttk.Label(self.kinetic_modelling,text='Arrhenius pre-factor results')
        self.Btit.grid(row=0,column=1)
        self.Atit.grid(row=0,column=2)
        self.SEtit.grid(row=0,column=3)
        self.sero=[]
        for i in range(len(self.Betas)):
            self.b=ttk.Label(self.sheet2,text=f'{self.Betas[i]}')
            self.a=ttk.Label(self.sheet2,text=f'{self.As[i]: .2E}')
            self.sero.append(((self.As[i]/(self.Rg*self.Tps[i]))+(self.As[i]/self.Eamean))*self.EaSE*1000)
            self.see=ttk.Label(self.sheet2,text=f'\u00b1{self.sero[i]: .1E}')
            self.b.grid(row=i+1,column=1)
            self.a.grid(row=i+1,column=2)
            self.see.grid(row=i+1,column=3)
        self.Asmean=np.mean(self.As)
        self.SEmean=np.mean(self.sero)
        self.amean=ttk.Label(self.sheet2,text=f'{self.Asmean :.2E}')
        self.sem=ttk.Label(self.sheet2,text=f'\u00b1{self.SEmean : .1E}')
        separator = ttk.Separator(self.sheet2, orient='horizontal')
        separator.grid(row=i+2,columnspan=4,sticky='ew')
        separator.config(style='primary.Horizontal.TSeparator')
        self.amean.grid(row=i+3,column=2)
        self.sem.grid(row=i+3,column=3)
        ttk.Label(self.sheet2,text='mean').grid(row=i+3, column=0)
        self.title2.place(x=20,y=650)
        self.sheet2.place(x=5,y=700)

        # Plotting activation energy dependency on conversion
        
        self.ax2.plot(conversions,self.Eas/1000, marker='o')
        self.ax2.set_xlabel(r'$Conversion (\alpha)$', fontsize=16)
        self.ax2.set_ylabel(r'$E_{a} (\frac{\text{kJ}}{\text{mol}}$)', fontsize=16)
        self.ax2.set_title('Plot of activation energy vs conversions (KAS method)', fontsize=20)
        self.ax2.tick_params(axis='both', which='major', labelsize=15)
        self.ax2.grid(visible=True)
        self.fig2.tight_layout()
        self.frame2.place(x=450,y=50)
        self.canvas2.draw()

        # save button (not needed as matplotlib offers saving)
    def save(self, fig):
        filename = asksaveasfilename(initialfile = 'Untitled.png',defaultextension=".png",filetypes=[("All Files","*.*"),("Portable Graphics Format","*.png")])
        fig.savefig(filename)
    
    # select model to optimize
    def avrami(self,y,t,n,beta):
            if y[0]>=1:
                return [0,beta]
            return [self.Asmean*np.exp(-self.Eamean/(self.Rg*y[1]))*(n*(1-y[0])*((-np.log(1-y[0])))**((n-1)/n)),beta]

    def PE(self,y,t,n,beta):
            if y[0]>=1:
                return [0,beta]
            return [self.Asmean*np.exp(-self.Eamean/(self.Rg*y[1]))*(n*(y[0]**((n-1)/n))),beta]
    def react(self,y,t,n,beta):
            if y[0]>=1:
                return [0,beta]
            return [self.Asmean*np.exp(-self.Eamean/(self.Rg*y[1]))*(1-y[0])**(n),beta]
    def SB(self,y,t,n,k,beta):
            if y[0]>=1:
                return [0,beta]
            return [self.Asmean*np.exp(-self.Eamean/(self.Rg*y[1]))*(y[0]**k)*(1-y[0])**n, beta] 
    # Masterplots
    def masterplots(self):
        self.ax3[0,0].clear()
        self.ax3[0,1].clear()
        self.ax3[1,0].clear()
        self.ax3[1,1].clear()
        self.Beta=int(self.input.get())
        Index=self.Betas.index(self.Beta) # Heating rate user wants to use
        self.dalpha_ind=self.dalpha[Index] 

        def theo(a, dan, Temp, Eas, R):
            self.alpharange=a[(a>=0.2) & (a<=0.7)]       # Range of master plots (0.2 to 0.7)
            self.dalpharange=dan[(a>=0.2) & (a<=0.7)]
            self.T=Temp[(a>=0.2) & (a<=0.7)]
            self.z=np.zeros(len(self.alpharange))
            Ea=np.mean(Eas)
            for i in range(0,len(self.alpharange)):
                x=Ea/(R*(self.T[i]+273.15))
                p=0.00484*np.exp(-1.0516*x) # CMP 2
                #self.z[i]=self.dalpharange[i]*Ea*np.exp(x)*p/R # Calculation of z=f(alpha)*g(alpha) of experimental
                self.z[i]=self.dalpharange[i]*(self.T[i]+273.15)*((x**3+18*x**2+86*x+96)/(x**4+20*x**3+120*x**2+240*x+120)) # CMP 3
            self.z05_exp=self.z[np.isclose(self.alpharange,0.5,atol=0.001)][0] # z at 0.5
            #self.z=self.z/self.z05_exp # Normalization
            return self.alpharange,self.z, self.T, self.dalpharange
        self.alpharange,self.z, self.Temp, self.dalpharange=theo(self.alpha[Index],self.dalpha_ind,self.T_actual[Index],self.Eas,self.Rg)
        
        # masterplots of theoretical models z=f*g
        # Diffusion
        def diff1(alpha,exp):
            z=(1/(2*alpha))*(alpha**2)
            z05=(1/(2*0.5))*(0.5**2)
            master=z
            self.ax3[0,0].plot(alpha,master, label='D1')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def diff2VB(alpha,exp):
            z=(-1/np.log(1-alpha))*(alpha + (1-alpha)*(np.log(1-alpha)))
            z05=(-1/np.log(1-0.5))*(0.5 + (1-0.5)*(np.log(1-0.5)))
            master=z
            self.ax3[0,0].plot(alpha,master, label='D2-VB')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def diff2J(alpha,exp):
            y=(((1-alpha)**(1/2))/(1-(1-alpha)**(1/2)))
            z=(((1-alpha)**(1/2))/(1-(1-alpha)**(1/2)))*((1-(1-alpha)**(0.5))**(2))
            z05=(((1-0.5)**(1/2))/(1-(1-0.5)**(1/2)))*(1-(1-0.5)**(0.5))**(2)
            master=z
            self.ax3[0,0].plot(alpha,master, label='D2-J')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master,y

        def diff2AJ(alpha,exp):
            y=(((1+alpha)**(1/2))/(-1+(1+alpha)**(1/2)))
            z=(((1+alpha)**(1/2))/(-1+(1+alpha)**(1/2)))*(-1+(1+alpha)**(0.5))**(2)
            z05=(((1+0.5)**(1/2))/(-1+(1+0.5)**(1/2)))*(-1+(1+0.5)**(0.5))**(2)
            master=z
            self.ax3[0,0].plot(alpha,master, label='D2-AJ')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master,y

        def diff3(alpha,exp):
            z=((2*(1-alpha)**(2/3))/(1-(1-alpha)**(1/3)))*(1-(1-alpha)**(1/3))**2
            z05=((2*(1-0.5)**(2/3))/(1-(1-0.5)**(1/3)))*(1-(1-0.5)**(1/3))**2
            master=z
            self.ax3[0,0].plot(alpha,master, label='D3')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diffIT(alpha,exp):
            z=(3*(1-alpha)**(4/3))*((1-alpha)**(-1/3)-1)
            z05=(3*(1-0.5)**(4/3))*((1-0.5)**(-1/3)-1)
            master=z
            self.ax3[0,0].plot(alpha,master, label='D-IT')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diffTD(alpha,exp):
            z=(3/((1-alpha)**(-4/3) - (1-alpha)**(-1)))*((1-alpha)**(-1/3)-1+((1/3)*np.log(1-alpha)))
            z05=(3/((1-0.5)**(-4/3) - (1-0.5)**(-1)))*((1-0.5)**(-1/3)-1+((1/3)*np.log(1-0.5)))
            master=z
            self.ax3[0,0].plot(alpha,master, label='D-TD')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diff2(alpha,exp):
            z=(3/((1-alpha)**(-8/3) - (1-alpha)**(-7/3)))*(((1/5)*(1-alpha)**(-5/3))-((1/4)*(1-alpha)**(-4/3)) + (1/20) )
            z05=(3/((1-0.5)**(-8/3) - (1-0.5)**(-7/3)))*(((1/5)*(1-0.5)**(-5/3))-((1/4)*(1-0.5)**(-4/3)) + (1/20) )
            master=z
            self.ax3[0,0].plot(alpha,master, label='D2')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diff3J(alpha,exp):
            z=((3*(1-alpha)**(2/3))/(2*(1-(1-alpha)**(1/3))))*(1-(1-alpha)**(1/3))**(2)
            z05=((3*(1-0.5)**(2/3))/(2*(1-(1-0.5)**(1/3))))*(1-(1-0.5)**(1/3))**(2)
            master=z
            self.ax3[0,0].plot(alpha,master, label='D3-J')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diff3GB(alpha,exp):
            z=(3/(2*((1-alpha)**(-1/3) - 1)))*(1-(2*alpha/3)-(1-alpha)**(2/3))
            z05=(3/(2*((1-0.5)**(-1/3) - 1)))*(1-(2*0.5/3)-(1-0.5)**(2/3))
            master=z
            self.ax3[0,0].plot(alpha,master, label='D3-GB')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def diff3ZL(alpha,exp):
            z=((3/2)*(1-alpha)**(4/3)*((1-alpha)**(-1/3)-1)**(-1))*(((1-alpha)**(-1/3)-1)**(2))
            z05=((3/2)*(1-0.5)**(4/3)*((1-0.5)**(-1/3)-1)**(-1))*(((1-0.5)**(-1/3)-1)**(2))
            master=z
            self.ax3[0,0].plot(alpha,master, label='D3-ZL')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        # Random nucleation and nuclei growth models

        def A4(alpha,exp):
            z=(4*(1-alpha)*(-np.log(1-alpha))**(3/4))*((-np.log(1-alpha))**(1/4))
            z05=(4*(1-0.5)*(-np.log(1-0.5))**(3/4))*((-np.log(1-0.5))**(1/4))
            master=z
            self.ax3[0,1].plot(alpha,master, label='A4')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def A3(alpha,exp):
            z=(3*(1-alpha)*(-np.log(1-alpha))**(2/3))*((-np.log(1-alpha))**(1/3))
            z05=(3*(1-0.5)*(-np.log(1-0.5))**(2/3))*((-np.log(1-0.5))**(1/3))
            master=z
            self.ax3[0,1].plot(alpha,master, label='A3')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def A2(alpha,exp):
            z=(2*(1-alpha)*(-np.log(1-alpha))**(1/2))*((-np.log(1-alpha))**(1/2))
            z05=(2*(1-0.5)*(-np.log(1-0.5))**(1/2))*((-np.log(1-0.5))**(1/2))
            master=z
            self.ax3[0,1].plot(alpha,master, label='A2')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def A1_5(alpha,exp):
            z=(1.5*(1-alpha)*(-np.log(1-alpha))**(0.5/1.5))*((-np.log(1-alpha))**(1/1.5))
            z05=(1.5*(1-0.5)*(-np.log(1-0.5))**(0.5/1.5))*((-np.log(1-0.5))**(1/1.5))
            master=z
            self.ax3[0,1].plot(alpha,master, label='A1.5')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        # Chemical reaction models 

        def R0(alpha,exp):
            z=alpha
            z05=0.5
            master=z
            self.ax3[1,0].plot(alpha,master, label='R0')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def R1(alpha,exp):
            z=(1-alpha)*(-np.log(1-alpha))
            z05=(1-0.5)*(-np.log(1-0.5))
            master=z
            self.ax3[1,0].plot(alpha,master, label='R1')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def R2(alpha,exp):
            z=((1-alpha)**(2))*((1-alpha)**(-1)-1)
            z05=((1-0.5)**(2))*((1-0.5)**(-1)-1)
            master=z
            self.ax3[1,0].plot(alpha,master, label='R2')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def R3(alpha,exp):
            z=((1-alpha)**(3))*((1/2)*((1-alpha)**(-2) - 1))
            z05=((1-0.5)**(3))*((1/2)*((1-0.5)**(-2) - 1))
            master=z
            self.ax3[1,0].plot(alpha,master, label='R3')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def R_CS(alpha,exp):
            z=(3*(1-alpha)**(2/3))*(1-(1-alpha)**(1/3))
            z05=(3*(1-0.5)**(2/3))*(1-(1-0.5)**(1/3))
            master=z
            self.ax3[1,0].plot(alpha,master, label='R-CS')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master

        def R_CC(alpha,exp):
            z=(2*(1-alpha)**(1/2))*(1-(1-alpha)**(1/2))
            z05=(2*(1-0.5)**(1/2))*(1-(1-0.5)**(1/2))
            master=z
            self.ax3[1,0].plot(alpha,master, label='R-CC')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master,master
        # Power models

        def P2(alpha,exp):
            z=2*alpha
            z05=2*0.5
            master=z
            self.ax3[1,1].plot(alpha,master, label='P2')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master,master
        def P3(alpha,exp):
            z=3*alpha
            z05=3*0.5
            master=z
            self.ax3[1,1].plot(alpha,master, label='P3')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master,master
        def P4(alpha,exp):
            z=4*alpha
            z05=4*0.5
            master=z
            self.ax3[1,1].plot(alpha,master, label='P4')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        def E1(alpha,exp):
            z=alpha*np.log(alpha)
            z05=0.5*np.log(0.5)
            master=z
            self.ax3[1,1].plot(alpha,master, label='E1')
            RRMSE=np.sqrt(sum((master-exp)**(2))/len(alpha))/(np.mean(exp))
            return RRMSE,master
        
        # Display errors in separate window
        self.lab=['D1','D2-VB','D2-J','D2-AJ','D3','D-IT','D-TD','D2','D3-J','D3-GB','D3-ZL','A4','A3','A2','A1.5','R0','R1', 'R2','R3','R-CS', 'R-CC', 'P2','P3','P4','E1']
        self.err=[]
        self.err.append(diff1(self.alpharange,self.z)[0]*100)
        self.err.append(diff2VB(self.alpharange,self.z)[0]*100)
        self.err.append(diff2J(self.alpharange,self.z)[0]*100)
        self.err.append(diff2AJ(self.alpharange,self.z)[0]*100)
        self.err.append(diff3(self.alpharange,self.z)[0]*100)
        self.err.append(diffIT(self.alpharange,self.z)[0]*100)
        self.err.append(diffTD(self.alpharange,self.z)[0]*100)
        self.err.append(diff2(self.alpharange,self.z)[0]*100)
        self.err.append(diff3J(self.alpharange,self.z)[0]*100)
        self.err.append(diff3GB(self.alpharange,self.z)[0]*100)
        self.err.append(diff3ZL(self.alpharange,self.z)[0]*100)
        self.ax3[0,0].plot(self.alpharange,self.z,label='Experimental',linestyle='--')
        self.ax3[0,0].set_xlabel('Conversion (\u03B1)')
        self.ax3[0,0].set_ylabel('z(\u03B1)')
        self.ax3[0,0].set_title('Diffusion Master plots')
        self.ax3[0,0].legend(bbox_to_anchor=(1.1, 1.05))
        self.ax3[0,0].grid(visible=True)
        self.err.append(A4(self.alpharange,self.z)[0]*100)
        self.err.append(A3(self.alpharange,self.z)[0]*100)
        self.err.append(A2(self.alpharange,self.z)[0]*100)
        self.err.append(A1_5(self.alpharange,self.z)[0]*100)
        self.ax3[0,1].plot(self.alpharange,self.z,label='Experimental',linestyle='--')
        self.ax3[0,1].set_xlabel('Conversion (\u03B1)')
        self.ax3[0,1].set_ylabel('z(\u03B1)')
        self.ax3[0,1].set_title('Avrami-Erofeev Master plots')
        self.ax3[0,1].legend(bbox_to_anchor=(1.1, 1.05))
        self.ax3[0,1].grid(visible=True)
        
        self.err.append(R0(self.alpharange,self.z)[0]*100)
        self.err.append(R1(self.alpharange,self.z)[0]*100)
        self.err.append(R2(self.alpharange,self.z)[0]*100)
        self.err.append(R3(self.alpharange,self.z)[0]*100)
        self.err.append(R_CS(self.alpharange,self.z)[0]*100)
        self.err.append(R_CC(self.alpharange,self.z)[0]*100)
        self.ax3[1,0].plot(self.alpharange,self.z,label='Experimental',linestyle='--')
        self.ax3[1,0].set_xlabel('Conversion (\u03B1)')
        self.ax3[1,0].set_ylabel('z(\u03B1)')
        self.ax3[1,0].set_title('Chemical Reaction Master plots')
        self.ax3[1,0].legend(bbox_to_anchor=(1.1, 1.05))
        self.ax3[1,0].grid(visible=True)

        
        self.err.append(P2(self.alpharange,self.z)[0]*100)
        self.err.append(P3(self.alpharange,self.z)[0]*100)
        self.err.append(P4(self.alpharange,self.z)[0]*100)
        self.err.append(E1(self.alpharange,self.z)[0]*100)
        self.ax3[1,1].plot(self.alpharange,self.z,label='Experimental',linestyle='--')
        self.ax3[1,1].set_xlabel('Conversion (\u03B1)')
        self.ax3[1,1].set_ylabel('z(\u03B1)')
        self.ax3[1,1].set_title('Power and Exponential law Master plots')
        self.ax3[1,1].legend(bbox_to_anchor=(1.1, 1.05))
        self.ax3[1,1].grid(visible=True)

        self.Ind=Index

        self.fig3.tight_layout()
        self.frame3.place(x=100,y=75)
        self.canvas3.draw()
        
        # Print masterplot errors in separate window
    def printerrors(self):
        newwindow=Toplevel(self.Master_plots)
        newwindow.configure(bg='#aeecf4')
        newwindow.state('zoomed')
        fr=Frame(master=newwindow)
        fr.columnconfigure(0,weight=1)
        fr.columnconfigure(1,weight=2)
        for i in range(len(self.err)):
            self.ent=ttk.Label(fr,text=f'{self.err[i]: .2f}')
            self.pnt=ttk.Label(fr,text=f'{self.lab[i]}')
            self.ent.grid(row=i,column=1)
            self.pnt.grid(row=i,column=0)
        fr.pack()
    def reconstruct(self):
        self.ax4[0].clear()
        self.ax4[1].clear()
        self.labelerror.place_forget()
        text=self.clicked.get()
        #self.lab=['D1','D2-VB','D2-J','D2-AJ','D3','D-IT','D-TD','D2','D3-J','D3-GB','D3-ZL','A4','A3','A2','A1.5','R0','R1', 'R2','R3','R-CS', 'R-CC', 'P2','P3','P4','E1']
        self.func_dict={'D1':self.funcD1,'D2-VB':self.funcD2VB,'D2-J':self.funcD2J,'D2-AJ':self.funcD2AJ,'D3':self.funcD3,'D-IT':self.funcDIT,'D-TD':self.funcDTD,'D2':self.funcD2,'D3-J':self.funcD3J,'D3-GB':self.funcD3GB,'D3-ZL':self.funcD3ZL,'A4':self.funcA4,'A3':self.funcA3,'A2':self.funcA2,'A1.5':self.funcA1_5,'R0':self.funcR0,'R1':self.funcR1,'R2':self.funcR2,'R3':self.funcR3,'R-CS':self.funcRCS,'R-CC':self.funcRCC,'P2':self.funcP2,'P3':self.funcP3,'P4':self.funcP4,'E1':self.funcE1} 
        sol=odeint(self.func_dict[text],y0=(self.alpha[self.Ind][self.alpha[self.Ind]>0][0],self.T_actual[self.Ind][self.alpha[self.Ind]>0][0]+273.15),t=self.t[self.Ind][self.alpha[self.Ind]>0],args=(self.Eamean,self.Rg,self.Asmean,self.Betas[self.Ind]), atol=1e-7,rtol=1e-7)
        self.ax4[0].plot(self.T_actual[self.Ind][self.alpha[self.Ind]>0],self.alpha[self.Ind][self.alpha[self.Ind]>0], label=f'Actual-{self.Betas[self.Ind]} (C/min)')
        self.ax4[0].plot(sol[:,1]-273.15,sol[:,0],label=f'Model-{self.Betas[self.Ind]} (C/min)')
        self.ax4[0].set_title('Model vs Actual TGA curves', fontsize=20)
        self.ax4[0].set_xlabel(r'Temperature ($^{\circ} C$)', fontsize=20)
        self.ax4[0].set_ylabel('Conversion (\u03B1)', fontsize=20)
        self.ax4[0].legend(fontsize=15)
        self.ax4[0].tick_params(axis='both', which='major', labelsize=15)
        self.ax4[0].grid(visible=True)
        self.ax4[1].scatter(self.T_actual[self.Ind][self.alpha[self.Ind]>0],self.alpha[self.Ind][self.alpha[self.Ind]>0]-sol[:,0])
        self.ax4[1].plot(self.T_actual[self.Ind][self.alpha[self.Ind]>0],[0 for i in range(len(self.alpha[self.Ind][self.alpha[self.Ind]>0]))],color='black')
        self.ax4[1].set_title('Residual plot', fontsize=20)
        self.ax4[1].set_xlabel(r'Temperature ($^{\circ} C$)', fontsize=20)
        self.ax4[1].set_ylabel(r'$\alpha_{e}-\alpha_{c}$', fontsize=20)
        self.ax4[1].tick_params(axis='both', which='major', labelsize=15)
        self.ax4[1].grid(visible=True)
        self.fig4.tight_layout()
        self.frame4.place(x=150,y=50)
        self.canvas4.draw()
        self.labelerror=ttk.Label(self.Tga_reconstruct, text=f'RRMSE : {100*(np.sqrt(sum((sol[:,0]-self.alpha[self.Ind][self.alpha[self.Ind]>0])**(2))/len(self.alpha[self.Ind]>0))/(np.mean(self.alpha[self.Ind][self.alpha[self.Ind]>0]))): .2f} %')
        self.labelerror.place(x=400,y=10)

        # Predict using model TGA curve at higher heating rate
    def predict(self):
        self.ax5.clear()
        txt=self.clicked2.get()
        bet=int(self.drop2enter.get())
        T_start=[]
        t_start=[]
        for i in range(len(self.Betas)):

            T_start.append(self.T_actual[i][self.alpha[i]>0][0])
            t_start.append(self.t[i][self.alpha[i]>0][0])

        # Linear regression to estimate starting conditions for numerical integration

        def Tstart(Temps,Betas): # temps is temperatures at a certain conversion, Betas are the heating rates

            r=sp.stats.linregress(Betas, Temps) # Linear regression

            R2=r.rvalue**2 # R square value calculation

            return R2, r.slope, r.intercept # Activation energy calculation
        R2,slope,intercept=Tstart(np.array(T_start),np.array(self.Betas))
        R2t, slopet, interceptt=Tstart(np.array(t_start), np.array(self.Betas))

        T_start=slope*bet + intercept 
        t_start=slopet*bet + interceptt 
        t_starts=[]
        T_starts=[]
        t_ranges=[]
        sols=[]
        if txt=='Optimized':
            if self.text3=='SB model':
                for i in range(len(self.Betas)):
                    t_starts.append(self.t[i][self.alpha[i]>0][0]) 
                    T_starts.append(self.T_actual[i][self.alpha[i]>0][0])
                    t_ranges.append(self.t[i][self.alpha[i]>0])
                    sol=odeint(self.SB,y0=(self.alpha[i][self.alpha[i]>0][0],self.T_actual[i][self.alpha[i]>0][0]+273.15),t=t_ranges[i],args=(self.poptSB.x[0],self.poptSB.x[1],self.Betas[i]), atol=1e-5,rtol=1e-5)
                    sols.append(sol) # Entire range of activation
                sol_chosen=odeint(self.SB,y0=(1e-5,T_start+273.15),t=np.linspace(t_start,t_start+((600-T_start)/bet),1000),args=(self.poptSB.x[0],self.poptSB.x[1],bet), atol=1e-7,rtol=1e-7)
                for i in range(len(self.Betas)):
                    self.ax5.plot(sols[i][:,1]-273.15,sols[i][:,0],label=f'Model-{self.Betas[i]} C/min')
            else:
                for i in range(len(self.Betas)):
                    t_starts.append(self.t[i][self.alpha[i]>0][0]) 
                    T_starts.append(self.T_actual[i][self.alpha[i]>0][0])
                    t_ranges.append(self.t[i][self.alpha[i]>0])
                    sol=odeint(self.modeldict[self.text3],y0=(self.alpha[i][self.alpha[i]>0][0],self.T_actual[i][self.alpha[i]>0][0]+273.15),t=t_ranges[i],args=(self.popt.x[0],self.Betas[i]), atol=1e-5,rtol=1e-5)
                    sols.append(sol) # Entire range of activation
                sol_chosen=odeint(self.modeldict[self.text3],y0=(1e-5,T_start+273.15),t=np.linspace(t_start,t_start+((600-T_start)/bet),1000),args=(self.popt.x[0],bet), atol=1e-7,rtol=1e-7)
                for i in range(len(self.Betas)):
                    self.ax5.plot(sols[i][:,1]-273.15,sols[i][:,0],label=f'Model (fitted) - {self.Betas[i]} C/min')
        else:
            for i in range(len(self.Betas)):
                t_starts.append(self.t[i][self.alpha[i]>0][0]) 
                T_starts.append(self.T_actual[i][self.alpha[i]>0][0])
                t_ranges.append(self.t[i][self.alpha[i]>0])
                sol=odeint(self.func_dict[txt],y0=(self.alpha[i][self.alpha[i]>0][0],self.T_actual[i][self.alpha[i]>0][0]+273.15),t=t_ranges[i],args=(self.Eamean,self.Rg,self.Asmean,int(self.Betas[i])), atol=1e-5,rtol=1e-5)
                sols.append(sol) # Entire range of activation
            sol_chosen=odeint(self.func_dict[txt],y0=(1e-5,T_start+273.15),t=np.linspace(t_start,t_start+((600-T_start)/bet),1000),args=(self.Eamean,self.Rg,self.Asmean,bet), atol=1e-7,rtol=1e-7)
            for i in range(len(self.Betas)):
                self.ax5.plot(sols[i][:,1]-273.15,sols[i][:,0],label=f'Model (fitted) - {self.Betas[i]} C/min')
        self.ax5.plot(sol_chosen[:,1]-273.15,sol_chosen[:,0],label=f'Model (predicted) - {bet} C/min')
        self.ax5.set_title('Model TGA curves and model predicted TGA curve', fontsize=20)
        self.ax5.set_xlabel(r'Temperature ($^{\circ} C$)', fontsize=20)
        self.ax5.set_ylabel('Conversion (\u03B1)', fontsize=20)
        self.ax5.legend(fontsize=15)
        self.ax5.grid(visible=True)
        self.fig5.tight_layout()
        self.ax5.tick_params(axis='both', which='major', labelsize=15)
        self.frame5.place(x=150,y=50)
        self.canvas5.draw()
        
        # model order optimization
    def optimize(self):
        self.order2.place_forget()
        self.order.place_forget()
        self.labelerror2.place_forget()
        self.ax6[0].clear()
        self.ax6[1].clear()
        self.frame6.place_forget()
        self.text3=self.clicked3.get()
        self.Index=self.Betas.index(int(self.drop3enter.get()))
        self.Ig=float(self.drop3enter2.get())
        self.Ig2=float(self.drop3enter3.get())
        self.modeldict={'Avrami':self.avrami, 'Chemical Reaction':self.react, 'Power law': self.PE}

        if self.text3 == 'SB model':
            def objective(x):
                solopt=[]
                res=[]
                for i in range (len(self.Betas)):
                    solopt.append(odeint(self.SB,y0=(1e-5,self.T_actual[i][self.alpha[i]>0][0]+273.15),t=self.t[i][self.alpha[i]>0],args=(x[0],x[1],self.Betas[i])))
                    resi=solopt[i][:,0]-self.alpha[i][self.alpha[i]>0]
                    res.extend(resi)
                return res
            self.poptSB=least_squares(objective,x0=[self.Ig,self.Ig2])
            solopt=odeint(self.SB,y0=(1e-5,self.T_actual[self.Index][self.alpha[self.Index]>0][0]+273.15),t=self.t[self.Index][self.alpha[self.Index]>0],args=(self.poptSB.x[0],self.poptSB.x[1],self.Betas[self.Index]))
            self.order=ttk.Label(self.Optimize,text=f'Order of SB model: n={self.poptSB.x[0]: .2f} and k={self.poptSB.x[1]:.2f}')
            self.order.place(x=50,y=900)
        else:
            def objective(x):
                solopt=[]
                res=[]
                for i in range (len(self.Betas)):
                    solopt.append(odeint(self.modeldict[self.text3],y0=(1e-5,self.T_actual[i][self.alpha[i]>0][0]+273.15),t=self.t[i][self.alpha[i]>0],args=(x[0],self.Betas[i])))
                    resi=solopt[i][:,0]-self.alpha[i][self.alpha[i]>0]
                    res.extend(resi)
                return res
            self.popt=least_squares(objective,x0=[self.Ig])
            solopt=odeint(self.modeldict[self.text3],y0=(1e-5,self.T_actual[self.Index][self.alpha[self.Index]>0][0]+273.15),t=self.t[self.Index][self.alpha[self.Index]>0],args=(self.popt.x[0],self.Betas[self.Index]))
            self.order2=ttk.Label(self.Optimize,text=f'Order of {self.text3} model: n={self.popt.x[0]: .2f}')
            self.order2.place(x=50,y=900)

        self.ax6[0].plot(self.T_actual[self.Index][self.alpha[self.Index]>0],self.alpha[self.Index][self.alpha[self.Index]>0], label=f'Actual-{self.Betas[self.Index]} (C/min)')
        self.ax6[0].plot(solopt[:,1]-273.15,solopt[:,0],label=f'Model-{self.Betas[self.Index]} (C/min)')
        self.ax6[0].set_title('Model vs Actual TGA curves', fontsize=20)
        self.ax6[0].set_xlabel(r'Temperature ($^{\circ} C$)', fontsize=20)
        self.ax6[0].set_ylabel('Conversion (\u03B1)', fontsize=20)
        self.ax6[0].legend(fontsize=15)
        self.ax6[0].tick_params(axis='both', which='major', labelsize=15)
        self.ax6[0].grid(visible=True)
        self.ax6[1].scatter(self.T_actual[self.Index][self.alpha[self.Index]>0],self.alpha[self.Index][self.alpha[self.Index]>0]-solopt[:,0])
        self.ax6[1].plot(self.T_actual[self.Index][self.alpha[self.Index]>0],[0 for i in range(len(self.alpha[self.Index][self.alpha[self.Index]>0]))],color='black')
        self.ax6[1].set_title('Residual plot', fontsize=20)
        self.ax6[1].set_xlabel(r'Temperature ($^{\circ} C$)', fontsize=20)
        self.ax6[1].set_ylabel(r'$\alpha_{e}-\alpha_{c}$', fontsize=20)
        self.ax6[1].tick_params(axis='both', which='major', labelsize=15)
        self.ax6[1].grid(visible=True)
        self.fig6.tight_layout()
        self.frame6.place(x=150,y=50)
        self.canvas6.draw()
        self.labelerror2=ttk.Label(self.Optimize, text=f'RRMSE : {100*(np.sqrt(sum((solopt[:,0]-self.alpha[self.Index][self.alpha[self.Index]>0])**(2))/len(self.alpha[self.Index]>0))/(np.mean(self.alpha[self.Index][self.alpha[self.Index]>0]))) : .2f} %')
        self.labelerror2.place(x=600,y=900)
MyGui()

# Things to do:

# Make nicer
# Option to view plots of KAS analysis (need to add)
# Fix figure layout (reconstruct)
# TGA prediction, increase temp to 800
# Add validation section, use any results you collected earlier (non fitted result) and plot to validate
# Optional: Add optimization button for order reactions --> Needs to be tested on base script first.

# Add try catch blocks to make readable errors  (Last thing to do).