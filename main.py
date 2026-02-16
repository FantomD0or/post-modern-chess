import pygame
import random
import math
import sqlite3
import ast
import tkinter
import os

pygame.init()

ekran = [1200, 900]

sc_main = pygame.Surface(ekran)

FPS = 60
clock = pygame.time.Clock()
RUN = True


def smart_int(a):
    if "-" in a:
        return -1 * int(a.replace("-", ""))
    try:
        int(a)
        return int(a)
    except:
        return a


class Player:
    def __init__(self, x, y, hp, cards, artefact, all_kill, soul):
        self.x = x
        self.y = y
        self.hp = hp
        self.soul = soul
        self.cards = cards
        self.artefact = artefact
        self.all_kill = all_kill

    def uron(self, hp):
        self.hp -= hp
        sounds["attack"].play()
        
class Sistem:
    def __init__(self, all_kill, time_game, boss, sound):
        self.all_kill = all_kill
        self.time_geam = time_game
        self.boss = boss
        self.sound = sound

    def start_music(self, music):
        try:
            if self.sound:
                self.sound.stop()
                self.sound = music
                self.sound.play(-1)
            else:
                self.sound = music
                self.sound.play(-1)
        except:
            if self.sound:
                self.sound.stop()
            self.sound = False



    def base_seting(self):
        return {
            "cards_now": 0,
            "choss_what": False,
            "scrool_opisanie": 0,
            "scrool_chat": 0,
            "dialog": 0,
            "item": False,
            "round_itom": 0,
            "round_artifact": 0,
            "mous_on": False,
            "figur on mous": False
        }

class Soul_class:
    def __init__(self, move_map, png, name, gid):
        self.move_map = move_map
        self.png = png
        self.name = name
        self.gid = gid
        self.razbienie(move_map)

    def razbienie(self, _move_map):

        tipe = {
         "k": "only_kill",
         "m": "free",
         "n": "skip"
        }
        return_map = {}
        map = _move_map.split(",")
        for i in map:
            for_time = []
            if i[1] in tipe:
                for_time.append(tipe[i[1]])
            for_time.append(smart_int(i[2:4]))
            for_time.append(smart_int(i[5:6]))
            return_map[pygame.key.key_code(i[0])] = for_time

        self.real_map = return_map

    def load_act_soul_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            if type(search) == int:
                cursor.execute("""SELECT * FROM soul WHERE id = ?""", (str(search),))



            for res in cursor:
                for_time = Soul_class(res[1], True_Save.foto_load(res[3]), res[2], True_Save.foto_load(res[4]))

            return for_time


setting = {
    "cards_now": 0,
    "choss_what": False,
    "scrool_opisanie": 0,
    "scrool_chat": 0,
    "dialog": 0,
    "item": False,
    "round_itom": 0,
    "round_artifact": 0,
    "mous_on": False,
    "figur on mous": False
}



class Scale:
    def __init__(self, _real_screen, _ekran):
        self.scale_up = _ekran[0]
        self.scale_right = _ekran[1]
    
    def mous_get(self):
        up, right = pygame.mouse.get_pos()
        up = up * (ekran[0] / sc_real.get_width())
        right = right * (ekran[1] / sc_real.get_height())
        up = math.floor(up)
        right = math.floor(right)
        return up, right


root = tkinter.Tk()
root.withdraw() # Скрываем главное окно Tkinter
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


real_screen = [screen_width * (600/1200) * 1.3, screen_height * (1200/1920) * 1.3]
scale = Scale(real_screen, ekran)
sc_real = pygame.display.set_mode(real_screen, pygame.RESIZABLE)

scale_texst = math.floor(36 * (ekran[0]/screen_width))

nots = pygame.font.Font('texst/Merriweather_36pt_SemiCondensed-BlackItalic.ttf', scale_texst)
mini_nots = pygame.font.Font('texst/Merriweather_36pt_SemiCondensed-BlackItalic.ttf',  scale_texst)

pygame.display.set_caption("пост модерн шахматы")
pygame.display.set_icon(pygame.image.load("png_like/logo-Photoroom.png"))




option_settings = {
    "all_png": "base texsture pack",
    "languje": "ru"
}

all_gif = {

}


class Save:
    def __init__(self):
        self.base = option_settings["all_png"]
        self.all_pak_texsture()

    def foto_load(self, z):
        c = z.replace("png_like/", "")

        try:
            a = pygame.image.load("png_like/" + self.base + "/" + c)
            return a
        except:
            try:
                a = pygame.image.load("png_like/base texsture pack/" + c)
                print("файл не найде в кастомной базе данных")
                return a
            except:
                print("файл не найде в базе данных")
                return pygame.image.load("png_like/debag.png")

    def all_pak_texsture(self):
        list = os.listdir("png_like")
        returning_list = []
        for i in list:
            if not "." in i:
                returning_list.append([i, pygame.image.load("png_like/" + i + "/logo.png")])
        self.pak_texsture = returning_list

    def up_save(self):

        data = sqlite3.connect('data base/save_file.db')

        now = 0
        cursor = data.cursor()
        long = cursor.execute("SELECT MAX(id) FROM save")

        for res in long:
            long = res[0]

        playr_to_time = self.start_seting()

        #try:
        for i in range(int(long) + 1):

            cursor = data.cursor()

            enter = cursor.execute("SELECT * FROM save WHERE id = " + str(i))

            for res in enter:
                now = res

            if now[0] == "player_info":
                    if now[2] == "x":
                        playr_to_time.x = int(now[3])
                    if now[2] == "y":
                        playr_to_time.y = int(now[3])
                    if now[2] == "hp":
                        playr_to_time.hp = int(now[3])



            elif now[0] == "cards":
                playr_to_time.cards.append(Cards.load_card_from_data_base(int(now[2])))
                playr_to_time.cards[len(playr_to_time.cards)-1].leval = int(res[3])

            elif now[0] == "artefact":
                playr_to_time.artefact.append(Cards.load_card_from_data_base(int(now[2])))
                playr_to_time.artefact[len(playr_to_time.artefact)-1].leval = int(res[3])

        return playr_to_time

    def creat_save(self, we_save):

        with sqlite3.connect('data base/save_file.db') as data:
            cursor = data.cursor()

            cursor.execute("DELETE FROM save")
            
            a = [
                [we_save.x, "x"],
                [we_save.y, "y"],
                [we_save.hp, "hp"]
            ]

            i = 0
            for j in range(3):

                enter = "INSERT INTO save (id,type,more_inf,more_more_inf) VALUES (" + str(
                    i) + """, 'player_info', '""" + str(a[j][1]) + "', '" + str(a[j][0]) + "')"
                
                i += 1

                cursor.execute(enter)

            for j in we_save.cards:

                enter = "INSERT INTO save (id,type,more_inf,more_more_inf) VALUES (" + str(
                    i) + """, 'cards', '""" + str(j.id) + "', " + str(j.leval) + ")"

                i += 1

                cursor.execute(enter)

            for j in we_save.artefact:
                enter = "INSERT INTO save (id,type,more_inf,more_more_inf) VALUES (" + str(
                    i) + """, 'artefact', """ + str(j.id) + ", " + str(j.leval) + ")"

                i += 1

                cursor.execute(enter)

    def render_pak(self):
        for i in range(len(self.pak_texsture)):

            sc_main.blit(pygame.transform.scale(self.pak_texsture[i][1], [100, 100]), [0, i * 100])
            sc_main.blit(nots.render(self.pak_texsture[i][0], True, (255, 255, 255)), [0, i * 100])

    def reload(self):

        tesxture_blok.update({
            "fon": True_Save.foto_load("fon.png"),
            "no_end_fon": True_Save.foto_load("fon_kill.png"),
            "hp": [True_Save.foto_load("hp1.png"),
                   True_Save.foto_load("hp2.png")],
            "reset": True_Save.foto_load("vibor.png"),
            })

    def pre_load(self):
        data = sqlite3.connect('data base/save_file.db')

        for i in range(1):

            cursor = data.cursor()

            enter = cursor.execute("SELECT * FROM save_staf")

            _settings = {}

            for res in enter:
                _settings[res[0]] = smart_int(res[1])

        return _settings




    def load_translate_from_data_base(self, what):
        data = sqlite3.connect('data base/all vrag.db')
        cursor = data.cursor()

        enter = "SELECT " + option_settings["languje"] + " FROM translate WHERE id = " + str(what)

        cursor.execute(enter)

        for res in cursor:
            return res[0]

    def start_seting(self):
        sus = Soul_class.load_act_soul_data_base(3)
        base = Player(3, -2, 3, [], [], [], sus)
        return base

    def load_chans(self, ip):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            cursor.execute("""SELECT * FROM chans WHERE ip = ?""", (str(ip),))

            now = 0

            for res in cursor:
                now = ast.literal_eval(res[1])
            return now

    def geting_staf(self, what, to):
        with sqlite3.connect('data base/save_file.db') as data:
            cursor = data.cursor()
            l = "UPDATE save_staf SET valium = '" + str(to) + "' WHERE tipe = '" + str(what) + "'"
            cursor.execute(l)

