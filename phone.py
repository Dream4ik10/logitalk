import customtkinter as ctk
import random
import string
import os
import socket
import threading
from tkinter import filedialog
from PIL import Image, ImageOps, ImageFilter, ImageEnhance


ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Телефон")
app.geometry("360x640")
app.resizable(False, False)

container = ctk.CTkFrame(app, fg_color="#181824")
container.pack(fill="both", expand=True)

frames = {}


def show_frame(name):
    frames[name].tkraise()


def back_button(frame):
    ctk.CTkButton(
        frame,
        text="⬅ Назад",
        width=140,
        height=36,
        fg_color="#3A3F58",
        hover_color="#4E5575",
        corner_radius=18,
        command=lambda: show_frame("home")
    ).pack(pady=12)


home = ctk.CTkFrame(container, fg_color="#181824")
home.place(relwidth=1, relheight=1)
frames["home"] = home

ctk.CTkLabel(home, text="Мій Телефон", font=("Arial", 22, "bold"), text_color="#E0E6ED").pack(pady=30)

apps_frame = ctk.CTkFrame(home, fg_color="transparent")
apps_frame.pack(pady=10)

menu_apps = [
    ("🖱 Клікер", "clicker", "#4F46E5", "#4338CA", 0, 0),
    ("🧮 Калькулятор", "calc", "#059669", "#047857", 0, 1),
    ("🎮 Гра", "game", "#D97706", "#B45309", 1, 0),
    ("⚙ Налаштування", "settings", "#4B5563", "#374151", 1, 1),
    ("🔑 Паролі", "password", "#7C3AED", "#6D28D9", 2, 0),
    ("🖼 Галерея", "gallery", "#DB2777", "#BE185D", 2, 1),
    ("💬 LogiTalk", "logitalk", "#2563EB", "#1D4ED8", 3, 0),
]

for title, target, color, hover, r, c in menu_apps:
    ctk.CTkButton(
        apps_frame,
        text=title,
        width=140,
        height=58,
        corner_radius=16,
        fg_color=color,
        hover_color=hover,
        font=("Arial", 14, "bold"),
        command=lambda t=target: show_frame(t)
    ).grid(row=r, column=c, padx=10, pady=10)



clicker = ctk.CTkFrame(container, fg_color="#181824")
clicker.place(relwidth=1, relheight=1)
frames["clicker"] = clicker

click_count = ctk.IntVar(value=0)

ctk.CTkLabel(clicker, text="Клікер", font=("Arial", 22, "bold"), text_color="#E0E6ED").pack(pady=25)
click_label = ctk.CTkLabel(clicker, text="0", font=("Arial", 46, "bold"), text_color="#818CF8")
click_label.pack(pady=35)


def click():
    click_count.set(click_count.get() + 1)
    click_label.configure(text=str(click_count.get()))


ctk.CTkButton(
    clicker,
    text="Тапни мене!",
    width=190,
    height=80,
    corner_radius=25,
    fg_color="#6366F1",
    hover_color="#4F46E5",
    font=("Arial", 18, "bold"),
    command=click
).pack(pady=25)
back_button(clicker)



calc = ctk.CTkFrame(container, fg_color="#181824")
calc.place(relwidth=1, relheight=1)
frames["calc"] = calc

ctk.CTkLabel(calc, text="Калькулятор", font=("Arial", 20, "bold"), text_color="#E0E6ED").pack(pady=10)

calc_entry = ctk.CTkEntry(
    calc,
    width=280,
    height=45,
    font=("Arial", 20),
    justify="right",
    fg_color="#232638",
    border_color="#374151",
    corner_radius=12
)
calc_entry.pack(pady=10)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
]

btn_frame = ctk.CTkFrame(calc, fg_color="transparent")
btn_frame.pack(pady=5)


def press(symbol):
    if symbol == "=":
        try:
            result = str(eval(calc_entry.get()))
        except Exception:
            result = "Помилка"
        calc_entry.delete(0, "end")
        calc_entry.insert(0, result)
    else:
        calc_entry.insert("end", symbol)


row = 0
col = 0
for b in buttons:
    if b in ["/", "*", "-", "+"]:
        btn_color = "#D97706"
        btn_hover = "#B45309"
    elif b == "=":
        btn_color = "#10B981"
        btn_hover = "#059669"
    else:
        btn_color = "#2E3349"
        btn_hover = "#3E4461"

    ctk.CTkButton(
        btn_frame,
        text=b,
        width=62,
        height=52,
        corner_radius=14,
        fg_color=btn_color,
        hover_color=btn_hover,
        font=("Arial", 16, "bold"),
        command=lambda s=b: press(s)
    ).grid(row=row, column=col, padx=4, pady=4)
    col += 1
    if col > 3:
        col = 0
        row += 1

