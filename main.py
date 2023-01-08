import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox



# Алгоритм шифрования
def encrypt_data(username, password):
    eng_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    rus_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    text1 = username
    text2 = password
    username = ''
    password = ''
    j = 0
    for j in range(len(text1)):
        i = text1[j]
        if text1[j] in text1:
            if text1[j] in rus_alphabet:
                username += rus_alphabet[rus_alphabet.find(i) + 15]
            elif text1[j] in eng_alphabet:
                username += eng_alphabet[eng_alphabet.find(i) + 15]
            else:
                username += i
    for j in range(len(text2)):
        i = text2[j]
        if text2[j] in text2:
            if text2[j] in rus_alphabet:
                password += rus_alphabet[rus_alphabet.find(i) + 15]
            elif text2[j] in eng_alphabet:
                password += eng_alphabet[eng_alphabet.find(i) + 15]
            else:
                password += i
    return username, password


# Проверка авторизации
def verify_login(username, password):
    if len(username) <= 5 or len(username) > 15 or len(password) < 6 or len(password) > 15:
        return False
    try:
        find_login = False
        username, password = encrypt_data(username, password)
        with open('users.txt', 'r', encoding='utf8') as login_file:
            for line in login_file:
                if (username + " " + password) in line:
                    find_login = True
            if find_login:
                return True
            return False
    except:
        return False


# Проверка регистрации
def verify_registr(username, password):
    if (len(username) <= 5 or len(username) > 15) and (len(password) < 6 or len(password) > 15):
        return False
    try:
        username, password = encrypt_data(username, password)
        flag_login = False
        with open('users.txt', 'r+', encoding='utf8') as login_file:
            for line in login_file:
                if (username in line) or (password in line):
                    flag_login = True
                    break
            if flag_login:
                return False
            new_login = "\n" + username + " " + password
            login_file.write(new_login)
            return True
    except:
        return False



# Класс начального окна
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.pushButton_log_in.clicked.connect(self.gotologin)
        self.pushButton_zaregistr.clicked.connect(self.registration)


    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # функция перехода к регистрации после нажатия кнопки "зарегистрироваться"
    def registration(self):
        registration = CreateAcc()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex()+1)


# Класс окна входа
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)   #сокрытие пароля
        self.login.clicked.connect(self.loginfunction)
        self.create_account.clicked.connect(self.gotocreate)

    #функция входа в лк
    def loginfunction(self):
        global username
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text()
        if verify_login(username, password):
            widget.addWidget(lk_window)
            widget.setFixedWidth(740)
            widget.setFixedHeight(770)
            widget.setCurrentWidget(lk_window)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Введен неверный логин или пароль.")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()


    #функция перехода к окну регистрации
    def gotocreate(self):
        create_acc = CreateAcc()
        widget.addWidget(create_acc)
        widget.setCurrentIndex(widget.currentIndex()+1)

# Класс окна регистрации
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("create_account.ui", self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_account_button.clicked.connect(lambda: self.createaccfunction(True))
        self.otmena_btn.clicked.connect(lambda: self.createaccfunction(False))
        self.otmena_btn.clicked.connect(self.otmena)

    #функция создания лк
    def createaccfunction(self, flag):

        if flag == True:
            username = self.lineEdit_username.text().strip()
            password = self.lineEdit_password.text()
            confirmpass = self.confirmpass.text()
            if password != confirmpass:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Пароли не совпадают!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return False
            registr_verify = verify_registr(username, password)
            if registr_verify == True:
                flag = False
            else:
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setText(
                    " Вы ввели неверные данные!\n Проверьте:\n 1) Пароль может содержать: \n цифры (0-9)\n латинские буквы (a-z; A-Z)\n знаки препинания ('.', '!', '?', ',', '_')\n Либо длина пароля меньше 6 или больше 15\n 2) Длина логина должна быть не менее 6 и не более 15\n 3) Пользователь с такими данными уже существует")
                error.exec_()
            if not flag:
                return widget.setCurrentWidget(login_window)

    # функция отмены регистрации
    def otmena(self):
        otmena = WelcomeScreen()
        widget.addWidget(otmena)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Класс окна личного кабинета
class LKabinet(QDialog):
    def __init__(self):
        super(LKabinet, self).__init__()
        loadUi("lk.ui", self)
        self.encoding.clicked.connect(self.encoding_function)
        self.decoding.clicked.connect(self.decoding_function)
        self.exit.clicked.connect(self.exitfunction)


    def encoding_function(self):
        eng_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
        rus_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        text = self.textline.text()
        result = ''
        j = 0
        for j in range(len(text)):
            i = text[j]
            if text[j] in text:
                if text[j] in rus_alphabet:
                    result += rus_alphabet[rus_alphabet.find(i) + 15]
                elif text[j] in eng_alphabet:
                    result += eng_alphabet[eng_alphabet.find(i) + 15]
                else:
                    result += i
                self.resultline.setText(result)
        with open('text.txt', 'r+', encoding='utf8') as text_file:
            text_file.truncate()
            text_file.write("\n" + result)

    def decoding_function(self):
        eng_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
        rus_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        text = self.textline.text()
        result = ''
        j = 0
        for j in range(len(text)):
            i = text[j]
            if text[j] in text:
                if text[j] in rus_alphabet:
                    result += rus_alphabet[rus_alphabet.find(i) + 18]
                elif text[j] in eng_alphabet:
                    result += eng_alphabet[eng_alphabet.find(i) + 11]
                else:
                    result += i
        self.resultline.setText(result)

    #предупреждение о выходе из личного кабинета
    def exitfunction(self):
        error = QMessageBox()
        error.setWindowTitle("Предупреждение")
        error.setText("Вы уверены, что хотите выйти из личного кабинета?")
        error.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        error.buttonClicked.connect(self.click_exit)
        error.exec_()

    def click_exit(self, btn):
        if btn.text() == 'OK':
            widget.removeWidget(lk_window)
            widget.setFixedWidth(740)
            widget.setFixedHeight(770)
            widget.setCurrentWidget(welcome)



app = QApplication(sys.argv)
welcome = WelcomeScreen()
login_window = LoginScreen()
lk_window = LKabinet()
create_acc = CreateAcc()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(740)
widget.setFixedWidth(770)
widget.show()
try:
    sys.exit(app.exec_())

except:
    print("Exiting")