import csv
import os
#изменения внесеные в branch2
# Устанавливаем имя файла и директорию
filename = "data.csv"
directory = r'D:\УлГТУ\2 курс\Разработка проф. приложений'


def count_files_in_directory(directory):#функция для вывода количества файлов в директории
    count = 0
    try:
        for entry in os.scandir(directory):#перебор содержимого директории
            if entry.is_file():#проверяет, является содержимое файлом
                count += 1
    except FileNotFoundError:
        print(f"Ошибка: Директория '{directory}' не найдена.")
    except NotADirectoryError:
        print(f"Ошибка: '{directory}' не является директорией.")
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


class DataRow:#класс для представления строки данных, содержащей несколько полей
    def __init__(self, *args):#Конструктор класса, который инициализирует объект
        #принимает переменное количество аргументов (*args), которые представляют поля строки данных и сохраняет их в атрибуте fields
        self.fields = args 

    def __getitem__(self, index): #позволяет получить доступ к полям строки данных по индексу
        return self.fields[index]

    def __len__(self):#возвращает количество полей в строке данных
        return len(self.fields)

    def __repr__(self):#возвращает строку, которая включает все поля, представленные в виде списка.
        return f"DataRow({', '.join(map(repr, self.fields))})"


class Animal(DataRow):
    def __init__(self, number: str, name: str, breed: str, age: str):# выполняет инициализацию нового объекта класса Animal
        super().__init__(number, name, breed, age)#вызывается конструктор родительского класса DataRow.
        
        # Установка значений атрибутов через setattr
        setattr(self,"number", number)
        setattr(self,"name", name)
        setattr(self,"breed", breed)
        setattr(self,"age", age)

    def setattr(self, name: str, value):#устанавливает значение атрибута с проверкой
        if name == "age":
            value = int(value)  # Если имя атрибута — "age", то значение преобразуется в целое число
        setattr(self, name, value)

    def __repr__(self) -> str: #возвращает строковое представление объекта Animal
        return f"Animal(number={self.number}, name={self.name}, breed={self.breed}, age={self.age})"

    def __str__(self) -> str:#возвращает удобное строковое представление объекта для отображения пользователю
        return "№ {}: Кличка: {}, Порода: {}, Возраст: {}".format(self.number, self.name, self.breed, self.age)


class Animal_list_storing:
    def __init__(self, filename): #конструктор класса, который вызывается при создании нового объекта AnimalShelter
        self.filename = filename #сохраняет имя файла
        self.animals = [] #инициализируется пустым списком для хранения объектов животных
        self.load_data() #вызывается для загрузки данных из файла сразу после создания объекта

    def load_data(self): #загрузка данных о животных из CSV-файла, используя функцию read_file_csv()
        data = read_file_csv(self.filename)
        if data: #если данные успешно загружены
            for row in data[1:]:  # проходит по каждой строке (пропуская первую, которая содержит заголовки)
                animal = Animal(*row) #создает экземпляр класса Animal для каждой строки
                self.animals.append(animal) #добавляет его в список self.animals

    def __iter__(self): #делает объект AnimalShelter итерабельным
        self.current_index = 0
        return self

    def __next__(self): #возвращает следующее животное из списка
        if self.current_index < len(self.animals): #если индекс текущего животного меньше длины списка
            animal = self.animals[self.current_index] #возвращается текущее животное
            self.current_index += 1#индекс увеливается на 1
            return animal
        else: #если индекс превышает длину списка, вызывается исключение StopIteration и итерация завершается
            raise StopIteration

    def __getitem__(self, index): #позволяет получить доступ к животному по индексу
        return self.animals[index]

    @staticmethod #статический метод 
    def sort_by_name(animals):# cортирует список объектов животных по их именам в алфавитном порядке
        """Сортирует животных по имени."""
        return sorted(animals, key=lambda animal: animal.name)

    @staticmethod #статический метод 
    def sort_by_age(animals):# cортирует список объектов животных по возрасту в обратном порядке
        return sorted(animals, key=lambda animal: animal.age, reverse=True)
#sorted()-встроенная функция Python, которая возвращает новый отсортированный список из заданного итерируемого объекта
#animals - список объектов
#key - параметр, который указывает, как следует извлекать значения для сортировки
#lambda animal: animal.age - Анонимная функция (лямбда-функция), которая принимает один аргумент (объект animal) и возвращает его возраст (animal.age).
   
    def filter_by_age(self, min_age):#генератор, который возвращает животных старше указанного возраста (min_age)
        for animal in self.animals:#проходит по всем животным в списке
            if int(animal.age) > min_age:
                yield animal #возвращает только тех, кто соответствует условию

    def save_data(self):#сохраняет данные обратно в CSV-файл
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile: #открывает файл для записи ('w')
                csvwriter = csv.writer(csvfile) #создает объект csv.writer.
                csvwriter.writerow(["№", "Кличка", "Порода", "Возраст"]) #В первую строку записывается заголовок
                for animal in self.animals: #проходит по каждому объекту animal в списке self.animals, который, содержит информацию о всех животных
                    csvwriter.writerow(animal.fields)#возвращает список значений, которые будут записаны в соответствующие колонки CSV-файла
            print("Данные успешно сохранены в файл.")
        except Exception as e:
            print(f"Произошла ошибка при сохранении файла: {e}")


