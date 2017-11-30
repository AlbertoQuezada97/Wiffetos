#Titulo: Wiffetos
#Autor: Juan Alberto Falcon Quezada
#Fecha:29 de Septiembre 2017
#Descripcion: Aplicacion para crear una red wifi virtual

#librerias de PyQt
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*

#librerias del SO
import sys, os, ctypes

class RunAs(object):
    def IsAdmin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, *kwargs)
        self.setWindowTitle('Wiffeto')
        self.setWindowIcon(QIcon(os.path.join('icons','wifi_64.png')))

        self.ModoAdmin = RunAs()

        #Creamos en layout principal
        MainWindowLayout = QVBoxLayout()

        #Creamos el titulo
        lblTitle = QLabel('WIFFETO')
        lblTitle.setAlignment(Qt.AlignCenter)

        lblSSID = QLabel('SSID:')
        lblSSID.setAlignment(Qt.AlignLeft)

        self.EdSSID = QLineEdit()
        self.EdSSID.setPlaceholderText('Ej. Mi Router')
        self.EdSSID.setAlignment(Qt.AlignLeft)

        lblPassword = QLabel('Contraseña:')
        lblPassword.setAlignment(Qt.AlignLeft)

        self.EdPassword = QLineEdit()
        self.EdPassword.setPlaceholderText('Contraseña de 10 digitos')
        self.EdPassword.setAlignment(Qt.AlignLeft)

        btnConfig = QPushButton('Configurar')
        btnConfig.clicked.connect(self.ConfigurarRouter)

        hor_Layout = QHBoxLayout()

        btnEncienderRouter = QPushButton('Encender')
        btnEncienderRouter.clicked.connect(self.IniciarRouter)

        btnApagarRouter = QPushButton('Apagar')
        btnApagarRouter.clicked.connect(self.DetenerRouter)

        hor_Layout.addWidget(btnEncienderRouter)
        hor_Layout.addWidget(btnApagarRouter)


        #Añadimos los widgets al Layout Principal
        MainWindowLayout.addWidget(lblTitle)
        MainWindowLayout.addWidget(lblSSID)
        MainWindowLayout.addWidget(self.EdSSID)
        MainWindowLayout.addWidget(lblPassword)
        MainWindowLayout.addWidget(self.EdPassword)
        MainWindowLayout.addWidget(btnConfig)
        MainWindowLayout.addLayout(hor_Layout)

        widget = QWidget()
        widget.setLayout(MainWindowLayout)
        self.setCentralWidget(widget)

    def ConfigurarRouter(self):
        ssid = self.EdSSID.text()
        password = self.EdPassword.text()

        if ssid  == '' or len(password) < 10:
            print('Necesita asignar un nombre de red o una contraseña mas larga')
        else:
            if self.ModoAdmin.IsAdmin():
                print('Permiso de administrador!')
                os.system('netsh wlan set hostednetwork mode=allow ssid={} key={}'.format(ssid, password))
            else:
                print('No administrador')

    def IniciarRouter(self):
        try:
            if self.ModoAdmin.IsAdmin():
                os.system('netsh wlan start hostednetwork')
                print('Router Virtual Encendido')
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
        except:
            print('Error al Iniciar Router')

    def DetenerRouter(self):
        try:
            if self.ModoAdmin.IsAdmin():
                os.system('netsh wlan stop hostednetwork')
                print('Router Virtual Apagado')
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
        except:
            print('Error al Detener Router')


app = QApplication(sys.argv)
app.setApplicationName('Wiffeto')

window = MainWindow()
window.show()

app.exec_()
