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
doble_click_chek = 0

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
                self.sound.set_volume(option_settings["music_voluom"]/100)
            else:
                self.sound = music
                self.sound.play(-1)
                self.sound.set_volume(option_settings["music_voluom"]/100)
        except:
            if self.sound:
                self.sound.stop()
            self.sound = False



    def base_seting(self):
        return {
            "cards_now": 0,
            "artifact_page_now": 0,
            "choss_what": False,
            "scrool_opisanie": 0,
            "scrool_chat": 0,
            "dialog": 0,
            "item": False,
            "round_itom": 0,
            "round_artifact": 0,
            "mous_on": False,
            "figur on mous": False,
            "soul vibor": 0,
            "map": [0, 0, 0]
        }

option_settings = {
    "all_png": "base texsture pack",
    "languje": "ru",
    "chate": False
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

    def get_all_soul(self = None):
        datka = sqlite3.connect('data base/save_file.db')

        cursor = datka.cursor()
        cursor.execute("""SELECT haw FROM metaprogress WHERE id = 1""")
        for res in cursor:
            for_time = res[0]

        for_time = for_time.split(",")
        returning = []

        for i in for_time:
            returning.append(Soul_class.load_act_soul_data_base(int(i)))

        return returning

    def unlock_soul(self=None):
        with sqlite3.connect('data base/save_file.db') as datka:
            cursor = datka.cursor()
            cursor.execute("SELECT haw FROM metaprogress WHERE id = 1")
            res = cursor.fetchone()

            if res:
                for_time = res[0]
                new_index = len(for_time.split(",")) + 1
                updated_haw = f"{for_time},{new_index}"
                cursor.execute("UPDATE metaprogress SET haw = ? WHERE id = 1", (updated_haw,))
                datka.commit()
        meta_progress["open soul"] = Soul_class.get_all_soul()

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
    "figur on mous": False,
    "soul vibor": 0,
    "map": [0, 0, 0]
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

class Foto:
    def __init__(self, _pic, _tip):
        self.pic = _pic
        self.tips = _tip

    def blid(self, were, rec):
        rec_now = rec

        if "shift" in self.tips:
            rec_now[0] += self.tips["shift"][0]
            rec_now[1] += self.tips["shift"][1]

        if "mp" in self.tips:
            if 0 < self.tips["mp"][3]:
                rec_now[0] += (self.tips["mp"][0] - rec_now[0]) / self.tips["mp"][2] * self.tips["mp"][3]
                rec_now[1] += (self.tips["mp"][1] - rec_now[1]) / self.tips["mp"][2] * self.tips["mp"][3]
                self.tips["mp"][3] -= 1/FPS
            else:
                del self.tips["mp"]
        were.blit(self.pic, rec_now)

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
                print("файл не найде в базе данных: " + z)
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
            "fon": True_Save.foto_load("fon - Copy.png"),
            "no_end_fon": True_Save.foto_load("fon_kill.png"),
            "hp": [True_Save.foto_load("hp1.png"),
                   True_Save.foto_load("hp2.png")],
            "reset": True_Save.foto_load("vibor.png"),
            "nothing": True_Save.foto_load("ничего.png"),
            "unlock": True_Save.foto_load("unknow.png")
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
        sus = Soul_class.load_act_soul_data_base(1)
        base = Player(3, -2, 3, [], [], [], sus)
        return base

    def load_chans(self, ip):
        with sqlite3.connect('data base/all vrag.db') as data:
            cursor = data.cursor()
            cursor.execute("""SELECT * FROM chans WHERE ip = ?""", (str(ip),))

            now = 0

            for res in cursor:
                a = res[1].split("\n")
                a[0] = ast.literal_eval(a[0])
                a[1] = ast.literal_eval(a[1])
                now = a
            return now

    def update_stuff(self, what, to):
        db_path = 'data base/save_file.db'

        with sqlite3.connect(db_path) as data:
            cursor = data.cursor()

            query = "UPDATE save_staf SET valium = ? WHERE tipe = ?"

            cursor.execute(query, (to, what))

            data.commit()

class Achievement:
    def __init__(self):
        self.kolvo_bink = 0
    def Load_Achievement_from_data_base(self):
        data = sqlite3.connect('data base/all vrag.db')

        cursor = data.cursor()

        enter = cursor.execute("SELECT * FROM achivments WHERE id = " + str(self))

        for res in enter:
            now = res

        sas = Achievement()

        sas.id = now[0]
        sas.name = now[1]
        sas.opisanie = now[2]
        sas.foto = True_Save.foto_load(now[3])

        return sas

    def all_achivment(self):

        data = sqlite3.connect('data base/all vrag.db')

        now = 0
        cursor = data.cursor()
        long = cursor.execute("SELECT MAX(id) FROM achivments")

        for res in long:
            long = res[0]

        sas = []

        for i in range(int(long) + 1):
            sas.append(Achievement.Load_Achievement_from_data_base(i))

        return sas

    def get_all_achivment(self):
        datka = sqlite3.connect('data base/save_file.db')

        cursor = datka.cursor()
        cursor.execute("""SELECT haw FROM metaprogress WHERE id = 2""")
        for res in cursor:
            for_time = res[0]

        for_time = for_time.split(",")

        return for_time

    def unlock_achivment(self, what):
        with sqlite3.connect('data base/save_file.db') as datka:
            cursor = datka.cursor()
            cursor.execute("SELECT haw FROM metaprogress WHERE id = 2")
            res = cursor.fetchone()

            if res:
                for_time = res[0]
                updated_haw = f"{for_time},{what}"
                cursor.execute("UPDATE metaprogress SET haw = ? WHERE id = 2", (updated_haw,))
                datka.commit()
        meta_progress["achivment"] = Achievement.get_all_achivment(None)


    def meta_achiv(self, what_kind):
        if what_kind in meta_progress["all_ach"]:
            pass
        else:
            if what_kind == 2:
                achiv_test[0] += 1
                if achiv_test[0] >= 20:
                    Achievement.unlock_achivment(None, 2)
            else:
                Achievement.unlock_achivment(None, what_kind)


True_Save = Save()

playr_now = True_Save.start_seting()

achiv_test = [0]

sistem_seting = Sistem([], 0, [0, 0], False)

all_gif = {

}

meta_progress = {
    "open soul": Soul_class.get_all_soul(),
    "achivment": Achievement.get_all_achivment(None),
    "all_ach": Achievement.all_achivment(None)
}

tesxture_blok = {
    "fon": True_Save.foto_load("fon.png"),
    "no_end_fon": True_Save.foto_load("fon_kill.png"),
    "hp": [True_Save.foto_load("hp1.png"),
           True_Save.foto_load("hp2.png")],
    "reset": True_Save.foto_load("vibor.png"),
    "seting": True_Save.foto_load("seting.png"),
    "soul_sect": True_Save.foto_load("soul_select.png"),
    "nothing": True_Save.foto_load("ничего.png"),
    "dont_unlock": True_Save.foto_load("achivment/dont_unlock.png")
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
            if ".png" in i:
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
            cursor.execute("""SELECT * FROM obj_inf WHERE id = ?""", (search,))
            for res in cursor:
                return_ing = Objet(Foto(True_Save.foto_load(res[2]),{}), {
                            "destrakt": int(res[5]),
                            "kill": int(res[6]),
                            "trans": truE(res[7]),
                            "dialog": truE(res[8]),
                            "id": search},
                            True_Save.load_translate_from_data_base(res[3]),
                            truE(res[4]),
                            truE(res[1]))




            if return_ing.ai:
                ai_set = {}
                if "!@#$" in return_ing.ai:
                    ai_set["use"] = True
                    return_ing.ai = return_ing.ai.replace("!@#$", "")
                else:
                    ai_set["use"] = False

                if "vipod_" in return_ing.ai:
                    return_ing.more_inf["use_ever"] = int(return_ing.ai.split("_")[1])

                ai_set["type"] = return_ing.ai

                return_ing.ai = ai_set
            else:
                return_ing.ai = {}

            if "_" in return_ing.type:
                if "sunduk_" in return_ing.type or "seller_" in return_ing.type:
                    return_ing.more_inf["chans"] = True_Save.load_chans(return_ing.type.split("_")[1])
                    return_ing.type = return_ing.type.split("_")[0]


            if return_ing.more_inf["dialog"]:
                return_ing.more_inf["dialog"] = Dialog.load_dialog_from_data_base(return_ing.more_inf["dialog"])
            if return_ing.more_inf["trans"]:
                return_ing.foto.tips = {"shift": [25 - (return_ing.foto.pic.get_size()[0] / 2), 25 - (return_ing.foto.pic.get_size()[1] / 2)]}
            else:
                return_ing.foto.pic = pygame.transform.scale(return_ing.foto.pic, (50, 50))
            return return_ing

    def ai_chet(self, were, x, y):
        go_to_ = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0],
                  "dont": [0, 0],
                  "UR": [1, -1], "UL": [-1, -1], "DR": [1, 1], "DL": [-1, 1]}

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
                            were.local_World[x + new_x_y[0]][y + new_x_y[1]].foto.tips["mp"] = [x * 50, y * 50, 0.1, 0.1]
                            were.local_World[x][y] = False
                            i = 1
                new_x_y = random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1
                i -= 1

        elif self.ai["type"] == "random+":
            new_x_y = random.randint(0, 2) - 1, random.randint(0, 2) - 1
            i = 10
            while i:
                if not (new_x_y[0] == 0 and new_x_y[1] == 0):
                    if were.exsit_to_space(x + new_x_y[0], y + new_x_y[1]):
                        were.local_World[x + new_x_y[0]][y + new_x_y[1]] = were.local_World[x][y]
                        were.local_World[x + new_x_y[0]][y + new_x_y[1]].foto.tips["mp"] = [x * 50, y * 50, 0.1, 0.1]
                        were.local_World[x][y] = False
                        i = 1
                new_x_y = random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1
                i -= 1

        elif "move_" in self.ai["type"]:
            vectore = [0, 0]
            com = self.ai["type"].split("_")
            vectore[0] = math.floor(go_to_[com[1]][0] * int(com[2]))
            vectore[1] = math.floor(go_to_[com[1]][1] * int(com[2]))
            if were.exsit_to_space(x + vectore[0], y + vectore[1]):
                were.local_World[x + vectore[0]][y + vectore[1]] = were.local_World[x][y]
                were.local_World[x + vectore[0]][y + vectore[1]].foto.tips["mp"] = [x * 50, y * 50, 0.1, 0.1]
            were.local_World[x][y] = False
            if self.type == "big":
                if were.exsit_to_space(x + vectore[0], y + vectore[1]-1): were.local_World[x + vectore[0]][
                    y + vectore[1] - 1] = False
                if were.exsit_to_space(x + vectore[0], y + vectore[1]+1): were.local_World[x + vectore[0]][
                    y + vectore[1] + 1] = False

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
                    were.local_World[x + new_x_y[0]][y + new_x_y[1]].foto.tips["mp"] = [x * 50, y * 50, 0.1, 0.1]
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
                were.local_World[ex + step_x][ey + step_y].foto.tips["mp"] = [ex * 50, ey * 50, 0.1, 0.1]
                were.local_World[x][y] = False

        elif "pushka_" in self.ai["type"]:
            if not self.more_inf["wait"]:
                self.more_inf["wait"] = 2
                a = go_to_[self.more_inf["rotaet"]]
                if were.exsit_to_space(x + a[0], y + a[1]):
                    were.local_World[x + a[0]][y + a[1]] = Objet.load_obj_from_data_base(int(self.ai["type"].split("_")[1]))
            else:
                self.more_inf["wait"] -= 1

        elif "podstic" in self.ai["type"]:
            dy = 1 if "!!!" in self.ai["type"] else -1
            if player_x_y in [(x + 1, y + dy), (x - 1, y + dy)]:
                dx = 2 if player_x_y[0] > x else -2
                were.local_World[x][y] = False
                playr_now.uron(1)
                if were.exsit_to_space(x + dx, y + 2 * dy): were.local_World[x + dx][y + 2 * dy] = self

        elif "transform_" in self.ai["type"]:
            com = self.ai["type"].split("_")
            com = int(com[1])
            for ex in range(-1, 2):
                for ey in range(-1, 2):
                    if were.exsit_to_space(x + ex, y + ey):
                        if were.local_World[ex + x][ey + y] and (ex != 0 or ey != 0):
                            new_obj = Objet.load_obj_from_data_base(com)
                            were.local_World[ex + x][ey + y] = new_obj

        elif "vipod_" in self.ai["type"]:
            if self.more_inf["use_ever"]:
                nx = player_x_y[0] - x
                ny = player_x_y[1] - y
                if -1 <= nx <= 1 and -1 <= ny <= 1:
                    self.more_inf["use_ever"] -= 1
                    were.local_World[x + nx][y + ny] = were.local_World[x][y]
                    were.local_World[x + nx][y + ny].foto.tips["mp"] = [x * 50, y * 50, 0.1, 0.1]
                    were.local_World[x][y] = False

        elif "SpawnerCircle_" in self.ai["type"]:
            if sistem_seting.time_geam%2:
                a = ("UL", "up", "UR", "left", "", "right", "DL", "down", "DR")
                com = self.ai["type"].split("_")
                com = int(com[1])
                for ex in range(-1, 2):
                    for ey in range(-1, 2):
                        if were.exsit_to_space(x + ex, y + ey):
                            if (ex, ey) != (0, 0):
                                new_obj = Objet.load_obj_from_data_base(com)
                                new_obj.ai["type"] = "move_" + a[(ex+1)+((ey+1)*3)] + "_1"
                                new_obj.ai["use"] = True
                                were.local_World[ex + x][ey + y] = new_obj


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
                             {},
                        int(res[3]),
                         more_inf,
                         search
                            )

            if res[2]:
                stak = res[2].split("!")
                for i in stak:
                    j = i.split('_')
                    if len(j) - 1:
                        if type(smart_int(j[0])) == int: returing.type[j[0]] = int(j[1])
                        else: returing.type[j[0]] = j[1]
                    else:
                        returing.type[j[0]] = j[0]

                if "tick" in returing.type:
                    returing.more_inf["tick"] = returing.type["tick"]

            return returing

    def efect_card(self, where):
        if "hp+" in self.type:
            playr_now.hp += self.leval

        if "move" in self.type:
            playr_now.y -= self.leval + where.RAZMER
            where.room_generate(playr_now.x, playr_now.y)

        if "SpawnArrowLeft" in self.type:
            if where.exsit_to_space(playr_now.x%where.RAZMER, playr_now.y%where.RAZMER):
                where.local_World[playr_now.x%where.RAZMER][(playr_now.y+1)%where.RAZMER] = Objet.load_obj_from_data_base(10)

        if "tp" in self.type:
            playr_now.y += random.randint(0, where.RAZMER-1) - math.floor(where.RAZMER/2)
            playr_now.x += random.randint(0, where.RAZMER-1) - math.floor(where.RAZMER/2)

        if "spial" in self.type:

            obj_id = self.type["spial"]
            directions = [
                (0, -1, "move_up_2"),
                (0, 1, "move_down_2"),
                (-1, 0, "move_left_2"),
                (1, 0, "move_right_2")
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

        if "dropplayre" in self.type:
            obj_id = self.type["dropplayre"]
            where.local_World[playr_now.x][0] = Objet.load_obj_from_data_base(obj_id)
            where.local_World[playr_now.x][0].ai["type"] = "move_down_1"
            where.local_World[playr_now.x][0].ai["use"] = True

        if "GiveBack" in self.type:
            if playr_now.all_kill != []:
                where.local_World[playr_now.x%where.RAZMER][playr_now.y%where.RAZMER] \
                    = Objet.load_obj_from_data_base(playr_now.all_kill[0].more_inf["id"])

        if "SaveFrom" in self.type:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if where.local_World[(playr_now.x + i) % where.RAZMER][(playr_now.y + j) % where.RAZMER]:
                        if where.local_World[(playr_now.x + i) % where.RAZMER][(playr_now.y + j) % where.RAZMER].more_inf["id"] == int(self.type["SaveFrom"]):
                            where.local_World[(playr_now.x + i) % where.RAZMER][(playr_now.y + j) % where.RAZMER] = False

        if "replace" in self.type:
            for ex in range(where.RAZMER):
                for ey in range(where.RAZMER):
                    if where.local_World[ex][ey]:
                        if where.local_World[ex][ey].more_inf["id"] == 73:
                            where.local_World[ex][ey] = Objet.load_obj_from_data_base(59)
                        elif where.local_World[ex][ey].more_inf["id"] == 59:
                            where.local_World[ex][ey] = Objet.load_obj_from_data_base(73)

        playr_now.cards.pop(setting["cards_now"])


        if setting["cards_now"]: setting["cards_now"] -= 1


    def efect_itom(self, where):
        go_to_ = {"up": [0, -1],
                  "down": [0, 1],
                  "left": [-1, 0],
                  "right": [1, 0],
                  "dont": [0, 0]}
        for_time = 0
        run = True
        x, y = playr_now.x%where.RAZMER, playr_now.y%where.RAZMER


        if "tick" in self.more_inf:
            if self.leval != 0:
                run = False
            else:
                self.leval = int(self.more_inf["tick"])

        if run:
            if "clear" in self.type:
                for_time = self.leval
                for i in playr_now.all_kill:
                    self.leval += 1
                    if i.more_inf["kill"]:
                        self.leval += 1
                playr_now.all_kill = []
                for_time -= self.leval


            if "cliker" in self.type:
                self.leval += 1

            if "MoveLeft" in self.type:
                playr_now.y -= 1
                playr_now.x -= 1

            if "MoveRight" in self.type:
                playr_now.y -= 1
                playr_now.x += 1

            if "FirstMove" in self.type:
                if playr_now.y%where.RAZMER == where.RAZMER -2:
                    playr_now.y -= 2

            if "hp_up" in self.type:

                if playr_now.artefact[0].leval >= self.leval:
                    playr_now.hp += 1
                    playr_now.artefact[0].leval -= self.leval

            if "spial" in self.type:

                obj_id = self.type["spial"]
                directions = [
                    (0, -1, "move_up_2"),
                    (0, 1, "move_down_2"),
                    (-1, 0, "move_left_2"),
                    (1, 0, "move_right_2")
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

            if "kill" in self.type:
                obj = go_to_[self.type["kill"]]
                where.local_World[(playr_now.x+obj[0])%where.RAZMER][(playr_now.y+obj[1])%where.RAZMER] = False

            elif "circl" in self.type:
                # Координаты по часовой стрелке (последний элемент не дублируем, если используем range)
                here = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))[::-1]

                # Сохраняем значение первой клетки, которую затрем
                first_val = where.local_World[here[0][0] + x][here[0][1] + y]

                for i in range(len(here) - 1):
                    # Текущая клетка получает значение следующей

                    where.local_World[here[i][0] + x][here[i][1] + y] = \
                        where.local_World[here[i + 1][0] + x][here[i + 1][1] + y]

                # Последняя клетка получает значение, которое мы сохранили в самом начале
                where.local_World[here[-1][0] + x][here[-1][1] + y] = first_val

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
                if self.test:
                    pygame.draw.rect(sc_main, (255, 255, 255), (x1, y1, x2 - x1, y2 - y1))
                if x1 <= m_x <= x2 and y1 <= m_y <= y2:
                    return i + 1

            elif len(element) == 3:
                cx, cy, r = element
                if self.test:
                    pygame.draw.circle(sc_main, (255, 255, 255), (cx, cy), r)
                if (m_x - cx) ** 2 + (m_y - cy) ** 2 <= r ** 2:
                    return i + 1
        return False

    def sub_select(self, index, mous, colvo):
        # index - это i+1 из button_mous, значит вычитаем 1
        element = self.gui[index - 1]

        # Проверяем, что это прямоугольник
        if len(element) != 4:
            return None

        x1, y1, x2, y2 = element
        m_x, m_y = mous

        # Считаем размеры ячейки
        cell_w = (x2 - x1) / colvo[0]
        cell_h = (y2 - y1) / colvo[1]

        # Рассчитываем относительные координаты
        sub_x = math.floor((m_x - x1) / cell_w)
        sub_y = math.floor((m_y - y1) / cell_h)

        # Ограничиваем значения, чтобы не выйти за пределы colvo
        sub_x = max(0, min(sub_x, colvo[0] - 1))
        sub_y = max(0, min(sub_y, colvo[1] - 1))

        return [sub_x, sub_y]