True_Save = Save()

playr_now = True_Save.start_seting()

sistem_seting = Sistem([], 0, [0, 0], False)



tesxture_blok = {
    "fon": True_Save.foto_load("fon.png"),
    "no_end_fon": True_Save.foto_load("fon_kill.png"),
    "hp": [True_Save.foto_load("hp1.png"),
           True_Save.foto_load("hp2.png")],
    "reset": True_Save.foto_load("vibor.png"),
    "seting": True_Save.foto_load("seting.png")
}

True_Save.reload()

def truE(a):
    if a == "False" or a == 0 or a == "0":
        return False
    return a

class Gif:
    def __init__(self, were, type, long):
        self.id = were
        self.type = type
        self.long = long
        self.time_pass = 0
        self.init()

    def init(self):
        list = os.listdir("png_like/base texsture pack/gif/" + self.id)
        returning_list = []
        for i in list:
                returning_list.append(True_Save.foto_load("gif/" + self.id + "/" + i))
        self.list = returning_list
        self.speed = self.long / len(self.list)

    def render(self, time):
        self.time_pass += time

        if self.time_pass > self.long:
            if self.type == "cycle":
                self.time_pass = 0
            elif self.type == "stop":
                self.time_pass = self.long
            else:
                self.type = False
        if self.type:
            return self.list[math.floor(self.time_pass/self.speed)]
        else:
            return self.list[len(self.list) -1]

class Objet:
    def __init__(self, foto, more_inf, name, ai, _type):
        self.foto = foto
        self.more_inf = more_inf
        self.name = name
        self.ai = ai
        self.type = _type

    def load_obj_from_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            if type(search) == int:
                cursor.execute("""SELECT * FROM obj_inf WHERE id = ?""", (search,))
            else:
                cursor.execute("""SELECT id FROM obj_inf WHERE id = ?""", (str(search),))

            for res in cursor:
                return_ing = Objet(True_Save.foto_load(res[2]), {
                            "destrakt": int(res[5]),
                            "kill": int(res[6]),
                            "trans": truE(res[7]),
                            "dialog": truE(res[8]),
                            },
                            True_Save.load_translate_from_data_base(res[3]),
                            truE(res[4]),
                            truE(res[1])
                                   )



            if return_ing.ai:
                ai_set = {}
                if "!@#$" in return_ing.ai:
                    ai_set["use"] = True
                    return_ing.ai = return_ing.ai.replace("!@#$", "")
                else:
                    ai_set["use"] = False

                ai_set["type"] = return_ing.ai

                return_ing.ai = ai_set
            else:
                return_ing.ai = {}

            if True:
                if "sunduk_" in return_ing.type or "seller_" in return_ing.type:
                    return_ing.more_inf["chans"] = True_Save.load_chans(return_ing.type.split("_")[1])
                    return_ing.type = return_ing.type.split("_")[0]

            if return_ing.more_inf["dialog"]:
                return_ing.more_inf["dialog"] = Dialog.load_dialog_from_data_base(return_ing.more_inf["dialog"])
            if not return_ing.more_inf["trans"]:
                return_ing.foto = pygame.transform.scale(return_ing.foto, (50, 50))
            return return_ing

    def ai_chet(self, were, x, y):


        go_to_ = {"up": [0, -1],
                  "down": [0, 1],
                  "left": [-1, 0],
                  "right": [1, 0]}
        player_x_y = playr_now.x%were.RAZMER, playr_now.y%were.RAZMER

        self.ai["use"] = True
        if self.ai["type"] == "random":
            new_x_y = random.randint(0, 2) - 1, random.randint(0, 2) - 1
            i = 10
            while i:
                if not (new_x_y[0] == 0 and new_x_y[1] == 0):
                    if were.exsit_to_space(x + new_x_y[0], y + new_x_y[1]):
                        if not were.local_World[x + new_x_y[0]][y + new_x_y[1]]:
                            were.local_World[x + new_x_y[0]][y + new_x_y[1]] = were.local_World[x][y]
                            were.local_World[x][y] = False
                            i = 1
                new_x_y = random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1
                i -= 1

        elif "move_" in self.ai["type"]:
            vectore = go_to_[self.ai["type"][5:]]
            if were.exsit_to_space(x + vectore[0], y + vectore[1]):
                were.local_World[x + vectore[0]][y + vectore[1]] = were.local_World[x][y]
                were.local_World[x][y] = False
            else:
                were.local_World[x][y] = False

        elif "goplayer" in self.ai["type"]:
            new_x_y = [0, 0]
            if player_x_y[0] > x:
                new_x_y[0] = 1
            elif player_x_y[0] < x:
                new_x_y[0] = -1
            elif player_x_y[1] > y:
                new_x_y[1] = 1
            elif player_x_y[1] < y:
                new_x_y[1] = -1
            if were.exsit_to_space(x + new_x_y[0], y + new_x_y[1]):
                if not were.local_World[x + new_x_y[0]][y + new_x_y[1]]:
                    were.local_World[x + new_x_y[0]][y + new_x_y[1]] = were.local_World[x][y]
                    if new_x_y[0] or new_x_y[1]:
                        were.local_World[x][y] = False

        elif "bishop" in self.ai["type"]:
            ex, ey = x, y
            px, py = player_x_y

            if (ex, ey) == (px, py):
                return (ex, ey)

            dx = 1 if px > ex else -1 if px < ex else 0
            dy = 1 if py > ey else -1 if py < ey else 0

            step_x = dx if dx != 0 else 1
            step_y = dy if dy != 0 else 1

            if were.exsit_to_space(step_x + ex, step_y + ey):
                were.local_World[ex + step_x][ey + step_y] = self
                were.local_World[x][y] = False

