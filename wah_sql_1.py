from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3 as sql

#################  заглушки, значения по умолчанию и тд.
SLOI, LEN_TEHN, itogo = 0, 0, 0
SLOI_1, nomer_vitrin = 1, 1
ohi, frak = " ", " "
ROSTER = [['']]
vitrina, baza_1, spisok_baz, spisok_rosterov, spisok_ynitov = [], [], [], [], []

### выделительные цвета
color = '#db6bc9'
color_1 = 'blue'
color_2 = 'red'
color_3 = '#FFF8DC'
color_4 = '#D3D3D3'

### координаты кнопок перелистывания
koordinat_stran = [[560, 620], [530, 590, 650], [500, 560, 620, 680], [470, 530, 590, 650, 710],
                   [440, 500, 560, 620, 680, 740], [410, 470, 530, 590, 650, 710, 770]]

def opred_frak(a):
    '''изменение значения фракции'''
    global frak
    frak = a


def izm_ohi(a): #
    ''' задание текста в вспомогательную строку (про ошибки и ход работы)'''
    global ohi
    ohi = a


def zapros_v_bazy_frakhii(a):
    '''запрос инфы из базы фракции'''
    opred_frak(a)
    global baza_1
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(f''' SELECT * FROM {a}''')
        v = list(cur)
        v_1 = []
        for i in v:
            v_1.append(list(i))
        v_2 = []
        for i in v_1:
            v_3 = []
            for l in i:
                if l != None:
                    v_3.append(l)
            v_2.append(v_3)
    baza_1 = v_2