class World:
    def __init__(self, seed, we_now):
        self.seed = seed
        self.RAZMER = 8
        self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
        self.we_now = we_now
        self.up_leval = {
                         8: 0,
                         9: -500,
                         10: -1000,
                         11: -1500
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
                        mesto[x][y].foto.blid(holst, [x * 50, y * 50])
                    else:
                        mesto[x][y].foto.blid(holst, [x * 50, y * 50])

        if type(setting["choss_what"]) == type([]):
            pygame.draw.rect(holst, (255, 255, 0),
                             (setting["choss_what"][0] * 50,
                              setting["choss_what"][1] * 50
                              , 50, 50), 3)

        self.jod(holst)
        self.other_staf()
        self.choss_render()
        self.texst_inf()
        self.texst_dialog()
        self.hp_render()

        if setting["figur on mous"]:
            sc_main.blit(pygame.transform.scale(playr_now.soul.png, (50 * size, 50 * size)), (scale.mous_get()))
        else:
            holst.blit(pygame.transform.scale(playr_now.soul.png, (50, 50)),
                         (playr_now.x % self.RAZMER * 50,
                          playr_now.y % self.RAZMER * 50))

        sc_main.blit(pygame.transform.scale(holst, (igra_gui.gui[7][2] - igra_gui.gui[7][0] + setting["map"][2],
                                                    igra_gui.gui[7][3] - igra_gui.gui[7][1] + setting["map"][2])),
                     (igra_gui.gui[7][0] + setting["map"][0], igra_gui.gui[7][1] + setting["map"][1]))

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
            sc_main.blit(pygame.transform.scale(tesxture_blok["hp"][math.floor(i/10)%len(tesxture_blok["hp"])], (32, 36)),
                         (403 + i%10 * 38, 60))

    def other_staf(self):
        size = 8 / self.RAZMER

        sc_main.blit(nots.render(str(playr_now.y * -1) + " - " + one_to_ABC(int(math.fabs(playr_now.x + 1))), True,
                                 (255, 255, 255)), (522, 11))
        sc_main.blit(pygame.transform.scale(playr_now.soul.png, (73, 73)), (17, 11))

        #sc_main.blit(playr_now.soul.gid, (336,663))

        if self.up_leval[self.RAZMER+1] - playr_now.y < 0:
            sc_main.blit(nots.render(str((self.up_leval[self.RAZMER+1] - playr_now.y) * -1),
                                     True, (255, 0, 0)), (105, 50))
        else:
            sc_main.blit(nots.render(str((self.up_leval[self.RAZMER+1] - playr_now.y) * -1),
                                     True, (0, 255, 0)), (105, 50))

        for i in range(len(playr_now.all_kill)):
            sc_main.blit(pygame.transform.scale(playr_now.all_kill[i].foto.pic, (50, 50)),
                         (10 + i*50, 828))


        if setting["cards_now"] + 3 < len(playr_now.cards):
            sc_main.blit(pygame.transform.rotate(
                pygame.transform.scale(playr_now.cards[setting["cards_now"] + 3].foto, (140, 200)), 330),
                         (998, 578))
        if setting["cards_now"] + 2 < len(playr_now.cards):
            sc_main.blit(pygame.transform.rotate(
                pygame.transform.scale(playr_now.cards[setting["cards_now"] + 2].foto, (140, 200)), 345),
                (997, 574))
        if setting["cards_now"] + 1 < len(playr_now.cards):
            sc_main.blit(pygame.transform.rotate(
                pygame.transform.scale(playr_now.cards[setting["cards_now"] + 1].foto, (140, 200)), 0),
                (979, 595))
        if playr_now.cards != []:
            sc_main.blit(pygame.transform.rotate(
                pygame.transform.scale(playr_now.cards[setting["cards_now"]].foto, (140, 200)), 15),
                (941, 583))

        for i in range(len(playr_now.artefact)):
            sc_main.blit(pygame.transform.scale(playr_now.artefact[i].foto, (40, 40)),
                         (igra_gui.gui[12][0] + 40*i, igra_gui.gui[12][1]))

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
                sc_main.blit(mini_nots.render(i, True, (255, 255, 255)), (igra_gui.gui[6][0], igra_gui.gui[6][1] + r * 25))
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
                                                                                         igra_gui.gui[8 + i][1]+60 + r*20))
                                    r += 1

    def choss_render(self):
        if setting["choss_what"] == "cards":
            pygame.draw.lines(sc_main, (255, 255, 0), True,
                              [[943, 615], [1075, 584], [1121, 773], [989, 808]], 3)
        if type(setting["item"]) == int:
            pygame.draw.rect(sc_main, (255, 255, 0), (setting["item"]%10*40 + igra_gui.gui[12][0], igra_gui.gui[12][1], 40, 40), 3)

    def room_generate(self, x, y):

        go_to_ = ["right", "up", "left", "down"]

        nomdore_desk_x = math.floor(x/self.RAZMER)
        nomdore_desk_y = math.floor(y/self.RAZMER)

        if self.we_now.type == "free":
            self.smena(y)
            self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
            code_input = int((str(self.seed % 10000) + str(x) + str(y)).replace("-", "")) % 100000
            random.seed(code_input)

            pass
            for x_index in range(self.RAZMER):
                for y_index in range(self.RAZMER):
                    code_input = random.randint(1, 4096)
                    placing = self.we_now.get_random(x, y)
                    if placing:
                        if placing.type == "portal":
                            placing.more_inf["teleport"] = random.randint(1, code_input % 10 + 2) * 8
                        if placing.ai != {} and "pushka" in placing.ai["type"]:
                            a = random.randint(0, 3)
                            placing.more_inf["rotaet"] = go_to_[a]
                            placing.more_inf["wait"] = 1
                            placing.foto.pic = pygame.transform.rotate(placing.foto.pic, a * 90)


                    self.local_World[x_index][y_index] = placing

            if self.we_now.name == "medium":
                if not random.randint(0, 10):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    Structor.load_in_game(Structor.load_form_data(2))

                if nomdore_desk_y == math.floor(-1050 / self.RAZMER) or nomdore_desk_y+1 == math.floor(-1050 / self.RAZMER):
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(33)
                if nomdore_desk_y == math.floor(-1400 / self.RAZMER) or nomdore_desk_y + 1 == math.floor(-1400 / self.RAZMER):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(37)
                if math.floor(-1410/ self.RAZMER) > nomdore_desk_y > math.floor(-1750/ self.RAZMER):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    Structor.load_in_game(Structor.load_form_data(3))

            if self.we_now.name == "PostStart":
                if nomdore_desk_y == math.floor(-750 / self.RAZMER) or nomdore_desk_y + 1 == math.floor(-750 / self.RAZMER):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    self.local_World[self.RAZMER - 2][self.RAZMER - 2] = Objet.load_obj_from_data_base(76)
                if math.floor(-760/ self.RAZMER) > nomdore_desk_y > math.floor(-1050/ self.RAZMER):
                    self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                    Structor.load_in_game(Structor.load_form_data(3))
                    self.local_World[6][6] = Objet.load_obj_from_data_base(76)


        if sistem_seting.boss[0] <= 0 and sistem_seting.boss[1]:
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

            if obj_triger.type == "swapX":
                playr_now.x = math.floor(playr_now.x/self.RAZMER) + (self.RAZMER -1 - playr_now.x%self.RAZMER)


    def canculate_tick(self):

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



    def exsit_to_space(self, plus_x, plus_y):
        if plus_x < self.RAZMER:
            if plus_x >= 0:
                if plus_y < self.RAZMER:
                    if plus_y >= 0:
                        return True
        return False

    def smena(self, y):
        smenit = False
        if self.we_now.type == "free":
            if 8 > y > -350 and self.we_now.name != "start":
                self.we_now = Place.load_place_from_data_base(1)
                smenit = True

            elif -350 > y > -1050 and self.we_now.name != "PostStart":
                self.we_now = Place.load_place_from_data_base(7)
                smenit = True

            elif -1050 > y > -1750 and self.we_now.name != "medium":
                self.we_now = Place.load_place_from_data_base(2)
                smenit = True

            elif -1750 > y and self.we_now.name != "end":
                self.we_now = Place.load_place_from_data_base(6)
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
                        what_take[0] = random.choices(run.slot[0], weights=run.slot[1], k=1)[0]
                        if playr_now.artefact[0].leval >= what_take[1]:
                            playr_now.artefact[0].leval -= what_take[1]
                            if what_take[2]%2:
                                playr_now.cards.append(Cards.load_card_from_data_base(what_take[0]))
                            else:
                                self.add_artifact(Cards.load_card_from_data_base(what_take[0]))

                    elif "predati_" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        what_take[2] = int(what_take[2])
                        what_take[3] = random.choices(run.slot[0], weights=run.slot[1], k=1)[0]
                        if playr_now.hp >= what_take[1]:
                            playr_now.hp -= what_take[1]
                            if what_take[2]%2:
                                playr_now.cards.append(Cards.load_card_from_data_base(what_take[0]))
                            else:
                                self.add_artifact(Cards.load_card_from_data_base(what_take[0]))

                    elif "barter_" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        what_take[2] = int(what_take[2])
                        passet = False
                        j = 0
                        if what_take[1]%2:
                            for i in playr_now.cards:
                                if run.slot[0].id == i.id:
                                    passet = True
                                    break
                                j += 1
                        else:
                            for i in playr_now.artefact:
                                if run.slot[1].id == i.id:
                                    passet = True
                                    break
                                j += 1
                        if passet:
                            if what_take[2] % 2:
                                playr_now.cards.pop(j)
                                playr_now.cards.append(run.slot[1])
                                pass
                            else:
                                playr_now.artefact.pop(j)
                                playr_now.artefact.append(run.slot[1])
                                pass


                    elif "tp_" in run.type:
                        what_take = run.type.split("_")
                        self.we_now = Place.load_place_from_data_base(int(what_take[1]))
                        if self.we_now.fon:
                            all_gif["profil"] = self.we_now.fon
                        self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                        if what_take[1] == "5":
                            Structor.load_in_game(Structor.load_form_data(4))

                    elif "transform_" in run.type:
                        what_take = run.type.split("_")
                        what_take[1] = int(what_take[1])
                        Achievement.meta_achiv(None, 2)
                        if what_take[1]:
                            self.local_World[we_see[0]][we_see[1]] = Objet.load_obj_from_data_base(what_take[1])
                        else:
                            self.local_World[we_see[0]][we_see[1]] = False

                    elif "go_to_" in run.type:
                        self.local_World[we_see[0]][we_see[1]].more_inf["dialog"] \
                            = Dialog.load_dialog_from_data_base(int(run.type.split("_")[2]))

                    elif "LoadStruckture_" in run.type:
                        self.local_World = [[False for _ in range(self.RAZMER)] for _ in range(self.RAZMER)]
                        Structor.load_in_game(Structor.load_form_data(int(run.type.split("_")[1])))

    def supruse(self):
        if sistem_seting.boss[1] and (not sistem_seting.boss[0]):
            self.we_now.type = "free"
            if self.we_now.name == "hell":
                if playr_now.y >= -750:
                    playr_now.y = -750 - self.RAZMER
            elif self.we_now.name == "vraglend":
                if playr_now.y >= -1050:
                    playr_now.y = -1050 - self.RAZMER
            sistem_seting.boss = [0, 0]

        if self.we_now.name == "hell":
            if not sistem_seting.boss[1]:
                 sistem_seting.boss = [15, 15]
                 all_gif["profil"] = Gif("boss", "cycle", 10)
                 sistem_seting.start_music(sounds["boss"])
                 Scena.scena = Gif("katstsena2", "bla", 8)

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
                            self.local_World[self.RAZMER-1][i].ai["type"] = "move_left_1"
                            self.local_World[self.RAZMER - 1][i].ai["use"] = True
                            self.local_World[self.RAZMER-1][i].foto.pic = pygame.transform.rotate(self.local_World[self.RAZMER-1 ][i].foto.pic, 180)
                        self.local_World[self.RAZMER - 1][get] = Objet.load_obj_from_data_base(35)
                        self.local_World[self.RAZMER - 1][get].ai["type"] = "move_left_1"
                        self.local_World[self.RAZMER - 1][get].ai["use"] = True
                        self.local_World[self.RAZMER - 1][get].foto.pic = pygame.transform.rotate(self.local_World[self.RAZMER-1 ][get].foto.pic, 180)
                    pass
                elif type_atack == 1 or type_atack == 4:
                    for i in range(3):
                        get = random.randint(0, self.RAZMER-1)
                        self.local_World[get][0] = Objet.load_obj_from_data_base(35)
                        self.local_World[get][0].ai["type"] = "move_down_1"
                        self.local_World[get][0].ai["use"] = True
                        self.local_World[get][0].foto.pic = pygame.transform.rotate(self.local_World[get][0].foto.pic, 270)

                elif type_atack == 2 or type_atack == 5:
                    for i in range(4):
                        self.local_World[spawn_base[i][0]][spawn_base[i][1]] = Objet.load_obj_from_data_base(36)

        if self.we_now.name == "vraglend":
            if not sistem_seting.boss[1]:
                sistem_seting.boss = [10, 10]
                Achievement.meta_achiv(None, 6)
                Scena.scena = Gif("katstsena1", "bla", 8)

            kit = True
            for i in self.local_World:
                for j in i:
                    if j and j.type == "boss":
                        kit = False
            if kit:
                sistem_seting.boss[0] -= 1
                coordinate = (random.randint(1, self.RAZMER-1), random.randint(1, self.RAZMER-1))
                self.local_World[coordinate[0]][coordinate[1]] = Objet.load_obj_from_data_base(75)


        elif self.we_now.name == "pustina":
            if not (sistem_seting.time_geam+10)%10:
                type_atack = math.floor((sistem_seting.time_geam + 10) / 10) % 6
                if type_atack == 0:
                    for i in range(10):
                        self.local_World[random.randint(0, self.RAZMER-1)][random.randint(0, self.RAZMER-1)] = Objet.load_obj_from_data_base(58)
                elif type_atack == 1:
                    for i in range(len(self.local_World)):
                        for j in range(len(self.local_World[i])):
                            if self.local_World[i][j]:
                                if not (self.local_World[i][j].type in ("fon", "block", "portal", "button")):
                                    self.local_World[i][j] = Objet.load_obj_from_data_base(21)