class Cards:
    def __init__(self, foto, name, type, leval, more_inf, id):
        self.foto = foto
        self.name = name
        self.type = type
        self.leval = leval
        self.more_inf = more_inf
        self.id = id

    def load_card_from_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()


            cursor.execute("""SELECT * FROM cards WHERE id = ? """, (str(search),))


            res = []

            more_inf = {}



            for a in cursor:
                res.append(a)

            if type(res[0]) == type(()):
                res = res[0]

            returing = Cards(True_Save.foto_load(res[4]),
                        True_Save.load_translate_from_data_base(res[1]),
                        res[2],
                        int(res[3]),
                         more_inf,
                         search
                            )

            if res[2]:
                if "_tick_" in returing.type:
                    more_inf["tick"] = int(returing.type.split("_")[2])
                    returing.type = returing.type.split("_")[0]


            return returing

    def efect_card(self, where):
        if self.type == "hp+":
            playr_now.hp += self.leval

        if self.type == "move":
            playr_now.y -= self.leval + where.RAZMER
            where.room_generate(playr_now.x, playr_now.y)

        if self.type == "spawn_arrow_left":
            if where.exsit_to_space(playr_now.x%where.RAZMER, playr_now.y%where.RAZMER):
                where.local_World[playr_now.x%where.RAZMER][playr_now.y%where.RAZMER] = Objet.load_obj_from_data_base(10)

        if self.type == "tp":
            playr_now.y += random.randint(0, where.RAZMER-1) - math.floor(where.RAZMER/2)
            playr_now.x += random.randint(0, where.RAZMER-1) - math.floor(where.RAZMER/2)

        if "spial_" in self.type:
            obj_id = int(self.type.split("_")[1])
            directions = [
                (0, -1, "move_up"),
                (0, 1, "move_down"),
                (-1, 0, "move_left"),
                (1, 0, "move_right")
            ]

            px, py = playr_now.x, playr_now.y
            size = where.RAZMER

            for dx, dy, ai_command in directions:
                nx, ny = (px + dx) % size, (py + dy) % size
                if not where.local_World[nx][ny]:
                    new_obj = Objet.load_obj_from_data_base(obj_id)
                    new_obj.ai = {}
                    new_obj.ai["type"] = ai_command
                    new_obj.ai["use"] = True
                    where.local_World[nx][ny] = new_obj

        if "dropplayre_" in self.type:
            obj_id = int(self.type.split("_")[1])
            where.local_World[playr_now.x][0] = Objet.load_obj_from_data_base(obj_id)
            where.local_World[playr_now.x][0].ai["type"] = "move_down"
            where.local_World[playr_now.x][0].ai["use"] = True



        playr_now.cards.pop(setting["cards_now"])
        if setting["cards_now"]: setting["cards_now"] -= 1


    def efect_itom(self, where):
        for_time = 0
        run = True
        if "tick" in self.more_inf:
            if self.leval != 0:
                run = False
            else:
                self.leval = self.more_inf["tick"]

        if run:
            if self.type == "clear":
                for_time = self.leval
                for i in playr_now.all_kill:
                    self.leval += 1
                    if i.more_inf["kill"]:
                        self.leval += 1
                playr_now.all_kill = []
                for_time -= self.leval


            if self.type == "cliker":
                self.leval += 1

            if self.type == "MoveLeft":
                playr_now.y -= 1
                playr_now.x -= 1

            if self.type == "MoveRight":
                playr_now.y -= 1
                playr_now.x += 1

            if self.type == "FirstMove":
                if playr_now.y%where.RAZMER == where.RAZMER -2:
                    playr_now.y -= 2

            if self.type == "hp_up":

                if for_time >= self.leval:
                    playr_now.hp += 1


        else:
            playr_now.artefact[setting["item"]].leval -= 1

class Place:
    def __init__(self, name, spawn_pice, cell1, cell2, type, fon, music):
        self.name = name
        self.spawn_pice = spawn_pice #[[айди объекта], [шанс]]
        self.cell1 = cell1
        self.cell2 = cell2
        self.type = type
        self.fon = fon
        self.music = music

    def get_random(self, _x_chank, _y_chank):
        if random.randint(1, 8) == 4:
            weight = self.spawn_pice[1]
            chos = random.choices(self.spawn_pice[0], weights=weight, k=1)[0]
            return Objet.load_obj_from_data_base(chos)
        return False


    def load_place_from_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            if type(search) == int:
                cursor.execute("""SELECT * FROM locathion_inf WHERE id = ?""", (str(search),))

            else:
                cursor.execute("""SELECT * FROM locathion_inf WHERE name = ?""", (search,))



            now = 0

            for res in cursor:
                now = Place(res[1], True_Save.load_chans(res[4]), True_Save.foto_load(res[2]), True_Save.foto_load(res[3]),
                            res[5],  truE(res[6]), truE(res[7]))


            if truE(now.fon):
                now.fon = Gif(res[6], "cycle", 2)
            if truE(now.music):
                now.music = pygame.mixer.Sound(now.music)



            return now

class IMenu:
    def __init__(self, gui):
        self.gui = gui
        self.test = False

    def button_mous(self, mous):
        m_x, m_y = mous[0], mous[1]

        for i, element in enumerate(self.gui):
            if len(element) == 4:
                x1, y1, x2, y2 = element
                if x1 <= m_x <= x2 and y1 <= m_y <= y2:
                    return i + 1

            elif len(element) == 3:
                cx, cy, r = element
                if self.test:
                    pygame.draw.circle(sc_main, (255, 255, 255), (cx, cy), r)
                if (m_x - cx) ** 2 + (m_y - cy) ** 2 <= r ** 2:
                    return i + 1

        return False

