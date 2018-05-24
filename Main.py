#!-*-coding:utf-8-*-
import sys
import gmdh
import numpy as np
import os
#
#C:\Python27\Lib\site-packages\PyQt4\pyuic4.bat -x window.ui -o window.py
#
# import PyQt4 QtCore and QtGui modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
dir = os.getcwd()+'\\'

(Ui_MainWindow, QMainWindow) = uic.loadUiType('window_1.ui')
(Ui_Dialog, QDialog) = uic.loadUiType('GMDH_results.ui')
(Ui_Dialog_gmdh, QDialog) = uic.loadUiType('GMDH_info.ui')
(Ui_Dialog_about,QDialog) = uic.loadUiType('About.ui')
#Labels = QStringList(["LEB","EYS","MED","GNI","HDI"])
Data = {"LEB":[],"EYS":[],"MYS":[],"GNI":[],"HDI":[]}
class My_Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        self.MainText =''
Data__Statistics  ={"Model":[],"R-sq.":[],"RSS":[],"DW":[],"MSE":[],"MAPE":[],"Theil":[],"Akaike":[],"Forecast":[]}

class My_info(QDialog,Ui_Dialog_about):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        bool_show_gmdh = False

class My_GMDH_info(QDialog,Ui_Dialog_gmdh):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        bool_show_gmdh = False



