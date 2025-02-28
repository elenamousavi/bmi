# Form implementation generated from reading ui file 'meow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import pprint
import os
import sqlite3
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(705, 507)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.weight = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.weight.setGeometry(QtCore.QRect(290, 180, 201, 41))
        self.weight.setText("")
        self.weight.setObjectName("weight")
        self.height = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.height.setGeometry(QtCore.QRect(290, 240, 201, 41))
        self.height.setText("")
        self.height.setObjectName("height")
        self.Name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(290, 60, 201, 41))
        self.Name.setText("")
        self.Name.setObjectName("Name")
        self.output = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.output.setGeometry(QtCore.QRect(290, 300, 201, 71))
        self.output.setAccessibleName("")
        self.output.setStyleSheet("")
        self.output.setObjectName("output")
        self.Run = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(70, 160, 121, 51))
        self.Run.setObjectName("Run")
        self.age = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.age.setGeometry(QtCore.QRect(290, 120, 201, 41))
        self.age.setInputMask("")
        self.age.setText("")
        self.age.setObjectName("age")
        self.label_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(238, 70, 41, 21))
        self.label_name.setLineWidth(-3)
        self.label_name.setObjectName("label_name")
        self.label_age = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_age.setGeometry(QtCore.QRect(250, 130, 41, 21))
        self.label_age.setLineWidth(-3)
        self.label_age.setObjectName("label_age")
        self.label_weight = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_weight.setGeometry(QtCore.QRect(220, 190, 121, 21))
        self.label_weight.setLineWidth(-3)
        self.label_weight.setObjectName("label_weight")
        self.label_height = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_height.setGeometry(QtCore.QRect(220, 250, 91, 21))
        self.label_height.setLineWidth(-3)
        self.label_height.setObjectName("label_height")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 705, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Run.clicked.connect(self.foo) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.weight.setAccessibleName(_translate("MainWindow", "weight"))
        self.Run.setText(_translate("MainWindow", "Submit"))
        self.label_name.setText(_translate("MainWindow", "Name"))
        self.label_age.setText(_translate("MainWindow", "age"))
        self.label_weight.setText(_translate("MainWindow", "weight (kg)"))
        self.label_height.setText(_translate("MainWindow", "height (m)"))
    def foo(self):
        Name = self.Name.text()
        age = self.age.text()
        weight = self.weight.text()
        height = self.height.text()

        if not re.match("^[a-zA-Z ]+$", Name):
                self.Name.setText("Please enter character!")
                return
        elif not re.match("^\d+$", age):
                self.age.setText("Please enter number!")
                return
        elif not re.match("^\d+(\.\d+)?$", height):
                self.height.setText("Please enter number!")
                return
        elif not re.match("^\d+(\.\d+)?$", weight):
                self.weight.setText("Please enter number!")
                return

        weight = float(weight)
        height = float(height)
        age = int(age)
        result = pow(height, 2)
        bmi = weight / result

        if bmi < 18.5:
            self.output.setText(f"Result {Name}, {age} years old: {bmi:.2f}. You are underweight.")
        elif 18.5 <= bmi < 25:
            self.output.setText(f"Result {Name}, {age} years old: {bmi:.2f}. You are normal.")
        elif 25 <= bmi < 30:
            self.output.setText(f"Result {Name}, {age} years old: {bmi:.2f}. You are overweight.")
        elif bmi >= 30:
            self.output.setText(f"Result {Name}, {age} years old: {bmi:.2f}. You are obese.")
            
            # Save to database
        conn = sqlite3.connect("bmi_database.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                age INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL
            )
            ''')
        conn.commit()

        cursor.execute('''
                INSERT INTO data (Name, age, weight, height, bmi)
                VALUES (?, ?, ?, ?, ?)
                ''', (Name, age, weight, height, bmi))
        conn.commit()

        cursor.execute('SELECT * FROM data WHERE Name = ? AND age = ? AND weight = ? AND height = ? AND bmi = ?',
                               (Name, age, weight, height, bmi))

        result_2 = cursor.fetchone()
        if result_2:
                print("Information saved successfully.")
        else:
                print("Failed.")

        with open('bmi_data.txt','a') as file : 
            file.write(f'Name : {Name}, Age : {age}, Height : {height}, Weight : {weight}, BMI : {bmi:.2f}\n') 
            conn.close()
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