class Structor:
    def load_form_data(self):
        massiv = []
        with sqlite3.connect('data base/structore.db') as data:
            cursor = data.cursor()
            if type(self) == int:
                cursor.execute("""SELECT * FROM struckture WHERE id = ? """, (str(self),))
                now = 0
                for res in cursor:
                    a = res[1]
                a = a.split("\r\n")
                b = ''
                for i in a:
                    b = i.split(',')
                    for j in range(len(b)):
                        b[j] = int(b[j])
                    massiv.append(b)
        return massiv

    def load_in_game(self):
        x, y = [0, 0]
        for i in self:
            for j in i:
                if j and zith.exsit_to_space(x, y):
                    zith.local_World[x][y] = Objet.load_obj_from_data_base(j)
                x += 1
            x = 0
            y += 1


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
                return_staf = Act(True_Save.load_translate_from_data_base(res[1]),res[2])

            if return_staf.type.split("_")[0] in ["trade", "predati"]:
                return_staf.slot = True_Save.load_chans(return_staf.type.split("_")[2])

            elif "barter_" in return_staf.type:
                a = True_Save.load_chans(return_staf.type.split("_")[2])
                a = random.choices(a[0], weights=a[1], k=1)[0]
                a = Cards.load_card_from_data_base(int(a))
                b = True_Save.load_chans(return_staf.type.split("_")[1])
                b = random.choices(b[0], weights=b[1], k=1)[0]
                b = Cards.load_card_from_data_base(int(b))
                return_staf.slot = (a, b)
                return_staf.text = return_staf.text.replace("!@#$", a.name.split("\n")[0])


            return return_staf


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