class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.GMDHwindow = None
        self.GMDH_window_info = None
        self.Main_Matrix = np.matrix([])
        self.Reg_hdi = None
        self.hdi = None
        self.Info = None
        self.gni = 0
        self.exp_ed = 0
        self.Reg_Main_matrix = []
        self.mean_ed = 0
        self.liv = 0
        self.GMDH_net = []
        self.GMDH_str = ''
        self.reg_teta = 0
        self.MovAv_3 = None
    #Block of statistics
        self.gmdh_Akaike = 0
        self.arma_Akaike = 0
        #Adequatnist modeli
        self.gmdh_R_kv = 0
        self.gmdh_sum_er = 0
        self.gmdh_DW = 0

        self.ARMA_R_kv =0
        self.ARMA_sum_er = 0
        self.ARMA_DW = 0

        #Quality of Model
        self.gmdh_MSE = 0
        self.gmdh_MAPE = 0
        self.gmdh_Theil = 0

        self.ARMA_MSE = 0
        self.ARMA_MAPE = 0
        self.ARMA_Theil = 0
        self.forecast_gmdh = 0
        self.forecast_arma = 0
        self.last_movav = None
        self.for_proof = None


    #opening explorer
        QObject.connect(self.ui.pushButton, SIGNAL("clicked()"), self.file_dialog1)
        QObject.connect(self.ui.pushButton_2, SIGNAL("clicked()"), self.file_dialog2)
        QObject.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.file_dialog3)
        QObject.connect(self.ui.pushButton_4, SIGNAL("clicked()"), self.file_dialog4)
        QObject.connect(self.ui.pushButton_5, SIGNAL("clicked()"), self.file_dialog5)



    def __del__(self):
        self.ui = None

    def Open_resultGMDH(self):
        #if self.GMDHwindow ==None:
        self.GMDHwindow = My_Dialog()
        self.GMDHwindow.textEdit.setText(self.GMDH_str)
        self.GMDHwindow.show()

    def about(self):
        self.Info = My_info()
        self.Info.show()

    def regression(self):
        self.reg_teta  = gmdh.mnko(self.Reg_Main_matrix,self.Reg_hdi)
        print(self.reg_teta)
        Forecast = np.dot(self.Reg_Main_matrix,self.reg_teta)
        errors = self.Reg_hdi - Forecast

        self.ARMA_DW = gmdh.Darbin_Watson(errors)
        self.ARMA_R_kv = gmdh.R_kv(self.Reg_hdi,Forecast)
        self.ARMA_sum_er = gmdh.Sum_of_S_errors(self.Reg_hdi,Forecast)
        self.ARMA_MSE = gmdh.trivial_MSE(Forecast,self.Reg_hdi)
        self.ARMA_MAPE = gmdh.MAPE(Forecast,self.Reg_hdi)
        self.ARMA_Theil = gmdh.Theil(self.Reg_hdi,Forecast)
        self.ARMA_Akaike = gmdh.Akaike(self.ARMA_sum_er,int(self.Reg_hdi.size),int(self.Reg_Main_matrix.shape[1]))
        Data__Statistics["Model"].append("ARMA(3)")
        Data__Statistics["R-sq."].append(str(round(float(self.ARMA_R_kv),3)))
        Data__Statistics["RSS"].append(str(round(float(self.ARMA_sum_er),6)))
        Data__Statistics["DW"].append(str(round(float(self.ARMA_DW),3)))
        Data__Statistics["MSE"].append(str(round(float(self.ARMA_MSE),6)))
        Data__Statistics["MAPE"].append(str(round(float(self.ARMA_MAPE),3))+'%')
        Data__Statistics["Theil"].append(str(round(float(self.ARMA_Theil),6)))
        Data__Statistics["Akaike"].append(str(round(float(self.ARMA_Akaike),3)))
        t =[]
        for i in range(self.reg_teta.size):
            t.append(str(round(float(self.reg_teta[i]),6)))
        self.ui.textBrowser.setText('HDI(t) = '+t[0]+'*GNI(t-1)+'+t[1]+'*LEB(t-1)+'+t[2]+'*EYS(t-1)+'+t[3]+'*MYS(t-1)+'+t[4]+'*MA(3)')
        tmp = np.concatenate((self.for_proof,self.last_movav),axis = 1)
        self.forecast_arma = np.dot(tmp,self.reg_teta)
        Data__Statistics["Forecast"].append(str(round(float(self.forecast_arma),3)))





    def GMDH(self):
        poriadok = self.ui.WayGMDH.currentIndex()
        if poriadok == 0:
            poriadokBool = True
        else:
            poriadokBool = False
        percentage = self.ui.comboBox.currentIndex()
        if percentage == 0 or type(percentage)=='NoneType':
            percentage  == 5
        percentage = gmdh.index_to_percent(percentage)
        Labels = []
        for key in Data:
            Labels.append(key)
        self.GMDH_net = gmdh.MGUA(self.Main_Matrix, self.hdi, percentage,Labels, poriadokBool)
        self.GMDH_str = 'HDI = '+gmdh.String_Result_of_Layer(Labels,self.GMDH_net,self.Main_Matrix,(len(self.GMDH_net)-1),gmdh.Index_of_best(self.GMDH_net[-2]),poriadokBool)

        resultGMDH = gmdh.Vec_res_of_net(self.GMDH_net,self.Main_Matrix,(len(self.GMDH_net)-1),poriadokBool)
        errors = resultGMDH - self.hdi
        self.gmdh_DW = gmdh.Darbin_Watson(errors)
        self.gmdh_R_kv = gmdh.R_kv(self.hdi,resultGMDH)
        self.gmdh_sum_er = gmdh.Sum_of_S_errors(self.hdi,resultGMDH)
        self.gmdh_MSE = gmdh.trivial_MSE(resultGMDH,self.hdi)
        self.gmdh_MAPE = gmdh.MAPE(resultGMDH,self.hdi)
        self.gmdh_Theil = gmdh.Theil(self.hdi,resultGMDH)
        self.gmdh_Akaike = gmdh.Akaike(self.gmdh_sum_er,int(self.hdi.size),int(self.Main_Matrix.shape[1]))
        s=""
        #self.filename = sys.decode(sys.getfilesystemencoding())
        if poriadokBool ==True:
            s="GMDH(2,"+str(percentage)+"%)"
        else:
            s = "GMDH(3,"+str(percentage)+"%)"
        Data__Statistics["Model"].append(s)
        Data__Statistics["R-sq."].append(str(round(float(self.gmdh_R_kv),3)))
        Data__Statistics["RSS"].append(str(round(float(self.gmdh_sum_er),6)))
        Data__Statistics["DW"].append(str(round(float(self.gmdh_DW),3)))
        Data__Statistics["MSE"].append(str(round(float(self.gmdh_MSE),6)))
        Data__Statistics["MAPE"].append(str(round(float(self.gmdh_MAPE),3))+"%")
        Data__Statistics["Theil"].append(str(round(float(self.gmdh_Theil),6)))
        Data__Statistics["Akaike"].append(str(round(float(self.gmdh_Akaike),3)))

        n= int(self.Main_Matrix.shape[0])
        vec = self.Main_Matrix[n-1]
        self.forecast_gmdh =gmdh.calculate_result(vec,self.GMDH_net,poriadokBool)
        Data__Statistics["Forecast"].append(str(round(float(self.forecast_gmdh),3)))




        self.GMDH_window_info = My_GMDH_info()
        self.GMDH_window_info.show()

    def Show_stats(self):
        m = 0

        Header = []
        for key in Data__Statistics:
            n = 0
            Header.append(key)
            for item in Data__Statistics[key]:
                newitem = QTableWidgetItem(item)
                self.ui.StatsWidget.setItem(n,m,newitem)
                n+= 1
            m+=1

        self.ui.StatsWidget.setHorizontalHeaderLabels(Header)



    def buttonClicked(self):
        a = int(self.ui.comboBox_3.currentText())
        b = int(self.ui.comboBox_2.currentText())
        Header =[]
        if a < b:
            for i in range(a,b+1):
                Header.append(str(i))
            self.ui.tableWidget.setVerticalHeaderLabels(Header)
        n = 0
        if (self.ui.lineEdit.text()=='') and (self.ui.lineEdit_2.text()=='') and (self.ui.lineEdit_3.text()=='') and (self.ui.lineEdit_4.text()=='') and (self.ui.lineEdit_5.text()==''):
            self.hdi = gmdh.make_mat(dir+'hdi.txt')
            self.mean_ed = gmdh.make_mat(dir+'mean_ed.txt')
            self.liv = gmdh.make_mat(dir+'li_ex.txt')
            self.exp_ed = gmdh.make_mat(dir+'ex_ed.txt')
            self.gni = gmdh.make_mat(dir+'gni_pc.txt')
        else:
            self.hdi = gmdh.make_mat(self.ui.lineEdit.Text())
            self.mean_ed = gmdh.make_mat(self.ui.lineEdit.Text())
            self.liv = gmdh.make_mat(self.ui.lineEdit.Text())
            self.exp_ed = gmdh.make_mat(self.ui.lineEdit.Text())
            self.gni = gmdh.make_mat(self.ui.lineEdit.Text())
        for i in range(len(self.hdi)):
            Data['HDI'].append(str(round(float(self.hdi[i]),3)))
            Data['GNI'].append(str(round(float(self.gni[i]),3)))
            Data['MYS'].append(str(round(float(self.mean_ed[i]),3)))
            Data['LEB'].append(str(round(float(self.liv[i]),3)))
            Data['EYS'].append(str(round(float(self.exp_ed[i]),3)))
        m = 0


        Header = []
        for key in Data:
            n = 0
            Header.append(key)
            for item in Data[key]:
                newitem = QTableWidgetItem(item)
                self.ui.tableWidget.setItem(n,m,newitem)
                n+= 1
            m+=1

        self.ui.tableWidget.setHorizontalHeaderLabels(Header)
        self.MovAv_3 = gmdh.Movav(self.hdi,3)
        self.Main_Matrix = np.concatenate((self.gni,self.liv,self.exp_ed,self.mean_ed),axis = 1)
    #  Deleting 1st meaning in hdi and last row in Matrix for making forecast for 1 year

        k = int(self.Main_Matrix.shape[0])-1
        self.for_proof = self.Main_Matrix[k,:]
        self.Main_Matrix = np.delete(self.Main_Matrix,k,0)
        self.Reg_hdi = np.delete(self.hdi,[0,1,2],0)
        self.hdi = np.delete(self.hdi,0,0)
    #Deleting fisrt two years from matrix to concatinate with movav(3)
        self.Reg_Main_matrix = np.delete(self.Main_Matrix,[0,1],0)
        k = int(self.MovAv_3.size) - 1
        self.last_movav= self.MovAv_3[k]
        self.MovAv_3 = np.delete(self.MovAv_3,k)
        self.MovAv_3 = np.transpose(self.MovAv_3)
        self.Reg_Main_matrix = np.concatenate((self.Reg_Main_matrix,self.MovAv_3),axis = 1)


    def file_dialog1(self):
        self.ui.lineEdit.setText(QFileDialog.getOpenFileName(self, QString(''), QString(dir), QString('*.txt')))

    def file_dialog2(self):
        self.ui.lineEdit_2.setText(QFileDialog.getOpenFileName(self, QString(''), QString(dir), QString('*.txt')))

    def file_dialog3(self):
        self.ui.lineEdit_3.setText(QFileDialog.getOpenFileName(self, QString(''), QString(dir), QString('*.txt')))

    def file_dialog4(self):
        self.ui.lineEdit_4.setText(QFileDialog.getOpenFileName(self, QString(''), QString(dir), QString('*.txt')))

    def file_dialog5(self):
        self.ui.lineEdit_5.setText(QFileDialog.getOpenFileName(self, QString(''), QString(dir), QString('*.txt')))




# -----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('Forecast analysis')

    # create widget
    w = MainWindow()
    w.setWindowTitle('Forecast analysis')

    w.show()


    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())

