# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from egdb import *
import math
import decimal as dc
import numpy as np
dbconfig = {"host": "127.0.0.1", "user": "vik", "password": "123", "dbname": "enggeo"}


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    print('Error: ', text)
    QtWidgets.QMessageBox.critical(None, 'Error', text)
    quit()


def formatcoma(nstr) -> dc.Decimal:
    """Форматирует строку числа с запятой в число с десятичной точкой"""
    i = 0
    for i in range(0, len(nstr)):
        if nstr[i] == ",":
            break
    if (i + 1) < len(nstr):
        str1 = nstr[:i]
        str2 = nstr[i + 1:]
        str = str1 + "." + str2
        n = dc.Decimal(str)
    else:
        n = dc.Decimal(nstr)
    return n


def b1zond(qs:float, flag:int=1, grunt:int=1) -> float:
    """Определение Кф b1 по результатам статического зондирования в зависимости от типа свай
    qs - среднее значение лобового сопротивления грунта под конусом зонда (kПа)
    полученное из значений на участке от одного диаметра (d) выше и четырех диаметров ниже отметок
    острия проектируемой сваи. d - диаметр круглой сваи или большая сторона прямоугольной сваи (м)
    flag = 1 - для забивных свай
    flag = 2 - для винтовых свай при нагрузке на вдавливание
    flag = 3 - для винтовых свай при нагрузке на выдергивание
    grunt = 2 - песчаный водонасыщенный"""
    b1 = 0.0
    if flag == 1:
        if qs < 1000.0:
            b1 = 0.90
        elif qs < 2500.0:
            b1 = 0.90 - 0.1 / 1500.0 * (qs - 1000.0)
        elif qs < 5000.0:
            b1 = 0.80 - 0.15 / 2500.0 * (qs - 2500.0)
        elif qs < 7500.0:
            b1 = 0.65 - 0.1 / 2500.0 * (qs - 5000.0)
        elif qs < 10000.0:
            b1 = 0.55 - 0.1 / 2500.0 * (qs - 7500.0)
        elif qs < 15000.0:
            b1 = 0.45 - 0.1 / 5000.0 * (qs - 10000.0)
        elif qs < 20000.0:
            b1 = 0.35 - 0.05 / 5000.0 * (qs - 15000.0)
        elif qs < 30000.0:
            b1 = 0.30 - 0.1 / 10000.0 * (qs - 20000.0)
        else:
            b1 = 0.20
    elif flag == 2:
        if qs < 1000.0:
            b1 = 0.50
        elif qs < 2500.0:
            b1 = 0.50 - 0.05 / 1500.0 * (qs - 1000.0)
        elif qs < 5000.0:
            b1 = 0.45 - 0.13 / 2500.0 * (qs - 2500.0)
        elif qs < 7500.0:
            b1 = 0.32 - 0.06 / 2500.0 * (qs - 5000.0)
        elif qs < 10000.0:
            b1 = 0.26 - 0.03 / 2500.0 * (qs - 7500.0)
        else:
            b1 = 0.23
        if grunt == 2 and b1 is not None:
            b1 = b1 / 2
    elif flag == 3:
        if qs < 1000.0:
            b1 = 0.40
        elif qs < 2500.0:
            b1 = 0.40 - 0.02 / 1500.0 * (qs - 1000.0)
        elif qs < 5000.0:
            b1 = 0.38 - 0.09 / 2500.0 * (qs - 2500.0)
        elif qs < 7500.0:
            b1 = 0.27 - 0.05 / 2500.0 * (qs - 5000.0)
        elif qs < 10000.0:
            b1 = 0.22 - 0.03 / 2500.0 * (qs - 7500.0)
        else:
            b1 = 0.19
        if grunt == 2 and b1 is not None:
            b1 = b1 / 2
    else:
        pass
    return b1


def b2zond(fs:float, grunt:int=1) -> float:
    """Определение Кф b2 по результатам статического зондирования в зависимости от типа грунта
    fs - среднее значение сопротивления грунта на боковой поверхности зонда, кПа (тс/м2),
    определяемое как частное от деления измеренного общего сопротивления грунта на боковой поверхности зонда
    на площади его боковой поверхности в пределах от поверхности грунта в точке зондирования
    до уровня расположения нижнего конца сваи в выбранном несущем слое
    grunt = 2 - песчаный
    grunt = 1 - глинистый"""
    if grunt == 2:
        if fs < 20:
            b2 = 2.40
        elif fs < 40:
            b2 = 2.40 - 0.75 / 20 * (fs - 20)
        elif fs < 60:
            b2 = 1.65 - 0.45 / 20 * (fs - 40)
        elif fs < 80:
            b2 = 1.20 - 0.20 / 20 * (fs - 60)
        elif fs < 100:
            b2 = 1.00 - 0.15 / 20 * (fs - 80)
        elif fs < 120:
            b2 = 0.85 - 0.10 / 20 * (fs - 100)
        else:
            b2 = 0.75
    elif grunt == 1:
        if fs < 20:
            b2 = 1.50
        elif fs < 40:
            b2 = 1.50 - 0.50 / 20 * (fs - 20)
        elif fs < 60:
            b2 = 1.00 - 0.25 / 20 * (fs - 40)
        elif fs < 80:
            b2 = 0.75 - 0.15 / 20 * (fs - 60)
        elif fs < 100:
            b2 = 0.60 - 0.10 / 20 * (fs - 80)
        elif fs < 120:
            b2 = 0.50 - 0.10 / 20 * (fs - 100)
        else:
            b2 = 0.40
    else:
        b2 = None
    return b2


def bizond(fsi:float, grunt:int=1) -> float:
    """Определение Кф bi по результатам статического зондирования в зависимости от типа грунта
    fsi - среднее сопротивление i-го слоя грунта на боковой поверхности зонда, кПа (тс/м2 )
    grunt = 2 - песчаный
    grunt = 1 - глинистый"""
    if grunt == 2:
        if fsi < 20:
            bi = 0.75
        elif fsi < 40:
            bi = 0.75 - 0.15 / 20 * (fsi - 20)
        elif fsi < 60:
            bi = 0.60 - 0.05 / 20 * (fsi - 40)
        elif fsi < 80:
            bi = 0.55 - 0.05 / 20 * (fsi - 60)
        elif fsi < 100:
            bi = 0.50 - 0.05 / 20 * (fsi - 80)
        elif fsi < 120:
            bi = 0.45 - 0.05 / 20 * (fsi - 100)
        else:
            bi = 0.40
    elif grunt == 1:
        if fsi < 20:
            bi = 1.00
        elif fsi < 40:
            bi = 1.00 - 0.25 / 20 * (fsi - 20)
        elif fsi < 60:
            bi = 0.75 - 0.15 / 20 * (fsi - 40)
        elif fsi < 80:
            bi = 0.60 - 0.15 / 20 * (fsi - 60)
        elif fsi < 100:
            bi = 0.45 - 0.05 / 20 * (fsi - 80)
        elif fsi < 120:
            bi = 0.40 - 0.10 / 20 * (fsi - 100)
        else:
            bi = 0.30
    else:
        bi = None
    return bi


def fs(Qs:float, plosh:float) -> float:
    """Qs - общее сопротивление грунта на боковой поверхности, кН
    plosh - площадь боковой поверхности сваи в грунте, м2"""
    val = 0.00
    return val


def favg(fs:float, fsi:float, h:float, hi:float, zond:int=2, grunt:int=1) -> float:
    """Среднее значение предельного сопротивления грунта на боковой поверхности забивной сваи  f , кПа (тс/м2),
    по данным зондирования грунта в рассматриваемой точке
    zond - тип зонда (1, 2, 3)
    grunt = 2 - песчаный
    grunt = 1 - глинистый
    fs - среднее значение сопротивления грунта на боковой поверхности зонда, кПа (тс/м2),
    определяемое как частное от деления измеренного общего сопротивления грунта на боковой поверхности зонда
    на площади его боковой поверхности в пределах от поверхности грунта в точке зондирования
    до уровня расположения нижнего конца сваи в выбранном несущем слое
    fsi - среднее сопротивление i-го слоя грунта на боковой поверхности зонда, кПа (тс/м2 )
    h - глубина погружения сваи от поверхности грунта (м)
    hi - мощность i-го слоя грунта"""
    f = 0.0
    if zond == 1:
        f = b2zond(fs, grunt) * fs
    elif zond == 2 or zond == 3:
        f = np.sum(bizond(fsi, grunt) * fsi * hi) / h
    return f


def konsszond(qc:float, fz:float) -> float:
    """Расчет консистенции грунтов по статическому зондированию
    qc - лобовое сопротивление грунта МПа
    fz - боковое сопротивление грунта кПа"""
    fzmpa = fz / 1000
    if fzmpa / qc * 100 < 0.9:
        il = None
    else:
        if qc < 1:
            il1 = -0.1470222526 * math.log(fzmpa) - 0.0798965392
            il2 = -0.1503893629 * math.log(fzmpa) - 0.2198804664
            il = (il1 - il2) / (2 - 1) * (1 - qc) + il1
        elif qc < 2:
            il1 = -0.1470222526 * math.log(fzmpa) - 0.0798965392
            il2 = -0.1503893629 * math.log(fzmpa) - 0.2198804664
            il = (il1 - il2) / (2 - 1) * (2 - qc) + il2
        elif qc < 3:
            il1 = -0.1503893629 * math.log(fzmpa) - 0.2198804664
            il2 = -0.0963000281 * math.log(fzmpa) - 0.1528648537
            il = (il1 - il2) / (3 - 2) * (3 - qc) + il2
        elif qc < 5:
            il1 = -0.0963000281 * math.log(fzmpa) - 0.1528648537
            il2 = -0.0670267822 * math.log(fzmpa) - 0.1741711823
            il = (il1 - il2) / (5 - 3) * (5 - qc) + il2
        elif qc < 8:
            il1 = -0.0670267822 * math.log(fzmpa) - 0.1741711823
            il2 = -0.051417819 * math.log(fzmpa) - 0.1885049453
            il = (il1 - il2) / (8 - 5) * (8 - qc) + il2
        elif qc < 10:
            il1 = -0.051417819 * math.log(fzmpa) - 0.1885049453
            il2 = -0.0475631202 * math.log(fzmpa) - 0.2018007813
            il = (il1 - il2) / (10 - 8) * (10 - qc) + il2
        elif qc < 12:
            il1 = -0.0475631202 * math.log(fzmpa) - 0.2018007813
            il2 = -0.0413174463 * math.log(fzmpa) - 0.2082739309
            il = (il1 - il2) / (12 - 10) * (12 - qc) + il2
        elif qc < 15:
            il1 = -0.0413174463 * math.log(fzmpa) - 0.2082739309
            il2 = -0.0364285375 * math.log(fzmpa) - 0.2254192153
            il = (il1 - il2) / (15 - 12) * (15 - qc) + il2
        elif qc < 20:
            il1 = -0.0364285375 * math.log(fzmpa) - 0.2254192153
            il2 = -0.0225425127 * math.log(fzmpa) - 0.2245957278
            il = (il1 - il2) / (20 - 15) * (20 - qc) + il2
        else:
            il1 = -0.0364285375 * math.log(fzmpa) - 0.2254192153
            il2 = -0.0225425127 * math.log(fzmpa) - 0.2245957278
            il = il2 - (il1 - il2) / (20 - 15) * (qc - 20)
        il = round(il, 2)
    return il


