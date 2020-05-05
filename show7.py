# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from layout import Ui_Form as Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from csv_read import csv_read
from concurrent.futures import ThreadPoolExecutor

import matplotlib
matplotlib.use("Qt5Agg")  # use QT5 for matplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import MultipleLocator

# basically as same as plt class, 
# but this figure can show graphs in QTpy5
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

# class including fuchtions of building graphs        
class Graphs:
     
    # generate cases&time graph
    def plotcase(self):
        
        # initialize csv_read class
        # you can see the code of the class in csv_read.py
        read = csv_read('us_covid19_daily.csv')
        self.cases, time = read.cases_time()
        
        for i in range(5):
            time.append('next{}'.format(i+1))
            
        self.time = time[:]
        grow_rate = 0
        
        for day in range(len(self.cases) - 6, len(self.cases)):
            if day+1 < len(self.cases):
                present = self.cases[day]
                next_day = self.cases[day+1]
                grow_rate += (next_day - present)/present
                
        grow_rate = grow_rate / 5
        print('5-day-growth rate{}'.format(grow_rate)) 
        prediction = [self.cases[len(self.cases)-5]]
        
        for day in range(9):
            if day+1 < 10:
                prediction.append(prediction[day]*(1+grow_rate))
        #     
        x_locat = MultipleLocator(5)
        self.F.axes.xaxis.set_major_locator(x_locat)
        # add a plot of Cumulative cases
        self.F.axes.plot(time[:-5], self.cases, 
                         marker = 'o',
                         label = 'Cumulative cases',
                         color = '#FF7E00')
        # add plot of Predicted Cases
        self.F.axes.plot(time[len(time) - 10:], prediction, 
                              color = 'green',
                              marker = 'o', 
                              alpha = 0.3,
                              label = 'Predicted Cases')
        # add title of the graph
        self.F.fig.suptitle("Cases&Time", size = 'xx-large')
        # add legend
        self.F.axes.legend()
        # add a single text
        self.F.axes.text(len(self.cases)-3, int(prediction[-1])*0.89,
                         '5-day Groth Rate:{:.2f}%'.format(grow_rate*100),
                         color = 'black',
                         style = 'oblique',
                         size = 'large',
                         alpha = 0.4)
        # add a text used to show data of a single note when mouse move on it
        self.num = self.F.axes.text(1, 500000, '',
                                    color = '#FF4500',
                                    style = 'oblique',
                                    size = 'large',
                                    ha = 'center',
                                    bbox = {'facecolor' : 'white',
                                            'alpha' : 0.75,
                                            'edgecolor' : '#FF975A'})
        self.mark = self.F.axes.text(1, 500000, '',
                                    color = '#FF3030',
                                    style = 'oblique',
                                    size = '24',
                                    ha = 'center',
                                    va = 'center')
                                            
        self.F.axes.set_xlabel('Measured Time Period 01/22/2020 - 04/21/2020')
        self.F.axes.set_ylabel('Cases')
        self.F.axes.spines['right'].set_visible(False)
        self.F.axes.spines['top'].set_visible(False)
        # when mouse move on the graph, it can trigger the function onmove() 
        self.F.mpl_connect('motion_notify_event', self.onmove)
     
    # generate the map of death graph
    def plotdeatharea(self):
        read = csv_read('time_series_covid_19_deaths_US.csv')
        state_death = read.states_death()
        x = 0
        for item in state_death:
            if item[1] > 0:
                self.F1.axes.barh(item[0], item[1])
                self.F1.axes.text(item[1]*1.05, x - 0.3, item[1],
                                  size = 'large')
                x += 1
        self.F1.axes.set_xscale('log')
        self.F1.axes.set_xlabel('Death')
        
        self.F1.axes.spines['right'].set_visible(False)
        self.F1.axes.spines['top'].set_visible(False)
        
        self.F1.axes.set_title("Only showing the states having death cases", 
                               size = 'large')
        self.F1.fig.suptitle("Death of states", size = 'xx-large')
        
     # generate the graph showing cured and death    
    def plotdeathcured(self):
        read = csv_read('us_covid19_daily.csv')
        self.death, self.cured, self.timedeath = read.reco_death()
        x_locat = MultipleLocator(5)
        self.F2.axes.xaxis.set_major_locator(x_locat)
        self.F2.axes.plot(self.timedeath, self.death, 
                         marker = 'o',
                         label = 'Death',
                         color = '#FF4F05')
        self.F2.axes.plot(self.timedeath, self.cured, 
                         marker = 'o',
                         label = 'Recovered',
                         color = '#20B2AA')
        self.F2.axes.legend()
        self.F2.fig.suptitle("Cured and Death", size = 'xx-large')
        self.num_dea = self.F2.axes.text(1, 5, '',
                                    color = '#FF3030',
                                    style = 'oblique',
                                    size = 'large',
                                    ha = 'center',
                                    bbox = {'facecolor' : 'white',
                                            'alpha' : 0.75,
                                            'edgecolor' : '#FF3030'})
        self.num_cur = self.F2.axes.text(1, 5, '',
                                    color = '#27408B',
                                    style = 'oblique',
                                    size = 'large',
                                    ha = 'center',
                                    bbox = {'facecolor' : 'white',
                                            'alpha' : 0.75,
                                            'edgecolor' : '#27408B'})
        
        self.mark_c = self.F2.axes.text(1, 500000, '',
                                    color = '#1C86EE',
                                    style = 'oblique',
                                    size = '24',
                                    ha = 'center',
                                    va = 'center')
        
        
        self.mark_d = self.F2.axes.text(1, 500000, '',
                                    color = '#EE0000',
                                    style = 'oblique',
                                    size = '24',
                                    ha = 'center',
                                    va = 'center')
                                            
        self.F2.axes.spines['right'].set_visible(False)
        self.F2.axes.spines['top'].set_visible(False)   
                                 
        self.F2.axes.set_xlabel('Date:MMDD')
        self.F2.axes.set_ylabel('Cured or Death')
        self.F2.mpl_connect('motion_notify_event', self.onmove2)
        
    def plotStateCases(self):
        read = csv_read('time_series_covid_19_confirmed_US.csv')
        state_cases = read.states_death()
        x = 0
        for item in state_cases:
            if item[1] > 0:
                self.F3.axes.barh(item[0], item[1])
                self.F3.axes.text(item[1]*1.05, x - 0.3, item[1],
                                  size = 'large')
                x += 1
        self.F3.axes.set_xscale('log')
        self.F3.axes.set_xlabel('Confirmed')
        
        self.F3.axes.spines['right'].set_visible(False)
        self.F3.axes.spines['top'].set_visible(False)
        
        self.F3.axes.set_title("Only showing the states having confirmed cases", 
                               size = 'x-large')
        self.F3.fig.suptitle("Confirmed Cases of States", size = 'xx-large')        
        
    