def render_achivment():
    for i in range(len(meta_progress["all_ach"])):
        if str(i) in meta_progress["achivment"]:
            sc_main.blit(pygame.transform.scale(meta_progress["all_ach"][i].foto, (57, 57)), (915 + i%5 * 57, 87 + math.floor(i/5)*57))
        else:
            sc_main.blit(pygame.transform.scale(tesxture_blok["dont_unlock"], (57, 57)), (915 + i%5 * 57, 87 + math.floor(i/5)*57))
def start_locashon():
    zith.we_now = Place.load_place_from_data_base(1)
    zith.local_World = [[False for _ in range(zith.RAZMER)] for _ in range(zith.RAZMER)]
    Structor.load_in_game(Structor.load_form_data(1))
    playr_now.cards.append(Cards.load_card_from_data_base(3))
    playr_now.artefact.append(Cards.load_card_from_data_base(4))

def comand(com):
    _comand = com.split(" ")
    if _comand[0] == "y":
        playr_now.y = int(_comand[1])
    elif _comand[0] == "x":
        playr_now.x = int(_comand[1])
    elif _comand[0] == "hp":
        playr_now.hp = int(_comand[1])
    elif _comand[0] == "smena":
        zith.smena(playr_now.y)
    elif _comand[0] == "loacsion":
        zith.we_now = Place.load_place_from_data_base(int(_comand[1]))
    elif _comand[0] == 'card':
        playr_now.cards.append(Cards.load_card_from_data_base(int(_comand[1])))
    elif _comand[0] == 'artefact':
        playr_now.artefact.append(Cards.load_card_from_data_base(int(_comand[1])))