def stn(f200:dc.Decimal, f200_10:dc.Decimal, f10_5:dc.Decimal, f5_2:dc.Decimal, f2_1:dc.Decimal, f1_05:dc.Decimal,
        f05_025:dc.Decimal, f025_01:dc.Decimal, f01_:dc.Decimal) -> dc.Decimal:
    """Фукция возвращает степень неоднородности крупнообломочных грунтов и песков
        по результатам ситового анализа"""
    if f01_ >= 60.0:
        d60 = dc.Decimal(60.0 * 0.1) / f01_
    elif (f01_ + f025_01) >= 60.0:
        d60 = dc.Decimal(0.25 - 0.1) * (dc.Decimal(60.0) - f01_) / f025_01 + dc.Decimal(0.1)
    elif (f01_ + f025_01 + f05_025) >= 60.0:
        d60 = dc.Decimal(0.5 - 0.25) * (dc.Decimal(60.0) - f01_ - f025_01) / f05_025 + dc.Decimal(0.25)
    elif (f01_ + f025_01 + f05_025 + f1_05) >= 60.0:
        d60 = dc.Decimal(1.0 - 0.5) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025) / f1_05 + dc.Decimal(0.5)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1) >= 60.0:
        d60 = dc.Decimal(2.0 - 1.0) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025 - f1_05) / f2_1 + dc.Decimal(1.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2) >= 60.0:
        d60 = dc.Decimal(5.0 - 2.0) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1) / f5_2 + dc.Decimal(2.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5) >= 60.0:
        d60 = dc.Decimal(10.0 - 5.0) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2) / f10_5 + dc.Decimal(5.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5 + f200_10) >= 60.0:
        d60 = dc.Decimal(200.0 - 10.0) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2 - f10_5) / f200_10 + dc.Decimal(10.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5 + f200_10 + f200) >= 60.0:
        d60 = dc.Decimal(200.0 - 10.0) * (dc.Decimal(60.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2 - f10_5 - f200_10) / f200_10 + dc.Decimal(200)
    else:
        d60 = 0
    if f01_ >= 10.0:
        d10 = dc.Decimal(10.0 * 0.1) / f01_
    elif (f01_ + f025_01) >= 10.0:
        d10 = dc.Decimal(0.25 - 0.1) * (dc.Decimal(10.0) - f01_) / f025_01 + dc.Decimal(0.1)
    elif (f01_ + f025_01 + f05_025) >= 10.0:
        d10 = dc.Decimal(0.5 - 0.25) * (dc.Decimal(10.0) - f01_ - f025_01) / f05_025 + dc.Decimal(0.25)
    elif (f01_ + f025_01 + f05_025 + f1_05) >= 10.0:
        d10 = dc.Decimal(1.0 - 0.5) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025) / f1_05 + dc.Decimal(0.5)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1) >= 10.0:
        d10 = dc.Decimal(2.0 - 1.0) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025 - f1_05) / f2_1 + dc.Decimal(1.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2) >= 10.0:
        d10 = dc.Decimal(5.0 - 2.0) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1) / f5_2 + dc.Decimal(2.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5) >= 10.0:
        d10 = dc.Decimal(10.0 - 5.0) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2) / f10_5 + dc.Decimal(5.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5 + f200_10) >= 10.0:
        d10 = dc.Decimal(200.0 - 10.0) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2 - f10_5) / f200_10 + dc.Decimal(10.0)
    elif (f01_ + f025_01 + f05_025 + f1_05 + f2_1 + f5_2 + f10_5 + f200_10 + f200) >= 10.0:
        d10 = dc.Decimal(200.0 - 10.0) * (dc.Decimal(10.0) - f01_ - f025_01 - f05_025 - f1_05 - f2_1 - f5_2 - f10_5 - f200_10) / f200_10 + dc.Decimal(200)
    else:
        d10 = 1
    stn = dc.Decimal(round(d60 / d10, 1))
    return stn


def nameskala_R(r:dc.Decimal) -> str:
    """Наименование скального грунта по пределу прочности на одноосное сжатие (R)
    r - предел прочности на одноосное сжатие, МПа"""
    if r is None:
        name_r = ""
    elif r > 120:
        name_r = " дуже мiцний"
    elif r >= 50:
        name_r = " мiцний"
    elif r >= 15:
        name_r = " cередньої мiцностi"
    elif r >= 5:
        name_r = " маломiцний"
    elif r >= 3:
        name_r = " зниженої мiцностi"
    elif r >= 1:
        name_r = " низької мiцностi"
    elif r < 1:
        name_r = " дуже низької мiцностi"
    else:
        name_r = ""
    return name_r


def nameskala_pd(pd:dc.Decimal) -> str:
    """Наименование скального грунта по плотности скелета
    pd - плотность скелета, г/см3"""
    if pd is None:
        name_pd = ""
    else:
        if pd >= 2.5:
            name_pd = " дуже щільний"
        elif pd >= 2.1:
            name_pd = " щільний"
        elif pd >= 1.2:
            name_pd = " пухкий"
        elif pd > 0.0:
            name_pd = " дуже пухкий"
        else:
            name_pd = ""
    return name_pd


def nameskala_Kwr(Kwr:dc.Decimal) -> str:
    """Наименование скального грунта по коэффициенту выветрелости
    Kwr - коэффициент выветрелости д.е."""
    if Kwr is None:
        name_Kwr = ""
    else:
        if Kwr >= 1.0:
            name_Kwr = " невивітрілий"
        elif Kwr >= 0.9:
            name_Kwr = " слабовивітрілий"
        elif Kwr >= 0.8:
            name_Kwr = " вивітрілий"
        elif Kwr > 0.0:
            name_Kwr = " сильновивітрілий"
        else:
            name_Kwr = ""
    return name_Kwr


def nameskala_Ksof(Ksof:dc.Decimal) -> str:
    """Наименование скального грунта по коэффициенту размягчаемости
    Ksof - коэффициент размягчаемости, д.е."""
    if Ksof is None:
        name_Ksof = ""
    else:
        if Ksof >= 0.75:
            name_Ksof = " нерозм'якшувальний"
        elif Ksof >= 0.00:
            name_Ksof = " розм'якшувальний"
        else:
            name_Ksof = ""
    return name_Ksof


def nameskala_qsr(qsr:dc.Decimal) -> str:
    """Наименование грунта по количеству воднорастворимых солей
    qsr - количество воднорастворимых солей, г/л"""
    if qsr is None:
        name_qsr = ""
    else:
        if qsr > 100.00:
            name_qsr = " сильнорозчинний"
        elif qsr > 10.00:
            name_qsr = " легкорозчинний"
        elif qsr > 1.00:
            name_qsr = " середньорозчинний"
        elif qsr > 0.01:
            name_qsr = " важкорозчинний"
        elif qsr >= 0.00:
            name_qsr = " нерозчинний"
        else:
            name_qsr = ""
    return name_qsr


def nameskala_Kf(Kf:dc.Decimal) -> str:
    """Наименование скального грунта по коэффициенту фильтрации
    Kf - коэффициент фильтрации, м/сут."""
    if Kf is None:
        name_Kf = ""
    else:
        if Kf > 30.000:
            name_Kf = " дуже сильноводопроникний"
        elif Kf > 3.000:
            name_Kf = " сильноводопроникний"
        elif Kf > 0.300:
            name_Kf = " водопроникний"
        elif Kf >= 0.005:
            name_Kf = " слабоводопроникний"
        elif Kf >= 0.000:
            name_Kf = " неводопроникний"
        else:
            name_Kf = ""
    return name_Kf


def nameskala_Dsal(Dsal:dc.Decimal) -> str:
    """Наименование грунта по количеству воднорастворимых солей
    Dsal - количество воднорастворимых солей, %"""
    if Dsal is None:
        name_Dsal = ""
    else:
        if Dsal > 2.0:
            name_Dsal = " засолений"
        elif Dsal >= 0:
            name_Dsal = " незасолений"
        else:
            name_Dsal = ""
    return name_Dsal


def nameskala_t(t:dc.Decimal) -> str:
    """Наименование скального грунта по температуре
    t - температура, град.С"""
    if t is None:
        name_t = ""
    else:
        if t >= 0:
            name_t = " немерзлий"
        elif t < 0:
            name_t = " морозний"
        else:
            name_t = ""
    return name_t


def namestn(stn:dc.Decimal) -> str:
    """Наименование степени неоднородности"""
    name = ""
    if stn > 3.0:
        name = " неоднорідний"
    elif stn > 0:
        name = " однорідний"
    else:
        pass
    return name


def namepesok(f200:float, f200_10:float, f10_5:float, f5_2:float, f2_1:float, f1_05:float, f05_025:float,
              f025_01:float, rakusha:float, okatan:int) -> str:
    """Определение наименования крупнообломочных грунтов и песков
    по ДСТУ Б В.2.1-2-96 (ГОСТ 25100)"""
    name = ""
    if okatan == None:
        pass  # Если есть грансостав образца то определяется наименование грунта
    else:
        if rakusha > 50:
            name = "Черепашковий грунт"
        else:
            if f200 > 50.0:
                if okatan == 2:
                    name = "Валунний грунт"
                else:
                    name = "Глибистий грунт"
            elif (f200 + f200_10) > 50.0:
                if okatan == 2:
                    name = "Галечниковий грунт"
                else:
                    name = "Щебенистий грунт"
            elif (f200 + f200_10 + f10_5 + f5_2) > 50.0:
                if okatan == 2:
                    name = "Гравiйний грунт"
                else:
                    name = "Дресв'яний грунт"
            elif (f200 + f200_10 + f10_5 + f5_2) > 25.0:
                if rakusha > 25:
                    name = "Пісок гравiюватий (черепашковий)"
                else:
                    name = "Пісок гравiюватий"
            elif (f200 + f200_10 + f10_5 + f5_2 + f2_1 + f1_05) > 50.0:
                name = "Пісок крупний"
            elif (f200 + f200_10 + f10_5 + f5_2 + f2_1 + f1_05 + f05_025) > 50.0:
                name = "Пісок середньої крупностi"
            elif (f200 + f200_10 + f10_5 + f5_2 + f2_1 + f1_05 + f05_025 + f025_01) >= 75.0:
                name = "Пісок дрібний"
            elif (f200 + f200_10 + f10_5 + f5_2 + f2_1 + f1_05 + f05_025 + f025_01) < 75.0:
                name = "Пісок пилуватий"
            else:
                name = "Зв'язний ґрунт"
    return name


def nameglina(e:float, ip:float, il:float) -> str:
    """Определение наименования глинистых грунтов по ДСТУ Б В.2.1-2-96 (ГОСТ 25100)
    e - Коэффициент пористости
    ip - Пластичность
    il - Показатель текучести"""
    name = ""
    if e is None:
        e = 0
    if ip != None and il != None:
        if e >= 0.9 and il > 1:
            if ip < 1:
                name = "Незв'язний ґрунт"
            elif ip >= 1 and ip < 7:
                name = "Мул супiщаний"
            elif ip >= 7 and ip < 17:
                name = "Мул суглинистий"
            elif ip >= 17:
                name = "Мул глинистий"
        else:
            if ip < 1:
                name = "Незв'язний ґрунт"
            elif ip >= 1 and ip < 7:
                if il < 0:
                    name = "Супiсок твердий"
                elif il >= 0 and il <= 1:
                    name = "Супiсок пластичний"
                elif il > 1:
                    name = "Супiсок текучий"
            elif ip >= 7 and ip < 12:
                if il < 0:
                    name = "Суглинок легкий твердий"
                if il >= 0 and il <= 0.25:
                    name = "Суглинок легкий напiвтвердий"
                if il > 0.25 and il <= 0.50:
                    name = "Суглинок легкий тугопластичний"
                if il > 0.50 and il <= 0.75:
                    name = "Суглинок легкий м'якопластичний"
                if il > 0.75 and il <= 1.00:
                    name = "Суглинок легкий текучопластичний"
                if il > 1.00:
                    name = "Суглинок легкий текучий"
            elif ip >= 12 and ip < 17:
                if il < 0:
                    name = "Суглинок важкий твердий"
                if il >= 0 and il <= 0.25:
                    name = "Суглинок важкий напiвтвердий"
                if il > 0.25 and il <= 0.50:
                    name = "Суглинок важкий тугопластичний"
                if il > 0.50 and il <= 0.75:
                    name = "Суглинок важкий м'якопластичний"
                if il > 0.75 and il <= 1.00:
                    name = "Суглинок важкий текучопластичний"
                if il > 1.00:
                    name = "Суглинок важкий текучий"
            elif ip >= 17 and ip < 27:
                if il < 0:
                    name = "Глина легка тверда"
                if il >= 0 and il <= 0.25:
                    name = "Глина легка напiвтверда"
                if il > 0.25 and il <= 0.50:
                    name = "Глина легка тугопластична"
                if il > 0.50 and il <= 0.75:
                    name = "Глина легка м'якопластична"
                if il > 0.75 and il <= 1.00:
                    name = "Глина легка текучопластична"
                if il > 1.00:
                    name = "Глина легка текуча"
            else:
                if il < 0:
                    name = "Глина важка тверда"
                if il >= 0 and il <= 0.25:
                    name = "Глина важка напiвтверда"
                if il > 0.25 and il <= 0.50:
                    name = "Глина важка тугопластична"
                if il > 0.50 and il <= 0.75:
                    name = "Глина важка м'якопластична"
                if il > 0.75 and il <= 1.00:
                    name = "Глина важка текучопластична"
                if il > 1.00:
                    name = "Глина важка текуча"
    return name


