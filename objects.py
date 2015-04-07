#-*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sqlite3

DB = 'data.db'
LINE_WIDTH = 2
LINE_BOLD_WIDTH = 4

class Tile:
    '''Klasa reprezentująca kafelek tablicy'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.overlap = False
        self.checked = False
        self.changed = False 

    def draw(self, qp, size):
        #color = QtGui.QColor(255, 255, 255)
        #pen = QtGui.QPen(QtCore.Qt.white, 0, QtCore.Qt.NoPen)
        pen = QtGui.QPen(QtGui.QColor(200,200,200), 0, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        if self.checked:
            qp.setBrush(QtGui.QColor(184,239, 252))
        else:
            qp.setBrush(QtGui.QColor(255 ,255, 255))

        qp.drawRect((self.x-1)*size, (self.y-1)*size, \
                    size+1, size+1)
        if self.changed:
            qp.drawRect((self.x-1)*size, (self.y-1)*size, \
                        5, 5)

class Object:
    '''Klasa reprezentująca obiekt w rozdzielni'''

    def __init__(self, x, y, type, id = None, connected_to = 0b0010, switch = None, measurement = None):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.connected_to = connected_to
        self.draw = self.init_draw()
        
        self.switch = switch
        if self.switch:
            self.switch.owner = self

        self.measurement = measurement
        if self.measurement:
            self.measurement.owner = self

    def check_switch_state(self):
        '''funkcja ustalajaca wyświetlany stan łacznika'''
        '''zamknięty tylko jesli wszystkie fazy zamknięte''' 
        state = 1 #styki zamknięte
        for contacts_state in self.switch.contacts_state:
            if contacts_state == 0:
                state = 0
                break
        return state

    def draw_contacts_state(self, qp, size):
        '''funkcja rysuje przedstawienie graficzne stanu styków łącznika'''

        color_closed = QtGui.QColor(255,10,10)
        color_closed.setAlpha(70)
        color_opened = QtGui.QColor(110,255,110)
        color_opened.setAlpha(70)

        #wysokosc i szerokosc 
        width = size/3
        height = size
        x=0
        y=0

        for phase in self.switch.contacts_state:
            if phase:
                qp.setBrush(color_closed)
            else:
                qp.setBrush(color_opened)
            qp.drawRect(x, 0, width, height)
            x=x+width

    def init_draw(self):
        if self.type == 'bus':
            def draw(qp, size):
                #funkcja ustawiajaca grubosc olowka
                def set_pen_if_bus(hook, x, y):
                    objects = self.layout.get_objects(x, y)
                    
                    thick = 1 #flaga
                    if objects is not None:
                        for obj in objects:
                            if obj.type != 'bus' and obj.connected_to & hook:
                                thick = 0
                                break
                    if thick:
                        pen = QtGui.QPen(QtCore.Qt.black, LINE_BOLD_WIDTH, QtCore.Qt.SolidLine)
                    else:
                        pen = QtGui.QPen(QtCore.Qt.black, LINE_WIDTH, QtCore.Qt.SolidLine)
                    qp.setPen(pen)

                direction = ''
                #sprawdzenie czy linia będzie pionowa czy pozioma
                if self.connected_to & 0b0001 and self.connected_to & 0b0100:
                    direction = 'horizontal'
                elif self.connected_to & 0b0010 and self.connected_to & 0b1000:
                    direction = 'vertical'
                    
                #flaga, czy punkt odczepowy został już narysowany
                point = False
                #promien punktu odczepu
                rad = size/4

                qp.translate((self.x-1)*size, (self.y-1)*size)

                qp.setBrush(QtGui.QColor(0, 0, 0))
                #podłączenie do odpowiednich kafelków bocznych 
                if self.connected_to & 0b0001:
                    if direction == 'vertical' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    set_pen_if_bus(0b0100, self.x+1, self.y)
                    qp.drawLine((size/2), (size/2), size, (size/2))
                if self.connected_to & 0b0010:
                    if direction == 'horizontal' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad,rad)
                        point = True
                    set_pen_if_bus(0b1000, self.x, self.y-1)
                    qp.drawLine((size/2), (size/2), (size/2), 0)
                if self.connected_to & 0b0100:
                    if direction == 'vertical' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    set_pen_if_bus(0b0001, self.x-1, self.y)
                    qp.drawLine((size/2), (size/2), 0, (size/2))
                if self.connected_to & 0b1000:
                    if direction == 'horizontal' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    set_pen_if_bus(0b0010, self.x, self.y+1)
                    qp.drawLine((size/2), (size/2), (size/2), size)

                qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        if self.type == 'line':
            def draw(qp, size):
                pen = QtGui.QPen(QtCore.Qt.black, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)
                
                direction = ''
                #sprawdzenie czy linia będzie pionowa czy pozioma
                if self.connected_to & 0b0001 and self.connected_to & 0b0100:
                    direction = 'horizontal'
                elif self.connected_to & 0b0010 and self.connected_to & 0b1000:
                    direction = 'vertical'
                    
                #flaga, czy punkt odczepowy został już narysowany
                point = False
                #promien punktu odczepu
                rad = size/4

                qp.translate((self.x-1)*size, (self.y-1)*size)
                
                qp.setBrush(QtGui.QColor(0, 0, 0))
                #podłączenie do odpowiednich kafelków bocznych 
                if self.connected_to & 0b0001:
                    if direction == 'vertical' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    qp.drawLine((size/2), (size/2), size, (size/2))
                if self.connected_to & 0b0010:
                    if direction == 'horizontal' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad,rad)
                        point = True
                    qp.drawLine((size/2), (size/2), (size/2), 0)
                if self.connected_to & 0b0100:
                    if direction == 'vertical' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    qp.drawLine((size/2), (size/2), 0, (size/2))
                if self.connected_to & 0b1000:
                    if direction == 'horizontal' and not point:
                        qp.drawEllipse((size/2)-rad/2, (size/2)-rad/2, rad, rad)
                        point = True
                    qp.drawLine((size/2), (size/2), (size/2), size)

                qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        elif self.type == 'node':
            def draw(qp, size):
                pen = QtGui.QPen(QtCore.Qt.black, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)
                
                if self.connected_to & 0b0001:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                elif self.connected_to & 0b0100:
                    qp.translate((self.x-1)*size, (self.y)*size)
                    qp.rotate(270)
                elif self.connected_to & 0b1000:
                    qp.translate((self.x)*size, (self.y)*size)
                    qp.rotate(180)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                #linia prosta
                qp.drawLine((size/2), 0, (size/2), size)
                #grot
                qp.drawLine((size/2), size, (size/3), (2*size/3))
                qp.drawLine((size/2), size, (2*size/3), (2*size/3))
                
                if self.connected_to & 0b0001:
                    qp.rotate(-90)
                    qp.translate(-((self.x)*size), -((self.y-1)*size))
                elif self.connected_to & 0b0100:
                    qp.rotate(-270)
                    qp.translate(-((self.x-1)*size), -((self.y)*size))
                elif self.connected_to & 0b1000:
                    qp.rotate(-180)
                    qp.translate(-((self.x)*size), -((self.y)*size))
                else:
                    qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        elif self.type == 'circuit_breaker':
            def draw(qp, size):
                if self.connected_to & 0b0101:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                pen = QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.NoPen)
                qp.setPen(pen)
                self.draw_contacts_state(qp, size)

                if self.switch.failure:
                    color = QtCore.Qt.red
                else:
                    color = QtCore.Qt.black
                pen = QtGui.QPen(color, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)

                if self.check_switch_state():
                    qp.drawLine((size/2), 0, (size/2), size)
                else:
                    qp.drawLine((size/2), 0, (size/2), (size/6))
                    #otwarty styk wyłącznika
                    qp.drawLine((size/2), (size/6), (5*size/6), (size/2))
                    qp.drawLine((size/2), (2*size/3), (size/2), size)
                # rysuje X wyłącznika
                qp.drawLine((size/3), (size/2), (2*size/3), (5*size/6))
                qp.drawLine((size/3), (5*size/6), (2*size/3), (1*size/2))

                if self.connected_to & 0b0101:
                    qp.rotate(-90)
                    qp.translate(-((self.x)*size), -((self.y-1)*size))
                else:
                    qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        elif self.type == 'disconnector':
            def draw(qp, size):
                if self.connected_to & 0b0101:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                pen = QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.NoPen)
                qp.setPen(pen)
                self.draw_contacts_state(qp, size)

                if self.switch.failure:
                    color = QtCore.Qt.red
                else:
                    color = QtCore.Qt.black
                pen = QtGui.QPen(color, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)

                #styki zamknięte lub otwarte
                if self.check_switch_state():
                    qp.drawLine((size/2), 0, (size/2), size)
                else:
                    qp.drawLine((size/2), 0, (size/2), (size/6))
                    #otwarty styk wyłącznika
                    qp.drawLine((size/2), (size/6), (5*size/6), (size/2))
                    qp.drawLine((size/2), (2*size/3), (size/2), size)
                # rysuje poprzeczke odłącznika
                qp.drawLine((size/3), (2*size/3), (2*size/3), (2*size/3))

                if self.connected_to & 0b0101:
                    qp.rotate(-90)
                    qp.translate(-(self.x)*size, -(self.y-1)*size)
                else:
                    qp.translate(-(self.x-1)*size, -(self.y-1)*size)
        elif self.type == 'earthing_switch':
            def draw(qp, size):

                if self.connected_to & 0b0001:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                elif self.connected_to & 0b0100:
                    qp.translate((self.x-1)*size, (self.y)*size)
                    qp.rotate(-90)
                elif self.connected_to & 0b1000:
                    qp.translate((self.x)*size, (self.y)*size)
                    qp.rotate(180)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                pen = QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.NoPen)
                qp.setPen(pen)
                self.draw_contacts_state(qp, size)

                if self.switch.failure:
                    color = QtCore.Qt.red
                else:
                    color = QtCore.Qt.black
                pen = QtGui.QPen(color, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)

                #styki zamknięte lub otwarte
                if self.check_switch_state():
                    qp.drawLine(size/2, 0, size/2, (2*size)/3)
                else:
                    qp.drawLine((size/2), 0, (size/2), (size/6))
                    #otwarty styk uziemnika
                    qp.drawLine((size/2), (size/6), (5*size/6), (size/2))

                qp.drawLine((size/2), (5*size/8), (size/2), (6*size/8))
                qp.drawLine(size/4, (6*size)/8, (3*size)/4, (6*size)/8)
                qp.drawLine((3*size)/8, (8*size)/9, (5*size)/8, (8*size)/9)

                if self.connected_to & 0b0001:
                    qp.rotate(-90)
                    qp.translate(-((self.x)*size), -((self.y-1)*size))
                elif self.connected_to & 0b0100:
                    qp.rotate(90)
                    qp.translate(-((self.x-1)*size), -((self.y)*size))
                elif self.connected_to & 0b1000:
                    qp.rotate(-180)
                    qp.translate(-((self.x)*size), -((self.y)*size))
                else:
                    qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        elif self.type == 'ct':
            def draw(qp, size):
                pen = QtGui.QPen(QtCore.Qt.black, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)

                if self.connected_to & 0b0101:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                #rysowanie przedkładnika prądowego
                qp.drawLine((size/2), 0, (size/2), size)
                qp.drawArc((size/4), (size/4), (size/2), (size/2), 16*360, 16*360)
                qp.drawLine((3*size/4), (size/2), (5*size/6), (size/2))

                if self.connected_to & 0b0101:
                    qp.rotate(-90)
                    qp.translate(-((self.x)*size), -((self.y-1)*size))
                else:
                    qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        elif self.type == 'vt':
            def draw(qp, size):
                pen = QtGui.QPen(QtCore.Qt.black, LINE_WIDTH, QtCore.Qt.SolidLine)
                qp.setPen(pen)

                #początek współrzędnych w punkcie rysowania oraz odpowiedni obrót
                if self.connected_to & 0b0001:
                    qp.translate((self.x)*size, (self.y-1)*size)
                    qp.rotate(90)
                elif self.connected_to & 0b0100:
                    qp.translate((self.x-1)*size, (self.y)*size)
                    qp.rotate(-90)
                elif self.connected_to & 0b1000:
                    qp.translate((self.x)*size, (self.y)*size)
                    qp.rotate(180)
                else:
                    qp.translate((self.x-1)*size, (self.y-1)*size)

                #rysowanie przedkładnika napięciowego 
                qp.drawLine((size/2), 0, (size/2), (size/6))
                qp.drawArc((size/4), (size/6), (size/2), (size/2), 16*360, 16*360)
                qp.drawArc((1*size/8), (2*size/5), (size/2), (size/2), 16*360, 16*360)
                qp.drawArc((3*size/8), (2*size/5), (size/2), (size/2), 16*360, 16*360)

                #powrót współrzędnych do punktu 0,0 
                if self.connected_to & 0b0001:
                    qp.rotate(-90)
                    qp.translate(-((self.x)*size), -((self.y-1)*size))
                elif self.connected_to & 0b0100:
                    qp.rotate(90)
                    qp.translate(-((self.x-1)*size), -((self.y)*size))
                elif self.connected_to & 0b1000:
                    qp.rotate(-180)
                    qp.translate(-((self.x)*size), -((self.y)*size))
                else:
                    qp.translate(-((self.x-1)*size), -((self.y-1)*size))
        return draw

class Switch:
    '''Klasa rozszerzająca obiekt o właściwości łączeniowe'''

    def __init__(self, status_l1, status_l2, status_l3, contacts_state_l1, contacts_state_l2, contacts_state_l3):
        self.status = [status_l1, status_l2, status_l3]
        self.contacts_state = [contacts_state_l1, contacts_state_l2, contacts_state_l3]
        self.failure = False
    
    def trip(self, phase_list = [1, 1, 1], closure=0):
        '''Wyłączenie 3f lub pofazowo, phase = [l1, l2, l3]'''
        changes = False
        i=0
        for phase, status, contacts_state in zip(phase_list, self.status, self.contacts_state):
            if phase and status:
                changes = True
                #jesli operacja na zamkniecie styków
                if closure:
                    self.contacts_state[i] = 1
                #jesli operacja na otwarcie
                else:
                    self.contacts_state[i] = 0
            elif phase and not status:
                self.failure = True
            i=i+1

        if changes:
            record = [contacts_state for contacts_state in self.contacts_state]
            record.append(self.owner.id)
            #zapisz stan łącznika w bazie
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute('UPDATE Objects SET contacts_state_l1=?, contacts_state_l2=?, contacts_state_l3=? WHERE id=?', record)
            conn.commit()
            conn.close()

    def set_status(self, phase):
        '''ustawienie statusu łącznika, sprawny, niesprawny'''
        
        if self.status[phase] == 1:
            new_state = 0
        else:
            new_state = 1

        #ustawienie nowego statusu w aplikacji i bazie danych
        self.status[phase] = new_state

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        record = [status for status in self.status]
        record.append(self.owner.id)
        c.execute('UPDATE Objects SET status_l1=?, status_l2=?, status_l3=? WHERE id=?', record)
        conn.commit()
        conn.close()

class MeasuringInstrument:
    '''Klasa rozszerzająca obiekt o właściwości pomiarowe'''

    def __init__(self, status_l1, status_l2, status_l3, measurement_l1, measurement_l2, measurement_l3):
        self.status = [status_l1, status_l2, status_l3]
        self.measurement = [measurement_l1, measurement_l2, measurement_l3]
