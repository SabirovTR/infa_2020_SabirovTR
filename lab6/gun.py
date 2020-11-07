from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
POINTS = 0
BULLET = 0


class ball:

    def __init__(self, x=40, y=450, vx=0, vy=0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 7

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def walltest(self):
        """Проверка на столкновение снаряда со стеной."""
        if self.x - self.r < 0 or self.x + self.r > 800:
            self.vx *= -1
        elif self.y - self.r < 0 or self.y + self.r > 600:
            self.vy *= -1

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.live -= 0.03
        self.x += self.vx
        self.y += self.vy + 0.1
        self.vy += 0.1
        canv.move(self.id, self.vx, self.vy)
        self.walltest()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 < (self.r + obj.r) ** 2)

    def __del__(self):
        """Уничтожение снаряда."""
        canv.delete(self.id)


class gun:

    def __init__(self, x=20, y=450, vx=0, vy=0, v=5):
        """Размещение пушки на экране."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.v = v
        self.f2_power = 1
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(self.x, self.y, self.x + 30, self.y - 30, width=7)
        self.rot = False

    def fire2_start(self, event):
        """Функция, фиксирующая зажатие ЛКМ."""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, BULLET
        bullet += 1
        BULLET += 1
        new_ball = ball(self.x + max(self.f2_power * 5, 20) * math.cos(self.an),
                    self.y + max(self.f2_power * 5, 20) * math.sin(self.an))
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) + self.vx
        new_ball.vy = self.f2_power * math.sin(self.an) + self.vy
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 1

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - self.y) / (event.x - self.x)) + math.pi * (math.copysign(1, event.x - self.x) - 1) / 2
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power * 5, 20) * math.cos(self.an),
                    self.y + max(self.f2_power * 5, 20) * math.sin(self.an)
                    )

    def power_up(self):
        """Регулировка мощности выстрела.
        Увеличение начальной скорости снаряда при зажатие ЛКМ."""
        if self.f2_on:
            if self.f2_power < 20:
                self.f2_power += 0.2
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def walltest(self):
        """Проверка столкновения пушки со стеной и её остановка."""
        if not self.rot:
            if self.x < 5 or self.x > 795:
                self.vx *= -1
                self.rot = True
            if self.y < 5 or self.y > 595:
                self.vy *= -1
                self.rot = True
        elif 5 < self.x < 795 and 5 < self.y < 595:
            self.rot = False

    def move(self, event=0):
        """Перемещение пушки по полю.
        Пушка двигается по вертикали в направлении курсора."""
        self.walltest()
        if not self.rot:
            # self.vx = self.v * math.cos(self.an)
            self.vy = self.v * math.sin(self.an)
        self.x += self.vx
        self.y += self.vy
        canv.move(self.id, self.vx, self.vy)


class target:

    def __init__(self):
        """ Инициализация новой цели. """
        self.x = rnd(520, 760)
        self.y = rnd(120, 530)
        self.Ax = self.x - 620
        self.Ay = self.y - 325
        self.time = time.time()
        self.r = rnd(2, 20)
        self.color = 'red'
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
        canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
        canv.itemconfig(self.id, fill=self.color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global POINTS
        canv.coords(self.id, -10, -10, -10, -10)
        POINTS += points

    def move(self):
        """Перемещение цели по полю."""
        canv.move(self.id,
                  self.Ax * math.cos(time.time() - self.time) + 620 - self.x + 20 * math.sin(5 * (time.time() - self.time)),
                  self.Ay * math.cos(time.time() - self.time) + 325 - self.y + 20 * math.sin(5 * (time.time() - self.time)))
        self.x = self.Ax * math.cos(time.time() - self.time) + 620 + 20 * math.sin(5 * (time.time() - self.time))
        self.y = self.Ay * math.cos(time.time() - self.time) + 325 + 20 * math.sin(5 * (time.time() - self.time))


screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []
screen2 = canv.create_text(30, 30, text=str(POINTS) + ' : ' + str(BULLET), font='28')


def new_game(event=''):
    global gun, t1, screen1, balls, bullet, POINTS, BULLET
    t1 = target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    while t1.live or balls:
        i = 0
        while i < len(balls):
            balls[i].move()
            if balls[i].hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
                canv.itemconfig(screen2, text=str(POINTS) + ' : ' + str(BULLET))
            if balls[i].live < 0:
                balls.pop(i)
            i += 1
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
        g1.move()
        t1.move()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(3, new_game)


new_game()

root.mainloop()