def por(w:float, p:float, ps:float) -> float:
    """Пористость (n)
    w - Влажность
    p - Плотность
    ps - Плотность частиц"""
    if w != None and p != None and ps != None and ps > 0:
        k = ps * (1 + w / 100)
        n = 1 - (p / k)
        n = round(n, 3)
    else:
        n = None
    return n


def kfPorw(w:float, p:float, ps:float) -> float:
    """Коэффициент пористости (e)
    w - Влажность
    p - Плотность
    ps - Плотность частиц"""
    if p != None and w != None and ps != None and p > 0:
        e = (ps * (1 + w / 100) / p) - 1
        e = round(e, 3)
    else:
        e = None
    return e


def kfPorpd(pd:float, ps:float) -> float:
    """Коэффициент пористости - e
    для песков при различном уплотнении
    pd - Плотность скелета
    ps - Плотность частиц"""
    if pd != None and ps != None and pd > 0:
        e = (ps - pd) / pd
        e = round(e, 3)
    else:
        e = None
    return e


def kfVodonas(w:float, p:float, ps:float) -> float:
    """Коэффициент водонасыщения - Sr
    w - Влажность
    p - Плотность
    ps - Плотность частиц"""
    if p != None and p > 0 and w != None and ps != None:
        e = (ps * (1 + w / 100) / p) - 1
        Sr = w / 100 * ps / e
        Sr = round(Sr, 2)
        if Sr > 1:
            Sr = 1.00
    else:
        Sr = None
    return Sr


def vlagAllW(w:float, p:float, ps:float) -> float:
    """Полная влагоемкость - Wsat
    w - Влажность, %
    p - Плотность
    ps - Плотность частиц"""
    if p != None and w != None:
        pd = p / (1 + w / 100)
    else:
        pd = None
    if ps != None and pd != None and ps > 0 and pd > 0:
        Wsat = (ps - pd) / ps / pd
        Wsat = round(Wsat * 100, 1)
    else:
        Wsat = None
    return Wsat


def vlagAll(pd:float, ps:float) -> float:
    """Полная влагоемкость - Wsat
    для песков при различном уплотнении
    pd - Плотность скелета
    ps - Плотность частиц"""
    if ps != None and pd != None and ps > 0 and pd > 0:
        Wsat = (ps - pd) / ps / pd
        Wsat = round(Wsat * 100, 1)
    else:
        Wsat = None
    return Wsat


def plotnAll(w:float, p:float, ps:float) -> float:
    """Плотность при полной влагоемкости - pWsat
     pd - Плотность скелета
     ps - Плотность частиц"""
    if w != None and p != None and ps != None and p > 0 and ps > 0:
        pd = p / (1 + w / 100)
        Wsat = (ps - pd) / ps / pd
        pWsat = pd * (1 + Wsat)
        pWsat = round(pWsat, 2)
    else:
        pWsat = None
    return pWsat


def plastich(wl:float, wp:float) -> float:
    """Число пластичности
    wl - Влажность на границе текучести, %
    wp - Влажность на границе раскатывания, %"""
    if wl != None and wp != None and wl > wp:
        ip = round(wl - wp, 1)
    else:
        ip = None
    return ip


def konsist(w:float, wl:float, wp:float) -> float:
    """Показатель текучести
    w - Природная влажность, %
    wl - Влажность на границе текучести, %
    wp - Влажность на границе раскатывания, %"""
    if w != None and wl != None and wp != None and wl > wp:
        il = (w - wp) / (wl - wp)
        il = round(il, 3)
    else:
        il = None
    return il


def plotsk(w:float, p:float) -> float:
    """Плотность скелета
     w - Природная влажность, %
     p - Плотность грунта"""
    if w != None and p != None and w != 0 and p != 0:
        pd = p / (1 + w / 100)
        pd = round(pd, 2)
    else:
        pd = None
    return pd


def plotnAllpd(ps:float, pd:float) -> float:
    """Плотность при полной влагоемкости - pWsat
     ps - Плотность частиц
     pd - Плотность скелета"""
    if ps != None and pd != None and ps > 0:
        Wsat = (ps - pd) / ps / pd
        pWsat = pd * (1 + Wsat)
        pWsat = round(pWsat, 2)
    else:
        pWsat = None
    return pWsat


def plotnW(ps:float, pd:float) -> float:
    """Плотность грунта взвешенного в воде - pw
     для песков при различном уплотнении
     ps - Плотность частиц
     pd - Плотность скелета"""
    if ps != None and pd != None and ps > 0:
        pw = pd * (ps - 1) / ps
        pw = round(pw, 2)
    else:
        pw = None
    return pw


def stepPlotn(w:float, p:float, ps:float, pdmin:float, pdmax:float) -> float:
    """Степень плотности песков - Id
    w - Влажность
    p - Плотность
    ps - Плотность частиц
    pdmin - Плотность скелета минимальный
    pdmax - Плотность скелета максимальна"""
    if w != None and p != None and ps != None and pdmin != None and pdmax != None and pdmin > 0 and pdmax > 0:
        pd = p / (1 + w / 100)
        e = (ps - pd) / pd
        emax = (ps - pdmin) / pdmin
        emin = (ps - pdmax) / pdmax
        if emax > emin:
            Id = (emax - e) / (emax - emin)
            Id = round(Id, 2)
        else:
            Id = None
    else:
        Id = None
    return Id


def stepPlotnpd(w:float, p:float, pdmin:float, pdmax:float) -> float:
    """Степень плотности песков - Id
    w - Влажность
    p - Плотность
    pdmin - Плотность скелета минимальный
    pdmax - Плотность скелета максимальна"""
    Id = 0.00
    if w != None and p != None and pdmin != None and pdmax != None:
        pd = p / (1 + w / 100)
        Id = ((pd - pdmin) * pdmax) / ((pdmax - pdmin) * pd)
        Id = round(Id, 2)
    else:
        Id = None
    return Id


def kfUplotn(ps:float, pdmin:float, pdmax:float) -> float:
    """Коэффициент уплотняемости - U
    ps - Плотность частиц
    pdmin - Плотность скелета мшншмальный
    pdmax - Плотность скелета максимальна"""
    U = 0.00
    if ps != None and pdmin != None and pdmax != None:
        emax = (ps - pdmin) / pdmin
        emin = (ps - pdmax) / pdmax
        U = (emax - emin) / emax
        U = round(U, 2)
    else:
        U = None
    return U


def udelVesps(ps:float) -> float:
    """Удельный вес частиц грунта - q
    ps - Плотность частиц"""
    q = 0.0
    if ps is not None and ps > 0:
        if type(ps) is dc.Decimal:
            q = round(ps * dc.Decimal(9.81), 1)
        elif type(ps) is float:
            q = round(ps * 9.81, 1)
    else:
        q = None
    return q


def udelVesW(ps:float, pd:float) -> float:
    """Удельный вес грунта взвешенного в воде - qw
     для песков при различном уплотнении
     ps - Плотность частиц
     pd - Плотность скелета"""
    qw = 0.00
    if ps != None and pd != None and ps > 0:
        if type(ps) is float and type(pd) is float:
            qw = pd * (ps - 1) / ps
            qw = round(qw * 9.81, 2)
        elif type(ps) is dc.Decimal and type(pd) is dc.Decimal:
            qw = pd * (ps - 1) / ps
            qw = round(qw * dc.Decimal(9.81), 2)
    else:
        qw = None
    return qw


def udelVesWW(w:float, p:float, ps:float) -> float:
    """Удельный вес грунта взвешенного в воде - qw
    w - Влажность
    p - Плотность
    ps - Плотность частиц
    pd - Плотность скелета"""
    if p != None and w != None:
        pd = p / (1 + w / 100)
    else:
        pd = None
    if ps != None and pd != None and ps > 0:
        qw = pd * (ps - 1) / ps
        if type(qw) is dc.Decimal:
            qw = round(qw * dc.Decimal(9.81), 2)
        elif type(qw) is float:
            qw = round(qw * 9.81, 2)
    else:
        qw = None
    return qw


def tgFiFiC(idSrez:int) -> list:
    """Функция возвращает список [tgFi, Fi, C]
    tgFi - тангенс угла внутреннего трения
    Fi - угол внутреннего трения
    C - сцепление
    idGroup - Идентификатор одноплоскостного среза (id_srez)"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT COUNT(srezi.nagruzka) AS count_n,
                            SUM(srezi.nagruzka * srezi.sopr_srez) AS sum_ns,
                            SUM(srezi.nagruzka * srezi.nagruzka) AS sum_nn,
                            SUM(srezi.nagruzka) AS sum_n,
                            SUM(srezi.sopr_srez) AS sum_s
                        FROM public.srezi 
                        GROUP BY srezi.id_srez
                        HAVING srezi.id_srez = %(v2)s""",
                     {'v2': idSrez})
        recAll = curs.fetchone()
    if recAll == None:
        retval = []
    else:
        chislTgF = recAll[0] * recAll[1] - recAll[3] * recAll[4]  # Числитель формулы расчета тангенса угла
        chislC = recAll[4] * recAll[2] - recAll[3] * recAll[1]  # Числитель формулы расчета сцепления
        znamTgFC = recAll[0] * recAll[2] - recAll[3] * recAll[3]  # Знаменатель формулы расчета угла и сцепления
        tgFi = round(chislTgF / znamTgFC, 4)
        scep = round(chislC / znamTgFC, 4)
        if scep < 0:
            scep = 0
            tgFi = recAll[1] / recAll[2]
        fitext = tgtodegrestr(tgFi)  # Текстовое выражение градусы и минуты
        retval = []  # Формирование кортежа из трех значений (тангенс угла, текстовое значение угла с минутами, сцепление)
        retval.append(tgFi)
        retval.append(fitext)
        retval.append(round(scep, 4))
    return retval


def degrestr(degrees:float) -> str:
    """Преобразует числовое значение градусов в строковое выражение градусы - минуты
    degrees - числовое значение градусов с десятыми долями"""
    grad = int(degrees)
    minut = int(round((degrees - grad) * 60, 0))
    if minut < 10:
        retval = str(grad) + "°" + "0" + str(minut) + "'"
    else:
        retval = str(grad) + "°" + str(minut) + "'"
    return retval


def tgtodegrestr(tgfi:float) -> str:
    """Преобразует тангенс угла в строковое выражение угла (градусы-минуты)
    tgfi - тангенс угла"""
    cornerrad = math.atan(tgfi)
    grad = math.degrees(cornerrad)
    retval = degrestr(grad)
    return retval


