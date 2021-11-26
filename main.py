from tkinter import (
    Tk,
    Button,
    Scale,
    HORIZONTAL,
    PhotoImage,
    Label,
    Listbox,
    END,
    Scrollbar,
    VERTICAL,
)
from tkinter.filedialog import askopenfilename, askdirectory
from pygame.mixer import music, init, quit
from tinytag import TinyTag
from glob import glob

# инилизация mixer, без него программа не будет работать
init()

# это переменные для функций
pause: bool = False
restart: bool = False

# пустой список для адресов
playlist: list = []

# позиция списка
trek: int = 0

# для тегов mp3 - TinyTag
a: None = None

# выбран язык
choose: int = 0

# первые настройки
lang: str = "language: English"

track_null: str = "add track"
track_none: str = "add track!"
added_file: str = "add"
added_folder: str = "add folder"

nesting: str = "next"
earning: str = "early"

name_trek_none: str = "no track name"
name_album_none: str = "no album name"
name_artist_none: str = "no performer"

pauses: str = "pause"
play: str = "play"


# он просто для громкости
def get_v(value):
    music.set_volume(int(value) / 100)


# убирает паузу если паузой не привычно
def playing(event=None):
    global pause
    if pause:
        music.unpause()


# добавляет в список адресс если адреса нет просто пропускаем
def add(event=None, file=None):
    if file is None:
        get_address: str = askopenfilename(
            filetypes=(
                ("MP3", "*.mp3"),
                ("Windows audio file", "*.wav"),
                ("instruction MIDI", "*.mid"),
                ("instruction MIDI", "*.midi"),
                ("all audio files", "*.midi",),
                ("all audio files", "*.mid"),
                ("all audio files", "*.wav"),
                ("all audio files", "*.mp3"),
            )
        )
    else:
        get_address: str = file

    if get_address is None:
        pass
    else:
        try:

            if (
                    TinyTag.get(get_address).title == " "
                    or TinyTag.get(get_address).title == "  "
                    or TinyTag.get(get_address).title == ""
                    or TinyTag.get(get_address).title is None
            ):
                name = get_address.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])
            else:
                list_track.insert(END, TinyTag.get(get_address).title)
            playlist.append(get_address)
        except AttributeError:
            name = get_address.split("/")
            list_track.insert(0, name[len(name) - 1][:-4])
        except FileNotFoundError:
            pass


def add_folder(event=None, file=None):
    if file == None:
        get_address: str = askdirectory()
    else:
        get_address: str = file

    if get_address is None:
        pass
    else:
        for filename in glob(get_address + "/*.mp3"):
            playlist.append(filename)
            try:
                if (
                        TinyTag.get(filename).title == " "
                        or TinyTag.get(filename).title == "  "
                        or TinyTag.get(filename).title == ""
                        or TinyTag.get(filename).title is None
                ):
                    name = filename.split("/")
                    list_track.insert(END, name[len(name) - 1][:-4])
                else:
                    list_track.insert(END, TinyTag.get(filename).title)

            except AttributeError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

            except LookupError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

        for filename in glob(get_address + "/*.mid"):
            playlist.append(filename)

            try:
                if (
                        TinyTag.get(filename).title == " "
                        or TinyTag.get(filename).title == "  "
                        or TinyTag.get(filename).title == ""
                        or TinyTag.get(filename).title is None
                ):
                    name = filename.split("/")
                    list_track.insert(END, name[len(name) - 1][:-4])
                else:
                    list_track.insert(END, TinyTag.get(filename).title)

            except AttributeError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

            except LookupError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

        for filename in glob(get_address + "/*.wav"):
            playlist.append(filename)

            try:
                if (
                        TinyTag.get(filename).title == " "
                        or TinyTag.get(filename).title == "  "
                        or TinyTag.get(filename).title == ""
                        or TinyTag.get(filename).title is None
                ):
                    name = filename.split("/")
                    list_track.insert(END, name[len(name) - 1][:-4])
                else:
                    list_track.insert(END, TinyTag.get(filename).title)
            except AttributeError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

            except LookupError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

        for filename in glob(get_address + "/*.midi"):
            playlist.append(filename)

            try:
                if (
                        TinyTag.get(filename).title == " "
                        or TinyTag.get(filename).title == "  "
                        or TinyTag.get(filename).title == ""
                        or TinyTag.get(filename).title is None
                ):
                    name = filename.split("/")
                    list_track.insert(END, name[len(name) - 1][:-4])
                else:
                    list_track.insert(END, TinyTag.get(get_address).title)
            except AttributeError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])

            except LookupError:
                name = filename.split("/")
                list_track.insert(END, name[len(name) - 1][:-4])