back_button(calc)



game = ctk.CTkFrame(container, fg_color="#181824")
game.place(relwidth=1, relheight=1)
frames["game"] = game

secret_number = random.randint(1, 20)

ctk.CTkLabel(game, text="Вгадай число від 1 до 20", font=("Arial", 18, "bold"), text_color="#FBBF24").pack(pady=20)

game_entry = ctk.CTkEntry(
    game,
    width=160,
    height=40,
    justify="center",
    font=("Arial", 18),
    fg_color="#232638",
    border_color="#374151"
)
game_entry.pack(pady=10)

game_result = ctk.CTkLabel(game, text="", font=("Arial", 16, "bold"), text_color="#FCD34D")
game_result.pack(pady=10)


def check_number():
    global secret_number
    try:
        guess = int(game_entry.get())
    except ValueError:
        game_result.configure(text="Введи число!")
        return

    if guess < secret_number:
        game_result.configure(text="Більше!")
    elif guess > secret_number:
        game_result.configure(text="Менше!")
    else:
        game_result.configure(text="Вгадав! 🎉")
        secret_number = random.randint(1, 20)


ctk.CTkButton(
    game,
    text="Перевірити",
    width=160,
    height=40,
    fg_color="#F59E0B",
    hover_color="#D97706",
    font=("Arial", 14, "bold"),
    corner_radius=12,
    command=check_number
).pack(pady=10)
back_button(game)


password_app = ctk.CTkFrame(container, fg_color="#181824")
password_app.place(relwidth=1, relheight=1)
frames["password"] = password_app

ctk.CTkLabel(password_app, text="Генератор паролів", font=("Arial", 18, "bold"), text_color="#A78BFA").pack(pady=15)

pass_entry = ctk.CTkEntry(
    password_app,
    width=260,
    height=40,
    justify="center",
    font=("Arial", 15),
    fg_color="#232638",
    border_color="#374151"
)
pass_entry.pack(pady=10)

pw_lower = ctk.BooleanVar(value=True)
pw_upper = ctk.BooleanVar(value=True)
pw_digits = ctk.BooleanVar(value=True)
pw_symbols = ctk.BooleanVar(value=False)

ctk.CTkCheckBox(password_app, text="a-z", variable=pw_lower, fg_color="#8B5CF6", hover_color="#7C3AED").pack(pady=3)
ctk.CTkCheckBox(password_app, text="A-Z", variable=pw_upper, fg_color="#8B5CF6", hover_color="#7C3AED").pack(pady=3)
ctk.CTkCheckBox(password_app, text="0-9", variable=pw_digits, fg_color="#8B5CF6", hover_color="#7C3AED").pack(pady=3)
ctk.CTkCheckBox(password_app, text="!@#$", variable=pw_symbols, fg_color="#8B5CF6", hover_color="#7C3AED").pack(pady=3)

pw_len_label = ctk.CTkLabel(password_app, text="Довжина: 12", font=("Arial", 13))
pw_len_label.pack(pady=(10, 0))


def pw_slide(value):
    pw_len_label.configure(text="Довжина: " + str(int(value)))


pw_slider = ctk.CTkSlider(password_app, from_=4, to=64, button_color="#8B5CF6", progress_color="#A78BFA", command=pw_slide)
pw_slider.set(12)
pw_slider.pack(pady=10)


def generate_password():
    chars = ""
    if pw_lower.get():
        chars += string.ascii_lowercase
    if pw_upper.get():
        chars += string.ascii_uppercase
    if pw_digits.get():
        chars += string.digits
    if pw_symbols.get():
        chars += "!@#$%^&*"

    if chars == "":
        pass_entry.delete(0, "end")
        pass_entry.insert(0, "Вибери хоч щось!")
        return

    length = int(pw_slider.get())
    password = ""
    for _ in range(length):
        password += random.choice(chars)

    pass_entry.delete(0, "end")
    pass_entry.insert(0, password)


ctk.CTkButton(
    password_app,
    text="Згенерувати",
    width=180,
    height=38,
    fg_color="#8B5CF6",
    hover_color="#7C3AED",
    corner_radius=12,
    font=("Arial", 14, "bold"),
    command=generate_password
).pack(pady=12)
back_button(password_app)


