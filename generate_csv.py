import csv
import random

name = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
    "Алексей", "Артём", "Илья", "Кирилл", "Михаил",
    "Никита", "Матвей", "Роман", "Егор", "Тимофей",
    "Даниил", "Владимир", "Павел", "Руслан", "Вадим",
    "Евгений", "Юрий", "Виктор", "Николай", "Борис",
    "Глеб", "Вячеслав", "Станислав", "Игорь", "Олег",
    "Денис", "Виталий", "Григорий", "Леонид", "Семён",
    "Фёдор", "Пётр", "Анатолий", "Валентин", "Константин",
    "Захар", "Давид", "Лев", "Марк", "Ярослав",
    "Владислав", "Святослав", "Родион", "Платон", "Тимур"
]

surname = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
    "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
    "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
    "Егоров", "Павлов", "Козлов", "Степанов", "Николаев",
    "Орлов", "Андреев", "Макаров", "Сафонов", "Захаров",
    "Соловьёв", "Борисов", "Тимофеев", "Григорьев", "Ильин",
    "Савельев", "Дмитриев", "Белов", "Гусев", "Тарасов",
    "Комаров", "Кудрявцев", "Баранов", "Воробьёв", "Зуев",
    "Крылов", "Лебедев", "Медведев", "Сорокин", "Тихомиров",
    "Фролов", "Чернов", "Щербаков", "Яковлев", "Абрамов"
]

def generate_games(games:int, filename = "data.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Дата матча", "Фамилия Имя", "Выход на поле", "Количество голов", "Пройденная дистанция"])
        for game in range(games):
            year = random.randint(1920, 2026)
            month = random.randint(1, 12)
            if month == 2:
                day = random.randint(1, 28)
            elif month in [4, 6, 9, 11]:
                day = random.randint(1, 30)
            else:
                day = random.randint(1, 31)
            date = f"{year}-{month:02d}-{day:02d}"

            players_in_game = 22 + random.randint(0, 10)
            in_game = [True] * players_in_game + [False] * (46 - players_in_game)
            random.shuffle(in_game)

            goals = random.randint(0, 10)

            for player in range(0, 46):
                if in_game[player] and goals > 0:
                    rand = random.random()
                    if rand <= 0.01:
                        goal = 3
                        goals -= 3
                    elif rand <= 0.07:
                        goal = 2
                        goals -= 2
                    elif rand <= 0.33:
                        goal = 1
                        goals -= 1
                    else:
                        goal = 0
                else:
                    goal = 0

                if in_game[player]:
                    distance = round(random.uniform(1.0, 12.0), 2)
                else:
                    distance = 0

                writer.writerow([
                    date,
                    f"{random.choice(surname)} {random.choice(name)}",
                    in_game[player],
                    goal,
                    distance
                ])

def generate_memory(gb:float, filename = "data.csv"):
    generate_games((int(gb * 1024**3) - 143) // 2358, filename)