def setBVP(plotn:float, plastich:float, konsist:float) -> float:
    """Функция возвращает коэффициент за отсутствие расширения грунта в приборе
    plotn - плотность грунтов (для крупнообломочных грунтов следует присваивать (-1))
    plastich - число пластичности
    konsist - консистенция
    nV - коэффициент Пуасона
    nvv - разброс коэффициента Пуасона в зависимости от плотности
    npp - разброс плотности"""
    maxp = 2.20
    minp = 1.30
    npp = maxp - minp
    nV = 0.5
    if plotn is not None and plastich is not None:
        plotn = float(plotn)
        if plastich < 0:  # Крупнообломочные грунты
            nV = 0.27
        elif plastich < 1:  # Пески
            nvv = 0.35 - 0.30
            if plotn > maxp:
                nV = 0.30
            elif plotn > minp:
                nV = nvv / npp * (maxp - plotn) + 0.30
            else:
                nV = 0.35
        elif plastich < 7:  # Супесь
            nvv = 0.35 - 0.30
            if plotn > maxp:
                nV = 0.30
            elif plotn > minp:
                nV = nvv / npp * (maxp - plotn) + 0.30
            else:
                nV = 0.35
        elif plastich < 17:  # Суглинок
            nvv = 0.37 - 0.35
            if plotn > maxp:
                nV = 0.35
            elif plotn > minp:
                nV = nvv / npp * (maxp - plotn) + 0.35
            else:
                nV = 0.37
        else:  # Глина
            if konsist < 0:
                nvv = 0.30 - 0.20
                if plotn > maxp:
                    nV = 0.20
                elif plotn > minp:
                    nV = nvv / npp * (maxp - plotn) + 0.20
                else:
                    nV = 0.30
            elif konsist <= 0.25:
                nvv = 0.38 - 0.30
                if plotn > maxp:
                    nV = 0.30
                elif plotn > minp:
                    nV = nvv / npp * (maxp - plotn) + 0.30
                else:
                    nV = 0.38
            else:
                nvv = 0.45 - 0.38
                if plotn > maxp:
                    nV = 0.38
                elif plotn > minp:
                    nV = nvv / npp * (maxp - plotn) + 0.38
                else:
                    nV = 0.45
        nBV = 1 - (2 * nV ** 2 / (1 - nV))
    else:
        nBV = 1.00
    return nBV


def setBV(kf_por:float, plastich:float, konsist:float) -> float:
    """Функция возвращает коэффициент за отсутствие расширения грунта в приборе
    kf_por - коэффициент пористости (для крупнообломочных грунтов следует присваивать (-1))
    plastich - число пластичности
    konsist - консистенция
    nV - коэффициент Пуасона
    nvv - разброс коэффициента Пуасона в зависимости от кф пористости
    npp - разброс коэфициентов пористости"""
    npp = 1.15 - 0.45
    nV = 1
    nBV = 0.00
    if kf_por is not None and plastich is not None:
        kf_por = float(kf_por)
        if plastich < 0:  # Крупнообломочные грунты
            nV = 0.27
        elif plastich < 1:  # Пески
            nvv = 0.35 - 0.30
            if kf_por < 0.45:
                nV = 0.30
            elif kf_por < 1.05:
                nV = nvv / npp * (kf_por - 0.45) + 0.30
            else:
                nV = 0.35
        elif plastich < 7:  # Супесь
            nvv = 0.35 - 0.30
            if kf_por < 0.45:
                nV = 0.30
            elif kf_por < 1.05:
                nV = nvv / npp * (kf_por - 0.45) + 0.30
            else:
                nV = 0.35
        elif plastich < 17:  # Суглинок
            nvv = 0.37 - 0.35
            if kf_por < 0.45:
                nV = 0.35
            elif kf_por < 1.05:
                nV = nvv / npp * (kf_por - 0.45) + 0.35
            else:
                nV = 0.37
        else:  # Глина
            if konsist < 0:
                nvv = 0.30 - 0.20
                if kf_por < 0.45:
                    nV = 0.20
                elif kf_por < 1.05:
                    nV = nvv / npp * (kf_por - 0.45) + 0.20
                else:
                    nV = 0.30
            elif konsist <= 0.25:
                nvv = 0.38 - 0.30
                if kf_por < 0.45:
                    nV = 0.30
                elif kf_por < 1.05:
                    nV = nvv / npp * (kf_por - 0.45) + 0.30
                else:
                    nV = 0.38
            else:
                nvv = 0.45 - 0.38
                if kf_por < 0.45:
                    nV = 0.38
                elif kf_por < 1.05:
                    nV = nvv / npp * (kf_por - 0.45) + 0.38
                else:
                    nV = 0.45
        nBV = 1 - (2 * nV ** 2 / (1 - nV))
    else:
        nVB = 1.00
    return nBV


def setBIL(plotnsk:float, plastich:float, konsist:float) -> float:
    """Функция возвращает коэффициент за отсутствие расширения грунта в приборе
    plastich - число пластичности
    konsist - консистенция
    nV - коэффициент Пуасона
    nvv - разброс коэффициента Пуасона в зависимости от консистенции
    npp - разброс консистенции"""
    nV = 0.5
    if konsist is None:
        plastich = 0
    else:
        konsist = float(konsist)
    if plastich < 0:  # Крупнообломочные грунты
        nV = 0.27
    elif plastich < 1:  # Пески
        nvv = 0.35 - 0.30
        npp = 1.00
        if plotnsk is not None and plotnsk < 1.30:
            nV = 0.30
        elif plotnsk is not None and plotnsk < 1.80:
            nV = nvv / npp * (float(plotnsk) - 1.30) + 0.30
        else:
            nV = 0.35
    elif plastich < 7:  # Супесь
        nvv = 0.35 - 0.30
        npp = 1.00 - 0.00
        if konsist < 0.00:
            nV = 0.30
        elif konsist < 1.00:
            nV = nvv / npp * (konsist - 0.00) + 0.30
        else:
            nV = 0.35
    elif plastich < 17:  # Суглинок
        nvv = 0.37 - 0.35
        npp = 1.00 - 0.00
        if konsist < 0.00:
            nV = 0.35
        elif konsist < 1.00:
            nV = nvv / npp * (konsist - 0.00) + 0.35
        elif konsist < 5.00:
            nvv = 0.40 - 0.37
            npp = 5.00 - 1.00
            nV = nvv / npp * (konsist - 1.00) + 0.37
        else:
            nV = 0.40
    else:  # Глина
        if konsist < 0.00:
            nvv = 0.30 - 0.20
            npp = 0.00 - (-1.00)
            if konsist < -1.00:
                nV = 0.20
            else:
                nV = nvv / npp * (konsist - (-1.0)) + 0.20
        elif konsist < 0.25:
            nvv = 0.38 - 0.30
            npp = 0.25 - 0.00
            if konsist < 0.25:
                nV = nvv / npp * (konsist - 0.00) + 0.30
            else:
                nV = 0.38
        elif konsist < 1.00:
            nvv = 0.45 - 0.38
            npp = 1.00 - 0.25
            if konsist < 1.00:
                nV = nvv / npp * (konsist - 0.25) + 0.38
            else:
                nV = 0.45
        elif konsist < 5.00:
            nvv = 0.5 - 0.45
            npp = 5.00 - 1.00
            if konsist < 5.00:
                nV = nvv / npp * (konsist - 1.00) + 0.45
            else:
                nV = 0.50
        else:
            nV = 0.50
    nBV = 1 - (2 * nV ** 2 / (1 - nV))
    return nBV


def setMkSNIP(lnKfPor:float, lnKonsisten:float) -> float:
    """Вычисление коэффициента Mk грунта природной влажности и после водонасыщения
    для пересчета модуля деформации по СНиП 2.02.02-85
    lnKfPor - Коэффициент пористости
    lnKonsisten - Консистенция"""
    if lnKfPor is not None and lnKonsisten is not None:
        lnKfPor = float(lnKfPor)
        lnKonsisten = float(lnKonsisten)
        if lnKonsisten > 0.75:
            lnMk = 1.00
        elif 0.25 <= lnKonsisten <= 0.75:
            lnMk = (1.25 * lnKfPor ** 2 - 4.75 * lnKfPor + 6.4) - (lnKonsisten - 0.25) * 100 * (0.025 * lnKfPor ** 2 - 0.095 * lnKfPor + 0.108)
            lnMk = round(lnMk, 2)
        else:
            lnMk = 1.25 * lnKfPor ** 2 - 4.75 * lnKfPor + 6.4
            lnMk = round(lnMk, 2)
    else:
        lnMk = None
    return lnMk


def setMkDBN(cVozrast:str, nPlastich:float, nKoefpor:float, nSr:float) -> float:
    """Расчет коэффициента Мк грунта природной влажности
    для пересчета модуля информации по ДБН А.2.1-1-2014
    cVozrast - Стратиграфо-генетический индекс
    nPlastich - Число пластичности
    nKoefpor - Коэффициент пористости
    nSr - Коэффициент водонасыщения"""
    if nKoefpor is not None:
        nKoefpor = float(nKoefpor)
    if cVozrast[0] == "v":
        if nSr is None or nKoefpor is None:
            nMk = None
        else:
            if nSr < 0.8:
                if nKoefpor < 0.85:
                    nMk = 3
                else:
                    nMk = 2
            else:
                if nKoefpor < 0.85:
                    nMk = 2
                else:
                    nMk = 1.5
    elif cVozrast[0] == "e":
        if nPlastich is None or nKoefpor is None:
            nMk = None
        else:
            if nPlastich < 7:
                nMk = None
            else:
                if nKoefpor < 0.45:
                    nMk = 5.5
                elif nKoefpor < 0.55:
                    nMk = 5.5 - (5.5 - 5.3) / 0.1 * (nKoefpor - 0.45)
                elif nKoefpor < 0.65:
                    nMk = 5.3 - (5.3 - 4.8) / 0.1 * (nKoefpor - 0.55)
                elif nKoefpor < 0.75:
                    nMk = 4.8 - (4.8 - 4.3) / 0.1 * (nKoefpor - 0.65)
                elif nKoefpor < 0.85:
                    nMk = 4.3 - (4.3 - 3.7) / 0.1 * (nKoefpor - 0.75)
                else:
                    nMk = 3.7
    else:
        if nPlastich is None or nKoefpor is None:
            nMk = None
        else:
            if nPlastich < 1:
                if nKoefpor < 0.45:
                    nMk = 6.0
                elif nKoefpor < 0.55:
                    nMk = 6.0 - (6.0 - 4.1) / 0.1 * (nKoefpor - 0.45)
                elif nKoefpor < 0.65:
                    nMk = 4.1 - (4.1 - 2.7) / 0.1 * (nKoefpor - 0.55)
                elif nKoefpor < 0.75:
                    nMk = 2.7 - (2.7 - 1.9) / 0.1 * (nKoefpor - 0.65)
                elif nKoefpor < 0.85:
                    nMk = 1.9 - (1.9 - 1.3) / 0.1 * (nKoefpor - 0.75)
                elif nKoefpor < 0.95:
                    nMk = 1.3 - (1.3 - 1.0) / 0.1 * (nKoefpor - 0.85)
                else:
                    nMk = 1
            elif nPlastich < 7:
                if nKoefpor < 0.55:
                    nMk = 4.0
                elif nKoefpor < 0.65:
                    nMk = 4.0 - (4.0 - 3.5) / 0.1 * (nKoefpor - 0.55)
                elif nKoefpor < 0.75:
                    nMk = 3.5 - (3.5 - 3.0) / 0.1 * (nKoefpor - 0.65)
                elif nKoefpor < 0.85:
                    nMk = 3.0 - (3.0 - 2.0) / 0.1 * (nKoefpor - 0.75)
                else:
                    nMk = 2.0
            elif nPlastich < 17:
                if nKoefpor < 0.55:
                    nMk = 5.0
                elif nKoefpor < 0.65:
                    nMk = 5.0 - (5.0 - 4.5) / 0.1 * (nKoefpor - 0.55)
                elif nKoefpor < 0.75:
                    nMk = 4.5 - (4.5 - 4.0) / 0.1 * (nKoefpor - 0.65)
                elif nKoefpor < 0.85:
                    nMk = 4.0 - (4.0 - 3.0) / 0.1 * (nKoefpor - 0.75)
                elif nKoefpor < 0.95:
                    nMk = 3.0 - (3.0 - 2.5) / 0.1 * (nKoefpor - 0.85)
                elif nKoefpor < 1.05:
                    nMk = 2.5 - (2.5 - 2.0) / 0.1 * (nKoefpor - 0.95)
                else:
                    nMk = 2.0
            else:
                if nKoefpor < 0.75:
                    nMk = 6.0
                elif nKoefpor < 0.85:
                    nMk = 6.0 - (6.0 - 5.5) / 0.1 * (nKoefpor - 0.75)
                elif nKoefpor < 0.95:
                    nMk = 5.5 - (5.5 - 5.0) / 0.1 * (nKoefpor - 0.85)
                elif nKoefpor < 1.05:
                    nMk = 5.0 - (5.0 - 4.5) / 0.1 * (nKoefpor - 0.95)
                else:
                    nMk = 4.5
    if nMk is None:
        pass
    else:
        nMk = round(nMk, 2)
    return nMk


