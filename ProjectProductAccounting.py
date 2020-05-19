#!/usr/bin/env python
db = []
user_history = []


def show(rows=db):
    """ Вывод на экран """
    if len(rows) == 0:
        print('Таблица пустая.')
        return

    # Подсчёт суммарного итога
    total_cost = sum([float(x[1]) * float(x[2]) for x in rows])
    total_count = sum([float(x[2]) for x in rows])
    total_weight = sum([float(x[3]) * float(x[2]) for x in rows])

    # Выводим таблицу
    print('')
    print(f'{"№":>3} | {"Наименование":20} | {"Цена":^8} | {"Кол-во":6} | {"Вес":^6} | {"Примечание":30}')
    print('-' * 80)

    for row in rows:
        print(f'{db.index(row)+1:3} | {row[0]:20} | {float(row[1]):>8.2f} | {row[2]:>6} | {row[3]:>6} | {row[4]:30}')
    print('-' * 80)

    print(f'{len(rows):>3} | Всего: {"":13} | {total_cost:>8.2f} | {total_count:>6} | {total_weight:>6} | ')
    print('')


def check(raw_data):
    """ Проверяет правильность ввода данных в таблицу и возвращает корректные данные """
    row = raw_data.strip().split('  ')

    # Если отсутствует примечание - добавляем пустое поле.
    if len(row) == 4:
        row.append('')

    # Если это похоже на ввод данных в таблицу
    if len(row) == 5:
        # Проверка правильности ввода полей.
        if len(row[0]) > 0 \
                and row[1].replace('.', '', 1).isdecimal() \
                and row[2].replace('.', '', 1).replace('-', '', 1).isdecimal() \
                and row[3].replace('.', '', 1).isdecimal():
            user_history.append(row)
            return row
        else:
            print('Неправильно введённые данные. Проверьте значения и повторите ввод.')
            return False
    else:
        return False


def check_db_index(index):
    """ Проверяет индекс в "базе" """
    if len(db) > index >= 0:
        return True
    else:
        print(f'Указанная строка ({index + 1}) отсутствует в таблице. Повторите попытку.')
        return False


def edit(index):
    """ Редактирует указанную строку в таблице """
    index = int(index) - 1
    if check_db_index(index):
        show([db[index]])
        print('Введите новую строку полностью, разделяя поля двумя пробелами:')
        print('Или введите exit для выхода.')

        while True:
            raw_data = input('Редактирование> ').strip()
            if raw_data == 'exit':
                break

            row = check(raw_data)
            if row:
                db.pop(index)
                db.insert(index, row)
                break
            else:
                continue


def move(source=0, destination=-1):
    """ Перемещает одну строку в таблице на другую позицию """
    source = int(source) - 1
    destination = int(destination) - 1
    if check_db_index(source) and check_db_index(destination):
        row = db[source]
        db.pop(source)
        db.insert(destination, row)
        return True


def delete(data):
    """ Удаление строк в таблице по номеру или поисковому запросу """
    if not data:
        return

    # Если номер строки
    if data.isdecimal():
        index = int(data) - 1
        if check_db_index(index):
            show([db[index]])
            if input('Вы уверены, что хотите удалить? [y] ') == 'y':
                db.pop(index)

    # Если поисковый запрос
    elif data.isprintable():
        delete_rows = find(data)
        if delete_rows:
            if input('Вы уверены, что хотите удалить все эти данные? [y] ') == 'y':
                for row in delete_rows:
                    db.remove(row)
                print('Выполнено :)')
            else:
                print('Отмена :(')


def find(text):
    """ Поиск строк в таблице и вывод их на экран """
    text = text.lower()
    rows_to_show = []
    for row in db:
        if row[0].lower().find(text) >= 0 or row[4].lower().find(text) >= 0:
            rows_to_show.append(row)
    if rows_to_show:
        show(rows_to_show)
        return rows_to_show
    else:
        print(f'Элемент "{text}" не найден. Или таблица пустая. :( ')
        return False


def help():
    """ Справка по командам """
    print('''
Введите данные через двойной пробел: Наименование, Цена, Количество, Вес, [Примечание].
Или используйте команды через одинарный пробел:
delete <номер или поисковый запрос> - удаляет найденное поле.
edit <номер> - редактирует указанное поле. Пустой ввод - выход.
move <номер откуда> <номер куда> - перемещает одно поле на место другого.
find <не точный поисковый запрос> - ищет поля по "наименованию" и "примечанию".
show - выводит на экран таблицу.
help - выводит на экран общую справку по всем командам.
history - выводит историю введённых данных.
exit - выход из скрипта
Пример:
find lavaz
delete egoiste
move 2 5
edit 1
    ''')


def history():
    """ История пользовательского ввода """
    for row in user_history:
        print(row)


print('Введите через двойной пробел данные: Наименование, Цена, Количество, Вес, Примечание.\n'
      'Или команду help для получения справки.\n')

# Тестовые данные
db.append('Lavazza  105  3  250  Молотый. Итальянский кофе'.split('  '))
db.append('Lavazza  120  6  250  Зёрна. Итальянский кофе'.split('  '))
db.append('Egoiste  130  2  250  Молотый. Мягкий вкус'.split('  '))
db.append('Egoiste  150  4  250  Зёрна. Мягкий вкус'.split('  '))
db.append('Sati Bio  141  5  250  Биорастворимый :D'.split('  '))
db.append('Sati Irish Cream  142  4  250  Хмммм...'.split('  '))
db.append('Sati Caramel  147  3  250  Карамельный вкус'.split('  '))
db.append('Sati Chocolat  153  6  250  Panzerschokolade'.split('  '))
db.append('Jacobs Monarch  80  4  250  Паршивый кофе'.split('  '))
db.append('Jacobs Monarch  80  8  250  Фу, гадость. Ещё одна упаковка... :('.split('  '))
# db.append(''.split('  '))

show()

while True:

    raw_data = input('Ввод> ').strip()
    command = raw_data.split(' ')
    # fields = raw_data.split('  ')
    row = check(raw_data)

    if row:
        db.append(row)
        continue

    if len(command) == 1:
        if command[0] == 'show':
            show()
        elif command[0] == 'help':
            help()
        elif command[0] == 'history':
            history()
        elif command[0] == 'exit':
            print('Пока-пока! Have a nice day :)\n' * 9999)
            break
        else:
            print(f'Нет такой комманды: "{raw_data}". Введите help для получения справки.')
            continue

    elif len(command) >= 2:
        if command[0] == 'delete':
            delete(command[1])
        elif command[0] == 'edit':
            edit(command[1])
        elif command[0] == 'find':
            find(command[1])
        elif command[0] == 'move' and len(command) == 3:
            move(command[1], command[2])
        else:
            print(f'Нет такой комманды: "{raw_data}". Введите help для получения справки.')