def main():
    
    list_storing = Animal_list_storing(filename)  #создает экземпляр (объект) класса Animal_list_storage

    while True:
        # Главное меню
        print("\nВыберите действие:")
        print("1 - Вывод количества файлов в директории")
        print("2 - Отобразить содержимое csv файла")
        print("3 - Отсортировать данные по кличке в алфавитном порядке")
        print("4 - Отсортировать данные по возрасту в убывающем порядке")
        print("5 - Фильтровать данные по возрасту (больше какого-либо значения)")
        print("6 - Выход")

        choice = input("Введите номер действия (1-6): ")  # Получаем выбор пользователя

        if choice == '1':
            count_files = count_files_in_directory(directory)
            print(f'Количество файлов в директории: {count_files}')  # Выводим количество файлов
            continue
        if choice == '2':
            # Вывод заголовков
            print("\nДанные:")
            print(f"{'№':<5} {'Кличка':<15} {'Порода':<20} {'Возраст':<7}")  # Заголовок таблицы
            print("-" * 50)  # Разделитель
            for animal in list_storing:  # Проходим по всем животным в приюте
                print(f"{animal.number:<5} {animal.name:<15} {animal.breed:<20} {animal.age:<7}")  # Выводим данные о животном

        elif choice == '3':
            
            sorted_animals = Animal_list_storing.sort_by_name(list_storing.animals)# Сортировка по имени
            
            list_storing.animals = sorted_animals# Обновление списока животных
            
            print("\nСортировка по кличке в алфавитном порядке:")
            print(f"{'№':<5} {'Кличка':<15} {'Порода':<20} {'Возраст':<7}")  # Заголовок таблицы
            print("-" * 50)  # Разделитель
            for animal in sorted_animals:  # Выводим отсортированные данные
                print(f"{animal.number:<5} {animal.name:<15} {animal.breed:<20} {animal.age:<7}")

            # Сохранение данных при необходимости
            ch = input("\nСохранить изменения в файл? (y - да, n - нет): ")
            if ch.lower() == "y":
                list_storing.save_data()  # Сохраняем данные
                print("Изменения успешно сохранены.")
            else:
                print("Изменения не были сохранены.")

        elif choice == '4':
            sorted_animals = Animal_list_storing.sort_by_age(list_storing.animals)  # Сортировка по возрасту
            list_storing.animals = sorted_animals# Обновление списока животных
            print("\nСортировка по возрасту в убывающем порядке:")
            print(f"{'№':<5} {'Кличка':<15} {'Порода':<20} {'Возраст':<7}")  # Заголовок таблицы
            print("-" * 50)  # Разделитель
            for animal in sorted_animals:
                print(f"{animal.number:<5} {animal.name:<15} {animal.breed:<20} {animal.age:<7}")  # Выводим отсортированные данные
            # Сохранение данных при необходимости
            ch = input("\nСохранить изменения в файл? (y - да, n - нет): ")
            if ch.lower() == "y":
                list_storing.save_data()  # Сохраняем данные
                print("Изменения успешно сохранены.")
            else:
                print("Изменения не были сохранены.")

        elif choice == '5':
            min_age = input("Введите минимальный возраст для фильтрации: ")
            try:
                min_age = int(min_age)  # Преобразуем ввод пользователя в число
                filtered_animals = list(list_storing.filter_by_age(min_age))  # Преобразуем генератор в список

                if not filtered_animals:  # Проверка на пустоту
                    print(f"\nЖивотные старше {min_age} лет не найдены.")
                    continue

                # Обновляем список животных
                list_storing.animals = filtered_animals

                # Выводим отфильтрованные данные
                print(f"\nЖивотные старше {min_age} лет:")
                print(f"{'№':<5} {'Кличка':<15} {'Порода':<20} {'Возраст':<7}")  # Заголовок таблицы
                print("-" * 50)  # Разделитель
                for animal in filtered_animals:
                    print(f"{animal.number:<5} {animal.name:<15} {animal.breed:<20} {animal.age:<7}")  # Выводим отфильтрованные данные

                # Запрашиваем пользователя о сохранении изменений
                ch = input("\nСохранить изменения в файл? (y - да, n - нет): ")
                if ch.lower() == 'y':
                    list_storing.save_data()  # Сохраняем данные
                    print("Изменения успешно сохранены.")
                else:
                    print("Изменения не были сохранены.")
            except ValueError:
                print("Некорректный ввод возраста.")

        elif choice == '6':
            print("Выход из программы.")
            break  # Завершение программы
        else:
            print("Неверный ввод! Пожалуйста, выберите номер от 1 до 6")

if __name__ == "__main__":
    main()  # Запуск программы