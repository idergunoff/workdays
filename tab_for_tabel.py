from tab_for_tabel_dial import *

import sys

import pickle

import pandas as pd

from networkdays import networkdays

import datetime as dt
import calendar

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

today = dt.datetime.today()
ui.dateEdit_from.setDate(today.replace(day=1))
ui.dateEdit_to.setDate(dt.datetime.today().replace(day=calendar.monthrange(today.year, today.month)[1]))
ui.dateEdit_holidays.setDate(today)
with open('holidays.day', "rb") as f:
    holidays = list(pickle.load(f))
    for holiday in holidays:
        ui.listWidget_holidays.addItem(holiday)
columns = ['idCard', 'ddate', 'IdAnalit01', 'ttimebegin', 'ttimeend', 'nextday']


temp_tab = pd.read_table('template.csv', header=0, sep=';')
print(temp_tab)



def list_holidays(list_hd):
    date_list_hd = []
    for d in list_hd:
        d_hd = dt.datetime.strptime(d, '%Y-%m-%d')
        date_list_hd.append(dt.date(d_hd.year, d_hd.month, d_hd.day))
    return date_list_hd


def add_holiday():
    global holidays
    holidays = []
    for i in range(ui.listWidget_holidays.count()):
        holidays.append(ui.listWidget_holidays.item(i).text())
    if ui.dateEdit_holidays.text() in holidays:
        ui.label_info.setText('Праздник ' + ui.dateEdit_holidays.text() + ' уже существует')
        ui.label_info.setStyleSheet('color:red')
    else:
        ui.listWidget_holidays.addItem(ui.dateEdit_holidays.text())
        ui.label_info.setText('Праздник ' + ui.dateEdit_holidays.text() + ' добавлен')
        ui.label_info.setStyleSheet('color:green')
        holidays.append(ui.dateEdit_holidays.text())
    ui.listWidget_holidays.sortItems()
    holidays.sort()
    with open('holidays.day', "wb") as f:
        pickle.dump(holidays, f)


def remove_holiday():
    global holidays
    remove_date = ui.listWidget_holidays.item(ui.listWidget_holidays.currentRow()).text()
    ui.listWidget_holidays.takeItem(ui.listWidget_holidays.currentRow())
    ui.label_info.setText('Праздник ' + remove_date + ' удален')
    ui.label_info.setStyleSheet('color:green')
    holidays = []
    for i in range(ui.listWidget_holidays.count()):
        holidays.append(ui.listWidget_holidays.item(i).text())
    with open('holidays.day', "wb") as f:
        pickle.dump(holidays, f)


def workdays():
    list_workdays = []
    result_tab = pd.DataFrame(columns=columns)
    d_from = ui.dateEdit_from.date()
    d_to = ui.dateEdit_to.date()
    days = networkdays.Networkdays(
        dt.date(d_from.year(), d_from.month(), d_from.day()),  # start date
        dt.date(d_to.year(), d_to.month(), d_to.day()),  # end date
        list_holidays(holidays)  # list of Holidays
    )
    for d in days.networkdays():
        list_workdays.append(d.strftime('%d.%m.%Y'))
    for id_C in range(len(temp_tab['idCard'])):
        result_id = pd.DataFrame(columns=columns)
        result_id['ddate'] = list_workdays
        result_id['idCard'] = temp_tab['idCard'][id_C]
        result_id['IdAnalit01'] = temp_tab['IdAnalit01'][id_C]
        result_id['ttimebegin'] = temp_tab['ttimebegin'][id_C]
        result_id['ttimeend'] = temp_tab['ttimeend'][id_C]
        result_id['nextday'] = temp_tab['nextday'][id_C]
        result_tab = result_tab.append(result_id, ignore_index=True)
    print(result_tab)
    result_tab.to_csv('result.csv', sep=';', index=None)
    ui.label_info.setText('Результат сохранён в файл "result.csv"')
    ui.label_info.setStyleSheet('color:green')


ui.pushButton_add_holiday.clicked.connect(add_holiday)
ui.pushButton_remove_holiday.clicked.connect(remove_holiday)
ui.pushButton_workday.clicked.connect(workdays)
sys.exit(app.exec_())