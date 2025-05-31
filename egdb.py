# -*- coding: utf-8 -*-
import psycopg2
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class ConnectionError(Exception):
    pass


class UseDatebase:
    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> "cursor":
        try:
            self.conn = psycopg2.connect(**self.configuration)
            self.curs = self.conn.cursor()
            return self.curs
        except:
            self.formMassWin = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "База даних",
                                                     "База даних не підключена."
                                                     "\nНеобхідно перевірити параметри підключення бази даних")
            btnOK = QtWidgets.QPushButton("&OK")
            btnOK.setIcon(QtGui.QIcon("./icons/16x16/dialog-ok-apply.png"))
            self.formMassWin.addButton(btnOK, QtWidgets.QMessageBox.AcceptRole)
            result = self.formMassWin.exec()
            if result == 0:
                self.formMassWin.close()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.curs.close()
        self.conn.close()