# пауза еще раз и воспроизведется как раньше
def stopping(event=None):
    global pause

    if pause:
        music.unpause()
        pause = False
    else:
        music.pause()
        pause = True


# следущий трек(здесь выбирает по позиции адрес из списка и загружает трек по этому адресу
# потом вырезает её имя из адреса и убирает расширение и выводит на экран
def next(event=None):
    global trek, a

    if trek >= len(playlist):
        trek = 0

    try:
        trek += 1
        if trek >= len(playlist):
            trek = 0

        music.load(playlist[trek])
        music.play(loops=-1)

        try:
            a = TinyTag.get(playlist[trek])
        except LookupError:
            pass
        name_trek.configure(text=name_trek_none)

        try:
            if a.title == " " or a.title == "  " or a.title == "":
                pass
            else:
                name_trek.configure(text=a.title)
        except AttributeError:
            pass

        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)
        name_artist.configure(text=name_artist_none)

        try:
            if a.artist == " " or a.artist == "  " or a.artist == "":
                pass
            else:
                name_artist.configure(text=a.artist)
        except AttributeError:
            pass

        x_center_artist_new = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
        name_artist.place(x=x_center_artist_new, y=20)
        name_album.configure(text=name_album_none)

        try:
            if a.album == " " or a.album == "  " or a.album == "":
                pass
            else:
                name_album.configure(text=a.album)
        except AttributeError:
            pass

        x_center_album_new = WIDTH // 2 - name_album.winfo_reqwidth() // 2
        name_album.place(x=x_center_album_new, y=40)

    except IndexError:
        name_trek.configure(text=track_none)
        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)

    except TypeError:
        name_trek.configure(text=track_none)
        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)

    if trek >= len(playlist):
        trek = 0


# тоже самое что "следущий" но переход наоборот
def early(event=None):
    global trek, a

    if trek >= len(playlist):
        trek = 0
    if trek < 0:
        trek = len(playlist) - 1

    try:
        trek -= 1
        if trek < 0:
            trek = len(playlist) - 1
        music.load(playlist[trek])
        music.play(loops=-1)

        try:
            a = TinyTag.get(playlist[trek])
        except LookupError:
            pass

        name_trek.configure(text=name_trek_none)

        try:
            if a.title == " " or a.title == "  " or a.title == "":
                pass
            else:
                name_trek.configure(text=a.title)
        except AttributeError:
            pass

        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)
        name_artist.configure(text=name_artist_none)

        try:
            if a.artist == " " or a.artist == "  " or a.artist == "":
                pass
            else:
                name_artist.configure(text=a.artist)
        except AttributeError:
            pass

        x_center_artist_new = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
        name_artist.place(x=x_center_artist_new, y=20)
        name_album.configure(text=name_album_none)

        try:
            if a.album == " " or a.album == "  " or a.album == "":
                pass
            else:
                name_album.configure(text=a.album)
        except AttributeError:
            pass

        x_center_album_new = WIDTH // 2 - name_album.winfo_reqwidth() // 2
        name_album.place(x=x_center_album_new, y=40)
    except IndexError:
        name_trek.configure(text=track_none)
        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)

    except TypeError:
        name_trek.configure(text=track_none)
        x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
        name_trek.place(x=x_center_name_new, y=0)

    if trek >= len(playlist):
        trek = 0
    if trek < 0:
        trek = len(playlist) - 1


