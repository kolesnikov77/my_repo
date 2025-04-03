import csv
import os

filename = "data.csv"
directory = r'D:\УлГТУ\2 курс\Разработка проф. приложений'
#r используется чтобы строка обрабатывалась как "сырая", т.е. чтобы Python не распознавал символы (обратный слеш"\") как escape-последовательности 

def count_files_in_directory(directory):#функция для вывода количества файлов в директории
    count = 0
    try:
        for entry in os.scandir(directory):#перебор содержимого директории
            if entry.is_file():#проверяет, является содержимое файлом
                count += 1
    except FileNotFoundError:
        print(f"Ошибка: Директория '{directory}' не найдена.")
        return 0  # Или другое значение по умолчанию
    except NotADirectoryError:
        print(f"Ошибка: '{directory}' не является директорией.")
        return 0

    return count

def read_file_csv(filename): #функция чтения csv файла
    data = []# пустой список для хранения данных
    try:  
        with open(filename, 'r', encoding='utf-8') as csvfile:# открытие файл в режиме чтения
            csvreader = csv.reader(csvfile)# создание объекта csvreader для чтения строк из файла
            for row in csvreader:# проход по каждой строке файла
                data.append(row)# добавление текущей строки в список data
    except FileNotFoundError:# обработка исключения, если файл не найден
        print(f"Ошибка: Файл '{filename}' не найден.")
    except Exception as e:# обработка других возможных исключений
        print(f"Ошибка при чтении файла: {e}")
    return data

def sort_by_string(data, field_index):# функция для сортировки данных по строковому полю
    if not data or len(data) <= 1:  # Проверка на наличие данных и заголовка
        print("Нет данных для сортировки или только заголовок.")
        return data

    try:
        header = data[0]  # Заголовки
        sorted_data = [header] + sorted(data[1:], key=lambda row: row[field_index])
        #сортирует данные (начиная со второго элемента) по индексу указанному столбце field_index. 
        # новый список сохраняется в sorted_data, который состоит из заголовка header и отсортированных данных 
        return sorted_data
    except IndexError:
        print(f"Ошибка: Индекс поля '{field_index}' вне диапазона.")
        return data
    except Exception as e:
        print(f"Ошибка при сортировке: {e}")
        return data

def sort_by_number(data, field_index):# функция для сортировки данных по числовому полю

    if not data or len(data) <= 1:  # Проверка на наличие данных и заголовка
        print("Нет данных для сортировки или только заголовок.")
        return data

    try:
        header = data[0]  # Заголовки
        sorted_data = [header] + sorted(data[1:], key=lambda row: int(row[field_index]),reverse=True)
        #сортирует данные (начиная со второго элемента) по индексу указанному столбце field_index. 
        # новый список сохраняется в sorted_data, который состоит из заголовка header и отсортированных данных 
        return sorted_data
    except ValueError:
        print(f"Ошибка: Невозможно преобразовать поле с индексом '{field_index}' в число.")
        return data
    except IndexError:
        print(f"Ошибка: Индекс поля '{field_index}' вне диапазона.")
        return data
    except Exception as e:
        print(f"Ошибка при сортировке: {e}")
        return data


def filter_by_age(data, age_index, min_age): #функция для фильтрации данных по минимальному возрасту
    if not data or len(data) <= 1:  # Проверка на наличие данных и заголовка
        print("Нет данных для фильтрации или только заголовок.")
        return data

    try:
        min_age = int(min_age)  # Преобразует минимальный возраст в целое число
        header = data[0]  # получаем заголовок (первую строку)
        
        # создание списка отфильтрованных данных
        filtered_data = [header]  # заносим в список заголовок

        for row in data[1:]:  # проходим по всем строкам данных, начиная со второй строки (индекс 1)
            try:
                age = int(row[age_index])  # получаем возраст из текущей строки
                if age > min_age:  # проверка, соответствует ли возраст минимальному требованию
                    filtered_data.append(row)  # если соответствует, добавляем строку в отфильтрованные данные
            except ValueError:
                print(f"Ошибка: Невозможно преобразовать значение '{row[age_index]}' в целое число.")
            except IndexError:
                print(f"Ошибка: поле 'Возраст' не найдено в строке: {row}.")
        
        return filtered_data  # Возвращаем отфильтрованные данные

    except ValueError:
        print("Ошибка: Некорректный формат возраста.")
        return []
    except Exception as e:
        print(f"Ошибка при фильтрации: {e}")
        return data

