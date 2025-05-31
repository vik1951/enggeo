# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtSql
from PyQt5 import QtWidgets
from egdb import *
import datetime
import decimal as dc

dbconfig = {"host": "127.0.0.1", "user": "vik", "password": "123", "dbname": "enggeo"}
global idActivObekt
idActivObekt = 0
namerazdel = ""

class ImageDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        img = index.model().data(index, QtCore.Qt.DecorationRole)
        if img is None:
            super().paint(painter, option, index)
            return
        rect = option.rect
        w, h = rect.size().width(), rect.size().height()
        img = img.scaled(w, h, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        painter.drawPixmap(rect, img)
        item_option = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(item_option, index)
        # Обработка при выделении ячейки делегата
        # Рисуем выделение полупрозрачным чтобы было видно нарисованное ранее
        if item_option.state & QtWidgets.QStyle.State_Selected:
            color = item_option.palette.color(QtGui.QPalette.Highlight)
            color.setAlpha(180)
            painter.save()
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(color)
            painter.drawRect(rect)
            painter.restore()
        # Если хотим что-то дорисовать (например текст)
        # super().paint(painter, option, index)


class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = str(self.editor.text())
        model.setData(index, value, QtCore.Qt.EditRole)


class TextEditDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QTextEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = str(self.editor.text())
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateTipBur(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["Шпіндельний", "Роторний", "З рухомим обертачем", "Без обертача"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateSposobBur(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "Ударно-канатний", "Колонковий", "Шнековий", "Вібраційний", "Ручний", "Комбінований"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateTypePoint(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "Свердловина", "Дудка", "Шурф", "Канава", "Розчистка", "Пункт відбору води"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateLabman(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                fio
                            FROM public.ispol 
                            WHERE ispol.vidrab = 0 OR ispol.vidrab = 7
                            ORDER BY ispol.fio ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateBurman(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                fio
                            FROM public.ispol 
                            WHERE ispol.vidrab = 2
                            ORDER BY ispol.fio ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        editor.insertItem(0, "")
        editor.setItemData(0, None, role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class DateDelegate(QtSql.QSqlRelationalDelegate):
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        strDate = index.data()
        dd = datetime.date(int(strDate.split('-')[0]),
                           int(strDate.split('-')[1]),
                           int(strDate.split('-')[2]))
        #dd = QtCore.QDate.currentDate()
        editor.setDisplayFormat('yyyy-MM-dd')
        editor.setDate(dd)
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor, index):
        data = index.data()
        editor.setDate(QtCore.QDate.fromString(data))

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.date().toString('yyyy-MM-dd')
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateSyskoord(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                sys,
                                region
                            FROM public.syskoord 
                            ORDER BY syskoord.id ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        editor.insertItem(0, "")
        editor.setItemData(0, None, role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateGeoman(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                fio
                            FROM public.ispol 
                            WHERE ispol.vidrab = 3
                            ORDER BY ispol.fio ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        editor.insertItem(0, "")
        editor.setItemData(0, None, role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateGdzman(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                fio
                            FROM public.ispol 
                            WHERE ispol.vidrab = 4
                            ORDER BY ispol.fio ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        editor.insertItem(0, "")
        editor.setItemData(0, None, role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateNumBurehole(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT burehole.id, 
                                burehole.num_hole 
                            FROM public.obekt,
                                public.burehole 
                            WHERE obekt.id = burehole.id_obekt 
                            AND obekt.id = %(v)s
                            AND burehole.vidhole = 'Свердловина' 
                            ORDER BY burehole.num_hole ASC""", {'v': idActivObekt})
            recAll = curs.fetchall()
            self.listNumBurehole = recAll   # Список скважин активного объекта
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        editor.insertItem(0, "")
        editor.setItemData(0, None, role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateTipbur(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id,
                                bur_name
                            FROM public.tipbur 
                            ORDER BY tipbur.bur_name ASC""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateTypeSZond(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT tipzonds.id, 
                                tipzonds.tip,
                                tipzonds.name
                            FROM public.tipzonds""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1] + " " + recOne[2])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole + 1)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegatePriborUsadka(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, 
                        name_pribor 
                        FROM pribor 
                        WHERE isput = 'Усадка'""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaUsadka(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, metod, shema 
                            FROM harakter 
                            WHERE metod = 'При вiльнiй трьохосьовiй деформацiї'
                            ORDER BY shema""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[2])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegatePriborNabuhV(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, 
                        name_pribor 
                        FROM pribor 
                        WHERE isput = 'Вільне набухання'""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaNabuh(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, metod, shema 
                            FROM harakter 
                            WHERE metod = 'Компресiйний стиск при набуханні'
                            ORDER BY shema""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[2])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegatePriborCompres(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, 
                        name_pribor 
                        FROM pribor 
                        WHERE isput = 'Компресійний стиск'""")
            recAll = curs.fetchall()
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[1])
            editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegatePriborSrez(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, 
                        name_pribor 
                        FROM pribor 
                        WHERE isput = 'Одноплощинний зріз'""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaCompres(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, metod, shema 
                            FROM harakter 
                            WHERE name_har = 'Модуль деформації'
                            ORDER BY shema""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[2])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaProsad(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, name_har, shema 
                            FROM harakter 
                            WHERE name_har = 'Вiдносне просiдання'
                            ORDER BY id""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[2])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaSrez(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT id, metod, shema 
                            FROM harakter 
                            WHERE metod = 'Одноплощинний зріз'
                            ORDER BY shema""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[2])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateShemaFiz(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT min(id) AS id, name_har 
                            FROM harakter 
                            WHERE id_groupsv > 0 AND id_groupsv < 11
                            GROUP BY name_har
                            ORDER BY id""")
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateLabnumVoda(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT obrazec.id, 
                                obrazec.lab_num
                            FROM obekt,
                                burehole,
                                obrazec
                            WHERE obekt.id = %(v)s 
                                AND obekt.id = burehole.id_obekt 
                                AND burehole.id = obrazec.id_burehole
                                AND obrazec.mater_obr = 'Вода'
                            ORDER BY obrazec.lab_num""", {'v': idActivObekt})
            recAll = list(curs.fetchall())
            recAll.append([0, '-'])
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateLabnumGrunt(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT obrazec.id, 
                                obrazec.lab_num
                            FROM obekt,
                                burehole,
                                obrazec
                            WHERE obekt.id = %(v)s 
                                AND obekt.id = burehole.id_obekt 
                                AND burehole.id = obrazec.id_burehole
                                AND obrazec.mater_obr != 'Вода'
                                AND obrazec.lab_num != ''
                            ORDER BY obrazec.lab_num""", {'v': idActivObekt})
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateLabnumSkala(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT obrazec.id, 
                                obrazec.lab_num
                            FROM obekt,
                                burehole,
                                obrazec
                            WHERE obekt.id = %(v)s 
                                AND obekt.id = burehole.id_obekt 
                                AND burehole.id = obrazec.id_burehole
                                AND obrazec.mater_obr = 'Скельний ґрунт'
                            ORDER BY obrazec.lab_num""", {'v': idActivObekt})
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateLabnumGran(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        with UseDatebase(dbconfig) as curs:
            curs.execute("""SELECT obrazec.id, 
                                obrazec.lab_num
                            FROM obekt,
                                burehole,
                                obrazec
                            WHERE obekt.id = %(v)s 
                                AND obekt.id = burehole.id_obekt 
                                AND burehole.id = obrazec.id_burehole
                                AND obrazec.mater_obr != 'Вода'
                            ORDER BY obrazec.lab_num""", {'v': idActivObekt})
            recAll = curs.fetchall()
            for i in range(0, len(recAll)):
                recOne = recAll[i]
                editor.addItem(recOne[1])
                editor.setItemData(i, recOne[0], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateMetodRaschCompres(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        recAll = [("Відносний стиск", 1), ("Кф пористості", 2)]
        editor = QtWidgets.QComboBox(parent)
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[0])
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateGroupPesok(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        recAll = [("Скорочений", 1), ("Повний", 2)]
        editor = QtWidgets.QComboBox(parent)
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[0])
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateMetodGran(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        recAll = [("Ситовий", 1), ("Ареометричний", 2), ("Піпеточний", 3)]
        editor = QtWidgets.QComboBox(parent)
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[0])
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateMetodVoda(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        recAll = [("Скорочений", 1), ("Стандартний", 2), ("Повний", 3)]
        editor = QtWidgets.QComboBox(parent)
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[0])
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateZonaVlag(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        recAll = [("Суха", 1), ("Нормальна", 2), ("Волога", 3)]
        editor = QtWidgets.QComboBox(parent)
        for i in range(0, len(recAll)):
            recOne = recAll[i]
            editor.addItem(recOne[0])
            editor.setItemData(i, recOne[1], role=QtCore.Qt.UserRole)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value1 = editor.itemData(editor.currentIndex(), QtCore.Qt.EditRole)
        value2 = editor.itemData(editor.currentIndex(), QtCore.Qt.UserRole)
        model.setData(index, value1, QtCore.Qt.EditRole)
        model.setData(index, value2, QtCore.Qt.UserRole)


class ComboBoxDelegateGroupRab(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["Польові роботи", "Лабораторні роботи", "Камеральні роботи", "Супутні витрати"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateUslovRab(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        if namerazdel == "Польові роботи":
            editor.addItems(["Акваторія", "Суходіл"])
        else:
            editor.addItems(["Експедиція", "Стаціонар"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateGrunt(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["Скельний ґрунт", "Напівскельний ґрунт", "Звʼязний ґрунт", "Незвʼязний ґрунт", "Вода"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateGruntname(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["Мул", "Глина", "Суглинок", "Супісок", "Пісок"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateObrazec(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["Банка", "Моноліт", "Мішок", "Зразок", "Пляшка"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateCvet(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "світло-сірий", "сірий", "темно-сірий",
                         "зеленувато-сірий", "блакитнувато-сірий", "жовтувато-сірий",
                         "бурувато-сірий", "бурувато-жовтий", "жовтий", "сірувато-жовтий",
                         "сірувато-бурий", "червонувато-бурий", "червоно-бурий",
                         "палевий", "палево-жовтий", "палево-сірий"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateTextura(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "тонкошарувата", "косошарувата", "шарувата", "грудкувата", "порфірова", "однорідна"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateProsloi(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "мулу", "черепашок", "піску", "супіску", "суглинку", "глини"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateVkluch(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "гальки", "гравію", "гальки та гравію",
                         "щебеню", "жорстви", "щебеню та жорстви",
                         "черепашок", "детриту черепашок"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class ComboBoxDelegateNovo(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(["-", "карбонатні конкреції та стягнення - білозірка", "карбонатні дутики або журавчики",
                         "карбонатний псевдоміцелій", "залізисто-марганцеві конкреції",
                         "залізисто-марганцеві бобовини",
                         "кристалічні агрегати гипсу", "гипсові стягнення",
                         "вохристи плівки та примазки сполук заліза",
                         "бобовини і конкреції заліза", "кірочки колоїдних сполук заліза", "глейові затьоки",
                         "білі кірки та примазки", "гумусові примазки"])
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, QtCore.Qt.EditRole))
        editor.setCurrentText(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)


class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setMinimum(0)
        editor.setMaximum(99)
        editor.setSingleStep(1)
        editor.setAlignment(QtCore.Qt.AlignCenter)
        return editor

    def setEditorData(self, editor, index):
        value = int(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class SpinBoxDelegate_Diametr(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setMinimum(0)
        editor.setMaximum(1000)
        editor.setSingleStep(1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = int(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class SpinBoxDelegate_Bal(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setMinimum(-1)
        editor.setMaximum(5)
        editor.setSingleStep(1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = int(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class SpinBoxDelegate_Gradus(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setMinimum(-1)
        editor.setMaximum(100)
        editor.setSingleStep(1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = int(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_Temper(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-99.9)
        editor.setMaximum(99.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate10(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(0.00)
        editor.setMaximum(9999999.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_Absotm(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(-10000.00)
        editor.setMaximum(9999.99)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-"  \
                or index.model().data(index, QtCore.Qt.EditRole) is None:
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(-0.01)
        editor.setMaximum(999.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == 'None' \
                or index.model().data(index, QtCore.Qt.EditRole) == '-':
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_31(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(0.0)
        editor.setMaximum(9.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None"\
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate4(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(4)
        editor.setMinimum(-0.0001)
        editor.setMaximum(9.9999)
        editor.setSingleStep(0.0001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate71(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(0.0)
        editor.setMaximum(99999.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_pH(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-0.1)
        editor.setMaximum(14.0)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None"\
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_71(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-0.1)
        editor.setMaximum(99999.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-"  \
                or index.model().data(index, QtCore.Qt.EditRole) is None:
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate62(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(0.00)
        editor.setMaximum(999.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = 0
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate53(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(3)
        editor.setMinimum(0.000)
        editor.setMaximum(9.999)
        editor.setSingleStep(0.001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = 0
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate5_3(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(3)
        editor.setMinimum(-1.000)
        editor.setMaximum(9.999)
        editor.setSingleStep(0.001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = 0
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate3(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(3)
        editor.setMinimum(0.000)
        editor.setMaximum(999.999)
        editor.setSingleStep(0.001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_5_1(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(0.0)
        editor.setMaximum(999.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" or \
                index.model().data(index, QtCore.Qt.EditRole) is None or \
                index.model().data(index, QtCore.Qt.EditRole) == '-':
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate1(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(0.0)
        editor.setMaximum(100.0)
        editor.setSingleStep(0.1)
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" or \
                index.model().data(index, QtCore.Qt.EditRole) is None or \
                index.model().data(index, QtCore.Qt.EditRole) == '-':
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate1_(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-0.1)
        editor.setMaximum(100.0)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate2(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(0.00)
        editor.setMaximum(9.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None" \
                or index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = "-"
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_41(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-0.1)
        editor.setMaximum(99.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_42(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(-0.01)
        editor.setMaximum(9.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_51(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(1)
        editor.setMinimum(-0.1)
        editor.setMaximum(999.9)
        editor.setSingleStep(0.1)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_52(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(-0.01)
        editor.setMaximum(99.99)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_53(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(3)
        editor.setMinimum(-0.001)
        editor.setMaximum(9.999)
        editor.setSingleStep(0.001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_62(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(2)
        editor.setMinimum(-0.01)
        editor.setMaximum(100.00)
        editor.setSingleStep(0.01)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == 'None':
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_84(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(4)
        editor.setMinimum(-0.0001)
        editor.setMaximum(999.0000)
        editor.setSingleStep(0.0001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) is None:
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)


class DoubleSpinBoxDelegate_64(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, options, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setLocale(QtCore.QLocale(QtCore.QLocale.C, QtCore.QLocale.AnyCountry))
        editor.setDecimals(4)
        editor.setMinimum(-0.0001)
        editor.setMaximum(1.0000)
        editor.setSingleStep(0.0001)
        editor.setSpecialValueText('-')
        editor.setAlignment(QtCore.Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        if index.model().data(index, QtCore.Qt.EditRole) == "None":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) == "-":
            value = editor.minimum()
        elif index.model().data(index, QtCore.Qt.EditRole) is None:
            value = editor.minimum()
        else:
            value = float(index.model().data(index, QtCore.Qt.EditRole))
        editor.setValue(value)

    def updateEditorGeometry(self, editor, options, index):
        editor.setGeometry(options.rect)

    def setModelData(self, editor, model, index):
        if editor.value() == editor.minimum():
            value = '-'
        else:
            value = str(editor.value())
        model.setData(index, value, QtCore.Qt.EditRole)