def language():
    global choose, lang, track_null, track_none, added_file, added_folder, nesting, earning, name_trek_none, name_album_none, name_artist_none, pauses, play, added_folder, a

    choose += 1

    if choose >= 2:
        choose = 0

    if choose == 0:
        lang = "language: English"
        track_null = "add track"
        track_none = "add track!"
        added_file = "add track"
        added_folder = "add folder"
        nesting = "next"
        earning = "early"
        name_trek_none = "no track name"
        name_album_none = "no album name"
        name_artist_none = "no performer"
        pauses = "pause"
        play = "play"

    elif choose == 1:
        lang = "язык: Русский"
        track_null = "Добавьте трек"
        track_none = "Добавьте трек!"
        added_file = "Добавить трек"
        added_folder = "добавить папку"
        nesting = """след-
ую-
щий"""
        earning = """пре-
дыду-
щий"""
        name_trek_none = "нет имени трека"
        name_album_none = "нет имени альбома"
        name_artist_none = "не указан исполнитель"
        pauses = "пауза"
        play = "играть"

    button1.configure(text=play)
    x_center_1_new = WIDTH // 2 - button1.winfo_reqwidth() // 2
    button1.place(x=x_center_1_new + 30, y=HEIGHT - 125)

    button2.configure(text=pauses)
    x_center_2_new = WIDTH // 2 - button2.winfo_reqwidth() // 2
    button2.place(x=x_center_2_new - 30, y=HEIGHT - 125)

    name_trek.configure(text=track_null)
    x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
    name_trek.place(x=x_center_name_new, y=0)

    name_artist.configure(text=track_null)
    x_center_artist_new = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
    name_artist.place(x=x_center_artist_new, y=20)

    name_album.configure(text=track_null)
    x_center_album_new = WIDTH // 2 - name_album.winfo_reqwidth() // 2
    name_album.place(x=x_center_album_new, y=40)

    button_restart.configure(text=added_file)
    button_restart.place(x=0, y=HEIGHT - 50)

    button_restart2.configure(text=added_folder)
    x_center_restart = WIDTH - button_restart.winfo_reqwidth()
    button_restart2.place(x=x_center_restart, y=HEIGHT - 50)

    button_next.configure(text=nesting)
    x_center_next_new = WIDTH // 2 - button_next.winfo_reqwidth() // 2
    button_next.place(x=x_center_next_new + 75, y=HEIGHT - 125)

    button_early.configure(text=earning)
    x_center_early_new = WIDTH // 2 - button_early.winfo_reqwidth() // 2
    button_early.place(x=x_center_early_new - 75, y=HEIGHT - 125)

    button_lang.configure(text=lang)
    x_center_lang_new = WIDTH // 2 - button_lang.winfo_reqwidth() // 2
    button_lang.place(x=x_center_lang_new, y=HEIGHT - 25)

    name_trek.configure(text=name_trek_none)

    try:
        if a.title != " " and a.title != "  " and a.title != "" and a.title is not None:
            name_trek.configure(text=a.title)
        else:
            pass
    except AttributeError:
        pass

    x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
    name_trek.place(x=x_center_name_new, y=0)
    name_artist.configure(text=name_artist_none)

    try:
        if a.artist != " " or a.artist != "  " or a.artist != "" or a.artist is not None:
            name_artist.configure(text=a.artist)
        else:
            pass
    except AttributeError:
        pass

    x_center_artist_new = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
    name_artist.place(x=x_center_artist_new, y=20)
    name_album.configure(text=name_album_none)

    try:
        if a.album != " " or a.album != "  " or a.album != "" or a.artist is not None:
            name_album.configure(text=a.album)
        else:
            pass
    except AttributeError:
        pass

    x_center_album_new = WIDTH // 2 - name_album.winfo_reqwidth() // 2
    name_album.place(x=x_center_album_new, y=40)


def trek_from_list(event=None):
    global trek, playlist, a

    select = list_track.curselection()
    trek = select[0]
    music.load(playlist[trek])
    music.play(loops=-1)

    try:
        a = TinyTag.get(playlist[trek])
    except LookupError:
        pass

    name_trek.configure(text=name_trek_none)

    try:
        if a.title == " " or a.title == "  " or a.title == "":
            pass
        else:
            name_trek.configure(text=a.title)
    except AttributeError:
        pass

    x_center_name_new = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
    name_trek.place(x=x_center_name_new, y=0)
    name_artist.configure(text=name_artist_none)

    try:
        if a.artist == " " or a.artist == "  " or a.artist == "":
            pass
        else:
            name_artist.configure(text=a.artist)
    except AttributeError:
        pass

    x_center_artist_new = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
    name_artist.place(x=x_center_artist_new, y=20)
    name_album.configure(text=name_album_none)

    try:
        if a.album == " " or a.album == "  " or a.album == "":
            pass
        else:
            name_album.configure(text=a.album)
    except AttributeError:
        pass

    x_center_album_new = WIDTH // 2 - name_album.winfo_reqwidth() // 2
    name_album.place(x=x_center_album_new, y=40)


def quiting(event=None):
    exit()
    quit()


# просто создаем окно tkinter
window = Tk()

# получает размер дисплея
# WIDTH=display.Info().current_w
# HEIGHT=display.Info().current_h

WIDTH = 400
HEIGHT = 190

# имя программы
window.title("AUPlay")
window.iconbitmap("./image/AUPlay.ico")
# круто выглядит в {} казывают переменную так удобней чем по старинке
window.geometry(f"{WIDTH}x{HEIGHT}")

WIDTH = 200
HEIGHT = 190

