#!/bin/python
#-*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt4 import QtCore, QtGui
from objects import Object, Tile, Switch, MeasuringInstrument

from ui_main_window import Ui_subStationSim
from ui_open_layout import Ui_openLayout
from ui_object_properties import Ui_ObjectProperties
from ui_switch_action import Ui_SwitchAction

DB = 'data.db'

class StartQt4(QtGui.QMainWindow):
    '''Główne okno programu'''

    open_layout_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(StartQt4, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.ui = Ui_subStationSim()
        self.ui.setupUi(self)

        layout_list = self.get_layouts()
        layout_list.sort()

        for layout in layout_list:
            self.ui.layout_list.addItem(layout)

        self.setFixedSize(595, 372)
        self.setWindowTitle('SubStationSimulator')
        self.show()

        self.ui.open_button.clicked.connect(self.open_layout)
        self.ui.new_button.clicked.connect(self.new_layout)
        self.ui.edit_button.clicked.connect(self.edit_layout)
        self.ui.delete_button.clicked.connect(self.delete_layout)

    def get_layouts(self):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT layout_name FROM Objects')
        rows = c.fetchall()
        conn.close()

        #usuwa duplikaty, tworząc kolekcje
        layout_list = list(set(row[0] for row in rows))

        return layout_list

    def delete_layout(self):
    	
    	if self.ui.layout_list.selectedItems():
            layout_name = unicode(self.ui.layout_list.selectedItems()[0].text())
            msg = u'Czy napewno usunąć układ stacji ' + layout_name + ' ?'
            reply = QtGui.QMessageBox.question(self, u'Usunięcie układu',
                             msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                conn = sqlite3.connect(DB)
                c = conn.cursor()
                c.execute("DELETE FROM Objects WHERE layout_name='%s'" % layout_name)
                conn.commit()
                conn.close()

                item = self.ui.layout_list.takeItem(self.ui.layout_list.currentRow())
                item = None

    def open_layout(self):
        if self.ui.layout_list.selectedItems():
            self.layout = OpenLayout(self.ui.layout_list.selectedItems()[0].text())

    def edit_layout(self):
        if self.ui.layout_list.selectedItems():
            self.layout= EditLayout(self.ui.layout_list.selectedItems()[0].text())

    def new_layout(self):
            text, ok = QtGui.QInputDialog.getText(self, u'Nowy układ stacji',
                u'Podaj nazwę układu:')

            if ok:
                layout_name = text
                if layout_name:
                    #sprawdzenie czy podana nazwa już istnieje
                    conn = sqlite3.connect(DB)
                    c = conn.cursor()
                    c.execute("SELECT id FROM objects WHERE layout_name='%s'" % layout_name)
                    row = c.fetchone()
                    conn.close()
                    if row:
                        q = QtGui.QMessageBox(QtGui.QMessageBox.Warning, u'Błąd', u'Układ o podanej nazwie istnieje')
                        q.setStandardButtons(QtGui.QMessageBox.Ok);
                        q.exec_()
                    else:
                        #dodanie nowego układu do listy oraz otworzenie okna edycji
                        self.ui.layout_list.addItem(layout_name)
                        self.layout = EditLayout(layout_name)

class Layout(QtGui.QMainWindow):
    '''Klasa po której inne klasy dziedziczą make_board i make_object'''

    def make_board(self):
        self.board = []

        self.board = [[Tile(x, y) for y in range(Board.HEIGHT + 1)] \
                for x in range(Board.WIDTH + 1)]

    def make_objects(self):
        self.objects = []
        #pobranie obiektów z bazy danych 
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM objects WHERE layout_name='%s'" % self.layout_name)
        rows = c.fetchall()
        conn.close()

        self.type_list = ('line', 'bus', 'node', 'disconnector', 'circuit_breaker', 'earthing_switch', 'ct', 'vt')
        self.switch_list = self.type_list[3:6]
        self.measurement_list = self.type_list[6:8]

        for row in rows:
            #sprawdzenie poprawności danych
            try:
                if not isinstance(row[0], int) or row[0] < 1:
                    raise BadSQLData(row[0], u'Nieprawidłowy numer id')
                if not isinstance(row[1], int) or not (row[1] > 0 and row[1] < Board.WIDTH+1):
                    raise BadSQLData(row[1], u'Nieprawidłowa wartość współrzędnej x')
                if not isinstance(row[2], int) or not (row[2] > 0 and row[2] < Board.HEIGHT+1):
                    raise BadSQLData(row[2], u'Nieprawidłowa wartość współrzędnej y')
                if row[3] not in self.type_list:
                    raise BadSQLData(row[3], u'Nieprawidłowy typ obiektu')
                if not isinstance(row[5], int) or row[5]>16 or row[5]<0:
                    raise BadSQLData(row[5], u'Nieprawidłowa wartość połączenia do obiektów sąsiadujących')
                if (row[6]!=1 and row[6]!=0) if row[3] in self.switch_list+self.measurement_list else False:
                    raise BadSQLData(row[6], u'Nieprawidłowy stan obiektu (L1)')
                if (row[7]!=1 and row[7]!=0) if row[3] in self.switch_list+self.measurement_list else False:
                    raise BadSQLData(row[7], u'Nieprawidłowy stan obiektu (L2)')
                if (row[8]!=1 and row[8]!=0) if row[3] in self.switch_list+self.measurement_list else False:
                    raise BadSQLData(row[8], u'Nieprawidłowy stan obiektu (L3)')
                if (row[9]!=1 and row[9]!=0) if row[3] in self.switch_list else False:
                    raise BadSQLData(row[9], u'Nieprawidłowy stan styków obiektu (L1)')
                if (row[10]!=1 and row[10]!=0) if row[3] in self.switch_list else False:
                    raise BadSQLData(row[10], u'Nieprawidłowy stan styków obiektu (L2)')
                if (row[11]!=1 and row[11]!=0) if row[3] in self.switch_list else False:
                    raise BadSQLData(row[11], u'Nieprawidłowy stan styków obiektu (L3)')
                if not isinstance(row[12], int) and not isinstance(row[12], float) if row[3] in self.measurement_list else False:
                    raise BadSQLData(row[12], u'Nieprawidłowa wartość pomiarowa L1')
                if not isinstance(row[13], int) and not isinstance(row[13], float) if row[3] in self.measurement_list else False:
                    raise BadSQLData(row[13], u'Nieprawidłowa wartość pomiarowa L2')
                if not isinstance(row[14], int) and not isinstance(row[14], float) if row[3] in self.measurement_list else False:
                    raise BadSQLData(row[14], u'Nieprawidłowa wartość pomiarowa L3')
            except BadSQLData as ex:
                msg = ex.msg + ': ' + unicode(ex.value)
                q = QtGui.QMessageBox(QtGui.QMessageBox.Warning, u'Błąd bazy danych', msg)
                q.setStandardButtons(QtGui.QMessageBox.Ok);
                q.exec_()
                break
            x = row[1]
            y = row[2]
            obj_type = row[3]
            #jeśli na danym kafelku istnieje już szyna badz linia to zajmij  go
            #max 2 szyny/linie na jednym kafelku, pozostałe obiekty dopuszczalne po 1 na kafelek
            if self.board[x][y].occupied:
                if obj_type in ('bus', 'line'):
                    if self.board[x][y].overlap:
                        continue
                    else:
                        self.board[x][y].overlap = True
                else:
                    continue
            else:
                self.board[x][y].occupied = True
            #ustawienie rozszerzenia obiektu jako obiekt dwustanowy lub urzadzenie pomiarowe na podstawie typu obiektu
            object_switch = None
            object_measurement = None
            if row[3] in self.switch_list:
                object_switch = Switch(status_l1=row[6], status_l2=row[7], status_l3=row[8],\
                                        contacts_state_l1=row[9], contacts_state_l2=row[10], contacts_state_l3=row[11])
            if row[3] in self.measurement_list:
                object_measurement = MeasuringInstrument(row[6], row[7], row[8], row[12], row[13], row[14])

            object = Object(id=row[0], x=row[1], y=row[2], type=row[3], connected_to=row[5], switch=object_switch, measurement=object_measurement)
            #referencja do obiektu układu, pozwala na dostęp do listy obiektów i tablicy kafelków z obiektu
            object.layout = self
            self.objects.append(object)

    def get_objects(self, x, y):
        objects = []
        for object in self.objects:
            if object.x == x and object.y == y:
                objects.append(object)
        if objects:
            return objects
        else:
            return None

class OpenLayout(Layout):
    '''Okno otwierające symulację stacji'''

    def __init__(self, layout_name):
        super(OpenLayout, self).__init__()
        self.layout_name = unicode(layout_name)
        self.initUi()

    def initUi(self):

        if self.layout_name:
            self.ui = Ui_openLayout()
            self.ui.setupUi(self)

            self.frame = Board()
            self.frame.owner = self
            self.make_board()
            self.make_objects()

            self.setCentralWidget(self.frame)

            self.resize(1100, 550)
            self.setWindowTitle(u'Symulacja ' + self.layout_name)
            self.show()

    def resizeEvent(self, event):
        #skaluj do podanych proporcji
        new_size = QtCore.QSize(2, 1)
        new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
        self.resize(new_size)

class EditLayout(Layout):
    '''Okno edycji układu stacji'''

    def __init__(self, layout_name):
        super(EditLayout, self).__init__()
        self.layout_name = unicode(layout_name)
        self.initUi()

    def initUi(self):

        if self.layout_name:
            self.ui = Ui_openLayout()
            self.ui.setupUi(self)

            self.frame = EditBoard()
            self.frame.owner = self
            self.make_board()
            self.make_objects()

            self.statusBar()

            exit_action = QtGui.QAction(QtGui.QIcon('icons/exit.png'), u'&Wyjście', self)
            exit_action.setStatusTip(u'Zamknięcie okna edycji')
            exit_action.triggered.connect(self.close_window)

            save_action= QtGui.QAction(QtGui.QIcon('icons/save.png'),'&Zapisz', self)
            save_action.setStatusTip(u'Zapisanie zmian na dysku')
            save_action.triggered.connect(self.save_changes)

            #ustawienie paska menu
            menubar = self.menuBar()
            filemenu = menubar.addMenu("&Plik")
            filemenu.addAction(save_action)
            filemenu.addAction(exit_action)
            modemenu = menubar.addMenu("&Tryb edycji")

            helpmenu = menubar.addMenu("&Pomoc")
            help_names = ("Pomoc", "O Aplikacji")
            help_functions = ("help", "about")
            i=0
            for name, function in zip(help_names, help_functions):
                action = QtGui.QAction(QtGui.QIcon('icons/'+function+'.png'), '&'+name, self)
                action.value = i
                action.triggered.connect(self.help_dialog)
                helpmenu.addAction(action)
                i+=1 

            toolbar_names = ( u'Szyna', u'Linia', u'Węzeł', u'Wyłącznik', u'Odłącznik',
                             u'Uziemnik', u'Przekładnik prądowy', u'Przekładnik napięciowy',
                             u'Obracanie obiektów', u'Usuwanie obiektów')
            toolbar_functions = ( u'bus', u'line', u'node', u'circuit_breaker', u'disconnector',
                                 u'earthing_switch', u'ct', u'vt', u'rotate', u'delete')  
            toolbar_buttons = []

            group = QtGui.QActionGroup(self)
            for name, function in zip(toolbar_names, toolbar_functions):
                button = QtGui.QAction(QtGui.QIcon('icons/'+function+'.png'), name, group)
                button.function = function
                button.name = name
                button.setCheckable( True)
                button.triggered.connect(self.frame.change_mode)
                toolbar_buttons.append(button)

            #ustawienie paska narzędzi
            self.toolbar = self.addToolBar(u'Narzędzia')
            for i in range(0, len(toolbar_buttons)):
                self.toolbar.addAction(toolbar_buttons[i])
                modemenu.addAction(toolbar_buttons[i])

            self.setCentralWidget(self.frame)

            self.resize(1100, 625)
            self.setWindowTitle('Edycja ' + unicode(self.layout_name))
            self.show()

    def add_object(self, new_obj):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        record = [new_obj.x, new_obj.y, new_obj.type, self.layout_name, new_obj.connected_to]
        if new_obj.type in self.switch_list:
            record = record +[status for status in new_obj.switch.status] + [contacts_state for contacts_state in new_obj.switch.contacts_state]
            c.execute("INSERT INTO objects (x, y , type, layout_name, connected_to, status_l1, status_l2, status_l3,\
                    contacts_state_l1, contacts_state_l2, contacts_state_l3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , record)
        elif new_obj.type in self.measurement_list:
            record = record + [status for status in new_obj.measurement.status] + [measurement for measurement in new_obj.measurement.measurement]
            c.execute("INSERT INTO objects (x, y , type, layout_name, connected_to, status_l1, status_l2, status_l3,\
                    measurement_l1, measurement_l2, measurement_l3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , record)
        else:
            c.execute("INSERT INTO objects (x, y , type, layout_name, connected_to)\
                       VALUES (?, ?, ?, ?, ?)" , record)

        conn.commit()
        #ustaw id obiektu w liście wczytanych aplikacji
        new_obj.id = c.lastrowid
        conn.close()

    def delete_object(self, id):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("DELETE FROM objects WHERE id='%s'" % id)
        conn.commit()
        conn.close()

    def update_object(self, obj):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        record = [obj.x, obj.y, obj.type, self.layout_name, obj.connected_to, obj.id]
        if obj.type in self.switch_list:
            record = record +[status for status in obj.switch.status] + [contacts_state for contacts_state in obj.switch.contacts_state]+[obj.id,]
            c.execute("UPDATE objects SET x=?, y=?, type=?, layout_name=?, connected_to=?, status_l1=?, status_l2=?, status_l3=?,\
                      contacts_state_l1=?, contacts_state_l2=?, contacts_state_l3=? WHERE id=?" , record)
        elif obj.type in self.measurement_list:
            record = record + [status for status in obj.measurement.status] + [measurement for measurement in obj.measurement.measurement]+[obj.id,]
            c.execute("UPDATE objects SET x=?, y=?, type=?, layout_name=?, connected_to=?, status_l1=?, status_l2=?, status_l3=?,\
                       measurement_l1=?,measurement_l2=?, measurement_l3=? WHERE id=?" , record)
        else:
            c.execute("UPDATE objects SET x=?, y=?, type=?, layout_name=?, connected_to=? WHERE id=?" , record)
        conn.commit()
        conn.close()

    def get_id_from_db(self, x, y):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id FROM objects WHERE x=? and y=?", (x,y))
        rows = c.fetchall()
        conn.close()

        if rows:
            rows_list=[id for tuple in rows for id in tuple]
            return rows_list
        else:
            return None

    def save_changes(self):
        for x in range(1,Board.WIDTH+1):
            for y in range(1, Board.HEIGHT+1):
                if self.board[x][y].changed:
                    rows = self.get_id_from_db(x,y)
                    objects_list = self.get_objects(x, y)
                    if rows:
                        #jesli zmieniono i istnieje w aplikacji -> uaktualnij w bazie
                        if objects_list:
                            for object in objects_list:
                                self.update_object(object)
                                self.board[x][y].changed = False
                        else:
                            #jesli zmieniono, ale nie istnieje w aplikacji -> usun z bazy
                            for row in rows:
                                self.delete_object(row)
                                self.board[x][y].changed = False
                    else:
                        #jesli nie istnieje w bazie, a istnieje w aplikacji -> dodaj
                        if objects_list:
                            for object in objects_list:
                                self.add_object(object)
                                self.board[x][y].changed = False
        self.frame.update()

    def help_dialog(self):
        if self.sender().value == 0:
            msg = u"LPP - wykonanie akcji właściwej dla wybranego trybu edycji \
                   \nPPP - okno właściwości wybranego obiektu \
                   \n\nModifikatory: \
                   \nCtrl - szybkie obracanie obiektu \
                   \nShift - wykonanie akcji na szeregu sąsiadujących kafelków"
        else:
            msg = u"Autorzy:\ninż. Karol Kurek\ndr inz. Ryszard Kowalik"

        q = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Pomoc', msg)
        q.setStandardButtons(QtGui.QMessageBox.Ok)
        q.exec_()

    def close_window(self):
        '''sprawdzenie czy były dokonane zmiany, jeśli tak wyświetl ostrzeżenie'''
        is_changed = False
        for x in range(1,Board.WIDTH+1):
            for y in range(1, Board.HEIGHT+1):
                if self.board[x][y].changed:
                    is_changed = True
                    break
        if is_changed:
            q = QtGui.QMessageBox(QtGui.QMessageBox.Question, u'Niezapisane zmiany', u'Istnieją niezapisane zmiany, co chcesz zrobić?')
            exit = QtGui.QPushButton()
            exit.setText(u'Anuluj')
            exit.setIcon(QtGui.QIcon('icons/exit.png'))
            q.addButton(exit, QtGui.QMessageBox.RejectRole)

            save = QtGui.QPushButton()
            save.setText('Zapisz')
            save.setIcon(QtGui.QIcon('icons/save.png'))
            save.clicked.connect(self.save_changes)
            q.addButton(save, QtGui.QMessageBox.YesRole)

            exit = QtGui.QPushButton()
            exit.setText(u'Wyjście')
            exit.setIcon(QtGui.QIcon('icons/exit.png'))
	    exit.clicked.connect(self.close)
            q.addButton(exit, QtGui.QMessageBox.NoRole)
            q.exec_()

    def resizeEvent(self, event):
        #skaluj do podanych proporcji
        new_size = QtCore.QSize(44, 25)
        new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
        self.resize(new_size)

class ObjectProperties(QtGui.QMainWindow):
    '''Okno dialogowe pozwalające zmienić właściwości wybranego obiektu'''

    def __init__(self, obj, owner):
        super(ObjectProperties, self).__init__()
        self.owner = owner
        self.obj = obj
        self.initUi()

    def initUi(self):
        self.ui = Ui_ObjectProperties()
        self.ui.setupUi(self)
        self.setWindowTitle(u'Właściwości obiektu ' + unicode(self.obj.id))

        self.ui.right.value = 0b0001
        self.ui.up.value = 0b0010
        self.ui.left.value = 0b0100
        self.ui.down.value = 0b1000

        #ustawienie stanu przycisków
        if self.obj.connected_to & 0b0001:
            self.ui.right.setChecked(True)
        if self.obj.connected_to & 0b0010:
            self.ui.up.setChecked(True)
        if self.obj.connected_to & 0b0100:
            self.ui.left.setChecked(True)
        if self.obj.connected_to & 0b1000:
            self.ui.down.setChecked(True)

        self.ui.left.clicked.connect(self.set_object_connection)
        self.ui.right.clicked.connect(self.set_object_connection)
        self.ui.up.clicked.connect(self.set_object_connection)
        self.ui.down.clicked.connect(self.set_object_connection)
        self.center_on_screen()
        self.show()

    def set_object_connection(self):
        #XOR
        self.obj.connected_to = self.obj.connected_to ^ self.sender().value
        self.owner.owner.board[self.obj.x][self.obj.y].changed = True
        self.owner.update()

    def center_on_screen(self):
        '''Ustawia okno dialogowe po środku ekranu'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

class SwitchAction(QtGui.QMainWindow):
    '''Okno dialogowe pozwalające na manipulację łącznikami'''

    def __init__(self, obj, owner):
        super(SwitchAction, self).__init__()
        self.owner = owner
        self.obj = obj
        self.initUi()

    def initUi(self):
        self.ui = Ui_SwitchAction()
        self.ui.setupUi(self)
        self.setWindowTitle(u'Łącznik ' + unicode(self.obj.id))

        self.status_tab = [self.ui.status_l1, self.ui.status_l2, self.ui.status_l3]
        self.frame_tab = [self.ui.contacts_state_l1_frame, self.ui.contacts_state_l2_frame, self.ui.contacts_state_l3_frame]
        self.open_tab= [self.ui.open_l1, self.ui.open_l2, self.ui.open_l3, self.ui.open]
        self.close_tab = [self.ui.close_l1, self.ui.close_l2, self.ui.close_l3, self.ui.close]
        #ustawienie przycisków statusu
        self.ui.status_l1.value = 0
        self.ui.status_l2.value = 1
        self.ui.status_l3.value = 2
        i=0
        for status in self.obj.switch.status:
            if status:
                self.status_tab[i].setChecked(True)
            i=i+1

        for status in self.status_tab:
            status.clicked.connect(self.set_status)

        #przycisk reset
        self.ui.reset.clicked.connect(self.reset_failure)
        #ustawienie statnu styków
        self.set_contacts_state()

        #ustawienie przyciskow trip
        self.ui.open_l1.value = [1, 0, 0]
        self.ui.close_l1.value = [1, 0, 0]
        self.ui.open_l2.value = [0, 1, 0]
        self.ui.close_l2.value = [0, 1, 0]
        self.ui.open_l3.value = [0, 0, 1]
        self.ui.close_l3.value = [0, 0, 1]
        self.ui.open.value = [1, 1, 1]
        self.ui.close.value = [1, 1, 1]
        #ustawienie działania otwarcie/zamknięcie
        for open in self.open_tab:
            open.closure = 0
        for close in self.close_tab:
            close.closure = 1
        for trip in self.open_tab+self.close_tab:
            trip.clicked.connect(self.set_trip)

        self.center_on_screen()
        self.show()

    def center_on_screen(self):
        '''Ustawia okno dialogowe po środku ekranu'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def reset_failure(self):
        self.obj.switch.failure = False
        self.owner.update()

    def set_trip(self):
        self.obj.switch.trip(self.sender().value, self.sender().closure)
        self.set_contacts_state()
        self.owner.update()

    def set_contacts_state(self):
        def color(state):
            red = '#FF7070'
            green = '#70FF70'
            if state:
                return red
            else:
                return green 
        i=0
        for frame in self.frame_tab:
            #frame.setStyleSheet("background-color: %s;" % color(self.obj.switch.status[i]))
            frame.setStyleSheet("background-color: %s;" % color(self.obj.switch.contacts_state[i]))
            frame.update()
            i=i+1

    def set_status(self):
       self.obj.switch.set_status(self.sender().value) 

class Board(QtGui.QFrame):
    WIDTH = 40
    HEIGHT = 20

    def __init__(self):
        super(Board, self).__init__()
        self.initBoard()

    def initBoard(self):
        self.start = 1

    def tile_size(self):
        return self.contentsRect().width() / Board.WIDTH

    def mousePressEvent(self, QMouseEvent):
        mouse_x = QMouseEvent.x()
        mouse_y = QMouseEvent.y()
        size = self.tile_size()
        x = int(mouse_x / size)+1
        y = int(mouse_y / size)+1

        #zmiana stanu łącznika
        clicked_object = None
        for object in self.owner.objects:
            if object.x == x and object.y == y:
                clicked_object = object

        if clicked_object:
            if clicked_object.switch:
                self.switch_action_window = SwitchAction(clicked_object, self)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        #qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        #ustaw id obiektu w liście wczytanych aplikacji
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        size = self.tile_size()
        self.draw_tiles(qp, size)
        self.draw_objects(qp, size)
        qp.end()

    def draw_tiles(self, qp, size):
        for x in range(Board.WIDTH+1):
            for y in range(Board.HEIGHT+1):
                self.owner.board[x][y].draw(qp, size)

    def draw_objects(self, qp, size):
        for object in self.owner.objects:
            object.draw(qp, size)

class EditBoard(Board):
    '''Tablica pozwajaląca na edycję układu stacji'''

    place_object_signal = QtCore.pyqtSignal()
    clear_object_signal = QtCore.pyqtSignal()
    rotate_object_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(EditBoard, self).__init__()
        self.mode = 'edit_property'
        self.start = None
        self.stop = None

        self.place_object_signal.connect(self.place_object)
        self.clear_object_signal.connect(self.clear_object)
        self.rotate_object_signal.connect(self.rotate_object)

    def change_mode(self, mode):
        source = self.sender()
        self.mode = source.function
        self.owner.statusBar().showMessage('Zmieniono tryb '+source.name)

    def mousePressEvent(self, event):
        global x, y
        mouse_x = event.x()
        mouse_y = event.y()
        size = self.tile_size()
        x = int(mouse_x / size)+1
        y = int(mouse_y / size)+1

        #Akcja na podstawie aktywowanego trybu
        #sprawdzenie czy wcisniete sa modyfikatory
        modifiers = QtGui.QApplication.keyboardModifiers()

        #jeśli wcisnięty shift to wstawiaj obiekty w linii start-stop
        if modifiers == QtCore.Qt.ShiftModifier:
            if not self.start:
                self.start = [x, y]
                self.owner.board[x][y].checked = True
                self.update()
            else:
                self.stop = [x, y]
                self.owner.board[self.start[0]][self.start[1]].checked = False
                self.update()
                #sprawdzenie czy linia obiektów będzie pionowa czy pozioma
                # 1- zmienna oś x, 2- zmienna oś y
                dim = None
                if self.start[0] == self.stop[0]:
                    dim = 1
                elif self.start[1] == self.stop[1]:
                    dim = 0

                if dim is not None:
                    #ustawienie liczb start/stop na odpowiednich miejscach
                    if self.start[dim] > self.stop[dim]:
                        (self.start[dim], self.stop[dim]) = (self.stop[dim], self.start[dim])
                    for i in range(self.start[dim], self.stop[dim]+1):
                        if dim == 1:
                            y = i
                            x = self.start[0]
                        else:
                            x = i
                            y = self.start[1]

                        #podjęcie akcji, wysłanie odpowiedniego sygnału, dla każdego z obiektów w linii
                        if self.mode in self.owner.type_list:
                            self.place_object_signal.emit()
                            #jesli linia lub szyna, dodatkowo obroc zgodnie z kieunkiem zaznaczenia
                            if self.mode in ('line', 'bus') and dim == 0:
                                self.rotate_object_signal.emit()

                        elif self.mode == 'delete':
                            self.clear_object_signal.emit()
                        elif self.mode == 'rotate':
                            self.rotate_object_signal.emit()
                self.start = None
                self.stop = None
        elif modifiers == QtCore.Qt.ControlModifier:
            self.rotate_object_signal.emit()
        elif event.button() == QtCore.Qt.LeftButton:
            if self.mode in self.owner.type_list:
                self.place_object_signal.emit()
            elif self.mode == 'delete':
                self.clear_object_signal.emit()
            elif self.mode == 'rotate':
                self.rotate_object_signal.emit()
        elif event.button() == QtCore.Qt.RightButton:
            clicked_object = None
            objects = self.owner.get_objects(x, y)

            if objects:
                for clicked_object in objects:
                    self.property_window = ObjectProperties(clicked_object, owner = self)

    def place_object(self):
        '''jeśli kliknięto w niezajęty kafelek, sprawdz w jakim trybie znajduje sie edytor i wypełnij konstr. obiektu'''

        clicked_object = None
        if not self.owner.board[x][y].occupied:
            if self.mode in self.owner.switch_list:
                switch_component = Switch(1,1,1,1,1,1)
                clicked_object = Object(x=x, y=y, type=self.mode, connected_to=(0b0010 if self.mode in ('earthing_switch') else 0b1010), switch=switch_component)
            elif self.mode in self.owner.measurement_list:
                measuring_component = MeasuringInstrument(1,1,1,0,0,0)
                clicked_object = Object(x=x, y=y, type=self.mode, connected_to=(0b0010 if self.mode in ('vt') else 0b1010), measurement=measuring_component)
            else:
                clicked_object = Object(x=x, y=y, type=self.mode, connected_to=(0b0010 if self.mode in ('node') else 0b1010))
        else:
            #obsługa zachodzących na siebie linii  i szyn
            if self.mode in ('bus', 'line') and not self.owner.board[x][y].overlap:
                #przeciwnie skierowana linia do już istniejącej
                present_object = self.owner.get_objects(x, y)
                if present_object[0].type in ('bus', 'line'):
                    if present_object[0].connected_to & 0b0101:
                        direction = 0b1010
                    else:
                        direction = 0b0101
                    clicked_object = Object(x=x, y=y, type=self.mode, connected_to=direction)
                    self.owner.board[x][y].overlap = True

        if clicked_object:
            clicked_object.layout = self.owner
            self.owner.board[x][y].occupied = True
            self.owner.board[x][y].changed = True
            self.owner.objects.append(clicked_object)
            self.update()

    def clear_object(self):
        '''usuwanie obiektów znajdujących się na klikniętym kafelku'''
        clicked_object = None
        objects = self.owner.get_objects(x, y)

        if objects:
            for clicked_object in objects:
                if self.owner.board[x][y].overlap:
                    self.owner.board[x][y].overlap = False
                else:
                    self.owner.board[x][y].occupied = False
                self.owner.board[x][y].changed = True
                del self.owner.objects[self.owner.objects.index(clicked_object)]
                self.update()

    def rotate_object(self):
        '''obracanie obiektów'''
        clicked_object = None

        clicked_objects = self.owner.get_objects(x, y)
        if clicked_objects:
            clicked_object = clicked_objects[0]
            if clicked_object.type in ('vt', 'earthing_switch', 'node'):
                if clicked_object.connected_to is not 0b1000:
                    clicked_object.connected_to = clicked_object.connected_to << 1
                else:
                    clicked_object.connected_to = 0b0001
            elif clicked_object.type in ('ct', 'circuit_breaker', 'disconnector'):
                if clicked_object.connected_to & 0b0101:
                    clicked_object.connected_to = 0b1010
                else:
                    clicked_object.connected_to = 0b0101
            else:
                #szyny i linie
                if clicked_object.connected_to & 0b0001 and clicked_object.connected_to & 0b0100:
                    clicked_object.connected_to = 0b1010
                elif clicked_object.connected_to & 0b0010 and clicked_object.connected_to & 0b1000:
                    clicked_object.connected_to = 0b0101

            self.owner.board[x][y].changed = True
            self.update()

class BadSQLData(Exception):
    '''Wyjątek obsługujący niepoprawne dane wczytane z bazy danych'''
    def __init__(self, value, msg):
        Exception.__init__(self)
        self.value = value
        if msg:
            self.msg = msg

def main():
        app = QtGui.QApplication(sys.argv)
        gui = StartQt4()

        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