class World:
    def __init__(self, seed, we_now):
        self.seed = seed
        self.RAZMER = 8
        self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
        self.we_now = we_now
        self.up_leval = {
                         8: 0,
                         9: -300,
                         10: -1000,
                         11: -10000000000
                         }

    def render(self):

        size = 8 / self.RAZMER

        mesto = self.local_World


        holst = pygame.Surface((self.RAZMER * 50, self.RAZMER * 50))

        for x in range(self.RAZMER):
            for y in range(self.RAZMER):
                if x % 2 == y % 2:
                    holst.blit(self.we_now.cell1, (x * 50, y * 50))
                else:
                    holst.blit(self.we_now.cell2, (x * 50, y * 50))


        for x in range(self.RAZMER):
            for y in range(self.RAZMER):
                if mesto[x][y]:
                    if mesto[x][y].more_inf["trans"]:
                        holst.blit(mesto[x][y].foto, (x * 50 * size - (mesto[x][y].foto.get_size()[0] / 4) * size,
                                    y * 50 * size - (mesto[x][y].foto.get_size()[1] / 4) * size))
                    else:
                        holst.blit(mesto[x][y].foto, (x * 50, y * 50))

        self.jod(holst)
        sc_main.blit(pygame.transform.scale(holst, (400, 400)), (400, 200))

        self.other_staf()
        self.choss_render()
        self.texst_inf()
        self.texst_dialog()
        self.hp_render()





        if setting["figur on mous"]:
            sc_main.blit(pygame.transform.scale(playr_now.soul.png, (50 * size, 50 * size)), (scale.mous_get()))
        else:
            sc_main.blit(pygame.transform.scale(playr_now.soul.png, (50 * size, 50 * size)),
                         (400 + playr_now.x % self.RAZMER * 50 * size,
                          200 + playr_now.y % self.RAZMER * 50 * size))



        pass

    def jod(self, where):
        size = 8 / self.RAZMER
        map = playr_now.soul.real_map
        cloro = {
            "free": (19, 136, 8),
            "only_kill": (228, 155, 15)
        }


        if setting["figur on mous"]:
            for i in map:
                FIG = map[i]
                pygame.draw.rect(where, cloro[FIG[0]], ((playr_now.x - FIG[1])%self.RAZMER * 50,
                                                      (playr_now.y - FIG[2])%self.RAZMER * 50,
                                                      50 * size, 50 * size))




    def hp_render(self):
        for i in range(playr_now.hp):
            sc_main.blit(pygame.transform.scale(tesxture_blok["hp"][math.floor(i/10)], (28, 28)),
                         (690 + i%10 * 28, 15))

    def other_staf(self):
        size = 8 / self.RAZMER

        sc_main.blit(nots.render(str(playr_now.y * -1) + " - " + one_to_ABC(int(math.fabs(playr_now.x + 1))), True,
                                 (255, 255, 255)), (0, 0))
        sc_main.blit(pygame.transform.scale(playr_now.soul.png, (182, 217)), (190, 40))

        sc_main.blit(playr_now.soul.gid, (336,663))

        if self.up_leval[self.RAZMER+1] - playr_now.y < 0:
            sc_main.blit(nots.render(str((self.up_leval[self.RAZMER+1] - playr_now.y) * -1),
                                     True, (255, 0, 0)), (47, 650))
        else:
            sc_main.blit(nots.render(str((self.up_leval[self.RAZMER+1] - playr_now.y) * -1),
                                     True, (0, 255, 0)), (47, 650))

        for i in range(len(playr_now.all_kill)):
            sc_main.blit(pygame.transform.scale(playr_now.all_kill[i].foto, (50, 50)),
                         (912 + i*50, 847))

        if setting["cards_now"] - 1 >= 0:
            sc_main.blit(pygame.transform.scale(playr_now.cards[setting["cards_now"] - 1].foto, (40, 64)),
                         (60, 800))
        if playr_now.cards != []:
            sc_main.blit(pygame.transform.scale(playr_now.cards[setting["cards_now"]].foto, (70, 100)),
                         (115, 785))
        if setting["cards_now"] + 1 < len(playr_now.cards):
            sc_main.blit(pygame.transform.scale(playr_now.cards[setting["cards_now"] + 1].foto, (40, 64)),
                         (200, 800))

        for i in range(len(playr_now.artefact)):
            sc_main.blit(pygame.transform.scale(playr_now.artefact[i].foto, (40, 40)),
                         (960 + i%6 * 40, 229 + math.floor(i/6)*40))

    def texst_inf(self):
        if setting["choss_what"] or type(setting["item"]) == int:
            text = ""
            if type(setting["item"]) == int:
                    we_see = playr_now.artefact[setting["item"]]
                    text = we_see.name
                    text += "\nуровень улучшения: " + str(we_see.leval)
            elif setting["choss_what"] == "cards":
                if playr_now.cards != []:
                    text = playr_now.cards[setting["cards_now"]].name
                    text += "\nуровень улучшения: " + str(playr_now.cards[setting["cards_now"]].leval)
            elif type(setting["choss_what"][0]) == int:
                if zith.local_World[setting["choss_what"][0]][setting["choss_what"][1]]:
                    text = zith.local_World[setting["choss_what"][0]][setting["choss_what"][1]].name



            #text = "круть! \n это работает \n я как минимум хочу \n я хочу верить"

            writing_text = []
            time_text = text.split("\n")
            for line in time_text:
                while len(line) > 20:
                    split_index = line.rfind(' ', 0, 20)
                    if split_index == -1:
                        split_index = 20

                    substring = line[:split_index].strip()
                    writing_text.append(substring)

                    line = line[split_index:].lstrip()
                if line:
                    writing_text.append(line)
            r = 0
            for i in writing_text[setting["scrool_opisanie"]:setting["scrool_opisanie"] + 8]:
                sc_main.blit(mini_nots.render(i, True, (0, 0, 0)), (670 - r * 5, 680 + r * 25))
                r += 1

    def texst_dialog(self):
        if setting["choss_what"]:
            if type(setting["choss_what"][0]) == int:
                what_we_chos = self.local_World[setting["choss_what"][0]][setting["choss_what"][1]]
                if what_we_chos:
                    if what_we_chos.more_inf["dialog"]:
                        all_we_need = []
                        all_we_need.append(what_we_chos.more_inf["dialog"].text)
                        if what_we_chos.more_inf["dialog"].opthion1: all_we_need.append(what_we_chos.more_inf["dialog"].opthion1.text)
                        else:
                            all_we_need.append(False)
                        if what_we_chos.more_inf["dialog"].opthion2:all_we_need.append(what_we_chos.more_inf["dialog"].opthion2.text)
                        else:
                            all_we_need.append(False)
                        if what_we_chos.more_inf["dialog"].opthion3:all_we_need.append(what_we_chos.more_inf["dialog"].opthion3.text)
                        else:
                            all_we_need.append(False)

                        for i in range(4):
                            text = all_we_need[i]
                            if text:
                                writing_text = []
                                time_text = text.split("\n")
                                for line in time_text:
                                    while len(line) > 10:
                                        split_index = line.rfind(' ', 0, 10)
                                        if split_index == -1:
                                            split_index = 10

                                        substring = line[:split_index].strip()
                                        writing_text.append(substring)

                                        line = line[split_index:].lstrip()
                                    if line:
                                        writing_text.append(line)

                                scrool = setting["dialog"]
                                if i:
                                    scrool = setting["scrool_chat"]

                                r = 0
                                for c in writing_text[scrool:scrool + 8]:
                                    sc_main.blit(mini_nots.render(c, True, (255, 255, 255)),
                                                                                    (igra_gui.gui[8 + i][0]+20,
                                                                                         igra_gui.gui[8 + i][1]+20 + r*20))
                                    r += 1

    def choss_render(self):
        SIZE = 8/zith.RAZMER
        if setting["choss_what"]:
            if setting["choss_what"] == "cards":
                pygame.draw.rect(sc_main, (255, 255, 0), (112, 782, 76, 106), 3)
            elif type(setting["choss_what"]) == type([]):
                pygame.draw.rect(sc_main, (255, 255, 0),
                                 (400 + setting["choss_what"][0] * (50 * SIZE),
                                  200 + setting["choss_what"][1] * (50 * SIZE)
                                  , 50, 50), 3)
        if type(setting["item"]) == int:
            pygame.draw.rect(sc_main, (255, 255, 0), (960 + setting["item"] % 6 * 40 - 3,
                                                      229 + math.floor(setting["item"] / 6) * 40 - 3,
                                                      40 + 3, 40 + 3), 3)

    def room_generate(self, x, y):

        if self.we_now.type == "free":

            _x = math.floor(x / self.RAZMER)
            _y = math.floor(y / self.RAZMER)
            self.smena(y)
            self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
            code_input = int((str(self.seed % 10000) + str(_x) + str(_y)).replace("-", "")) % 100000
            random.seed(code_input)

            pass
            for x_index in range(self.RAZMER):
                for y_index in range(self.RAZMER):
                    code_input = random.randint(1, 4096)
                    placing = self.we_now.get_random(x, y)
                    if placing:
                        if placing.type == "portal":
                            placing.more_inf["teleport"] = random.randint(1, code_input % 10 + 2) * 8

                    self.local_World[x_index][y_index] = placing

            if self.we_now.name == "medium":
                if not random.randint(1, 10) - 1:
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    for _X in range(3):
                        for _Y in range(3):
                            self.local_World[0 + _X][2 + _Y] = Objet.load_obj_from_data_base(8)
                    self.local_World[1][3] = Objet.load_obj_from_data_base(7)

                if _y == math.floor(-250 / self.RAZMER) or _y+1 == math.floor(-250 / self.RAZMER):
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(33)
                if _y == math.floor(-550 / self.RAZMER) or _y + 1 == math.floor(-550 / self.RAZMER):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(37)
                if math.floor(-550/ self.RAZMER) > _y > math.floor(-660/ self.RAZMER):
                    self.local_World = [[Objet.load_obj_from_data_base(38) for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(37)

        if not(sistem_seting.boss[0]) and sistem_seting.boss[1]:
            if self.we_now.name == "hell":


                playr_now.y -= 300
    def triger(self):
        obj_triger = self.local_World[playr_now.x%self.RAZMER][playr_now.y%self.RAZMER]

        if obj_triger:
            if "portal" == obj_triger.type:
                playr_now.y -= obj_triger.more_inf["teleport"]
                self.room_generate(playr_now.x, playr_now.y)

            if "sunduk" == obj_triger.type:
                choos = random.choices(obj_triger.more_inf["chans"][0], weights=obj_triger.more_inf["chans"][1], k=1)[0]

                playr_now.cards.append(Cards.load_card_from_data_base(choos))



            if obj_triger.more_inf["destrakt"]:
                if len(playr_now.all_kill) == 5:
                    #этот кусок кода оставлен для тех кто захочет опровергнуть мои мучения
                    #тоетсь не трогайте этот кусок кода
                    playr_now.all_kill[4] = playr_now.all_kill[3]
                    playr_now.all_kill[3] = playr_now.all_kill[2]
                    playr_now.all_kill[2] = playr_now.all_kill[1]
                    playr_now.all_kill[1] = playr_now.all_kill[0]
                    playr_now.all_kill[0] = obj_triger
                else:
                    playr_now.all_kill.append(obj_triger)
                self.local_World[playr_now.x%self.RAZMER][playr_now.y%self.RAZMER] = False

            if "give_artfact_" in obj_triger.type:
                self.add_artifact(
                    Cards.load_card_from_data_base(int(obj_triger.type.replace("give_artfact_", ""))))

            if obj_triger.type == "hp+":
                playr_now.hp += 1

            if obj_triger.type == "chet":
                if sistem_seting.boss[1]:
                    sistem_seting.boss[0] -= 1

    def canculate_tick(self):

        pass

        self.supruse()
        for x in range(self.RAZMER):
            for y in range(self.RAZMER):
                if self.local_World[x][y]:
                    if self.local_World[x][y].ai != {}:
                        if not self.local_World[x][y].ai["use"]:
                            self.local_World[x][y].ai_chet(self, x, y)


        for x in range(self.RAZMER):
            for y in range(self.RAZMER):
                if self.local_World[x][y]:
                    if self.local_World[x][y].ai:
                        self.local_World[x][y].ai["use"] = False

        obj_triger = zith.local_World[playr_now.x%zith.RAZMER][playr_now.y%zith.RAZMER]

        if obj_triger:
            if obj_triger.more_inf["kill"]:
                playr_now.uron(obj_triger.more_inf["kill"])



    def exsit_to_space(self, plus_y, plus_x):
        if plus_x < self.RAZMER:
            if plus_x >= 0:
                if plus_y < self.RAZMER:
                    if plus_y >= 0:
                        return True
        return False

    def smena(self, y):
        smenit = False
        if self.we_now.type == "free":
            if -250 < y < 8 and self.we_now.name != "start":
                self.we_now = Place.load_place_from_data_base(1)
                smenit = True

            elif -750 < y < -250 and self.we_now.name != "medium":
                self.we_now = Place.load_place_from_data_base(2)
                smenit = True

            elif y < -750 and self.we_now.name != "end":
                self.we_now = Place.load_place_from_data_base(3)
                smenit = True

            if smenit:

                sistem_seting.start_music(self.we_now.music)
                
                if self.we_now.fon:
                    all_gif["profil"] = self.we_now.fon

    def add_artifact(self, adding):
        go = True
        for i in playr_now.artefact:
            if i.name == adding.name:
                go = False
        if go:
            playr_now.artefact.append(adding)

    def spael(self, choss):
        we_see = setting["choss_what"]
        run = False
        if we_see:
            if self.local_World[we_see[0]][we_see[1]].more_inf["dialog"]:
                if choss == 1:
                    if self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion1:
                        run = self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion1
                if choss == 2:
                    if self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion2:
                        run = self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion2
                if choss == 3:
                    if self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion3:
                        run = self.local_World[we_see[0]][we_see[1]].more_inf["dialog"].opthion3
                if run:
                    if run.type == "End":
                        self.local_World[we_see[0]][we_see[1]].more_inf["dialog"] = Dialog.load_dialog_from_data_base(3)
                        playr_now.y -= 200

                    elif "trade" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        what_take[2] = int(what_take[2])
                        if playr_now.artefact[0].leval >= what_take[1]:
                            playr_now.artefact[0].leval -= what_take[1]
                            if what_take[2]%2:
                                playr_now.cards.append(Cards.load_card_from_data_base(what_take[2]))
                            else:
                                self.add_artifact(Cards.load_card_from_data_base(what_take[2]))

                    elif "predati_" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        what_take[2] = int(what_take[2])
                        if playr_now.hp >= what_take[1]:
                            playr_now.hp -= what_take[1]
                            if what_take[2]%2:
                                playr_now.cards.append(Cards.load_card_from_data_base(what_take[2], True))
                            else:
                                self.add_artifact(Cards.load_card_from_data_base(what_take[2], True))

                    elif "tp_" in run.type:
                        what_take = run.type.split("_")
                        self.we_now = Place.load_place_from_data_base(int(what_take[1]))
                        if self.we_now.fon:
                            all_gif["profil"] = self.we_now.fon
                        self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]

                    elif "transform_" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        if what_take[1]:
                            self.local_World[we_see[0]][we_see[1]] = Objet.load_obj_from_data_base(what_take[1])
                        else:
                            self.local_World[we_see[0]][we_see[1]] = False

                    elif "go_to_" in run.type:
                        self.local_World[we_see[0]][we_see[1]].more_inf["dialog"] \
                            = Dialog.load_dialog_from_data_base(int(run.type.split("_")[2]))

    def supruse(self):
        if sistem_seting.boss[1] and (not sistem_seting.boss[0]):
            self.we_now.type = "free"
            if self.we_now.name == "hell":
                if playr_now.y >= -750:
                    playr_now.y = -750 - self.RAZMER
        if self.we_now.name == "hell":
            if not sistem_seting.boss[1]:
                 sistem_seting.boss = [15, 15]
                 all_gif["profil"] = Gif("boss", "cycle", 10)
                 sistem_seting.start_music(sounds["boss"])
                 Scena.scena = Gif("katstsena", "bla", 8)

            if not (sistem_seting.time_geam+10)%10:
                type_atack = math.floor((sistem_seting.time_geam+10)/10)%6
                spawn_base = [
                    [0, 0],
                    [0, self.RAZMER-1],
                    [self.RAZMER-1, 0],
                    [self.RAZMER-1, self.RAZMER-1]
                              ]
                if type_atack == 0 or type_atack == 3:
                    if type_atack:
                        self.local_World[0] = [Objet.load_obj_from_data_base(34) for _ in range(self.RAZMER)]
                        self.local_World[0][random.randint(0, self.RAZMER-1)] = Objet.load_obj_from_data_base(35)
                    else:
                        get = random.randint(0, self.RAZMER - 1)
                        for i in range(self.RAZMER):
                            get = random.randint(0, self.RAZMER - 1)
                            self.local_World[self.RAZMER-1][i] = Objet.load_obj_from_data_base(34)
                            self.local_World[self.RAZMER-1][i].ai["type"] = "move_left"
                            self.local_World[self.RAZMER - 1][i].ai["use"] = True
                            self.local_World[self.RAZMER-1][i].foto = pygame.transform.rotate(self.local_World[self.RAZMER-1 ][i].foto, 180)
                        self.local_World[self.RAZMER - 1][get] = Objet.load_obj_from_data_base(35)
                        self.local_World[self.RAZMER - 1][get].ai["type"] = "move_left"
                        self.local_World[self.RAZMER - 1][get].ai["use"] = True
                        self.local_World[self.RAZMER - 1][get].foto = pygame.transform.rotate(self.local_World[self.RAZMER-1 ][get].foto, 180)

                elif type_atack == 1 or type_atack == 4:
                    for i in range(3):
                        get = random.randint(0, self.RAZMER-1)
                        self.local_World[get][0] = Objet.load_obj_from_data_base(35)
                        self.local_World[get][0].ai["type"] = "move_down"
                        self.local_World[get][0].ai["use"] = True
                        self.local_World[get][0].foto = pygame.transform.rotate(self.local_World[get][0].foto, 270)

                elif type_atack == 2 or type_atack == 5:
                    for i in range(4):
                        self.local_World[spawn_base[i][0]][spawn_base[i][1]] = Objet.load_obj_from_data_base(36)

class Dialog:
    def __init__(self, text, opthion1, opthion2, opthion3):
        self.text = text
        self.opthion1 = opthion1
        self.opthion2 = opthion2
        self.opthion3 = opthion3

    def load_dialog_from_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            if type(search) == int:
                cursor.execute("""SELECT * FROM dialog WHERE id = ? """, (str(search),))

            for res in cursor:
                return_ing = Dialog(True_Save.load_translate_from_data_base(res[1]),
                            truE(res[2]),
                            truE(res[3]),
                            truE(res[4])
                                )
            if return_ing.opthion1:
                return_ing.opthion1 = Act.load_act_from_data_base(int(return_ing.opthion1))
            if return_ing.opthion2:
                return_ing.opthion2 = Act.load_act_from_data_base(int(return_ing.opthion2))
            if return_ing.opthion3:
                return_ing.opthion3 = Act.load_act_from_data_base(int(return_ing.opthion3))

            return return_ing

class Act:
    def __init__(self, text, type):
        self.text = text
        self.type = type

    def load_act_from_data_base(search):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            if type(search) == int:
                cursor.execute("""SELECT * FROM ACT WHERE id = ? """, (search,))
            else:
                cursor.execute("""SELECT id FROM ACT WHERE id = ?""", (str(search),))

            for res in cursor:
                return Act(True_Save.load_translate_from_data_base(res[1]),
                           res[2])

class line:
    def __init__(self, color1, color2, coordinate):
        self.color1 = color1
        self.color2 = color2
        self.coor = coordinate


    def print(self, min, max):
        pygame.draw.rect(sc_main, self.color1, [self.coor[0],
                                                self.coor[1],
                                                self.coor[2] - self.coor[0],
                                                self.coor[3] - self.coor[1]])
        pygame.draw.rect(sc_main, self.color2, [self.coor[0],
                                                self.coor[1],
                                                (self.coor[2] - self.coor[0]) * min/max,
                                                self.coor[3] - self.coor[1]])

class Trangul:
    def round(x, y, r, d):
        return math.sin(r)*d + x, math.cos(r)*d + y

    def angel(x1, y1, x2, y2):
        return math.atan2(y1-y2, x1-x2)



def one_to_ABC(n):
    if n == 0:
        return "0"

    letters = "ABCDEFGH"
    result = ""

    while n > 0:
        n -= 1
        remainder = n % 8
        result = letters[remainder] + result
        n //= 8

    return result

def move(world, ikey, for_who):


    sistem_seting.time_geam += 1

    past_chunk_x = playr_now.x // zith.RAZMER
    past_chunk_y = playr_now.y // zith.RAZMER

    job = False
    move_pos = False

    if ikey in for_who.real_map:
        sounds["move"].play()
        job = True
        what_do = for_who.real_map[ikey]
        move_pos = False

        if what_do[0] == "free":
            move_pos = True


        elif what_do[0] == "only_kill":
            if world.exsit_to_space(playr_now.x % world.RAZMER - what_do[1], playr_now.y % world.RAZMER - what_do[2]):
                if world.local_World[playr_now.x % world.RAZMER - what_do[1]][playr_now.y % world.RAZMER - what_do[2]]:
                    move_pos = True

    if move_pos:
        playr_now.x -= what_do[1]
        playr_now.y -= what_do[2]
        sounds["move"].play()
        job = True



    elif ikey == pygame.K_TAB:
        job = True

    elif ikey == pygame.K_i:
        comand(input("команду пж: "))

    if job:

        pass

        zith.triger()
        zith.canculate_tick()




    current_chunk_x = playr_now.x // zith.RAZMER
    current_chunk_y = playr_now.y // zith.RAZMER

    if past_chunk_x != current_chunk_x or past_chunk_y != current_chunk_y:
        zith.room_generate(playr_now.x, playr_now.y)


    pass

def other_mov(ichela):
    mapi = playr_now.soul.real_map

    for i in mapi:
        now = mapi[i]
        if [playr_now.x%zith.RAZMER - now[1], playr_now.y%zith.RAZMER - now[2]] == ichela:
            move(zith, i, playr_now.soul)

def renre_reset():
    # rad * 225 начало линии
    # rad * 45 конец линии
    rad = math.pi/180
    len_ = len(playr_now.cards)
    len2_ = len(playr_now.artefact)

    pygame.draw.circle(sc_main, (255, 255, 255),
                       (225, 255)
                       , 103, 1)
    pygame.draw.circle(sc_main, (255, 255, 255),
                       (225, 725)
                       , 103, 1)
    if len_:
        pygame.draw.circle(sc_main, (255, 0, 0),
                           Trangul.round(200, 255 - 37, math.pi / len_ * setting["round_itom"] + rad * 45, 103),
                           25)
#        Trangul.round(225 - 25, 255 - 37, math.pi / len_ * setting["round_itom"] + rad * 45, 103)

        for i in range(len_):
            sc_main.blit(pygame.transform.scale(playr_now.cards[i].foto, (50, 75)),
                         Trangul.round(225 - 25, 255 - 37, math.pi / len_ * i + rad * 45, 103))

    if len2_:
        pygame.draw.circle(sc_main, (255, 0, 0),
                           Trangul.round(225 - 25, 725 - 25, math.pi / len2_ * setting["round_artifact"] + rad * 300, 103),
                           25)

        for i in range(len2_):
            sc_main.blit(pygame.transform.scale(playr_now.artefact[i].foto, (50, 50)),
                         Trangul.round(225 - 25, 725 - 25, math.pi / len2_ * i + rad * 300, 103))

def start_locashon():

    zith.local_World = [[False for _ in range(zith.RAZMER)] for _ in range(zith.RAZMER)]
    zith.local_World[7][7] = Objet.load_obj_from_data_base(40)
    zith.local_World[6][7] = Objet.load_obj_from_data_base(41)
    zith.local_World[5][7] = Objet.load_obj_from_data_base(42)

    playr_now.cards.append(Cards.load_card_from_data_base(3))
    playr_now.artefact.append(Cards.load_card_from_data_base(4))

def comand(com):
    _comand = com.split(" ")
    if _comand[0] == "y":
        playr_now.y = int(_comand[1])
    elif _comand[0] == "x":
        playr_now.x = int(_comand[1])
    elif _comand[0] == "smena":
        zith.smena(playr_now.y)
    elif _comand[0] == "loacsion":
        zith.we_now = Place.load_place_from_data_base(int(_comand[1]))


zith = World(random.randint(0, 100000000), Place("", [], "", "", "free", "", ""))
zith.smena(playr_now.y)
start_locashon()


#playr_now.cards.append(Cards.load_card_from_data_base(11, False))

#playr_now.artefact.append(Cards.load_card_from_data_base(13, False))
#playr_now.artefact[0].leval = 10000



igra_gui = IMenu([
    [36, 570, 145, 679], #начать моргание глазом
    [161, 570, 270, 679], #прекратить моргание глазом
    [252, 808, 295, 850], #стрелка на право в картах
    [5, 808, 48, 850], #стрелка на лево в картах
    [970, 720, 1189, 778], #ACT
    [115, 785, 186, 885], #карта
    [612, 646, 895, 900], #текст описания
    [400, 200, 800, 600], #доска
    [19, 56, 170, 250], #диолог
    [7, 293, 134, 512], #нопка диалага 1
    [134, 293, 269, 512], #кнопка дилога 2
    [269, 293, 383, 512], #кнопка дилога 3
    [960, 229, 1199, 708], #артевакты
    [1146, 1, 1198, 53], #сохронение
    [1083, 4, 1137, 56] #настройки
                 ])

kill_gui = IMenu([
      [497, 773, 186],
      [737, 773, 186],
      [0, 0, 300, 900],
      [782, 368, 50]
      ])

reset_gui = IMenu([
    [140, 340, 103], #верхняя кнопка
    [140, 600, 103], #нижняя кнопка
    [225, 255, 113], #верхняя панель
    [225, 725, 113] #нижняя панель
])

seting_gui = IMenu([
    [972, 20, 1178, 110], #выход
    [237, 129, 414, 230], #русский язык
    [237, 242, 414, 343], #англиский язык
    [75, 590, 237, 636]   #музыка
])



sounds = {
    "locashon 1": pygame.mixer.Sound("music/SFX_852.mp3"),
    "entar": pygame.mixer.Sound("music/entermenu.mp3"),
    "attack": pygame.mixer.Sound("music/undertale-damage-taken.mp3"),
    "ACT": pygame.mixer.Sound("music/snow4.mp3"),
    "move": pygame.mixer.Sound("music/6a897efd83627af.mp3"),
    "boss": pygame.mixer.Sound("music/boss.mp3"),
    "2 act": pygame.mixer.Sound("music/15. Sentient.mp3"),
    "recant": pygame.mixer.Sound("music/10 - Lava Lake.mp3")
}

option_settings = True_Save.pre_load()

class C_scena:
    def __init__(self):
        self.scena = False

Scena = C_scena()

thel_prothent = line((100, 100, 255), (0, 0, 255), (429, 95, 767, 112))
thel_hp_boss = line((255, 100, 100), (255, 0, 0), (429, 95, 767, 112))

menu = 2

lang = {2: "ru", 3: "en"}

sistem_seting.start_music(sounds["entar"])

original_scen = 2

save_itom = {}

while RUN:

    sc_main.blit(nots.render("версия 0.8", True, (255, 255, 255)), (500 * scale.scale_right, 0))

    scaled_canvas = pygame.transform.scale(sc_main, (sc_real.get_width(), sc_real.get_height()))

    sc_real.blit(scaled_canvas, (0, 0))

    pygame.display.update()


    if Scena.scena:
        menu = 4


    sc_main.fill((0, 0, 0))

    for i in all_gif:
        if i == "profil":
            sc_main.blit(pygame.transform.scale(all_gif[i].render(1 / FPS), real_screen), (0, 0))



    if menu == 1:

        if playr_now.hp <= 0:
            menu = 3
            sistem_seting.start_music(sounds["recant"])

        sc_main.blit(tesxture_blok["fon"], (0, 0))

        zith.render()

        thel_prothent.print(playr_now.y * -1, 15000)

        BUTTON = igra_gui.button_mous(scale.mous_get())

        if sistem_seting.boss[1]:
            thel_hp_boss.print(sistem_seting.boss[0], sistem_seting.boss[1])



        for i in pygame.event.get():

            if i.type == pygame.MOUSEBUTTONUP:
                BUTTON = igra_gui.button_mous(scale.mous_get())
                setting["mous_on"] = False
                if setting["figur on mous"]:
                    setting["figur on mous"] = False
                    other_mov([math.floor((scale.mous_get()[0] - 400) / (50 * (8/zith.RAZMER))),
                               math.floor((scale.mous_get()[1] - 200) / (50 * (8/zith.RAZMER)))])


            if i.type == pygame.MOUSEBUTTONDOWN:



                if i.button == 1:

                    setting["mous_on"] = True

                    if BUTTON == 5: #ACT
                        if setting["choss_what"] == "cards":
                            sounds["ACT"].play()
                            playr_now.cards[setting["cards_now"]].efect_card(zith)

                            zith.canculate_tick()

                        elif type(setting["item"]) == int:
                            playr_now.artefact[setting["item"]].efect_itom(zith)
                            sounds["ACT"].play()

                            zith.canculate_tick()

                    if setting["choss_what"]:
                        if type(setting["choss_what"][0]) == int:
                            if BUTTON == 10:
                                zith.spael(1)
                            elif BUTTON == 11:
                                zith.spael(2)
                            elif BUTTON == 12:
                                zith.spael(3)

                    setting["choss_what"] = False
                    setting["item"] = False
                    setting["scrool_chat"] = 0
                    setting["scrool_opisanie"] = 0
                    setting["dialog"] = 0

                    if BUTTON == 1: #начать моргание глазом
                        if zith.up_leval[zith.RAZMER+1] - playr_now.y > 0:
                            zith.RAZMER += 1
                            zith.room_generate(playr_now.x, playr_now.y)

                    elif BUTTON == 2:
                        print("нельзя")

                    elif BUTTON == 3: #стрелка на право в картах
                        if setting["cards_now"] + 1 < len(playr_now.cards):
                            setting["cards_now"] += 1

                    elif BUTTON == 4: #стрелка на лево в картах
                        if setting["cards_now"] - 1 >= 0:
                            setting["cards_now"] -= 1

                    elif BUTTON == 6: #выбираем карту
                        setting["choss_what"] = "cards"

                    elif BUTTON == 8: #игровое поле
                        setting["choss_what"] = [math.floor((scale.mous_get()[0] - 400) / (50 * (8 / zith.RAZMER))),
                                                 math.floor((scale.mous_get()[1] - 200) / (50 * (8/zith.RAZMER)))]
                        if setting["choss_what"] == [playr_now.x % zith.RAZMER, playr_now.y % zith.RAZMER]:
                            setting["figur on mous"] = True

                    elif BUTTON == 13:
                        setting["item"] = [math.floor((scale.mous_get()[0] - 960) / 40), math.floor((scale.mous_get()[1] - 229) / 40)]
                        setting["item"] = setting["item"][0] + setting["item"][1] * 6
                        if setting["item"] > len(playr_now.artefact)-1:
                            setting["item"] = False

                    elif BUTTON == 14:
                        True_Save.creat_save(playr_now)

                if i.button == 4: # Колесико вверх
                    if BUTTON == 7:

                        setting["scrool_opisanie"] += 1

                    if BUTTON == 9:

                        setting["dialog"] += 1

                    if 10 <= BUTTON <= 13:
                        setting["scrool_chat"] += 1


                if i.button == 5: # Колесико вниз
                    if BUTTON == 7:
                        if setting["scrool_opisanie"]:
                            setting["scrool_opisanie"] -= 1

                    if BUTTON == 9:
                        if setting["dialog"]:
                            setting["dialog"] -= 1


                    if 10 <= BUTTON <= 13 :
                        if setting["scrool_chat"]:
                            setting["scrool_chat"] -= 1


            if i.type == pygame.KEYDOWN:
                move(zith, i.key, playr_now.soul)


            if i.type == pygame.QUIT:
                RUN = False
                #активная игра

    elif menu == 2:
        sc_main.blit(tesxture_blok["no_end_fon"], (0, 0))

        BUTTON = kill_gui.button_mous(scale.mous_get())

        True_Save.render_pak()

        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if BUTTON == 1:
                        RUN = False

                    elif BUTTON == 2:


                        playr_now = True_Save.start_seting()
                        zith.we_now.name = False
                        zith.smena(playr_now.y)
                        start_locashon()

                        menu = 1

                        if save_itom:
                            if save_itom[1].type == "clear":
                                playr_now.artefact[0] = save_itom[1]
                            else:
                                if save_itom[0] == "cards":
                                    playr_now.cards.append(save_itom[1])
                                elif save_itom[0] == "artefact":
                                    playr_now.artefact.append(save_itom[1])

                    elif BUTTON == 3:
                        if scale.mous_get()[0] <= 300:
                            if math.floor(scale.mous_get()[1]/100 * scale.scale_up) < len(True_Save.pak_texsture):
                                True_Save.base = True_Save.pak_texsture[math.floor(scale.mous_get()[1]/100 * scale.scale_up)][0]
                                True_Save.reload()

                    elif BUTTON == 4:


                        playr_now = True_Save.start_seting()
                        start_locashon()
                        True_Save.reload()
                        playr_now = True_Save.up_save()
                        zith.we_now.name = False
                        zith.smena(playr_now.y)
                        menu = 1




            if i.type == pygame.QUIT:
                pass
                RUN = False
                 #меню входа

    elif menu == 3:
        sc_main.blit(tesxture_blok["reset"], (0, 0))

        renre_reset()

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                pass
            if i.type == pygame.MOUSEBUTTONDOWN:
                BUTTON = reset_gui.button_mous(scale.mous_get())

                if i.button == 1:
                    if BUTTON == 1:
                        if len(playr_now.cards):
                            menu = 2

                            sistem_seting.start_music(sounds["entar"])
                            save_itom = ("cards", playr_now.cards[setting["round_itom"]])
                            setting = sistem_seting.base_seting()

                    elif BUTTON == 2:
                        menu = 2

                        sistem_seting.start_music(sounds["entar"])
                        save_itom = ("cards", playr_now.artefact[setting["round_artifact"]])
                        setting = sistem_seting.base_seting()

                if i.button == 4: #колёсеко верх
                    if BUTTON == 3:
                        if setting["round_itom"] + 1 < len(playr_now.cards):
                            setting["round_itom"] += 1
                    if BUTTON == 4:
                        if setting["round_artifact"] + 1 < len(playr_now.artefact):
                            setting["round_artifact"] += 1

                if i.button == 5: #колёсеко вниз
                    if BUTTON == 3:
                        if setting["round_itom"]:
                            setting["round_itom"] -= 1
                    if BUTTON == 4:
                        if setting["round_artifact"]:
                            setting["round_artifact"] -= 1

            if i.type == pygame.QUIT:
                RUN = False

    elif menu == 4:

        sc_main.blit(pygame.transform.scale(Scena.scena.render(1 / FPS), real_screen), (0, 0))

        if not Scena.scena.type:
            menu = 1
            Scena.scena = False
            zith.smena(playr_now.y)

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_e:
                    menu = 1
                    Scena.scena = False
                    zith.smena(playr_now.y)





                #перерождение

    elif menu == 5:
        sc_main.blit(tesxture_blok["seting"], (0, 0))

        for i in range(2):
            if lang[i+2] == option_settings["languje"]:
                c = [seting_gui.gui[i+1][0], seting_gui.gui[i+1][1], seting_gui.gui[i+1][2]-seting_gui.gui[i+1][0], seting_gui.gui[i+1][3]-seting_gui.gui[i+1][1]]
                pygame.draw.rect(sc_main, (255, 0, 255), c, 1)

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                pass
            if i.type == pygame.MOUSEBUTTONDOWN:
                BUTTON = seting_gui.button_mous(scale.mous_get())

                if i.button == 1:
                    if BUTTON == 1:
                        menu = original_scen

                    if 2 <= BUTTON <= 3:
                        option_settings["languje"] = lang[BUTTON]
                        True_Save.geting_staf("languge", lang[BUTTON])



            if i.type == pygame.QUIT:
                RUN = False





    clock.tick(FPS)