zith = World(random.randint(0, 100000000), Place("", [], "", "", "free", "", ""))
zith.smena(playr_now.y)
start_locashon()


#playr_now.cards.append(Cards.load_card_from_data_base(11, False))

#playr_now.artefact.append(Cards.load_card_from_data_base(13, False))
#playr_now.artefact[0].leval = 10000



igra_gui = IMenu([
    [100, 8, 181, 86], #начать моргание глазом
    [188, 8, 269, 86], #прекратить моргание глазом
    [],
    [],
    [728, 803, 1009, 897], #ACT
    [955, 600, 1100, 978], #карта
    [965, 116, 1189, 557], #текст описания
    [266, 109, 933, 786], #доска
    [19, 56, 170, 250], #диолог
    [14, 336, 241, 501], #нопка диалага 1
    [14, 504, 241, 662], #кнопка дилога 2
    [14, 667, 241, 771], #кнопка дилога 3
    [313, 857, 712, 896], #артевакты
    [1146, 1, 1198, 53], #сохронение
    [1083, 4, 1137, 56] #настройки
                 ])

kill_gui = IMenu([
      [497, 773, 93], #выход
      [737, 773, 93], #играть
      [0, 0, 100, 900], #текстур пак
      [784, 372, 50], #прошлая игра
      [984, 768, 93], #настройки
      [915, 87, 1200, 87+57*2] #ачивки
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
    [75, 590, 537, 636]   #музыка
])

