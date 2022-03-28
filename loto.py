import random


class Player:
    def __init__(self, id_number, name, identity):
        self.id_number = id_number
        self.identity = identity
        self.name = name
        self.card = Card()

    def __repr__(self):
        return f"Player {self.id_number} (Name: {self.name}, Identity: {self.identity}, Card: {self.card})"


class Bag:
    def __init__(self):
        self.kegs = []
        self.set_bag()

    def __repr__(self):
        return f"{self.kegs}"

    def __call__(self):
        keg = self.kegs.pop()
        print(f"Новый бочонок: {keg} (осталось {len(self.kegs)})")
        return keg

    def set_bag(self):
        # print("Generating bag...")
        self.kegs = [i for i in range(1, 91)]
        random.shuffle(self.kegs)
        return self


class Card:
    empty_num = 0
    crossed_num = -1

    def __init__(self):
        self.data = []
        self.set_card()
        # self.show_card()

    def __repr__(self):
        return f"{self.data}"

    def __contains__(self, item):
        return item in self.data

    def set_card(self):
        num_row = 3
        num_col = 9
        num_in_row = 5
        """
        Функция создает карточку для игры в лото. Каждая карточка содержит
        3 строки по 9 клеток. В каждой строке по 5 уникальных случайных чисел,
        расположенных по возрастанию. Результат выполнения функции -
        одномерный массив чисел с нулями на месте пустых клеток.
        """
        # выборка 15 случайных чисел в диапазоне от 1 до 90
        list1 = [i for i in range(1, 91)]
        list2 = random.sample(list1, num_row * num_in_row)
        # разбиение и сортировка чисел по строкам в карточке
        list3 = [[list2.pop() for i in range(num_in_row)] for j in range(num_row)]
        for row in list3:
            row.sort()
        # создание матрицы индексов для ненулевых элементов с сортировкой
        list4 = [random.sample(range(num_col), num_in_row) for j in range(num_row)]
        for row in list4:
            row.sort()
        # заполнение карточки сгенерированными числами
        list5 = [[self.empty_num] * num_col for i in range(num_row)]
        for i in range(num_row):
            for j in range(num_in_row):
                list5[i][list4[i][j]] = list3[i][j]
        # представление данных карточки в виде одномерного списка
        for item in list5:
            self.data += item
        return self

    def show_card(self):
        print('-'*26)
        for index, num in enumerate(self.data):
            if num == self.empty_num:
                print("%2s" % '', end=' ')
            elif num == self.crossed_num:
                print("%2s" % '-', end=' ')
            else:
                print("%2s" % num, end=' ')
            if (index + 1) % 9 == 0:
                print()
        print('-'*26, '\n')

    def cross_num(self, num):
        for index, item in enumerate(self.data):
            if item == num:
                self.data[index] = self.crossed_num
                return
        raise ValueError(f'Number not in card: {num}')

    def empty_card_check(self):
        return set(self.data) == {self.empty_num, self.crossed_num}


class Game:
    def __init__(self):
        self.bag = Bag()
        # print(self.bag)

        self.number_of_players = int(input('Введите количество игроков: '))
        print('Игроков в игре:', self.number_of_players)

        self.players = []
        self.set_players()
        # print(f"Players in the game: {self.players}")
        print('Все готово. Начинаем игру!')

    def set_players(self):
        # print("Setting players...")
        for id_number in range(1, self.number_of_players + 1):
            identity = input(f"Игрок #{id_number} человек (h) или бот (b)? ")
            name = input(f"Введите имя игрока #{id_number}: ")
            self.players.append(Player(id_number + 1, name, identity))
        return self

    def play_round(self):
        """
        :return:
        0     - game goes on;
        not 0 - someone wins.
        """
        print('\n---- Карточки игроков ----')
        for player in self.players:
            print(f'Карточка игрока {player.name}:')
            player.card.show_card()

        keg = self.bag()

        for player in self.players:
            if player.identity == 'h':
                print(f'{player.name}, ваш ход!')
                user_answer = input('Зачеркнуть цифру? (y/n): ').lower().strip()
                if (user_answer == 'y' and not(keg in player.card)) or (user_answer != 'y' and keg in player.card):
                    print('Ответ неверный. Вы выбываете из игры.')
                    self.players.remove(player)
                    continue

            if keg in player.card:
                player.card.cross_num(keg)
            if player.card.empty_card_check():
                print(f'{player.name}, you win!')
                return player.id_number

        if len(self.players) == 1:
            print(f'{self.players[0].name}, you win!')
            return self.players[0].id_number

        return 0


if __name__ == '__main__':
    # print("Starting game...")
    print("Добро пожаловать в игру \"Лото\"!")
    game = Game()
    while True:
        score = game.play_round()
        if score != 0:
            print('Конец игры.')
            break