def setV(ncount:int, recSetV:list) -> float:
    """Функция возвращает Значения критерия v при двусторонней доверительной вероятности а = 0,95
    ncount - количество определений
    recSetV - список значений критерия v"""
    v = None
    for a, b in recSetV:
        if a == ncount:
            v = b
            break
    if v == None:
        v = round(1.86664 * ncount ** 0.133, 2)
    return v


def setta(k:int, recSetta:tuple) -> list:
    """Функция возвращает коэффициент, принимаемый по таблице Ж.2 приложения Ж ДСТУ 20522-96,
    в зависимости от заданной односторонней доверительной вероятности
    а и числа степеней свободы K = n - 1 или K = (n1 + n2) - 2"""
    ta = []
    if k > 100:
        ta = [100.00, 1.05, 1.30, 1.67, 2.00, 2.11, 2.37]
    elif k > 2:
        for a, b, c, d, e, f, g in recSetta:
            if a == k:
                ta = [float(a), float(b), float(c), float(d), float(e), float(f), float(g)]
                break
    else:
        ta = []
    return ta


def setVal(ka:int, l:float, recSetVal:tuple) -> float:
    """Функция возвращает коэффициент Val по таблице Ж.3 приложения Ж ДСТУ 20522-96
    в зависимости от односторонней доверительной вероятности a = 0.95,
    числа степеней свободы Ka = n - 2 и параметра l"""
    arrval = np.asarray(recSetVal, dtype=np.float64)  # Массив значений (val) Таблица Ж3
    x, y, _ = arrval.T
    mask = ((x == ka) & (y == l))
    arrval_one = arrval[mask]  # Одна строка массива выбранная по маске
    val = arrval_one[0][2]  # коэффициент по таблице Ж.3
    return val


def setfa(k1:int, k2:int, recSetfa:tuple) -> float:
    """Функция возвращает коэффициент, принимаемый по таблице Ж.4 приложения Ж ДСТУ 20522-96,
    в зависимости от заданной односторонней доверительной вероятности
    а и числа степеней свободы K1 = n - 1 и K2 = n - 1"""
    fa = 0.00
    arrfa = np.array(recSetfa, dtype=np.float64)
    if k1 > 60:
        arrfa = arrfa[55, :]
        if k2 < 5:
            fa = 0
        if k2 < 13:
            fa = arrfa[k2 - 4]
        elif k2 < 14:
            recfa = arrfa[8: 10]
            fa = recfa[0] - (recfa[0] - recfa[1]) / 2
        elif k2 < 15:
            fa = arrfa[9]
        elif k2 < 16:
            recfa = arrfa[9: 11]
            fa = recfa[0] - (recfa[0] - recfa[1]) / 2
        elif k2 < 17:
            fa = arrfa[10]
        elif k2 < 20:
            recfa = arrfa[10: 12]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 4) * (k2 - 16)
        elif k2 < 21:
            fa = arrfa[11]
        elif k2 < 30:
            recfa = arrfa[11: 13]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 10) * (k2 - 20)
        elif k2 < 31:
            fa = arrfa[12]
        elif k2 < 40:
            recfa = arrfa[12: 14]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 10) * (k2 - 30)
        elif k2 < 41:
            fa = arrfa[13]
        elif k2 < 60:
            recfa = arrfa[13:]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 20) * (k2 - 40)
        elif k2 < 1000:
            fa = arrfa[14]
    elif k1 > 4:
        if k2 < 5:
            fa = 0
        if k2 < 13:
            fa = arrfa[k1 - 5, k2 - 4]
        elif k2 < 14:
            recfa = arrfa[k1 - 5, 8: 10]
            fa = recfa[0] - (recfa[0] - recfa[1]) / 2
        elif k2 < 15:
            fa = arrfa[k1 - 5, 9]
        elif k2 < 16:
            recfa = arrfa[k1 - 5, 9: 11]
            fa = recfa[0] - (recfa[0] - recfa[1]) / 2
        elif k2 < 17:
            fa = arrfa[k1 - 5, 10]
        elif k2 < 20:
            recfa = arrfa[k1 - 5, 10: 12]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 4) * (k2 - 16)
        elif k2 < 21:
            fa = arrfa[k1 - 5, 11]
        elif k2 < 30:
            recfa = arrfa[k1 - 5, 11: 13]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 10) * (k2 - 20)
        elif k2 < 31:
            fa = arrfa[k1 - 5, 12]
        elif k2 < 40:
            recfa = arrfa[k1 - 5, 12: 14]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 10) * (k2 - 30)
        elif k2 < 41:
            fa = arrfa[k1 - 5, 13]
        elif k2 < 60:
            recfa = arrfa[k1 - 5, 13:]
            fa = recfa[0] - ((recfa[0] - recfa[1]) / 20) * (k2 - 40)
        else:
            fa = arrfa[k1 - 5, 14]
    else:
        fa = 0
    return fa


def stat_one(recval:list, flag:bool) -> list:
    """Вычисление нормативных и расчетных значений характеристик грунтов, представленных одной величиной
    recval - список данных (list)
    arr - массив данных
    recSetV - список значений критерия v таблица Ж.1 приложения Ж ДСТУ 20522-96
    recSetta - список значений коэффициента ta таблица Ж.2 ДСТУ 20522-96
    flag - определяет Знак перед величиной надежность основания или сооружения
    (True для знака (+) False для знака (-)"""
    list_x = []
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        recSetV = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setta""")
        recSetta = curs.fetchall()
    arr = np.array(recval)          # начальный массив данных
    n0 = len(recval)                # начальное количество значений
    list_brak = []
    n_cikl = 0
    if n0 > 3:
        while True:
            xn = np.mean(arr)               # нормативное значение
            n = np.count_nonzero(arr)       # начальное количество элементов в массиве
            s = np.std(arr, ddof=1)         # стандартное отклонение (степень свободы = n-1)
            vi = float(setV(n, recSetV))           # значение критерия v при двусторонней доверительной вероятности а = 0,95
            valbrak = np.extract(np.abs(xn - arr) > vi * s, arr)    # массив отбракованых значений после цикла проверки
            arr = np.extract(np.abs(xn - arr) <= vi * s, arr)  # массив после отбраковки
            list_brak += list(valbrak)
            nn = np.count_nonzero(arr)      # количество значений после цикла отбраковки
            n_cikl = n_cikl + 1             # количество циклов
            if n == nn:
                break
        xmin = np.min(arr)                  # минимальное значение
        xmax = np.max(arr)                  # максимальное значение
        v = s / xn                          # коэффициент вариации
        ta = setta(n-1, recSetta)           # коэффициент, принимаемый по таблице Ж.2 ДСТУ 20522-96
        pa085 = ta[1] * v / n ** 0.5        # показатель точности среднего значения характеристики грунта
        pa090 = ta[2] * v / n ** 0.5
        pa095 = ta[3] * v / n ** 0.5
        pa0975 = ta[4] * v / n ** 0.5
        pa098 = ta[5] * v / n ** 0.5
        pa099 = ta[6] * v / n ** 0.5
        if flag == True:
            x085 = xn * (1 + pa085)         # вычисление расчетных значений характеристик грунта
            x090 = xn * (1 + pa090)
            x095 = xn * (1 + pa095)
            x0975 = xn * (1 + pa0975)
            x098 = xn * (1 + pa098)
            x099 = xn * (1 + pa099)
        else:
            x085 = xn * (1 - pa085)
            x090 = xn * (1 - pa090)
            x095 = xn * (1 - pa095)
            x0975 = xn * (1 - pa0975)
            x098 = xn * (1 - pa098)
            x099 = xn * (1 - pa099)
        list_x = [n_cikl, n0, nn, xmin, xmax, xn, s, v, x085, x090, x095, x0975, x098, x099]
        list_b = str(list_brak)
        list_x.append(list_b)
    elif n0 > 1:
        nn = n0
        xmin = np.min(arr)  # минимальное значение
        xmax = np.max(arr)  # максимальное значение
        xn = np.mean(arr)  # нормативное значение
        s = np.std(arr, ddof=1)  # стандартное отклонение (степень свободы = n-1)
        v = s / xn  # коэффициент вариации
        list_x = [n_cikl, n0, nn, xmin, xmax, xn, s, v, None, None, None, None, None, None]
    elif n0 > 0:
        nn = n0
        xmin = xmax = xn = arr[0]  # xmin - минимальные значения
        list_x = [n_cikl, n0, nn, xmin, xmax, xn, None, None, None, None, None, None, None, None]
    return [list_x]


def stat_1log(recval:list, flag:bool) -> list:
    """Вычисление нормативных и расчетных значений характеристик грунтов, представленных одной величиной
    при логнормальном законе распределения
    recval - список данных (list)
    flag - определяет Знак перед величиной надежность основания или сооружения
    (True для знака (+) False для знака (-)"""
    list_x = []
    arr0 = np.array(recval)     # начальный массив данных
    n0 = len(recval)            # начальное количество значений
    xmin = np.min(arr0)         # минимальное значение начального массива
    xmax = np.max(arr0)         # максимальное значение начального массива
    arrlog = np.log10(arr0)      # массив логарифмов преобразованых значений (все > 0)
    n_cikl = 1
    if n0 > 1:
        av = np.mean(arrlog)            # среднеарифметическое значение логарифмов
        s2log = np.sum(np.square(arrlog - av)) / (n0 - 1)  # Дисперсия логарифмов
        slog = np.std(arrlog, ddof=1)       # стандартное отклонение (степень свободы = n-1) логарифмов
        s = 10 ** slog                      # стандартное отклонение значений
        d = 10 ** s2log
        xnlog = av + 1.1513 * np.square(slog)      # логарифм нормативного значения
        xn = 10 ** xnlog    # Нормативное значение
        s2 = np.square(xn) * (10 ** (2.3026 * s2log) - 1)   # Дисперсия значений
        v = np.sqrt(10 ** (2.3026 * s2log) - 1) # коэффициент вариации
        # Вычисление полудлин доверительного интервала в зависимости от односторонней доверительной вероятности
        uk = slog * np.sqrt(1 + 2.65 * np.square(slog)) / np.sqrt(n0)
        # Через логарифм Ua
#        d085 = np.log10(1.03) + uk
#        d090 = np.log10(1.28) + uk
#        d095 = np.log10(1.65) + uk
#        d0975 = np.log10(1.96) + uk
#        d099 = np.log10(2.33) + uk
        # Строго по ГОСТ (вместо сложения принято умножение)
        d085 = (1.03) * uk
        d090 = (1.28) * uk
        d095 = (1.65) * uk
        d0975 = (1.96) * uk
        d099 = (2.33) * uk
        # Вычисление логарифмов расчетных значений
        if flag == True:
            xlog085 = xnlog + d085
            xlog090 = xnlog + d090
            xlog095 = xnlog + d095
            xlog0975 = xnlog + d0975
            xlog099 = xnlog + d099
        else:
            xlog085 = xnlog - d085
            xlog090 = xnlog - d090
            xlog095 = xnlog - d095
            xlog0975 = xnlog - d0975
            xlog099 = xnlog - d099
        # Вычисление нормативного и расчетных значений
        x085 = 10 ** xlog085
        x090 = 10 ** xlog090
        x095 = 10 ** xlog095
        x0975 = 10 ** xlog0975
        x099 = 10 ** xlog099
        list_x = [n_cikl, n0, xmin, xmax, xn, s2, s, v, x085, x090, x095, x0975, x099]
    elif n0 > 0:
        xmin = xmax = xn = arr0[0]  # xmin - минимальные значения
        list_x = [n_cikl, n0, xmin, xmax, xn, None, None, None, None, None, None, None, None]
    return [list_x]


def statsreztgc(rectg:list, recc:list) -> list:
    """Статистическая обработка результатов срезных испытаний по показателям tg(f), c"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        recSetV = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setta""")
        recSetta = curs.fetchall()
    arrtgc = np.array([rectg, recc])	# arrtgc - начальный массив данных [[tg(f)], [c]]
    arr = arrtgc.transpose()			# arr - начальный массив данных пар значений [tg(f), c]
    n0 = len(arr)						# n0 - начальное количество пар значений
    list_brak = []						# list_brak - список отбракованых значений
    n_cikl = 0							# n_cikl - количество циклов отбраковки
    if n0 > 3:
        while True:
            n = len(arr)   					# n - количество пар элементов в массиве до очередного цикла отбраковки
            xn = np.mean(arr, axis=0)		# xn - нормативное значение tg, c
            s = np.std(arr, axis=0, ddof=1) # среднее квадратическое отклонение tg, c
            if n < 201:
                vi = float(setV(n, recSetV))			# vi - значение критерия v при двусторонней доверительной вероятности а = 0,95
            else:
                vi = float(round(1.86664 * n ** 0.133, 2))
            cond = np.abs(xn - arr) > (vi * s)
            valbrak = np.extract(cond, arr)  # массив отбракованых значений после цикла проверки
            if len(valbrak) > 0:
                for i in range(0, len(valbrak)):
                    ind = np.where(arr == valbrak[i])
                    arr = np.delete(arr, ind[0], 0)
            list_brak += list(valbrak)
            nn = len(arr)                   # nn - количество пар значений после цикла отбраковки
            n_cikl = n_cikl + 1             # n_cikl - количество циклов
            if n == nn:
                break
        xmin = np.min(arr, axis=0)          # минимальное значение
        xmax = np.max(arr, axis=0)          # максимальное значение
        v = s / xn                          # коэффициент вариации для tg, c
        ta = setta(n - 1, recSetta)         # коэффициент, принимаемый по таблице Ж.2 ДСТУ 20522-96
        pa085 = ta[1] * v / n ** 0.5        # показатель точности среднего значения характеристики грунта
        pa090 = ta[2] * v / n ** 0.5
        pa095 = ta[3] * v / n ** 0.5
        pa0975 = ta[4] * v / n ** 0.5
        pa098 = ta[5] * v / n ** 0.5
        pa099 = ta[6] * v / n ** 0.5
        x085 = xn * (1 - pa085)             # расчетные значения пар [tg(f), C] при доверительной вероятности от 0.85 до 0.99
        x090 = xn * (1 - pa090)
        x095 = xn * (1 - pa095)
        x0975 = xn * (1 - pa0975)
        x098 = xn * (1 - pa098)
        x099 = xn * (1 - pa099)
        if x0975[0] < 0:
            x0975[0] = 0.0000
        if x0975[1] < 0:
            x0975[1] = 0.0000
        if x098[0] < 0:
            x098[0] = 0.0000
        if x098[1] < 0:
            x098[1] = 0.0000
        if x099[0] < 0:
            x099[0] = 0.0000
        if x099[1] < 0:
            x099[1] = 0.0000
        f = tgtodegrestr(xn[0])  # нормативный угол (fi) в градусах и минутах
        fn = np.arctan(xn[0])*180/np.pi     # нормативный угол (fi) в градусах
        fin = np.divmod(fn, 1)
        fingm = str(int(fin[0])) + "º" + str(int(round(fin[1] * 60, 0))) + "'"   # нормативный угол в градусах-минутах
        list_x = np.concatenate([[n_cikl, n0, nn], xmin, xmax, xn, s, v, x085, x090, x095, x0975, x098, x099, list_brak], axis=0)
    elif n0 > 1:
        nn = n0
        xmin = np.min(arr, axis=0)  # xmin - минимальное значение tg(f), c
        xmax = np.max(arr, axis=0)  # xmax - максимальное значение tg(f), c
        xn = np.mean(arr, axis=0)  # xn - нормативное значение tg(f), c
        s = np.std(arr, axis=0, ddof=1)  # s - стандартное отклонение (степень свободы = n-1) tg(f), c
        v = s / xn  # v - коэффициент вариации tg(f), c
        list_x = np.concatenate([[n_cikl, n0, nn], xmin, xmax, xn, s, v, [None, None, None, None, None, None, None, None, None, None, None, None]], axis=0)
    elif n0 > 0:
        nn = n0
        xmin = xmax = xn = arr[0]  # xmin - минимальные значения tg(f), c
        list_x = np.concatenate([[n_cikl, n0, nn], xmin, xmax, xn, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]], axis=0)
    else:
        list_x = np.concatenate([[n_cikl, 0, 0],
                                 [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                                  None, None, None, None, None, None, None, None]], axis=0)
    return list_x