# указываю запрет на изменение разрешения окна
window.resizable(False, False)

# изображение это фон
image = PhotoImage(file="./image/menu_bg.png")
label = Label(window, image=image)
label.image_ref = image
label.place(x=-2, y=-2)

# button play, кнопка play
button1 = Button(
    window, text=play,
    bg="white", command=playing
)

# formula for center place button, формула для центра расмещения кнопки
x_center_1 = WIDTH // 2 - button1.winfo_reqwidth() // 2
y_center_1 = HEIGHT // 2 - button1.winfo_reqheight() // 2 - 15
button1.place(x=x_center_1 + 30, y=HEIGHT - 125)

# button pause, кнопка пауза
button2 = Button(
    window, text=pauses,
    bg="white", command=stopping
)

# в button2.winfo_reqwidth() надо указать наш виджет чтобы он ровно сделал по середине
x_center_2 = WIDTH // 2 - button2.winfo_reqwidth() // 2

# place take two position in x and y, place принимает два значения x и y
button2.place(x=x_center_2 - 30, y=HEIGHT - 125)

# scale it scale for setting volume, scale это шкала для настройки громкости
scale = Scale(
    window, orient=HORIZONTAL,
    length=100, from_=0,
    to=100, resolution=1,
    bg="black", fg="white",
    command=get_v,
)
x_center_scale = WIDTH // 2 - scale.winfo_reqwidth() // 2
scale.place(x=x_center_scale, y=HEIGHT - 95)

# название через TinyTag
name_trek = Label(
    window, text=track_null,
    bg="black", fg="white"
)
x_center_name = WIDTH // 2 - name_trek.winfo_reqwidth() // 2
name_trek.place(x=x_center_name, y=-1)

# артист через TinyTag
name_artist = Label(
    window, text=track_null,
    bg="black", fg="white"
)
x_center_artist = WIDTH // 2 - name_artist.winfo_reqwidth() // 2
name_artist.place(x=x_center_artist, y=19)

# альбом через TinyTag
name_album = Label(
    window, text=track_null,
    bg="black", fg="white"
)
x_center_album = WIDTH // 2 - name_album.winfo_reqwidth() // 2
name_album.place(x=x_center_album, y=39)

# на самом деле я собирался сделать настройку чтобы трек повторятся и не повторятся мог но не сработало
button_restart = Button(
    window, text=added_file, command=add,
    bg="black", fg="white",
    width=12
)
button_restart.place(x=0, y=HEIGHT - 50)

# добавить папку-точнее содержимое
button_restart2 = Button(
    window, text=added_folder,
    command=add_folder, bg="black",
    fg="white", width=12
)
x_center_restart2 = WIDTH - button_restart.winfo_reqwidth()
button_restart2.place(x=x_center_restart2, y=HEIGHT - 50)

# кнопка для смены языка
button_lang = Button(
    window, text=lang,
    command=language, bg="black",
    fg="white", width=13
)
x_center_lang = WIDTH // 2 - button_lang.winfo_reqwidth() // 2
button_lang.place(x=x_center_lang, y=HEIGHT - 25)

# следущий и преведущий трек
button_next = Button(
    window, text=nesting,
    command=next, bg="black",
    fg="white", height=4
)
x_center_next = WIDTH // 2 - button_next.winfo_reqwidth() // 2
button_next.place(x=x_center_next + 75, y=HEIGHT - 125)

# назад нечисть
button_early = Button(
    window, text=earning,
    command=early, bg="black",
    fg="white", height=4
)
x_center_early = WIDTH // 2 - button_early.winfo_reqwidth() // 2
button_early.place(x=x_center_early - 75, y=HEIGHT - 125)

# это ползунок для промотки списка
scroll = Scrollbar(window, orient=VERTICAL)

# это сам список
list_track = Listbox(
    width=30, height=12, bg="#00EBFD", yscrollcommand=scroll.set
)
scroll.config(command=list_track.yview)
list_track.place(x=199, y=-1)

# размещает ползунок для списка
scroll.place(in_=list_track, relx=1.0, relheight=1.0)

# это обработка нажатия в списке
window.bind("<<ListboxSelect>>", trek_from_list)


# it demo music
add_folder(file="./demo")

# обработка клавиш полезно если лень мышью нажимать
window.bind("<+>", add)
window.bind("<*>", add_folder)
window.bind("<Right>", next)
window.bind("<Left>", early)
window.bind("<Escape>", quiting)
window.bind("<space>", stopping)
window.overrideredirect(False)
window.mainloop()