# main function of combining and showing graph        
class MainDialogImgBW(QDialog,Ui_Dialog):
    def __init__(self):
        super(MainDialogImgBW,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('COVID')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        
        self.figures = []
        self.F = MyFigure(width=3, height=2, dpi=120)
        self.figures.append(self.F)
        for i in range(1, 4):
            exec('self.F{} = MyFigure(width=3, height=2, dpi=120)'.format(i))
            exec('self.figures.append(self.F{})'.format(i))
        print(self.figures)
        # initial the figure of death and cured

        
        # make a trigger for the buttons which deployed in pyqt5 GUI class
        # ex. if the button1 is clicked, the function btnstate() will be called
        self.button1.clicked.connect(self.btnstate)
        self.button2.clicked.connect(self.btnstate2)
        self.button3.clicked.connect(self.btnstate3)
        self.button4.clicked.connect(self.btnstate4)
        
        # connect with the GroupBox in the GUI
        self.gridlayout = QGridLayout(self.groupBox)
        
        # call and generate the graphs
        Graphs.plotdeatharea(self)
        Graphs.plotcase(self)
        Graphs.plotdeathcured(self)
        Graphs.plotStateCases(self)
        
        # add graphs into the GroupBox
        self.gridlayout.addWidget(self.F3, 0, 1)
        self.gridlayout.addWidget(self.F2, 0, 1)
        self.gridlayout.addWidget(self.F1, 0, 1)
        self.gridlayout.addWidget(self.F, 0, 1)
        
        
        # hide the graphs at begining
        for figure in self.figures:
            figure.hide()
            
    # if the button1 is clicked, show the graph of cases&time and hide others
    def btnstate(self):
        for figure in self.figures:
            figure.hide()
        self.figures[0].show()

    # button2, show F2 hide others
    def btnstate2(self):
        for figure in self.figures:
            figure.hide()
        self.figures[1].show()
    # button3       
    def btnstate3(self):
        for figure in self.figures:
            figure.hide()
        self.figures[2].show()
        
    def btnstate4(self):
        for figure in self.figures:
            figure.hide()
        self.figures[3].show()
            
    # when program detected mouse movement on F(cases&time graph)
    def onmove(self, event):
        x = 0
        try:
            x = float(event.xdata) #, int(float(event.ydata))
            if x > -1:
                case1 = self.cases[int(x)]
                if x > 1:
                    case0 = self.cases[int(x)]-self.cases[int(x-1)]
                    self.num.set_text('Date:{}\nCases:{}\n+{}'.format(
                                        self.time[int(x)],
                                        case1,
                                        case0))
                else:
                    self.num.set_text('Date:{}\nCases:{}'.format(
                                        self.time[int(x)],
                                        case1))
                    
                self.num.set_x(round(int(x)))
                self.num.set_y(int(self.cases[int(x)])+50000)
                self.mark.set_text('+')
                self.mark.set_x(round(int(x)))
                self.mark.set_y(int(self.cases[int(x)]))
                self.F.draw()
                # print('Day:{}, Cases:{}'.format(round(x), self.cases[int(x)]))
        except:
            pass
    # movement on F2(death&cured graph)   
    def onmove2(self, event):
        x = 0
        try:
            x = float(event.xdata) #, int(float(event.ydata))
            if x > -1:
                death1 = self.death[int(x)]
                cured1 = self.cured[int(x)]
                if x > 1:   
                    death0 = self.death[int(x)]-self.death[int(x-1)]
                    cured0 = self.cured[int(x)]-self.cured[int(x-1)]
                    self.num_dea.set_text('Date:{}\nDeath:{}\n+{}'.format(
                                        self.timedeath[int(x)],
                                        death1,
                                        death0))
                    self.num_cur.set_text('Date:{}\nCured:{}\n+{}'.format(
                                        self.timedeath[int(x)],
                                        cured1,
                                        cured0))
                else:
                    self.num_dea.set_text('Date:{}\nDeath:{}'.format(
                                        self.timedeath[int(x)],
                                        death1))
                    self.num_cur.set_text('Date:{}\nCured:{}'.format(
                                        self.timedeath[int(x)],
                                        cured1))
                    
                self.num_dea.set_x(round(int(x)))
                self.num_dea.set_y(int(self.death[int(x)])-5000)
                self.mark_d.set_text('+')
                self.mark_d.set_x(round(int(x)))
                self.mark_d.set_y(int(self.death[int(x)]))
                
                self.num_cur.set_x(round(int(x)))
                self.num_cur.set_y(int(self.cured[int(x)])+2500)
                self.mark_c.set_text('+')
                self.mark_c.set_x(round(int(x)))
                self.mark_c.set_y(int(self.cured[int(x)]))                
                self.F2.draw()
                # print('Day:{}, Cases:{}'.format(round(x), self.cases[int(x)]))
        except:
            pass

# main function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainDialogImgBW()
    executor = ThreadPoolExecutor(max_workers=8)
    main.show()
    #app.installEventFilter(main)
    sys.exit(app.exec_())