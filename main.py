
import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    @staticmethod
    def hash_password(password):
        """Хэширует пароль и возвращает его в виде целого числа."""
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def check_password(self, password):
        """Проверяет правильность пароля."""
        return self.password == self.hash_password(password)

    def __repr__(self):
        return f"User(nickname='{self.nickname}', age={self.age})"

class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration  # Продолжительность в секундах
        self.time_now = 0         # Текущая секунда остановки
        self.adult_mode = adult_mode  # Ограничение по возрасту

    def __repr__(self):
        return f"Video(title='{self.title}', duration={self.duration}, adult_mode={self.adult_mode})"

class UrTube:
    def __init__(self):
        self.users = []          # Список пользователей
        self.videos = []         # Список видео
        self.current_user = None  # Текущий пользователь

    def log_in(self, nickname, password):
        """Авторизация пользователя."""
        for user in self.users:
            if user.nickname == nickname and user.check_password(password):
                self.current_user = user
                print(f"Пользователь {nickname} вошёл в аккаунт.")
                return
        print("Неправильный логин или пароль.")

    def register(self, nickname, password, age):
        """Регистрация нового пользователя."""
        if any(user.nickname == nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует.")
            return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован и вошёл в аккаунт.")

    def log_out(self):
        """Выход из аккаунта."""
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из аккаунта.")
        self.current_user = None

    def add(self, *videos):
        """Добавляет видео в список, если оно ещё не существует."""
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Добавлено видео: {video.title}")

    def get_videos(self, keyword):
        """Возвращает список названий всех видео, содержащих поисковое слово."""
        return [video.title for video in self.videos if keyword.lower() in video.title.lower()]

    def watch_video(self, title):
        """Воспроизводит видео с заданным названием."""
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео.")
            return

        for video in self.videos:
            if video.title == title:
                if self.current_user.age < 18 and video.adult_mode:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу.")
                    return

                print(f"Начало воспроизведения видео: {video.title}.")
                while video.time_now < video.duration:
                    print(f'Текущая секунда просмотра: {video.time_now + 1}')
                    time.sleep(1)  # пауза в секунду
                    video.time_now += 1
                print("Конец видео.")
                video.time_now = 0  # Сброс текущего времени
                return

        print("Видео не найдено.")

# Код для проверки
ur = UrTube()

v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))     # ['Лучший язык программирования 2024 года']

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')  # Нет входа

ur.register('vasya_pupkin', 'lolkekcheburek', 13)  # Регистрация успешна
ur.watch_video('Для чего девушкам парень программист?')  # Просмотр не разрешен

ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)  # Регистрация успешна
ur.watch_video('Для чего девушкам парень программист?')  # Начало просмотра

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)  # Пользователь уже существует
print(ur.current_user)  # Аргумент показывает текущего пользователя

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')  # Видео не найдено