def save_data_to_csv(filename, data): #функция для сохранения данных в CSV-файл
    if not data:
        print("Нет данных для сохранения.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile) # создает объект для записи данных в формате CSV в открытый файл csvfile
            csvwriter.writerows(data)  # записывает все строки из списка data в CSV-файл
        print(f"Данные успешно сохранены в файл '{filename}'.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


animals_data = read_file_csv(filename)  # переменная data присваивает значение функции "read_file_csv"
if not animals_data:
    print("Не удалось загрузить данные, выход из программы.")
    exit()

# Индексы столбцов
name_index = 1 # Индекс столбца "Кличка" (для сортировки строкового типа)
age_index = 3 # Индекс столбца "Возраст" (для сортировки числового типа)

#инициализация переменных
sorted_by_name = None
sorted_by_age = None
filtered_data = None    

while True:
    print("\nВыберите действие:")
    print("1 - Вывод количества файлов в директории")
    print("2 - Отобразить содержимое csv файла")
    print("3 - Отсортировать данные по кличке")
    print("4 - Отсортировать данные по возрасту")
    print("5 - Фильтровать данные по возрасту (больше какого-либо значения)")
    print("6 - Сохранить измененные данные в файл")
    print("7 - Выход")
    
    choice = input("Введите номер действия (1-7): ")
    if choice == '1':#вывод количества файлов в директории
        count_files = count_files_in_directory(directory)
        print(f'Количество файлов в директории: {count_files}')
        input("Нажмите ENTER, чтобы перейти в меню")
    
    elif choice == '2':
       #вывод содержимого файла  
        print("Исходные данные:")
        for row in animals_data:
            print(row)
        input("Нажмите ENTER, чтобы перейти в меню")

    elif choice == '3':
        sorted_by_name = sort_by_string(animals_data, name_index)
        if sorted_by_name:
            print("\nСортировка по кличке:")
            for row in sorted_by_name:
                print(row)
        input("Нажмите ENTER, чтобы перейти в меню")

    elif choice == '4':
        sorted_by_age = sort_by_number(animals_data, age_index)
        if sorted_by_age:
            print("\nСортировка по возрасту:")
            for row in sorted_by_age:
                print(row)
        input("Нажмите ENTER, чтобы перейти в меню")
    elif choice == '5':
        min_age = input("Введите минимальный возраст для фильтрации: ")
        filtered_data = filter_by_age(animals_data, age_index, min_age)
        if filtered_data:
            print(f"\nЖивотные старше {min_age} лет:")
            for row in filtered_data:
                print(row)
        input("Нажмите ENTER, чтобы перейти в меню")
    elif choice == '6':
        data_to_save = input("Какие данные сохранить (1-исходные, 2-сортировка по полю кличка, 3-сортировка по полю возраст, 4-отфильтрованные данные по минимальному возрасту? ").lower()
        if data_to_save == "1":
            save_data_to_csv(filename, animals_data)
        elif data_to_save == "2":
            if sorted_by_name:
                save_data_to_csv(filename, sorted_by_name)
            else:
                print("Сортировка по кличке не выполнялась.")
        elif data_to_save == "3":
            if sorted_by_age:
                save_data_to_csv(filename, sorted_by_age)
            else:
                print("Сортировка по возрасту не выполнялась.")
        elif data_to_save == "4":
            if filtered_data:
                save_data_to_csv(filename, filtered_data)
            else:
                print("Фильтрация не выполнялась.")
        else:
            print("Некорректный ввод. Данные не сохранены.")
        input("Нажмите ENTER, чтобы перейти в меню")
            
    elif choice == '7':
        print("Выход из программы.")
        break

    else:
        print("Неверный ввод! Пожалуйста, выберите номер от 1 до 7")