def nahalo():
    '''эта функция узнаёт названия баз данных'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(''' SELECT name FROM sqlite_master WHERE type="table" AND name != "Rostera" ''')
        a_0 = list(cur)
        a = []
        for i in a_0:
            a.append(*i)
        a_1 = dict()
        for i in a:
            with sql.connect('baza_Waha_1.db') as con:
                cur = con.cursor()
                cur.execute(f''' SELECT nazv_ynita FROM {i} WHERE razdel = 0 ''')
                nazv = list(*cur)
                a_1.setdefault(*nazv, i)
    global spisok_baz
    spisok_baz = a_1


def form_spis_rosterov():
    '''формирование списка ростеров'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(''' SELECT nazv FROM Rostera ''')
        a = set(cur)
        a_2 = []
        for i in a:
            a_2.append(*i)
        return a_2


def form_spis_ynitov_v_rostere():
    '''формирование списка юнитов в ростере'''
    global nazvanie_rostera
    spisok_ynitov = []
    nazvanie_rostera = ROSTER[0][0]
    for i in ROSTER[1::]:
        spisok_ynitov.append(f'{i[2]} | {str(i[3])}')
    return spisok_ynitov


def sym_prais_ros():
    '''подсчет итоговой цены ростера'''
    global itogo
    itogo = 0
    for i in ROSTER[1::]:
        itogo += i[4]


def slo(a):
    '''переключение основного слоя'''
    global SLOI, nomer_vitrin
    izm_ohi(' ')
    nomer_vitrin = 1
    SLOI = a
    ui.setupUi(MainWindow)


def slo_1(a):
    '''переключение слоя второстепенного. нужно для 3 основного слоя'''
    global SLOI_1, nomer_vitrin, SLOI
    izm_ohi(' ')
    SLOI = 3
    nomer_vitrin = 1
    SLOI_1 = a
    ui.setupUi(MainWindow)


def formirovanie_vitrin (a, dlina):
    '''формирование витрины'''
    global vitrina, LEN_TEHN, nomer_vitrin
    vitrina = []
    l = 0
    vitrina_1 = []
    for i in a:
        vitrina_1.append(i)
        l += 1
        if l == dlina:
            vitrina.append(vitrina_1)
            l = 0
            vitrina_1 = []
    if len(vitrina_1):
        vitrina.append(vitrina_1)
    LEN_TEHN = len(vitrina)
    if len(vitrina) == 0:
        vitrina = [[]]
    try:        # это проверяет, закончилась ли страница витрины. и если закончилась возврацает на предыдущую
        t = vitrina[nomer_vitrin - 1]
    except:
        nomer_vitrin -= 1


def listanie_vitrin(a):
    '''перелистывание витрин (нужно, если кнопки не влазят в 1 лист)'''
    global nomer_vitrin
    nomer_vitrin = a
    ui.setupUi(MainWindow)


def del_iz_rostera(a):
    '''удаление юнита из ростера'''
    global ROSTER
    a = a.split(' | ')
    for i, l in enumerate(ROSTER[1::]):
        if l[2] == a[0] and l[3] == int(a[1]):
            nomer_del = i+1
    del ROSTER[nomer_del]


def ydalenie_rostera(nazv):
    '''удаление ростера'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(f''' DELETE FROM Rostera WHERE nazv = '{nazv}' ''')


def zagryz_rostera(nazv_r):
    '''загрузка ростера'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(f''' SELECT nazv, frak, ynit, ht, prais FROM Rostera WHERE nazv = "{nazv_r}" ''')
        c = list(cur)
        opred_frak(c[0][1])
        zapros_v_bazy_frakhii(c[0][1])
        global ROSTER
        ROSTER = [[nazv_r]]
        for i in c:
            ROSTER.append(list(i))
        slo(1)


def dobavl_ynita_v_roster(var, ynit):
    '''добавление нового юнита в ростер'''
    for i in baza_1:
        if i[1] == ynit[1]:
            a = i
            break
    if var == 1:
        ROSTER.append([ROSTER[0][0], frak, a[1], a[3], a[2]])
    elif var == 2:
        ROSTER.append([ROSTER[0][0], frak, a[1], a[5], a[4]])
    elif var == 3:
        ROSTER.append([ROSTER[0][0], frak, a[1], a[8], a[7]])
    elif var == 4:
        ROSTER.append([ROSTER[0][0], frak, a[1], a[10], a[9]])


def proverka_ynikal_nazv_rost(a):
    '''проверка уникальности названия ростера'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(f''' SELECT nazv FROM Rostera GROUP BY nazv ''')
        c = list(cur)
        c_1 = []
        for i in c:
            c_1.append(*i)
    if a in c_1:
        izm_ohi('ростер с таким названием уже есть. выберите другое, или удалите его.')
        return False
    else:
        return True


def vivid_bazi(a, b):
    '''кнопка-селектор. обрабатывае 6 вариантов запроса с заранее не известного количества кнопок.'''
    global ROSTER, nomer_vitrin
    izm_ohi(' ')
    if a == 1:  # начало создание нового ростера (с выбора фракции)
        if proverka_ynikal_nazv_rost(ui.textEdit.toPlainText()):
            ROSTER = []
            ROSTER.append([ui.textEdit.toPlainText()])
            zapros_v_bazy_frakhii(spisok_baz[vitrina[nomer_vitrin-1][b]])
            slo(3)
            slo_1(1)
            if len(ui.textEdit.toPlainText())<41:
                izm_ohi('можете приступать к формированию ростера.')
            else:
                izm_ohi('название слегка длинновато...')
    elif a == 2:        # удаление юнита из ростера.
        del_iz_rostera(vitrina[nomer_vitrin-1][b])
    elif a == 3:        # загрузка сохранённого ростера.
        zagryz_rostera(vitrina[nomer_vitrin-1][b])
    elif a == 4:        # добавление юнита в ростер (минемальный вариант).
        dobavl_ynita_v_roster(1, vitrina[nomer_vitrin-1][b])
    elif a == 5:        # добавление юнита в ростер (второй вариант).
        dobavl_ynita_v_roster(2, vitrina[nomer_vitrin - 1][b])
    elif a == 6:        # удаление сохранённого ростера.
        ydalenie_rostera(vitrina[nomer_vitrin-1][b])
    elif a == 7:        # добавление юнита в ростер (третий вариант).
        dobavl_ynita_v_roster(3, vitrina[nomer_vitrin - 1][b])
    elif a == 8:        # добавление юнита в ростер (четвёртый вариант).
        dobavl_ynita_v_roster(4, vitrina[nomer_vitrin - 1][b])
    ui.setupUi(MainWindow)


def otsev_nedopystim_povtorenii(a):
    '''отсев тех опций которые уже есть, и недопустимо их брать ещё.'''
    a_1 = []
    r = []
    for i in ROSTER[1::]:
        r.append(i[2])
    for i in a:
        if 'True' in i and i[1] in r:
            pass
        elif (i[0] != 2 and i[0] != 3) and r.count(i[1]) >= 3:
            pass
        elif (i[0] == 2 or i[0] == 3) and r.count(i[1]) >= 6:
            pass
        else:
            a_1.append(i)
    return a_1


def knopka_sohr_roster():
    '''сохранение ростера'''
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(''' SELECT nazv FROM Rostera GROUP BY nazv''')
        a = list(cur)
        a_2 = []
        for i in a:
            a_2.append(*i)
        if ROSTER[0][0] in a_2:
            cur.execute(f''' DELETE FROM Rostera WHERE nazv = '{ROSTER[0][0]}' ''')
        for i in ROSTER[1::]:
            cur.execute(f''' INSERT INTO Rostera VALUES('{i[0]}', '{i[1]}', '{i[2]}', {i[3]}, {i[4]})''')
    if len(ROSTER) == 1:
        izm_ohi('увы... ростер пуст. ')
    else:
        izm_ohi('готово!')
    ui.setupUi(MainWindow)

def podskaz_ikanomii(a):
    '''вывод цены юнита. на кнопку удаления.'''
    a = a.split(' | ')
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        try:
            cur.execute(f''' SELECT * FROM {frak} WHERE nazv_ynita = "{a[0]}" ''')
            c = list(*cur)
            if int(c[3]) == int(a[1]):
                return f'-{str(c[2])}'
            elif int(c[5]) == int(a[1]):
                return f'-{str(c[4])}'
            elif int(c[8]) == int(a[1]):
                return f'-{str(c[7])}'
            elif int(c[10]) == int(a[1]):
                return f'-{str(c[9])}'
        except:
            return ''

def nov_stroka (a):
    '''разбивка длинного названия на 2 строки.'''
    if len(a) <= 20:
        return a
    elif len(a) >= 20 and a[20] == ' ':
        return a[0:20:] + '\n' + a[20::]
    else:
        return a[0:20:] + '-\n' + a[20::]


def kostil_lambda(spisok, indeks):
    ''' функция "костыль". когда разберусь, как зациклить ламбду так,
    чтобы значение не терялось, переделаю. а пока это тут, чтобы было 1 такое чудовище вместо четырёх.'''
    try:
        spisok[0][0].clicked.connect(lambda: vivid_bazi(indeks, 0))
        spisok[1][0].clicked.connect(lambda: vivid_bazi(indeks, 1))
        spisok[2][0].clicked.connect(lambda: vivid_bazi(indeks, 2))
        spisok[3][0].clicked.connect(lambda: vivid_bazi(indeks, 3))
        spisok[4][0].clicked.connect(lambda: vivid_bazi(indeks, 4))
        spisok[5][0].clicked.connect(lambda: vivid_bazi(indeks, 5))
        spisok[6][0].clicked.connect(lambda: vivid_bazi(indeks, 6))
        spisok[7][0].clicked.connect(lambda: vivid_bazi(indeks, 7))
        spisok[8][0].clicked.connect(lambda: vivid_bazi(indeks, 8))
        spisok[9][0].clicked.connect(lambda: vivid_bazi(indeks, 9))
        spisok[10][0].clicked.connect(lambda: vivid_bazi(indeks, 10))
        spisok[11][0].clicked.connect(lambda: vivid_bazi(indeks, 11))
        spisok[12][0].clicked.connect(lambda: vivid_bazi(indeks, 12))
        spisok[13][0].clicked.connect(lambda: vivid_bazi(indeks, 13))
        spisok[14][0].clicked.connect(lambda: vivid_bazi(indeks, 14))
        spisok[15][0].clicked.connect(lambda: vivid_bazi(indeks, 15))
        spisok[16][0].clicked.connect(lambda: vivid_bazi(indeks, 16))
        spisok[17][0].clicked.connect(lambda: vivid_bazi(indeks, 17))
        spisok[18][0].clicked.connect(lambda: vivid_bazi(indeks, 18))
        spisok[19][0].clicked.connect(lambda: vivid_bazi(indeks, 19))
        spisok[20][0].clicked.connect(lambda: vivid_bazi(indeks, 20))
    except:
        pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        sym_prais_ros()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1220, 750)

        font_1, font_2, font_3, font_4, font_5 = QtGui.QFont(), QtGui.QFont(), QtGui.QFont(), QtGui.QFont(), QtGui.QFont()
        spisok_f = [[font_1, 9], [font_2, 10], [font_3, 12],  [font_4, 16],  [font_5, 20]]
        for i in spisok_f:
            i[0].setFamily("Segoe Print")
            i[0].setPointSize(i[1])
            i[0].setBold(True)
            i[0].setWeight(75)
        MainWindow.setFont(font_4)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        def raskidka_knopok(self, spis, obiekt, nohalo_x, nohalo_y, plys_x, plys_y, gabarit_1, gabarit_2,
                            v_1_riad=3, f=font_4, f_2=False, tekst='', fon=False):
            '''функция формирования и растановки неизвестного количества кнопок и надписей.'''
            vihod = []
            x = 0
            y = 0
            for i in spis:
                if f_2 != False:
                    i = nov_stroka (i)
                self.A = obiekt(self.centralwidget)
                self.A.setGeometry(QtCore.QRect(nohalo_x+x*plys_x, nohalo_y+y*plys_y, gabarit_1, gabarit_2))
                if f_2 != False and '\n' in i:
                    self.A.setFont(f_2)
                else:
                    self.A.setFont(f)
                if tekst == '':
                    I = i
                else:
                    I = tekst
                if fon == True:
                    self.A.setStyleSheet((f'background-color: {color_4}'))
                vihod.append([self.A, I])
                x += 1
                if x == v_1_riad:
                    x = 0
                    y += 1
            return vihod
###########################################################################################
        self.spi_label_1 = [["разработчик: Тарасов Д.Л.", 1020, 680, 180, 20, font_1],
                            [ohi, 230, 610, 700, 25, font_3], [f"ИТОГО:   {str(itogo)}.", 30, 660, 210, 40, font_4]]
        self.spi_label_1_poln =[]
        for i in self.spi_label_1:
            L = QtWidgets.QLabel(self.centralwidget)
            L.setGeometry(QtCore.QRect(i[1], i[2], i[3], i[4]))
            L.setFont(i[5])
            self.spi_label_1_poln.append([L, i[0]])
        self.spi_label_1_poln[1][0].setStyleSheet((f'color: {color_2}'))

        self.spi_push_1 = [["персонажи", 20, 20, 80, 3, 1], ["линия\nфронта", 220, 20, 80, 3, 2],
                           ["транспорт", 420, 20, 80, 3, 3], ["фортификации", 620, 20, 80, 3, 4],
                           ["другое", 820, 20, 80, 3, 5], ["доп. опции", 1020, 20, 80, 3, 6],
                           ["РОСТЭР", 520, 650, 50, 1, 0], ["новый ростер", 320, 650, 50, 0, 0],
                           ["загрузить", 720, 650, 50, 2, 0]
                           ]
        for i in self.spi_push_1:
            B = QtWidgets.QPushButton(self.centralwidget)
            B.setGeometry(QtCore.QRect(i[1], i[2], 180, i[3]))
            B.setFont(font_4)
            self.spi_label_1_poln.append([B, i[0]])

        if SLOI == 3 and SLOI_1 == 1:
            self.spi_label_1_poln[3][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 3 and SLOI_1 == 2:
            self.spi_label_1_poln[4][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 3 and SLOI_1 == 3:
            self.spi_label_1_poln[5][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 3 and SLOI_1 == 4:
            self.spi_label_1_poln[6][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 3 and SLOI_1 == 5:
            self.spi_label_1_poln[7][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 3 and SLOI_1 == 6:
            self.spi_label_1_poln[8][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 1:
            self.spi_label_1_poln[9][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 0:
            self.spi_label_1_poln[10][0].setStyleSheet((f'background-color: {color}'))
        if SLOI == 2:
            self.spi_label_1_poln[11][0].setStyleSheet((f'background-color: {color}'))

        self.spi_label_1_poln[3][0].clicked.connect(lambda: slo_1(1))
        self.spi_label_1_poln[4][0].clicked.connect(lambda: slo_1(2))
        self.spi_label_1_poln[5][0].clicked.connect(lambda: slo_1(3))
        self.spi_label_1_poln[6][0].clicked.connect(lambda: slo_1(4))
        self.spi_label_1_poln[7][0].clicked.connect(lambda: slo_1(5))
        self.spi_label_1_poln[8][0].clicked.connect(lambda: slo_1(6))
        self.spi_label_1_poln[9][0].clicked.connect(lambda: slo(1))
        self.spi_label_1_poln[10][0].clicked.connect(lambda: slo(0))
        self.spi_label_1_poln[11][0].clicked.connect(lambda: slo(2))


        if SLOI == 0:
            self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
            self.textEdit.setGeometry(QtCore.QRect(220, 180, 640, 50))

            self.label_16 = QtWidgets.QLabel(self.centralwidget)
            self.label_16.setGeometry(QtCore.QRect(220, 140, 110, 40))
            self.label_16.setFont(font_4)

            self.label_17 = QtWidgets.QLabel(self.centralwidget)
            self.label_17.setGeometry(QtCore.QRect(20, 240, 111, 40))
            self.label_17.setFont(font_4)

            formirovanie_vitrin(spisok_baz, 12)
            self.spisok_baz_1 = raskidka_knopok(self, vitrina[nomer_vitrin-1], QtWidgets.QPushButton,
                                                20, 290, 410, 75, 350, 50)
            kostil_lambda(self.spisok_baz_1, 1)


        if SLOI == 1:
            self.label_19 = QtWidgets.QLabel(self.centralwidget)
            self.label_19.setGeometry(QtCore.QRect(50, 120, 850, 40))
            self.label_19.setFont(font_5)
            global spisok_ynitov
            spisok_ynitov = form_spis_ynitov_v_rostere()
            formirovanie_vitrin(spisok_ynitov, 21)
            self.spisok_lab_1 = raskidka_knopok(self, vitrina[nomer_vitrin-1], QtWidgets.QLabel,
                                                30, 170, 400, 60, 320, 50, f=font_2, fon=True)
            self.spisok_del = raskidka_knopok(self, vitrina[nomer_vitrin-1], QtWidgets.QPushButton,
                                              360, 170, 400, 60, 50, 50, f=font_2)
            kostil_lambda(self.spisok_del, 2)

            self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_14.setGeometry(QtCore.QRect(1000, 590, 180, 50))
            self.pushButton_14.setFont(font_4)
            self.pushButton_14.clicked.connect(knopka_sohr_roster)


        if SLOI == 2:
            self.label_20 = QtWidgets.QLabel(self.centralwidget)
            self.label_20.setGeometry(QtCore.QRect(100, 140, 400, 50))
            self.label_20.setFont(font_5)
            global spisok_rosterov
            spisok_rosterov = form_spis_rosterov()
            formirovanie_vitrin(spisok_rosterov, 16)
            self.spisok_zagryz = raskidka_knopok(self, vitrina[nomer_vitrin-1], QtWidgets.QPushButton,
                                                 45, 230, 290, 100, 260, 60, v_1_riad=4, f=font_4, f_2=font_3)
            self.spisok_del_1 = raskidka_knopok(self, vitrina[nomer_vitrin-1], QtWidgets.QPushButton,
                                                175, 210, 290, 100, 130, 20, v_1_riad=4, f=font_2)
            kostil_lambda(self.spisok_zagryz, 3)
            kostil_lambda(self.spisok_del_1, 6)


        if SLOI == 3:
            x = 0
            y = 0
            self.spisok_ynitov = []
            self.spisok_ynitov_0 = []
            for i in baza_1:
                if i[0] == SLOI_1:
                    self.spisok_ynitov_0.append(i)
            self.spisok_ynitov_0 = otsev_nedopystim_povtorenii(self.spisok_ynitov_0)
            formirovanie_vitrin(self.spisok_ynitov_0, 14)
            for i in vitrina[nomer_vitrin-1]:
                self.a = []
                self.label_15 = QtWidgets.QLabel(self.centralwidget)
                self.label_15.setGeometry(QtCore.QRect(40 + x * 580, 190 + y * 60, 295, 40))
                self.label_15.setFont(font_2)
                if '(F.)' in i[1]:
                    self.label_15.setStyleSheet((f'color: {color_1}'))
                if '(L.)' in i[1]:
                    self.label_15.setStyleSheet((f'color: {color_2}'))
                if 'True' in i:
                    self.label_15.setStyleSheet((f'background-color: {color_3}'))
                    if '(F.)' in i[1]:
                        self.label_15.setStyleSheet((f'color: {color_1}; background-color: {color_3}'))
                    if '(L.)' in i[1]:
                        self.label_15.setStyleSheet((f'color: {color_2}; background-color: {color_3}'))
                self.a.append(self.label_15)

                self.pushButton_19 = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton_19.setGeometry(QtCore.QRect(350 + x * 580, 195 + y * 60, 50, 30))
                self.pushButton_19.setFont(font_3)
                self.a.append(self.pushButton_19)

                self.label_14 = QtWidgets.QLabel(self.centralwidget)
                self.label_14.setGeometry(QtCore.QRect(350 + x * 580, 170 + y * 60, 65, 20))
                self.label_14.setFont(font_2)
                self.a.append(self.label_14)

                if len(i) >= 7:
                    self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget)
                    self.pushButton_20.setGeometry(QtCore.QRect(420 + x * 580, 195 + y * 60, 50, 30))
                    self.pushButton_20.setFont(font_3)
                    self.a.append(self.pushButton_20)

                    self.label_13 = QtWidgets.QLabel(self.centralwidget)
                    self.label_13.setGeometry(QtCore.QRect(420 + x * 580, 170 + y * 60, 65, 20))
                    self.label_13.setFont(font_2)
                    self.a.append(self.label_13)

                if len(i) >= 9:
                    self.pushButton_30 = QtWidgets.QPushButton(self.centralwidget)
                    self.pushButton_30.setGeometry(QtCore.QRect(490 + x * 580, 195 + y * 60, 50, 30))
                    self.pushButton_30.setFont(font_3)
                    self.a.append(self.pushButton_30)

                    self.label_31 = QtWidgets.QLabel(self.centralwidget)
                    self.label_31.setGeometry(QtCore.QRect(490 + x * 580, 170 + y * 60, 65, 20))
                    self.label_31.setFont(font_2)
                    self.a.append(self.label_31)

                if len(i) >= 11:
                    self.pushButton_40 = QtWidgets.QPushButton(self.centralwidget)
                    self.pushButton_40.setGeometry(QtCore.QRect(560 + x * 580, 195 + y * 60, 50, 30))
                    self.pushButton_40.setFont(font_3)
                    self.a.append(self.pushButton_40)

                    self.label_41 = QtWidgets.QLabel(self.centralwidget)
                    self.label_41.setGeometry(QtCore.QRect(560 + x * 580, 170 + y * 60, 65, 20))
                    self.label_41.setFont(font_2)
                    self.a.append(self.label_41)

                self.spisok_ynitov.append([self.a, i])
                x += 1
                if x == 2:
                    x = 0
                    y += 1
            # этот кадавр вариация решения тойже проблемы что и kostil_lambda.
            # иначе ламбда сбивает значение всех кнопок в последнее
            try:
                self.spisok_ynitov[0][0][1].clicked.connect(lambda: vivid_bazi(4, 0))
                try:
                    self.spisok_ynitov[0][0][3].clicked.connect(lambda: vivid_bazi(5, 0))
                    self.spisok_ynitov[0][0][5].clicked.connect(lambda: vivid_bazi(7, 0))
                    self.spisok_ynitov[0][0][7].clicked.connect(lambda: vivid_bazi(8, 0))
                except:
                    pass
                self.spisok_ynitov[1][0][1].clicked.connect(lambda: vivid_bazi(4, 1))
                try:
                    self.spisok_ynitov[1][0][3].clicked.connect(lambda: vivid_bazi(5, 1))
                    self.spisok_ynitov[1][0][5].clicked.connect(lambda: vivid_bazi(7, 1))
                    self.spisok_ynitov[1][0][7].clicked.connect(lambda: vivid_bazi(8, 1))
                except:
                    pass
                self.spisok_ynitov[2][0][1].clicked.connect(lambda: vivid_bazi(4, 2))
                try:
                    self.spisok_ynitov[2][0][3].clicked.connect(lambda: vivid_bazi(5, 2))
                    self.spisok_ynitov[2][0][5].clicked.connect(lambda: vivid_bazi(7, 2))
                    self.spisok_ynitov[2][0][7].clicked.connect(lambda: vivid_bazi(8, 2))
                except:
                    pass
                self.spisok_ynitov[3][0][1].clicked.connect(lambda: vivid_bazi(4, 3))
                try:
                    self.spisok_ynitov[3][0][3].clicked.connect(lambda: vivid_bazi(5, 3))
                    self.spisok_ynitov[3][0][5].clicked.connect(lambda: vivid_bazi(7, 3))
                    self.spisok_ynitov[3][0][7].clicked.connect(lambda: vivid_bazi(8, 3))
                except:
                    pass
                self.spisok_ynitov[4][0][1].clicked.connect(lambda: vivid_bazi(4, 4))
                try:
                    self.spisok_ynitov[4][0][3].clicked.connect(lambda: vivid_bazi(5, 4))
                    self.spisok_ynitov[4][0][5].clicked.connect(lambda: vivid_bazi(7, 4))
                    self.spisok_ynitov[4][0][7].clicked.connect(lambda: vivid_bazi(8, 4))
                except:
                    pass
                self.spisok_ynitov[5][0][1].clicked.connect(lambda: vivid_bazi(4, 5))
                try:
                    self.spisok_ynitov[5][0][3].clicked.connect(lambda: vivid_bazi(5, 5))
                    self.spisok_ynitov[5][0][5].clicked.connect(lambda: vivid_bazi(7, 5))
                    self.spisok_ynitov[5][0][7].clicked.connect(lambda: vivid_bazi(8, 5))
                except:
                    pass
                self.spisok_ynitov[6][0][1].clicked.connect(lambda: vivid_bazi(4, 6))
                try:
                    self.spisok_ynitov[6][0][3].clicked.connect(lambda: vivid_bazi(5, 6))
                    self.spisok_ynitov[6][0][5].clicked.connect(lambda: vivid_bazi(7, 6))
                    self.spisok_ynitov[6][0][7].clicked.connect(lambda: vivid_bazi(8, 6))
                except:
                    pass
                self.spisok_ynitov[7][0][1].clicked.connect(lambda: vivid_bazi(4, 7))
                try:
                    self.spisok_ynitov[7][0][3].clicked.connect(lambda: vivid_bazi(5, 7))
                    self.spisok_ynitov[7][0][5].clicked.connect(lambda: vivid_bazi(7, 7))
                    self.spisok_ynitov[7][0][7].clicked.connect(lambda: vivid_bazi(8, 7))
                except:
                    pass
                self.spisok_ynitov[8][0][1].clicked.connect(lambda: vivid_bazi(4, 8))
                try:
                    self.spisok_ynitov[8][0][3].clicked.connect(lambda: vivid_bazi(5, 8))
                    self.spisok_ynitov[8][0][5].clicked.connect(lambda: vivid_bazi(7, 8))
                    self.spisok_ynitov[8][0][7].clicked.connect(lambda: vivid_bazi(8, 8))
                except:
                    pass
                self.spisok_ynitov[9][0][1].clicked.connect(lambda: vivid_bazi(4, 9))
                try:
                    self.spisok_ynitov[9][0][3].clicked.connect(lambda: vivid_bazi(5, 9))
                    self.spisok_ynitov[9][0][5].clicked.connect(lambda: vivid_bazi(7, 9))
                    self.spisok_ynitov[9][0][7].clicked.connect(lambda: vivid_bazi(8, 9))
                except:
                    pass
                self.spisok_ynitov[10][0][1].clicked.connect(lambda: vivid_bazi(4, 10))
                try:
                    self.spisok_ynitov[10][0][3].clicked.connect(lambda: vivid_bazi(5, 10))
                    self.spisok_ynitov[10][0][5].clicked.connect(lambda: vivid_bazi(7, 10))
                    self.spisok_ynitov[10][0][7].clicked.connect(lambda: vivid_bazi(8, 10))
                except:
                    pass
                self.spisok_ynitov[11][0][1].clicked.connect(lambda: vivid_bazi(4, 11))
                try:
                    self.spisok_ynitov[11][0][3].clicked.connect(lambda: vivid_bazi(5, 11))
                    self.spisok_ynitov[11][0][5].clicked.connect(lambda: vivid_bazi(7, 11))
                    self.spisok_ynitov[11][0][7].clicked.connect(lambda: vivid_bazi(8, 11))
                except:
                    pass
                self.spisok_ynitov[12][0][1].clicked.connect(lambda: vivid_bazi(4, 12))
                try:
                    self.spisok_ynitov[12][0][3].clicked.connect(lambda: vivid_bazi(5, 12))
                    self.spisok_ynitov[12][0][5].clicked.connect(lambda: vivid_bazi(7, 12))
                    self.spisok_ynitov[12][0][7].clicked.connect(lambda: vivid_bazi(8, 12))
                except:
                    pass
                self.spisok_ynitov[13][0][1].clicked.connect(lambda: vivid_bazi(4, 13))
                try:
                    self.spisok_ynitov[13][0][3].clicked.connect(lambda: vivid_bazi(5, 13))
                    self.spisok_ynitov[13][0][5].clicked.connect(lambda: vivid_bazi(7, 13))
                    self.spisok_ynitov[13][0][7].clicked.connect(lambda: vivid_bazi(8, 13))
                except:
                    pass
            except:
                pass
#############################################################################################
        if LEN_TEHN > 1:
            self.spis_rastan_knopok = []
            for i in koordinat_stran[LEN_TEHN - 2]:
                a = QtWidgets.QPushButton(self.centralwidget)
                a.setGeometry(QtCore.QRect(i, 120, 40, 30))
                a.setFont(font_4)
                self.spis_rastan_knopok.append(a)

            self.spis_rastan_knopok[0].clicked.connect(lambda: listanie_vitrin(1))
            if nomer_vitrin == 1:
                self.spis_rastan_knopok[0].setStyleSheet((f'background-color: {color}'))

            self.spis_rastan_knopok[1].clicked.connect(lambda: listanie_vitrin(2))
            if nomer_vitrin == 2:
                self.spis_rastan_knopok[1].setStyleSheet((f'background-color: {color}'))

            if len(self.spis_rastan_knopok) > 2:
                self.spis_rastan_knopok[2].clicked.connect(lambda: listanie_vitrin(3))
                if nomer_vitrin == 3:
                    self.spis_rastan_knopok[2].setStyleSheet((f'background-color: {color}'))

            if len(self.spis_rastan_knopok) > 3:
                self.spis_rastan_knopok[3].clicked.connect(lambda: listanie_vitrin(4))
                if nomer_vitrin == 4:
                    self.spis_rastan_knopok[3].setStyleSheet((f'background-color: {color}'))

            if len(self.spis_rastan_knopok) > 4:
                self.spis_rastan_knopok[4].clicked.connect(lambda: listanie_vitrin(5))
                if nomer_vitrin == 5:
                    self.spis_rastan_knopok[4].setStyleSheet((f'background-color: {color}'))

            if len(self.spis_rastan_knopok) > 5:
                self.spis_rastan_knopok[5].clicked.connect(lambda: listanie_vitrin(6))
                if nomer_vitrin == 6:
                    self.spis_rastan_knopok[5].setStyleSheet((f'background-color: {color}'))

            if len(self.spis_rastan_knopok) > 6:
                self.spis_rastan_knopok[6].clicked.connect(lambda: listanie_vitrin(7))
                if nomer_vitrin == 7:
                    self.spis_rastan_knopok[6].setStyleSheet((f'background-color: {color}'))

################################################################################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1220, 43))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f'{frak}'))
        for i in self.spi_label_1_poln:
            i[0].setText(_translate("MainWindow", i[1]))

        if SLOI == 0:
            self.label_16.setText(_translate("MainWindow", "название:"))
            self.label_17.setText(_translate("MainWindow", "фракция:"))
            for i in self.spisok_baz_1:
                i[0].setText(_translate("MainWindow", i[1]))

        if SLOI == 1:

            for i in self.spisok_lab_1:
                i[0].setText(_translate("MainWindow", i[1]))
            for i in self.spisok_del:
                i[0].setText(_translate("MainWindow", f'del\n{podskaz_ikanomii(i[1])}'))
            self.label_19.setText(_translate("MainWindow", nazvanie_rostera))
            self.pushButton_14.setText(_translate("MainWindow", "сохранить"))

        if SLOI == 2:
            self.label_20.setText(_translate("MainWindow", "сохранённые ростера:"))
            for i in self.spisok_zagryz:
                i[0].setText(_translate("MainWindow", i[1]))
            for i in self.spisok_del_1:
                i[0].setText(_translate("MainWindow", 'del'))

        if SLOI == 3:
            for i in self.spisok_ynitov:
                i[0][0].setText(_translate("MainWindow", i[1][1]))
                i[0][1].setText(_translate("MainWindow", str(i[1][2])))
                i[0][2].setText(_translate("MainWindow", f"{str(i[1][3])} шт."))
                if len(i[1]) >= 7:
                    i[0][3].setText(_translate("MainWindow", str(i[1][4])))
                    i[0][4].setText(_translate("MainWindow", f"{str(i[1][5])} шт."))
                if len(i[1]) >= 9:
                    i[0][5].setText(_translate("MainWindow", str(i[1][7])))
                    i[0][6].setText(_translate("MainWindow", f"{str(i[1][8])} шт."))
                if len(i[1]) >= 11:
                    i[0][7].setText(_translate("MainWindow", str(i[1][9])))
                    i[0][8].setText(_translate("MainWindow", f"{str(i[1][10])} шт."))

        if LEN_TEHN > 1:
            for l, i in enumerate(self.spis_rastan_knopok):
                i.setText(_translate("MainWindow", str(l+1)))


nahalo()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
