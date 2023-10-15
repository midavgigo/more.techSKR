# more.techSKR
Для запуска требуется выполнить следующие команды:__
pip install flask__
pip install folium__
pip install osmnx__
pip install networkx__
pip install scikit-learn__
pip install geopy__

Запуск сервера:__
flask --app main run__

Сервер открывается по ссылке 125.0.0.1:5000/test__

Первая выполняемая функция - def test()__

point - местоположение пользователя__
Дальше выбирается 3 возможных варианта в выборе возвращаемой функции:__
def atmView(point, distance) - возвращает карту с ближайшими банкоматами от точки point, максимальное расстояние - distance в километрах__
def officeView(point, distance) - возвращает карту с ближайшими офисами аналогично atmView__
def shortestWay(start, end, mode = "walk", optimizer="time") - возвращает самый короткий маршрут между точками start и end. mode - способ, по которому можно добраться (возможны "all_private", "all", "bike", "drive", "drive_service", "walk"). optimizer - способ оптимизации маршрута ("time", "length")__


методы data_reader.py__
def getServicesAtm(atm) - получает доступные сервисы данного банкомата__
def getAtmInfo(self, userAddress, distance = 0, allDay = False, wheelchair = False, blind = False, nfcForBankCards = False, qrRead = False, suppurtsUsd = False, suppurtsChargeRub = False, suppurtsEur=False, suppurtsRub=False)-возвращает массив с маркерами, где указаны нужные банкоматы__
def hoursToSeg(st) - конвертирует строку типа "ab:cd-ef:gh" в массив типа [int(ab), int(cd), int(ef), int(gh)]__
def daysToSeg(st) - возвращает дни и график работы нужного офиса__
def procSchedule(office) - возвращает график работы офиса в виде словаря, где ключи от 0 до 7 - индексы дней недели, а 7 индекс - перерыв__
def checkTime(state, schedule, currentTime) - возвращает истину, если офис сейчас работает. state = 0 - для физ. лиц, state = 1 - для юр. лиц__
def initedSchedule(sch) - возвращает истину, если график полностью сформировна__
def getOfficeInfo(self, userAddress, currentTime, distance = 0, userState = 0) - возвращает массив с маркерами, где указаны нужные офисы__