gallery = ctk.CTkFrame(container, fg_color="#181824")
gallery.place(relwidth=1, relheight=1)
frames["gallery"] = gallery

ctk.CTkLabel(gallery, text="Галерея", font=("Arial", 18, "bold"), text_color="#F472B6").pack(pady=10)

gallery_pic = ctk.CTkLabel(
    gallery,
    text="Немає фото",
    width=240,
    height=240,
    fg_color="#232638",
    corner_radius=16
)
gallery_pic.pack(pady=10)

gallery_original = None
gallery_rotation = 0
gallery_gray = False
gallery_invert = False
gallery_blur = False


def gallery_render():
    if gallery_original is None:
        return

    img = gallery_original.copy()
    img = img.rotate(gallery_rotation, expand=True)

    if gallery_gray:
        img = ImageOps.grayscale(img).convert("RGB")

    if gallery_invert:
        img = ImageOps.invert(img)

    if gallery_blur:
        img = img.filter(ImageFilter.BLUR)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(gallery_contrast.get())

    img.thumbnail((240, 240))
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
    gallery_pic.configure(image=ctk_img, text="")
    gallery_pic.image = ctk_img


def gallery_choose_image(path=None):
    global gallery_original, gallery_rotation, gallery_gray, gallery_invert, gallery_blur
    if path is None:
        path = filedialog.askopenfilename(
            filetypes=[("Зображення", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
    if not path:
        return

    gallery_original = Image.open(path).convert("RGB")
    gallery_rotation = 0
    gallery_gray = False
    gallery_invert = False
    gallery_blur = False
    gallery_contrast.set(1)
    gallery_render()


def gallery_rotate():
    global gallery_rotation
    gallery_rotation = (gallery_rotation - 90) % 360
    gallery_render()


def gallery_toggle_gray():
    global gallery_gray
    gallery_gray = not gallery_gray
    gallery_render()


def gallery_toggle_invert():
    global gallery_invert
    gallery_invert = not gallery_invert
    gallery_render()


def gallery_toggle_blur():
    global gallery_blur
    gallery_blur = not gallery_blur
    gallery_render()


def gallery_on_contrast(value):
    gallery_render()


ctk.CTkButton(
    gallery,
    text="Обрати фото",
    command=gallery_choose_image,
    width=200,
    height=35,
    fg_color="#EC4899",
    hover_color="#DB2777",
    corner_radius=12
).pack(pady=6)

gallery_btn_row = ctk.CTkFrame(gallery, fg_color="transparent")
gallery_btn_row.pack(pady=4)

ctk.CTkButton(gallery_btn_row, text="Повернути 90°", command=gallery_rotate, width=105, fg_color="#374151", hover_color="#4B5563").grid(row=0, column=0, padx=3, pady=3)
ctk.CTkButton(gallery_btn_row, text="Ч/Б", command=gallery_toggle_gray, width=105, fg_color="#374151", hover_color="#4B5563").grid(row=0, column=1, padx=3, pady=3)
ctk.CTkButton(gallery_btn_row, text="Інверсія", command=gallery_toggle_invert, width=105, fg_color="#374151", hover_color="#4B5563").grid(row=1, column=0, padx=3, pady=3)
ctk.CTkButton(gallery_btn_row, text="Розмиття", command=gallery_toggle_blur, width=105, fg_color="#374151", hover_color="#4B5563").grid(row=1, column=1, padx=3, pady=3)

ctk.CTkLabel(gallery, text="Контраст").pack(pady=(6, 0))
gallery_contrast = ctk.CTkSlider(gallery, from_=0, to=3, number_of_steps=30, button_color="#EC4899", progress_color="#F472B6", command=gallery_on_contrast)
gallery_contrast.set(1)
gallery_contrast.pack(pady=6, padx=30, fill="x")

back_button(gallery)

default_gallery_image = os.path.join(os.path.dirname(__file__), "sample.png")
if os.path.exists(default_gallery_image):
    gallery_choose_image(default_gallery_image)



logitalk = ctk.CTkFrame(container, fg_color="#181824")
logitalk.place(relwidth=1, relheight=1)
frames["logitalk"] = logitalk

lt_user = {"name": ""}
LT_BLUE = "#3B82F6"
LT_BUBBLE = ("#2D3348", "#232638")


HOST = "7.tcp.eu.ngrok.io"
PORT = 22318

lt_net = {"sock": None, "connected": False}


def lt_connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HOST, PORT))
        s.settimeout(None)
    except Exception as e:
        print(f"Не змогли приєднатися до сервера: {e}")
        return False
    lt_net["sock"] = s
    lt_net["connected"] = True
    print("Успішно приєднався до сервера!")
    threading.Thread(target=lt_receive_loop, daemon=True).start()
    return True


def lt_disconnect():
    lt_net["connected"] = False
    if lt_net["sock"]:
        try:
            lt_net["sock"].close()
        except Exception:
            pass
        lt_net["sock"] = None


def lt_receive_loop():
    s = lt_net["sock"]
    while lt_net["connected"]:
        try:
            data = s.recv(4096)
        except Exception:
            break
        if not data:
            break
        message = data.decode("utf-8", errors="ignore")
       
        app.after(0, lambda m=message: lt_handle_line(m))
    if lt_net["connected"]:
        app.after(0, lambda: lt_add_message("LogiTalk", "З'єднання з сервером втрачено"))
    lt_net["connected"] = False


def lt_handle_line(message):
    if message.strip():
        lt_add_message("LogiTalk", message.strip())


def lt_send_to_server(text):
    if not lt_net["connected"]:
        return False
    try:
        lt_net["sock"].sendall(f"{lt_user['name']}: {text}".encode("utf-8"))
        return True
    except Exception:
        lt_net["connected"] = False
        return False



def lt_avatar(parent, size, text="👤"):
    return ctk.CTkLabel(
        parent,
        text=text,
        width=size,
        height=size,
        corner_radius=size // 2,
        fg_color=LT_BLUE,
        font=("Arial", size // 2)
    )


lt_reg = ctk.CTkFrame(logitalk, fg_color="transparent")
lt_reg.place(relwidth=1, relheight=1)

ctk.CTkLabel(lt_reg, text="Реєстрація", font=("Arial", 22, "bold"), text_color="#E0E6ED").pack(pady=(40, 20))
lt_avatar(lt_reg, 100).pack(pady=10)
ctk.CTkButton(lt_reg, text="Обрати зображення", width=180, fg_color="#374151", hover_color="#4B5563").pack(pady=10)

lt_name_entry = ctk.CTkEntry(lt_reg, width=180, height=36, justify="center", fg_color="#232638", border_color="#374151")
lt_name_entry.pack(pady=10)

lt_reg_error = ctk.CTkLabel(lt_reg, text="", text_color="#EF4444")
lt_reg_error.pack()


def lt_register():
    name = lt_name_entry.get().strip()
    if len(name) < 2:
        lt_reg_error.configure(text="Ім'я має містити мінімум 2 символи")
        return
    lt_reg_error.configure(text="Підключення...")
    lt_reg.update_idletasks()
    if not lt_connect():
        lt_reg_error.configure(text="Не вдалося підключитися до сервера")
        return
    lt_reg_error.configure(text="")
    lt_user["name"] = name
    lt_side_name.configure(text=name)
    lt_show_chat()
    lt_add_message("LogiTalk", f"Вітаю {name} в LogiTalk чаті!")


ctk.CTkButton(lt_reg, text="Зареєструватися", width=180, height=38, fg_color="#3B82F6", hover_color="#2563EB", command=lt_register).pack(pady=10)
ctk.CTkButton(lt_reg, text="⬅ Назад", width=180, height=38, fg_color="#374151", hover_color="#4B5563",
              command=lambda: show_frame("home")).pack(pady=10)
lt_name_entry.bind("<Return>", lambda e: lt_register())


lt_chat = ctk.CTkFrame(logitalk, fg_color="transparent")

lt_top = ctk.CTkFrame(lt_chat, fg_color="#1F2333", height=50)
lt_top.pack(fill="x", padx=6, pady=6)
lt_menu_btn = ctk.CTkButton(lt_top, text="☰", width=36, height=36, fg_color="#374151", hover_color="#4B5563")
lt_menu_btn.pack(side="left", padx=5, pady=5)
ctk.CTkLabel(lt_top, text="LogiTalk", font=("Arial", 15, "bold"), text_color="#E0E6ED").pack(side="left", expand=True)
ctk.CTkLabel(lt_top, text="", width=36).pack(side="right")

lt_messages = ctk.CTkScrollableFrame(lt_chat, fg_color="#181824")
lt_messages.pack(fill="both", expand=True, padx=6, pady=(0, 6))

lt_bottom = ctk.CTkFrame(lt_chat, fg_color="transparent")
lt_bottom.pack(fill="x", padx=6, pady=(0, 10))
lt_entry = ctk.CTkEntry(lt_bottom, height=38, fg_color="#232638", border_color="#374151")
lt_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
lt_send_btn = ctk.CTkButton(lt_bottom, text=">", width=40, height=38, fg_color="#3B82F6", hover_color="#2563EB")
lt_send_btn.pack(side="right")


def lt_add_message(author, text):
    row = ctk.CTkFrame(lt_messages, fg_color="transparent")
    row.pack(fill="x", pady=4, anchor="w")
    lt_avatar(row, 30).pack(side="left", padx=(0, 8), anchor="n")
    shown = text if author == "LogiTalk" else f"{author}: {text}"
    ctk.CTkLabel(
        row,
        text=shown,
        wraplength=220,
        justify="left",
        fg_color=LT_BUBBLE,
        corner_radius=12,
        padx=10,
        pady=6
    ).pack(side="left")
    lt_messages._parent_canvas.update_idletasks()
    lt_messages._parent_canvas.yview_moveto(1.0)


def lt_send():
    text = lt_entry.get().strip()
    if not text:
        return
    if lt_send_to_server(text):
        lt_add_message(lt_user["name"], text)
        lt_entry.delete(0, "end")
    else:
        lt_add_message("LogiTalk", "Не вдалося надіслати повідомлення")


lt_send_btn.configure(command=lt_send)
lt_entry.bind("<Return>", lambda e: lt_send())


lt_side = ctk.CTkFrame(lt_chat, width=190, corner_radius=0, fg_color="#1E2235")
lt_side.pack_propagate(False)
lt_side_open = {"value": False}

lt_avatar(lt_side, 70).pack(pady=(20, 10))
ctk.CTkButton(lt_side, text="Load image", width=140, fg_color="#374151", hover_color="#4B5563").pack(pady=5)
lt_side_name = ctk.CTkLabel(lt_side, text="", font=("Arial", 14, "bold"))
lt_side_name.pack(pady=(12, 5))
lt_side_entry = ctk.CTkEntry(lt_side, width=140, fg_color="#232638", border_color="#374151")
lt_side_entry.pack(pady=5)


def lt_save_name():
    name = lt_side_entry.get().strip()
    if name:
        lt_user["name"] = name
        lt_side_name.configure(text=name)
        lt_side_entry.delete(0, "end")


ctk.CTkButton(lt_side, text="Save name", width=140, fg_color="#3B82F6", hover_color="#2563EB", command=lt_save_name).pack(pady=5)

ctk.CTkButton(
    lt_side,
    text="⬅ У телефон",
    width=140,
    fg_color="#374151",
    hover_color="#4B5563",
    command=lambda: lt_exit()
).pack(side="bottom", pady=(5, 15))

ctk.CTkOptionMenu(
    lt_side,
    values=["Dark", "Light", "System"],
    width=140,
    fg_color="#374151",
    button_color="#4B5563",
    command=lambda v: switch_mode(v.lower())
).pack(side="bottom", pady=5)


def lt_toggle_side():
    if lt_side_open["value"]:
        lt_side.place_forget()
    else:
        lt_side.place(x=0, y=0, relheight=1)
        lt_side.lift()
    lt_side_open["value"] = not lt_side_open["value"]


lt_menu_btn.configure(command=lt_toggle_side)


def lt_show_chat():
    lt_reg.place_forget()
    lt_chat.place(relwidth=1, relheight=1)


def lt_exit():
    lt_disconnect()
    lt_toggle_side()
    lt_chat.place_forget()
    lt_reg.place(relwidth=1, relheight=1)
    for w in lt_messages.winfo_children():
        w.destroy()
    show_frame("home")



settings = ctk.CTkFrame(container, fg_color="#181824")
settings.place(relwidth=1, relheight=1)
frames["settings"] = settings

ctk.CTkLabel(settings, text="Налаштування", font=("Arial", 20, "bold"), text_color="#E0E6ED").pack(pady=25)


def switch_mode(mode):
    ctk.set_appearance_mode(mode)


ctk.CTkButton(settings, text="Світла тема", width=160, height=40, fg_color="#E5E7EB", text_color="#111827", hover_color="#D1D5DB", corner_radius=12, command=lambda: switch_mode("light")).pack(pady=10)
ctk.CTkButton(settings, text="Темна тема", width=160, height=40, fg_color="#374151", hover_color="#4B5563", corner_radius=12, command=lambda: switch_mode("dark")).pack(pady=10)
back_button(settings)

show_frame("home")


app.protocol("WM_DELETE_WINDOW", lambda: (lt_disconnect(), app.destroy()))
app.mainloop()