soul_select_gui = IMenu([
    [481, 757, 86],
    [766, 763, 84],
    [760, 485, 966, 566],
    [520, 77, 1058, 308],
    [90, 128, 307, 345]
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

mus = line((0, 0, 0), (255, 255, 255), [75, 590, 537, 636])

original_menu = 2

save_itom = {}

while RUN:
    sc_main.blit(nots.render("версия 0.8", True, (255, 255, 255)), (500 * scale.scale_right, 0))

    scaled_canvas = pygame.transform.scale(sc_main, (sc_real.get_width(), sc_real.get_height()))

    sc_real.blit(scaled_canvas, (0, 0))

    pygame.display.update()
    if doble_click_chek: doble_click_chek -= 1

    if Scena.scena:
        original_menu = 1
        menu = 4


    sc_main.fill((0, 0, 0))

    for i in all_gif:
        if i == "profil":
            sc_main.blit(pygame.transform.scale(all_gif[i].render(1 / FPS), real_screen), (0, 0))



    if menu == 1:

        if playr_now.hp >= 100:
            Achievement.meta_achiv(None, 4)

        if playr_now.hp <= 0:
            menu = 3
            sistem_seting.start_music(sounds["recant"])
            Achievement.meta_achiv(None, 1)
            if playr_now.y <= -1400:
                Achievement.meta_achiv(None, 3)
            elif playr_now.y <= -3000:
                Achievement.meta_achiv(None, 7)
            if zith.RAZMER - 8 >= len(meta_progress["open soul"]):
                Soul_class.unlock_soul()
                if 3 in meta_progress["open soul"]:
                    Achievement.meta_achiv(None, 5)
                Scena.scena = Gif("новая_жиза", True, 1)


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
                    other_mov(igra_gui.sub_select(8, scale.mous_get(), [zith.RAZMER]*2))


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

                    elif BUTTON == 6: #выбираем карту
                        setting["choss_what"] = "cards"
                        if doble_click_chek:
                            if setting["choss_what"] == "cards":
                                sounds["ACT"].play()
                                playr_now.cards[setting["cards_now"]].efect_card(zith)
                                zith.canculate_tick()

                    elif BUTTON == 8: #игровое поле
                        setting["choss_what"] = igra_gui.sub_select(BUTTON, scale.mous_get(), [zith.RAZMER]*2)
                        if setting["choss_what"] == [playr_now.x % zith.RAZMER, playr_now.y % zith.RAZMER]:
                            setting["figur on mous"] = True

                    elif BUTTON == 13:
                        setting["item"] = igra_gui.sub_select(BUTTON, scale.mous_get(), [10, 1])[0]
                        if setting["item"] > len(playr_now.artefact)-1:
                            setting["item"] = False

                    elif BUTTON == 14:
                        True_Save.creat_save(playr_now)

                    elif BUTTON == 15:
                        original_menu = menu
                        menu = 5

                    doble_click_chek = 5

                if i.button == 5: # Колесико вверх
                    if BUTTON == 7:
                        setting["scrool_opisanie"] += 1

                    elif BUTTON == 9:
                        setting["dialog"] += 1

                    elif BUTTON == 6:
                        if setting["cards_now"] > 0:
                            setting["cards_now"] -= 1

                    elif 10 <= BUTTON <= 13:
                        setting["scrool_chat"] += 1


                if i.button == 4: # Колесико вниз
                    if BUTTON == 6:
                        if setting["cards_now"] + 1 < len(playr_now.cards):
                            setting["cards_now"] += 1

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

                if i.key == pygame.K_LEFT:
                    setting["map"][0] -= 25
                if i.key == pygame.K_RIGHT:
                    setting["map"][0] += 25
                if i.key == pygame.K_UP:
                    setting["map"][1] -= 25
                if i.key == pygame.K_DOWN:
                    setting["map"][1] += 25
                if i.key == pygame.K_EQUALS:
                    setting["map"][2] += 25
                    setting["map"][1] -= 25/2
                    setting["map"][0] -= 25/2
                if i.key == pygame.K_MINUS:
                    setting["map"][2] -= 25
                    setting["map"][1] += 25/2
                    setting["map"][0] += 25/2
                if i.key == pygame.K_h:
                    setting["map"] = [0, 0, 0]

                move(zith, i.key, playr_now.soul)



            if i.type == pygame.QUIT:
                RUN = False
                #активная игра

    elif menu == 2:
        sc_main.blit(tesxture_blok["no_end_fon"], (0, 0))

        BUTTON = kill_gui.button_mous(scale.mous_get())

        render_achivment()

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

                        menu = 6

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

                    elif BUTTON == 5:
                        menu = 5
                        original_menu = 2
            if i.type == pygame.QUIT:
                pass
                RUN = False

        if BUTTON == 6:
            a = kill_gui.sub_select(6, scale.mous_get(), [5, 2])
            a = a[0] + a[1]*5
            if len(meta_progress["all_ach"]) > a:
                sc_main.blit(nots.render(meta_progress["all_ach"][a].name, False, (255, 255, 255)), (scale.mous_get()[0]-300, scale.mous_get()[1]))
                sc_main.blit(nots.render(meta_progress["all_ach"][a].opisanie, False, (255, 255, 255)),
                             (scale.mous_get()[0] - 300, scale.mous_get()[1]+50))


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
            menu = original_menu
            Scena.scena = False
            zith.smena(playr_now.y)

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_e:
                    menu = original_menu
                    Scena.scena = False
                    zith.smena(playr_now.y)

    elif menu == 5:
        sc_main.blit(tesxture_blok["seting"], (0, 0))
        mus.print(option_settings["music_voluom"], 100)
        BUTTON = seting_gui.button_mous(scale.mous_get())

        for i in range(2):
            if lang[i+2] == option_settings["languje"]:
                c = [seting_gui.gui[i+1][0], seting_gui.gui[i+1][1], seting_gui.gui[i+1][2]-seting_gui.gui[i+1][0], seting_gui.gui[i+1][3]-seting_gui.gui[i+1][1]]
                pygame.draw.rect(sc_main, (255, 0, 255), c, 1)

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                pass
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if BUTTON == 1:
                        menu = original_menu

                    if 2 <= BUTTON <= 3:
                        option_settings["languje"] = lang[BUTTON]
                        True_Save.update_stuff("languge", lang[BUTTON])

                    if BUTTON == 4:
                        option_settings["music_voluom"] = seting_gui.sub_select(4, scale.mous_get(), [100, 1])[0]
                        True_Save.update_stuff("music_voluom", option_settings["music_voluom"])
                        sistem_seting.start_music(sistem_seting.sound)

            if i.type == pygame.QUIT:
                RUN = False

    elif menu == 6:
        sc_main.blit(tesxture_blok["soul_sect"], (0, 0))

        sc_main.blit(pygame.transform.scale(meta_progress["open soul"][setting["soul vibor"]].png, (218, 218)), (90, 128))
        sc_main.blit(pygame.transform.scale(meta_progress["open soul"][setting["soul vibor"]].gid, (300, 300)),
                     (545, 77))

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                pass
            if i.type == pygame.MOUSEBUTTONDOWN:
                BUTTON = soul_select_gui.button_mous(scale.mous_get())

                if i.button == 1:
                    if BUTTON == 1:
                        menu = 2
                    if BUTTON == 2:
                        playr_now.soul = meta_progress["open soul"][setting["soul vibor"]]
                        menu = 1
                    if BUTTON == 3:
                        if len(meta_progress["open soul"])-1 == setting["soul vibor"]:
                            setting["soul vibor"] = 0
                        else:
                            setting["soul vibor"] += 1
                    if BUTTON == 4:
                        pass

            if i.type == pygame.QUIT:
                RUN = False

    clock.tick(FPS)

pygame.quit()