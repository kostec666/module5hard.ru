import hashlib
import time


# Класс User представляет пользователя на платформе.
class User:
    # Инициализатор класса User.
    def __init__(self, nickname, password, age):
        # Атрибут класса User: nickname(имя пользователя, строка)
        self.nickname = nickname
        # Атрибут класса User: password(в хэшированном виде, число)
        self.password = self.hash_password(password)  # Хеширование пароля
        #  # Атрибут класса User: age(возраст, число)
        self.age = age

    # Функция хеширования пароля.
    def hash_password(self, password): # https://docs.python.org/3/library/hashlib.html
        """Хеширование пароля с использованием алгоритма SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()  # https://www.yourtodo.ru/posts/heshirovanie-v-python/

    # Функция проверки пользователя по имени пользователя.
    def __eq__(self, other):
        """Переопределяем метод сравнения, чтобы проверять пользователя по имени пользователя."""
        return self.nickname == other.nickname

    # Функция строкового представления имени и возраста пользователя.
    def __str__(self):
        # return f"User(nickname='{self.nickname}', age={self.age})"
        return f"{self.nickname}"


# Класс Video представляет видео на платформе.
class Video:
    # Инициализатор класса Video.
    def __init__(self, title, duration, adult_mode=False):
        # Атрибут класса Video: title(заголовок, строка)
        self.title = title
        # Атрибут класса Video: duration(продолжительность, секунды)
        self.duration = duration
        # Атрибут класса Video: time_now(секунда остановки (изначально 0))
        self.time_now = 0  # Текущее время просмотра видео
        # Атрибут класса Video: adult_mode(ограничение по возрасту, bool (False по умолчанию))
        self.adult_mode = adult_mode

    # Функция проверки видео по заголовку.
    def __eq__(self, other):
        """Переопределяем метод сравнения, чтобы проверять видео по заголовку."""
        return self.title.lower() == other.title.lower()

    # Функция строкового представления параметров видео.
    def __str__(self):
        return f"Video(title='{self.title}', duration={self.duration}, adult_mode={self.adult_mode})"


# Класс UrTube представляет платформу и включает методы для взаимодействия с пользователями и видео.
class UrTube:
    # Инициализатор класса UrTube.
    def __init__(self):
        # Атрибут  класса UrTube: users(список объектов User)
        self.users = []  # Список зарегистрированных пользователей
        # Атрибут  класса UrTube: videos(список объектов Video)
        self.videos = []  # Список доступных видео
        # Атрибут  класса UrTube: current_user(текущий пользователь, User)
        self.current_user = None  # Текущий пользователь

    # Метод log_in, принимает на вход аргументы: login, password и пытается найти пользователя в users
    # с такими же логином и паролем.
    def log_in(self, nickname, password):
        """Проверяет наличие пользователя с указанным логином и паролем."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                # Если такой пользователь существует, то current_user меняется на найденного.
                self.current_user = user
                print(f"Пользователь {nickname} вошёл в систему.")
                return True
        print("Ошибка входа: неверный логин или пароль.")
        return False

    # Метод register, принимает три аргумента: nickname, password, age, и добавляет пользователя
    # в список, если пользователя не существует (с таким же nickname).
    # После регистрации, вход выполняется автоматически.
    def register(self, nickname, password, age):
        """Регистрирует нового пользователя и автоматически выполняет вход."""
        new_user = User(nickname, password, age)
        if new_user in self.users:
            # Если пользователь с таким же nickname существует, выводит на экран:
            # "Пользователь {nickname} уже существует".
            print(f"Пользователь {nickname} уже существует.")
        else:
            # После регистрации, вход выполняется автоматически.
            self.users.append(new_user)
            self.current_user = new_user
            # print(f"Пользователь {nickname} успешно зарегистрирован и вошёл в систему.")

    # Метод log_out используется для сброса текущего пользователя на None.
    def log_out(self):
        """Выходит из текущего пользователя."""
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из системы.")
            self.current_user = None
        else:
            print("В системе нет активного пользователя.")

    # Метод add, принимает неограниченное кол-во объектов класса Video и все добавляет в videos,
    # если с таким же названием видео ещё не существует.  В противном случае ничего не происходит.
    def add(self, *videos):
        """Добавляет новые видео в список, если видео с таким названием ещё нет."""
        for video in videos:
            # Если с таким же названием видео ещё не существует:
            if video not in self.videos:
                # Добавляет video в videos.
                self.videos.append(video)
                # print(f"Видео '{video.title}' добавлено.")
            # else:
                # В противном случае ничего не происходит.
                # print(f"Видео '{video.title}' уже существует.")

    # Метод get_videos, принимает поисковое слово и возвращает список названий всех видео,
    # содержащих поисковое слово.
    # Следует учесть, что слово 'UrbaN' присутствует в строке 'Urban the best' (не учитывать регистр).
    def get_videos(self, search_term):
        """Возвращает список названий видео, содержащих поисковое слово (регистр не учитывается)."""
        # Перевод поискового запроса в нижний регистр.
        search_term_lower = search_term.lower()
        # Поисковый запрос, представленный в нижнем регистре,
        # сравнивается с заголовком видео в нижнем регистре.
        return [video.title for video in self.videos if search_term_lower in video.title.lower()]

    # Метод watch_video, принимает название фильма, если не находит точного совпадения(вплоть до пробела),
    # то ничего не воспроизводится, если же находит - ведётся отчёт в консоль на какой секунде ведётся
    # просмотр. После текущее время просмотра данного видео сбрасывается.
    def watch_video(self, title):
        """Воспроизводит видео, если пользователь вошёл в систему и имеет право на просмотр."""
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                # print(f"Начинается воспроизведение видео: {video.title}")
                for second in range(video.time_now + 1, video.duration + 1):
                    print(second, end=' ', flush=True)
                    time.sleep(1)  # Имитируем просмотр по одной секунде
                print("Конец видео")
                video.time_now = 0  # Сбрасываем время остановки после полного просмотра
                return

        # print("Видео не найдено")


# Код для проверки:
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
# Вывод: ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))
# Вывод: ['Лучший язык программирования 2024 года', 'Для чего девушкам парень программист?']

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
# Вывод: Войдите в аккаунт, чтобы смотреть видео
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
# Вывод: Вам нет 18 лет, пожалуйста покиньте страницу
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')
# Вывод: 1 2 3 4 5 6 7 8 9 10 Конец видео

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
# Вывод: Пользователь vasya_pupkin уже существует
print(ur.current_user)
# Вывод: urban_pythonist

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
# Вывод: Видео не найдено
