# more.techSKR
Для запуска требуется выполнить следующие команды:</br>
pip install flask</br>
pip install folium</br>
pip install osmnx</br>
pip install networkx</br>
pip install scikit-learn</br>
pip install geopy</br>

Запуск сервера:</br>
flask --app main run</br>

Сервер открывается по ссылке 125.0.0.1:5000/test</br>

Первая выполняемая функция - def test()</br>

point - местоположение пользователя</br>
Дальше выбирается 3 возможных варианта в выборе возвращаемой функции:</br>
def atmView(point, distance) - возвращает карту с ближайшими банкоматами от точки point, максимальное расстояние - distance в километрах</br>
def officeView(point, distance) - возвращает карту с ближайшими офисами аналогично atmView</br>
def shortestWay(start, end, mode = "walk", optimizer="time") - возвращает самый короткий маршрут между точками start и end. mode - способ, по которому можно добраться (возможны "all_private", "all", "bike", "drive", "drive_service", "walk"). optimizer - способ оптимизации маршрута ("time", "length")</br>


методы data_reader.py</br>
def getServicesAtm(atm) - получает доступные сервисы данного банкомата</br>
def getAtmInfo(self, userAddress, distance = 0, allDay = False, wheelchair = False, blind = False, nfcForBankCards = False, qrRead = False, suppurtsUsd = False, suppurtsChargeRub = False, suppurtsEur=False, suppurtsRub=False)-возвращает массив с маркерами, где указаны нужные банкоматы</br>
def hoursToSeg(st) - конвертирует строку типа "ab:cd-ef:gh" в массив типа [int(ab), int(cd), int(ef), int(gh)]</br>
def daysToSeg(st) - возвращает дни и график работы нужного офиса</br>
def procSchedule(office) - возвращает график работы офиса в виде словаря, где ключи от 0 до 7 - индексы дней недели, а 7 индекс - перерыв</br>
def checkTime(state, schedule, currentTime) - возвращает истину, если офис сейчас работает. state = 0 - для физ. лиц, state = 1 - для юр. лиц</br>
def initedSchedule(sch) - возвращает истину, если график полностью сформировна</br>
def getOfficeInfo(self, userAddress, currentTime, distance = 0, userState = 0) - возвращает массив с маркерами, где указаны нужные офисы</br>