def statsreztp(rect:list, recp:list, namegrunt:str) -> list:
    """"Статистическая обработка результатов срезных испытаний по показателям t, p"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        recSetV = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setta""")
        recSetta = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv095""")
        recva = curs.fetchall()
    arrval = np.asarray(recva, dtype=np.float64)  # массив значений {val}
    arrval = arrval.reshape(-1, 3)
    arrtp = np.array([rect, recp])  # arrtp - начальный массив данных [[t], [p]]
    arr = arrtp.transpose()  # arr - начальный массив данных пар значений [t, p]
    n0 = len(arr)  # n0 - начальное количество пар значений
    list_brak = []  # list_brak - список отбракованых значений
    n_cikl = 0  # n_cikl - количество циклов отбраковки
    if n0 > 5:
        while True:
            n = len(arr)  # n - количество пар элементов в массиве до очередного цикла отбраковки
            tgfn = (n * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
                   (n * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1]))))  # tgfn - нормативное значение tg(f)
            cn = (np.sum(arr, 0)[0] - tgfn * np.sum(arr, 0)[1]) / n  # нормативное значение с
            if cn <= 0:  # значения т и р если cn = 0
                cn = 0
                tgfn = np.sum(np.prod(arr, 1)) / np.sum(np.square(arr[:, 1]))
            tn = cn + arr[:, 1] * tgfn  # нормативные значения t
            if cn > 0.0:
                st = np.sqrt(
                    np.sum(np.square(arr[:, 1] * tgfn + cn - arr[:, 0])) / (n - 2))  # среднее квадратическое отклонение (t)
            else:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * tgfn + cn - arr[:, 0])) / (n - 1))
            if n < 201:
                vi = float(recSetV[n][1])  # vi - значение критерия v при двусторонней доверительной вероятности а = 0,95
            else:
                vi = round(1.86664 * n ** 0.133, 2)
            valbrak = np.extract(np.abs(tn - arr[:, 0]) > (vi * st),
                                 arr[:, 0])  # массив отбракованых значений (t) после цикла проверки
            if len(valbrak) > 0:
                for i in range(0, len(valbrak)):
                    ind = np.where(arr == valbrak[i])
                    arr = np.delete(arr, ind[0], 0)
            list_brak += list(valbrak)
            nn = len(arr)  # nn - количество пар значений после цикла отбраковки
            n_cikl = n_cikl + 1  # n_cikl - количество циклов
            if n == nn:
                break
        xmin = np.min(arr, axis=0)  # минимальное значение t, p
        xmax = np.max(arr, axis=0)  # максимальное значение t, p
        pmin = xmin[1]  # минимальная нагрузка
        pmax = xmax[1]  # максимальная нагрузка
        pn = np.mean(arr[:, 1], axis=0)  # среднее значение нагрузки
        tn1 = cn + pmin * tgfn  # нормативное значение t при pmin
        tn2 = cn + pmax * tgfn  # нормативное значение t при pmax
        G = (pmin - pn) / np.sqrt(np.sum(np.square(arr[:, 1] - pn)))
        D = (pmax - pn) / np.sqrt(np.sum(np.square(arr[:, 1] - pn)))
        chis = 1 + nn * float(G) * float(D)
        l = np.sqrt(0.5 * (1 - (1 + nn * float(G) * float(D)) / float(np.sqrt((1 + nn * float(np.square(G))) * (
                    1 + nn * float(np.square(D)))))))  # l - параметр, учитывающий значения диапазона pmin - pmax
        l = np.round(l, 2)
        x, y, _ = arrval.T
        nold = nn
        if nn > 102:
            nn = 102
        mask = ((x == nn - 2) & (y == l))
        nn = nold
        arrval_new = arrval[mask]
        val = arrval_new[0][2]  # коэффициент по таблице Ж.3
        dt1 = val * float(st) / np.sqrt(nn) * np.sqrt(1 + nn * float(np.square(pmin - pn)) / float(
            np.sum(np.square(arr[:, 1] - pn))))  # значения полудлин совместных доверительных интервалов
        dt2 = val * float(st) / np.sqrt(nn) * np.sqrt(
            1 + nn * float(np.square(pmax - pn)) / float(np.sum(np.square(arr[:, 1] - pn))))
        t1 = float(tn1) - dt1  # расчетные значения t при pmin
        t2 = float(tn2) - dt2  # расчетные значения t при pmax
        if (t1 / float(pmin)) < (t2 / float(pmax)):  # расчет коэффициента надежности по грунту (g_tfc)
            g_tgfc = (float(tn1 + tn2) * float(pmax)) / (t2 * float(pmin + pmax))
        else:
            g_tgfc = float(tn1 + tn2) / (t1 + t2)
        g_tgfcs = g_tgfc
        if len(namegrunt) > 2:  # Внесение поправок согласно п.2.7 СНиП 2.02.02-85
            if namegrunt[:3] == 'Мул' and g_tgfc > 1.4:
                g_tgfcs = 1.4
            if namegrunt[:3] != 'Мул' and g_tgfc > 1.25:
                g_tgfcs = 1.25
            if g_tgfc < 1.05:
                g_tgfcs = 1.05
        tgf1 = tgfn / g_tgfc
        fi1 = tgtodegrestr(tgf1)  # расчетное значение угла (fi) в градусах и минутах
        c1 = cn / g_tgfc
        tgf1s = tgfn / g_tgfc
        fi1s = tgtodegrestr(tgf1s)  # расчетное значение угла (fi) в градусах и минутах с учетом поправок
        c1s = cn / g_tgfc
        tgf2 = tgfn
        c2 = cn
        list_x = [n_cikl, n0, nn, tgfn, cn, st, pmin, pmax, pn, t1, t2, g_tgfc, g_tgfcs, tgf1, c1, tgf1s, c1s, tgf2, c2]
        list_x.extend(list_brak)
    elif n0 > 0:
        nn = n0
        xmin = np.min(arr, 0)  # минимальное значение t, p
        xmax = np.max(arr, 0)  # максимальное значение t, p
        pmin = xmin[1]  # минимальная нагрузка
        pmax = xmax[1]  # максимальная нагрузка
        pn = np.mean(arr[:, 1], axis=0)  # среднее значение нагрузки
        tgfn = (nn * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
               (nn * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1]))))  # tgfn - нормативное значение tg(f)
        cn = (np.sum(arr, 0)[0] - tgfn * np.sum(arr, 0)[1]) / nn  # нормативное значение с
        list_x = [n_cikl, n0, nn, tgfn, cn, None, pmin, pmax, pn, None, None, None, None, None, None, None, None, None,
                  None]
    else:
        list_x = [n_cikl, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                  None, None]
    return list_x


def statsreztp75(rect:list, recp:list) -> list:
    """"Статистическая обработка результатов срезных испытаний по показателям t, p (ГОСТ 20522-75)"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        recSetV = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setta""")
        recSetta = curs.fetchall()
    # Формирование массива исходных данных
    arrtp = np.array([rect, recp])  # arrtp - начальный массив данных [[t], [p]]
    arr = arrtp.transpose()  # arr - начальный массив данных пар значений [t, p]
    # Определение исходных параметров и переменных
    unp = np.unique(arr[:, 1], axis=0)  # Список нагрузок
    colp = len(unp)     # Количество нагрузок
    n0 = len(arr)  # n0 - начальное количество пар значений
    list_brak = []  # list_brak - список отбракованых значений
    n_cikl = 0  # n_cikl - количество циклов отбраковки
    list_x = []
    # Начало статистической обработки
    if n0 > 4:
        while True:
            n = len(arr)  # n - количество пар элементов в массиве до очередного цикла отбраковки
            delta = (n * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1])))) # знаменатель в формулах
            tgfn = (n * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / delta  # tgfn - нормативное значение tg(f)
            cn = (np.sum(arr, 0)[0] * np.sum(np.square(arr[:, 1])) - np.sum(arr, 0)[1] * np.sum(np.prod(arr, 1))) / delta
#            cn = (np.sum(arr, 0)[0] - tgfn * np.sum(arr, 0)[1]) / n  # нормативное значение с
            if cn <= 0:  # значения т и р если cn = 0
                cn = 0
                tgfn = np.sum(np.prod(arr, 1)) / np.sum(np.square(arr[:, 1]))
            tn = (cn + arr[:, 1] * tgfn)    # нормативные значения t для каждой нагрузки
            utn = np.unique(tn)             # уникальные нормативые значения t для каждой нагрузки
            if cn > 0.0:
                st = np.sqrt(
                    np.sum(np.square(arr[:, 1] * tgfn + cn - arr[:, 0])) / (n - 2))  # среднее квадратическое отклонение (t)
            else:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * tgfn + cn - arr[:, 0])) / (n - 1))
            sc = st * np.sqrt(np.sum(np.square(arr[:, 1])) / delta)
            stgf = st * np.sqrt(n / delta)
            if n < 201:
                vi = float(recSetV[n][1])  # vi - значение критерия v при двусторонней доверительной вероятности а = 0,95
            else:
                vi = round(1.86664 * n ** 0.133, 2)
            valbrak = np.extract(np.abs(tn - arr[:, 0]) > (vi * st),
                                 arr[:, 0])  # массив отбракованых значений (t) после цикла проверки
            if len(valbrak) > 0:
                for i in range(0, len(valbrak)):
                    ind = np.where(arr == valbrak[i])
                    arr = np.delete(arr, ind[0], 0)
            list_brak += list(valbrak)
            nn = len(arr)  # nn - количество пар значений после цикла отбраковки
            n_cikl = n_cikl + 1  # n_cikl - количество циклов
            if n == nn:
                break
        vt = st / tn        # Коэффициент вариации t
        uvt = st / utn      # Уникальные значения коэффициента вариации t
        utn = np.around(utn, 4)
        uvt = np.around(uvt, 4)
        vtgf = stgf / tgfn  # Коэффициент вариации tgf
        vc = sc / cn        # Коэффициент вариации c
        xmin = np.min(arr, axis=0)  # минимальное значение t, p
        xmax = np.max(arr, axis=0)  # максимальное значение t, p
        pmin = xmin[1]  # минимальная нагрузка
        pmax = xmax[1]  # максимальная нагрузка
        if nn < 4:  # rta - строка значений ta для степени свободы n-2 с учетом значения первой записи k=3
            rta = (None, None, None, None, None, None, None)
        elif nn < 100:
            rta = recSetta[n - 5]  # строка коэффициентов, принимаемый по таблице 2 ГОСТ 20522-75
        else:
            rta = (dc.Decimal('100'), dc.Decimal('1.05'), dc.Decimal('1.30'),
                   dc.Decimal('1.67'), dc.Decimal('2.00'), dc.Decimal('2.11'),
                   dc.Decimal('2.37'))
        # показатель точности среднего значения характеристики tgf
        if rta[0] is None:
            pass
        else:
            pa085tgf = float(rta[1]) * vtgf
            pa090tgf = float(rta[2]) * vtgf
            pa095tgf = float(rta[3]) * vtgf
            pa0975tgf = float(rta[4]) * vtgf
            pa098tgf = float(rta[5]) * vtgf
            pa099tgf = float(rta[6]) * vtgf
            # показатель точности среднего значения характеристики c
            pa085c = float(rta[1]) * vc
            pa090c = float(rta[2]) * vc
            pa095c = float(rta[3]) * vc
            pa0975c = float(rta[4]) * vc
            pa098c = float(rta[5]) * vc
            pa099c = float(rta[6]) * vc
            # расчетные значения пар tg(f) при доверительной вероятности от 0.85 до 0.99
            if pa085tgf < 1:
                tgf085 = np.round(tgfn * (1 - pa085tgf), 4)
            else:
                tgf085 = 0.0000
            if pa090tgf < 1:
                tgf090 = np.round(tgfn * (1 - pa090tgf), 4)
            else:
                tgf090 = 0.0000
            if pa095tgf < 1:
                tgf095 = np.round(tgfn * (1 - pa095tgf), 4)
            else:
                tgf095 = 0.0000
            if pa0975tgf < 1:
                tgf0975 = np.round(tgfn * (1 - pa0975tgf), 4)
            else:
                tgf0975 = 0.0000
            if pa098tgf < 1:
                tgf098 = np.round(tgfn * (1 - pa098tgf), 4)
            else:
                tgf098 = 0.0000
            if pa099tgf < 1:
                tgf099 = np.round(tgfn * (1 - pa099tgf), 4)
            else:
                tgf099 = 0.0000
            # расчетные значения пар C при доверительной вероятности от 0.85 до 0.99
            if pa085c < 1:
                c085 = np.round(cn * (1 - pa085c), 4)
            else:
                c085 = 0.0000
            if pa090c < 1:
                c090 = np.round(cn * (1 - pa090c), 4)
            else:
                c090 = 0.0000
            if pa095c < 1:
                c095 = np.round(cn * (1 - pa095c), 4)
            else:
                c095 = 0.0000
            if pa0975c < 1:
                c0975 = np.round(cn * (1 - pa0975c), 4)
            else:
                c0975 = 0.0000
            if pa098c < 1:
                c098 = np.round(cn * (1 - pa098c), 4)
            else:
                c098 = 0.0000
            if pa099c < 1:
                c099 = np.round(cn * (1 - pa099c), 4)
            else:
                c099 = 0.0000
            fin = tgtodegrestr(tgfn)  # нормативный угол (fi) в градусах и минутах
            fgn = np.arctan(tgfn) * 180 / np.pi  # нормативный угол (fi) в градусах
            # Расчетные значения углов при доверительной вероятности от 0.85 до 0.99
            fi085 = tgtodegrestr(tgf085)
            fi090 = tgtodegrestr(tgf090)
            fi095 = tgtodegrestr(tgf095)
            fi0975 = tgtodegrestr(tgf0975)
            fi098 = tgtodegrestr(tgf098)
            fi099 = tgtodegrestr(tgf099)
            list_x = np.concatenate([[n_cikl, n0, nn, colp, pmin, pmax, tgfn, cn, st, stgf, sc, vtgf, vc,
                                      tgf085, c085, tgf090, c090, tgf095, c095, tgf0975, c0975, tgf098, c098, tgf099, c099],
                                     unp, utn, uvt, list_brak], axis=0)
    elif n0 > 0:
        nn = n0
        xmin = np.min(arr, 0)  # минимальное значение t, p
        xmax = np.max(arr, 0)  # максимальное значение t, p
        pmin = xmin[1]  # минимальная нагрузка
        pmax = xmax[1]  # максимальная нагрузка
        tgfn = (nn * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
               (nn * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1]))))  # tgfn - нормативное значение tg(f)
        cn = (np.sum(arr, 0)[0] - tgfn * np.sum(arr, 0)[1]) / nn  # нормативное значение с
        utn = np.full((colp), None)
        uvt = np.full((colp), None)
        list_x = np.concatenate([[n_cikl, n0, nn, colp, pmin, pmax, tgfn, cn, None, None, None, None, None, None, None,
                                  None, None, None, None, None, None, None, None, None], unp, utn, uvt, list_brak])
    else:
        nn = n0
        unp = utn = uvt =[]
        list_x = np.concatenate([[n_cikl, n0, nn, None, None, None, None, None, None, None, None, None, None, None, None,
                                 None, None, None, None, None, None, None, None, None], unp, utn, uvt, list_brak])
    return list_x


def statcompresep(rece:list, recp:list, recb:list) -> list:
    """"Статистическая обработка результатов компрессионных испытаний.
    Вычисление нормативного и расчетного значений модуля деформации с использованием аналитической аппроксимации
    компрессионной кривой по показателям: относительное сжатие (eps) и давления (p) (ДСТУ Б В.2.1-5-96 Приложение В)"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        recSetV = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setta""")
        recSetta = curs.fetchall()
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv095""")
        recSetVal = curs.fetchall()
    avgb = np.average(recb)         # Среднее значение коэффициента b
    reclnp = np.log(recp)           # reclnp - Натуральный логарифм нагрузок
    arrep = np.array([rece, reclnp])  # arrep - начальный массив данных [[eps], [lnp]]
    arr = arrep.transpose()         # arr - начальный массив данных пар значений [eps, lnp]
    n0 = len(arr)                   # n0 - начальное количество пар значений
    list_brak = []                  # list_brak - список отбракованых значений
    n_cikl = 0                      # n_cikl - количество циклов отбраковки
    if n0 > 5:
        while True:
            n = len(arr)   					# n - количество пар элементов в массиве до очередного цикла отбраковки
            a1 =  (n * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
                    (n * np.sum(np.square(arr[:,1])) - (np.square(np.sum(arr[:,1]))))   # a1 - нормативное значение a1
            a0 = (np.sum(arr, 0)[0] - a1 * np.sum(arr, 0)[1]) / n                     # нормативное значение a0
            if a0 <= 0:  # значения eps и р если a0 = 0
                a0 = 0
                a1 = np.sum(np.prod(arr, 1)) / np.sum(np.square(arr[:, 1]))
            epsn = a0 + arr[:,1] * a1       # нормативные значения epsilon (относительная деформация)
            if a0 > 0.0:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * a1 + a0 - arr[:, 0])) / (n - 2))  # среднее квадратическое отклонение (eps)
            else:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * a1 + a0 - arr[:, 0])) / (n - 1))
            if n < 201:
                vi = setV(n, recSetV)  # vi - значение критерия v при двусторонней доверительной вероятности а = 0,95
            else:
                vi = dc.Decimal(round(1.86664 * n ** 0.133, 2))
            vi = float(vi)
            valbrak = np.extract(np.abs(epsn - arr[:, 0]) > (vi * st), arr[:, 0])  # массив отбракованых значений (eps) после цикла проверки
            if len(valbrak) > 0:
                for i in range(0, len(valbrak)):
                    ind = np.where(arr == valbrak[i])
                    arr = np.delete(arr, ind[0], 0)
            list_brak += list(valbrak)
            nn = len(arr)  # nn - количество пар значений после цикла отбраковки
            n_cikl = n_cikl + 1  # n_cikl - количество циклов
            if n == nn:
                break
        avgeps = np.mean(arr, 0)[0]  # Среднеарифметическое значение eps
        V = st / avgeps  # Коэффициент корреляции eps
        xmin = np.min(arr, axis=0)   # минимальное значение eps, lnp
        xmax = np.max(arr, axis=0)   # максимальное значение eps, lnp
        lnpmin = xmin[1]          # логорифм минимальной нагрузки
        lnpmax = xmax[1]          # логарифм максимальной нагрузки
        pmin = np.min(recp)       # Минимальная нагрузка (нормальное напряжение)
        pmax = np.max(recp)       # Максимальная нагрузка (нормальное напряжение)
        lnpn = np.mean(arr[:,1], axis=0)      # среднее значение логарифма нагрузки
        epsn1 = a0 + lnpmin * a1  # нормативное значение eps при lnpmin
        epsn2 = a0 + lnpmax * a1  #  нормативное значение eps при lnpmax
        epsn = a0 + lnpn * a1  # нормативное значение eps при lnpn
        En = (lnpmax - lnpmin) / (epsn2 - epsn1)    # Логарифмированный модуль деформации нормативный без бетта
        En0 = (np.e ** lnpmax - np.e ** lnpmin) / (epsn2 - epsn1)   # Модуль деформации нормативный без бетта
        En0b = En0 * avgb   # Модуль деформации нормативный с учетом кф бетта
        G = (lnpmin - lnpn) / np.sqrt(np.sum(np.square(arr[:,1] - lnpn)))
        D = (lnpmax - lnpn) / np.sqrt(np.sum(np.square(arr[:,1] - lnpn)))
        l = np.round(np.sqrt(0.5 * (1 - (1 + n0 * G * D) / np.sqrt((1 + n0 * np.square(G)) * (1 + n0 * np.square(D))))), 2) # l - параметр, учитывающий значения диапазона pmin - pmax
        val = setVal(n0 - 2, l, recSetVal)  # коэффициент по таблице Ж.3
        de1 = val * st / np.sqrt(n0) * np.sqrt(1 + n0 * np.square((lnpmin - lnpn)) / (np.sum(np.square(arr[:, 1] - lnpn))))  # значения полудлин совместных доверительных интервалов
        de2 = val * st / np.sqrt(n0) * np.sqrt(1 + n0 * np.square((lnpmax - lnpn)) / np.sum(np.square(arr[:, 1] - lnpn)))
        eps1 = epsn1 - float(de1)    # расчетные значения eps при pmin
        eps2 = epsn2 - float(de2)    # расчетные значения eps при pmax
        if (eps1 / lnpmin) < (eps2 / lnpmax):   # расчет коэффициента надежности по грунту (g_eps)
            g_eps = ((epsn1 + epsn2) * lnpmax) / (eps2 * (lnpmin + lnpmax))
        else:
            g_eps = (epsn1 + epsn2) / (eps1 + eps2)
        Er = En0 / g_eps        # Расчетный модуль деформации без бетта
        Erb = En0b / g_eps      # Расчетный модуль деформации с учетом бетта
        list_x = [n_cikl, n0, nn, a1, a0, st, V, pmin, pmax, eps1, eps2, g_eps, En0b, Erb]
        list_x.extend(list_brak)
    elif n0 > 0:
        nn = n0
        xmin = np.min(arr, axis=0)  # минимальное значение eps, lnp
        xmax = np.max(arr, axis=0)  # максимальное значение eps, lnp
        pmin = np.min(recp)  # Минимальная нагрузка (нормальное напряжение)
        pmax = np.max(recp)  # Максимальная нагрузка (нормальное напряжение)
        lnpmin = xmin[1]  # логорифм минимальной нагрузки
        lnpmax = xmax[1]  # логарифм максимальной нагрузки
        lnpn = np.mean(arr[:, 1], axis=0)  # среднее значение логарифма нагрузки
        a1 = (n0 * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
               (n0 * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1]))))  # нормативное значение а1
        a0 = (np.sum(arr, 0)[0] - a1 * np.sum(arr, 0)[1]) / n0  # нормативное значение а0
        list_x = [n_cikl, n0, nn, a1, a0, None, None, pmin, pmax, None, None, None, None, None]
    else:
        list_x = [n_cikl, 0, 0, None, None, None, None, None, None, None, None, None, None, None]
    return list_x


def statcomprese(rece:list, recp:list, recb:list) -> list  :
    """Вычисление нормативного и расчетного значений модуля деформации с использованием аналитической аппроксимации
    компрессионной кривой по показателям e, p в заданном диапазоне нагрузок (0,1 - 0,2 МПа)"""
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv""")
        listSetV = curs.fetchall()           # Список Таблица Ж1
    with UseDatebase(dbconfig) as curs:
        curs.execute("""SELECT * FROM setv095""")
        listSetVal = curs.fetchall()         # Список Таблица Ж3
    arrvi = np.asarray(listSetV, dtype = np.float64)    # массив значений (vi) Таблица Ж1
    arrval = np.asarray(listSetVal, dtype = np.float64)  # Массив значений (val) Таблица Ж3
    avgb = np.average(np.asarray(recb, dtype = np.float64))         # Среднее значение коэффициента b (бетта)
    reclnp = np.log(np.asarray(recp, dtype = np.float64))       # reclnp - Натуральный логарифм нагрузок
    arrep0 = np.array([rece, reclnp], dtype = np.float64)       # arrep0 - начальный массив данных [[e], [lnp]] с e0
    arrep = np.ma.compress_cols(np.ma.masked_invalid(arrep0))   # arrep - начальный массив данных [[e], [lnp]] без e0
    arre0 = np.hsplit(arrep0, 3)[0][0]      # Массив природных коеффициентов пористости (e0)
    e0n = np.mean(arre0)
    arr = arrep.transpose()         # arr - начальный массив данных пар значений [e, lnp] без e0
    n0 = len(arr)                   # n0 - начальное количество пар значений
    list_brak = []                  # list_brak - список отбракованых значений
    n_cikl = 0                      # n_cikl - количество циклов отбраковки
    if n0 > 5:
        while True:
            n = len(arr)   			# n - количество пар элементов в массиве до очередного цикла отбраковки
            a1 =  np.abs((n * np.sum(np.prod(arr, axis = 1, dtype = np.float64)) - np.prod(np.sum(arr, axis = 0, dtype = np.float64))) / \
                    (n * np.sum(np.square(arr[:,1]), axis = 0) - (np.square(np.sum(arr[:,1], axis = 0)))))   # a1 - нормативное значение a1
            a0 = (np.sum(arr, axis = 0, dtype = np.float64)[0] - a1 * np.sum(arr, axis = 0, dtype = np.float64)[1]) / n     # нормативное значение a0
            if a0 <= 0:  # значения e и р если a0 = 0
                a0 = 0
                a1 = np.sum(np.prod(arr, 1), axis = 0) / np.sum(np.square(arr[:, 1]), axis = 0)
            en = a0 + arr[:,1] * a1       # нормативные значения коэффициента пористости (e) для каждого значения lnp
            if a0 > 0.0:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * a1 + a0 - arr[:, 0]), axis = 0) / (n - 2))  # среднее квадратическое отклонение (e)
            else:
                st = np.sqrt(np.sum(np.square(arr[:, 1] * a1 + a0 - arr[:, 0]), axis = 0) / (n - 1))
            if n < 201:
                vi = arrvi[n][1]   # vi - значение критерия v при двусторонней доверительной вероятности а = 0,95
            else:
                vi = np.float64(round(1.86664 * n ** 0.133, 2))
            valbrak = np.extract(np.abs(en - arr[:, 0]) > (vi * st), arr[:, 0])  # массив отбракованых значений (e) после цикла проверки
            if len(valbrak) > 0:
                for i in range(0, len(valbrak)):
                    ind = np.where(arr == valbrak[i])
                    arr = np.delete(arr, ind[0], 0)
            list_brak += list(valbrak)
            nn = len(arr)  # nn - количество пар значений после цикла отбраковки
            n_cikl = n_cikl + 1  # n_cikl - количество циклов
            if n == nn:
                break
        avge = np.mean(arr, 0)[0]     # Среднеарифметическое значение e
        V = st / avge                 # Коэффициент корреляции e
        xmin = np.min(arr, axis=0)   # минимальное значение [e, lnp]
        xmax = np.max(arr, axis=0)   # максимальное значение [e, lnp]
        Vc = st / (avge - xmin[0])  # Сравнительный коэффициент вариации
        lnpmin = xmin[1]          # логорифм минимальной нагрузки
        lnpmax = xmax[1]          # логарифм максимальной нагрузки
        pmin = np.e ** xmin[1]      # Минимальная нагрузка (нормальное напряжение)
        pmax = np.e ** xmax[1]      # Максимальная нагрузка (нормальное напряжение)
        lnpn = np.mean(arr[:,1], axis=0)      # среднее значение логарифма нагрузки
        en1 = a0 + lnpmin * a1  # нормативное значение e при lnpmin
        en2 = a0 + lnpmax * a1  #  нормативное значение e при lnpmax
        en0 = a0 + lnpn * a1  # нормативное значение e при lnpn
        lnm0 = (en1 - en2) / (lnpmax - lnpmin)    # Логарифмированный коэффициент сжимаемости
        m0 = np.abs((en1 - en2) / (np.e ** lnpmax - np.e ** lnpmin))    # Коэффициент сжимаемости
        En0 = (1 + e0n) / m0
        En0b = En0 * avgb   # Модуль деформации нормативный с учетом кф бетта
        G = (lnpmin - lnpn) / np.sqrt(np.sum(np.square(arr[:,1] - lnpn)))
        D = (lnpmax - lnpn) / np.sqrt(np.sum(np.square(arr[:,1] - lnpn)))
        l = np.round(np.sqrt(0.5 * (1 - (1 + n0 * G * D) / np.sqrt((1 + n0 * np.square(G)) * (1 + n0 * np.square(D))))), 2) # l - параметр, учитывающий значения диапазона pmin - pmax
        x,y,_ = arrval.T
        if nn > 102:
            nn = 102
        ka = nn - 2
        mask = ((x == ka) & (y == l))
        arrval_one = arrval[mask]   # Одна строка массива выбранная по маске
        val = arrval_one[0][2]	# коэффициент по таблице Ж.3
        de1 = val * st / np.sqrt(n0) * np.sqrt(1 + n0 * np.square((lnpmin - lnpn)) / np.sum(np.square(arr[:,1] - lnpn)))    # значения полудлины совместных доверительных интервалов при pmin
        de2 = val * st / np.sqrt(n0) * np.sqrt(1 + n0 * np.square((lnpmax - lnpn)) / np.sum(np.square(arr[:, 1] - lnpn)))   # значения полудлины совместных доверительных интервалов при pmax
        e1 = en1 - de1    # расчетные значения e при pmin
        e2 = en2 - de2    # расчетные значения e при pmax
        if (e1 / lnpmin) < (e2 / lnpmax):   # расчет коэффициента надежности по грунту (g_e)
            g_e = ((en1 + en2) * lnpmax) / (e2 * (lnpmin + lnpmax))
        else:
            g_e = (en1 + en2) / (e1 + e2)
        Er = En0 / g_e        # Расчетный модуль деформации без бетта
        Erb = En0b / g_e      # Расчетный модуль деформации с учетом бетта
        list_x = [n_cikl, n0, nn, a1, a0, st, V, Vc, pmin, pmax, e1, e2, g_e, En0b, Erb]
        list_x.extend(list_brak)
    elif n0 > 0:
        nn = n0
        xmin = np.min(arr, axis=0)  # минимальное значение e, lnp
        xmax = np.max(arr, axis=0)  # максимальное значение e, lnp
        pmin = np.min(recp)  # Минимальная нагрузка (нормальное напряжение)
        pmax = np.max(recp)  # Максимальная нагрузка (нормальное напряжение)
        lnpmin = xmin[1]  # логорифм минимальной нагрузки
        lnpmax = xmax[1]  # логарифм максимальной нагрузки
        lnpn = np.mean(arr[:, 1], axis=0)  # среднее значение логарифма нагрузки
        a1 = (n0 * np.sum(np.prod(arr, 1)) - np.prod(np.sum(arr, 0))) / \
               (n0 * np.sum(np.square(arr[:, 1])) - (np.square(np.sum(arr[:, 1]))))  # нормативное значение а1
        a0 = (np.sum(arr, 0)[0] - a1 * np.sum(arr, 0)[1]) / n0  # нормативное значение а0
        list_x = [n_cikl, n0, nn, a1, a0, None, None, None, pmin, pmax, None, None, None, None, None]
    else:
        list_x = [n_cikl, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None]
    return list_x
