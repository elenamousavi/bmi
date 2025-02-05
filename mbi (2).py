
from PyQt6 import QtCore, QtGui, QtWidgets
from pprint import pprint
import os
import sqlite3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(705, 507)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.weight = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.weight.setGeometry(QtCore.QRect(290, 220, 201, 41))
        self.weight.setText("")
        self.weight.setObjectName("weight")
        self.setWeightValidator(self.weight)

        self.height = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.height.setGeometry(QtCore.QRect(290, 280, 201, 41))
        self.height.setText("")
        self.height.setObjectName("height")
        self.setHeightValidator(self.height)

        self.Name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(290, 100, 201, 41))
        self.Name.setText("")
        self.Name.setObjectName("Name")
        self.setNameValidator(self.Name)

        self.output = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.output.setGeometry(QtCore.QRect(290, 340, 201, 111))
        self.output.setAccessibleName("")
        self.output.setStyleSheet("")
        self.output.setObjectName("output")

        self.Run = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(70, 110, 121, 51))
        self.Run.setObjectName("Run")

        self.age = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.age.setGeometry(QtCore.QRect(290, 160, 201, 41))
        self.age.setInputMask("")
        self.age.setText("")
        self.age.setObjectName("age")
        self.setAgeValidator(self.age)

        self.Guidance = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.Guidance.setEnabled(True)
        self.Guidance.setGeometry(QtCore.QRect(290, 10, 201, 71))
        self.Guidance.setAccessibleDescription("")
        self.Guidance.setDocumentTitle("")
        self.Guidance.setReadOnly(False)
        self.Guidance.setObjectName("Guidance")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 705, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Run.clicked.connect(self.foo)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.weight.setAccessibleName(_translate("MainWindow", "weight"))
        self.Run.setText(_translate("MainWindow", "run"))
        self.Guidance.setAccessibleName(_translate("MainWindow", "Guidance"))
        self.Guidance.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">name </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">age (e.g.: 18)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">weight (e.g.: 50)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">height (e.g.: 1.60)</p></body></html>"))


    def foo(self):
        Name = self.Name.text()
        age = self.age.text()
        weight = self.weight.text()
        height = self.height.text()

        try:
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
            try:
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
                    pprint(result_2)
                else:
                    print("Failed.")
            except sqlite3.Error as e:
                self.output.setText(f"Database error: {e}")
            finally:
                conn.close()
        except ValueError:
            self.output.setText("Enter valid numbers!")
            os.chdir('BMIproj') 
        with open('bmi_data.txt','a') as file : 
            file.write(f'ID: {id}, Name : {Name}, Age : {age}, Height : {height}, Weight : {weight}, BMI : {bmi:.2f}\n') 
    def setNameValidator(self, line_edit):
        regex = QtCore.QRegularExpression("^[A-Za-z]+$")
        validator = QtGui.QRegularExpressionValidator(regex)
        line_edit.setValidator(validator)

    def setAgeValidator(self, line_edit):
        regex = QtCore.QRegularExpression("^[0-9]+$")
        validator = QtGui.QRegularExpressionValidator(regex)
        line_edit.setValidator(validator)

    def setWeightValidator(self, line_edit):
        regex = QtCore.QRegularExpression("^[0-9]+(\.[0-9]+)?$")
        validator = QtGui.QRegularExpressionValidator(regex)
        line_edit.setValidator(validator)

    def setHeightValidator(self, line_edit):
        regex = QtCore.QRegularExpression("^[0-9]+(\.[0-9]+)?$")
        validator = QtGui.QRegularExpressionValidator(regex)
        line_edit.setValidator(validator)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
