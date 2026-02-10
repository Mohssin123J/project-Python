import tkinter as tk
from tkinter import ttk, messagebox
import func

func.create_table()
func.add_admins_once()

ROOM_PRICES = {
    "Chambre Simple": 350,
    "Chambre Double": 550,
    "Suite": 850,
    "Chambre VIP": 1200
}


win = tk.Tk()
win.title("Hotel Atlas")
win.geometry("1000x750")
win.resizable(False, False)
BG = "#181515"
HEADER = "#ffe600"


frames = {}

def show_frame(name):
    frames[name].tkraise()

container = tk.Frame(win, bg=BG)
container.pack(fill="both", expand=True)


customer = tk.Frame(container, bg=BG)
tk.Label(customer, text="Hotel Atlas", font=("Arial Black", 24), bg=BG, fg=HEADER).pack()
check_frame = tk.Frame(container, bg=BG)
admin = tk.Frame(container, bg=BG)
admin_panel = tk.Frame(container, bg=BG)

for f in (customer, check_frame, admin, admin_panel):
    f.place(relwidth=1, relheight=1)

frames["customer"] = customer
frames["check"] = check_frame
frames["admin"] = admin
frames["admin_panel"] = admin_panel

def labeled_entry(parent, text):
    tk.Label(parent, text=text, bg=BG, fg=HEADER, font=("Arial Black", 11)).pack(anchor="w", padx=40)
    e = ttk.Entry(parent, width=45)
    e.pack(pady=3)
    return e

def date_picker(parent, title):
    box = tk.Frame(parent, bg=BG)
    box.pack(pady=6)
    tk.Label(box, text=title, bg=BG, fg=HEADER, font=("Arial Black", 11)).pack(anchor="w")
    row = tk.Frame(box, bg=BG)
    row.pack()

    years = [str(y) for y in range(2024, 2051)]
    months = [f"{m:02}" for m in range(1, 13)]
    days = [f"{d:02}" for d in range(1, 32)]

    y = ttk.Combobox(row, values=years, width=8, state="readonly")
    m = ttk.Combobox(row, values=months, width=6, state="readonly")
    d = ttk.Combobox(row, values=days, width=6, state="readonly")

    y.set("Année")
    m.set("Mois")
    d.set("Jour")

    y.pack(side="left", padx=4)
    m.pack(side="left", padx=4)
    d.pack(side="left", padx=4)

    return y, m, d

tk.Label(customer, text="Réservation Client", font=("Arial", 18, "bold"), bg=BG, fg=HEADER).pack(pady=10)

name_entry = labeled_entry(customer, "Nom Complet")
phone_entry = labeled_entry(customer, "Numéro de Téléphone")
nid_entry = labeled_entry(customer, "Numéro d'Identité")

tk.Label(customer, text="Type de Chambre", bg=BG, fg=HEADER, font=("Arial Black", 11)).pack(anchor="w", padx=40)
room_combo = ttk.Combobox(customer, values=list(ROOM_PRICES.keys()), state="readonly", width=42)
room_combo.pack(pady=3)

tk.Label(customer, text="Nombre de Chambres", bg=BG, fg=HEADER, font=("Arial Black", 11)).pack(anchor="w", padx=40)
rooms_spin = tk.Spinbox(customer, from_=1, to=10, width=10)
rooms_spin.pack(pady=3)

checkin_y, checkin_m, checkin_d = date_picker(customer, "Date d'Entrée")
checkout_y, checkout_m, checkout_d = date_picker(customer, "Date de Sortie")

def book_now():
    try:
        if not all([name_entry.get(), phone_entry.get(), nid_entry.get(), room_combo.get()]):
            messagebox.showerror("Erreur", "Veuillez remplir toutes les informations")
            return

        check_in = f"{checkin_y.get()}-{checkin_m.get()}-{checkin_d.get()}"
        check_out = f"{checkout_y.get()}-{checkout_m.get()}-{checkout_d.get()}"

        res_id, total_price = func.insert_reservation(
            name_entry.get(),
            phone_entry.get(),
            nid_entry.get(),
            room_combo.get(),
            int(rooms_spin.get()),
            check_in,
            check_out,
            ROOM_PRICES[room_combo.get()]
        )

        messagebox.showinfo(
            "Succès",
            f"Réservation confirmée\nNuméro: {res_id}\nTotal: {total_price} MAD"
        )
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

tk.Button(customer, text="Réserver Maintenant", command=book_now, bg=BG, fg=HEADER, font=("Arial Black", 11)).pack(pady=12)


tk.Label(check_frame, text="Vérification de Réservation", font=("Arial", 18, "bold"), bg=BG, fg=HEADER).pack(pady=20)

check_input = tk.Entry(check_frame, width=30, bg=HEADER)
check_input.pack(pady=5)

search_type = tk.StringVar(value="nid")
tk.Radiobutton(check_frame, text="Par Numéro d'Identité", variable=search_type, value="nid", bg=BG, fg=HEADER, selectcolor="black").pack()
tk.Radiobutton(check_frame, text="Par Numéro de Réservation", variable=search_type, value="id", bg=BG, fg=HEADER, selectcolor="black").pack()

result = tk.Label(check_frame, text="", bg=BG)
result.pack(pady=10)

def check_reservation():
    key = check_input.get().strip()
    if search_type.get() == "nid":
        data = func.get_reservation_by_nid(key)
    else:
        data = func.get_reservation_by_id(int(key)) if key.isdigit() else None

    if data:
        result.config(text=f"Réservation #{data[0]}\nNom: {data[1]}\nTotal: {data[9]} MAD", fg="green")
    else:
        result.config(text="Réservation introuvable", fg="red")

tk.Button(check_frame, text="Vérifier", command=check_reservation, fg=HEADER, bg=BG, font=("Arial Black", 11)).pack(pady=10)

tk.Label(admin, text="Connexion Administrateur", font=("Arial", 18, "bold"), fg=HEADER, bg=BG,).pack(pady=20)

tk.Label(admin, text="Nom d'utilisateur", bg=BG, fg=HEADER, font=("Arial Black", 11)).pack()
admin_user = tk.Entry(admin, width=30, bg=HEADER)
admin_user.pack(pady=5)

tk.Label(admin, text="Email", bg=BG, fg=HEADER, font=("Arial Black", 11)).pack()
admin_email = tk.Entry(admin, width=30, bg=HEADER)
admin_email.pack(pady=5)

tk.Label(admin, text="Mot de passe", bg=BG, fg=HEADER, font=("Arial Black", 11)).pack()
admin_pass = tk.Entry(admin, width=30, show="*", bg=HEADER)
admin_pass.pack(pady=5)

def admin_login():
    admin_data = func.check_admin_login(
        admin_user.get(),
        admin_email.get(),
        admin_pass.get()
    )
    if admin_data:
        load_data()
        show_frame("admin_panel")
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects")

tk.Button(admin, text="Se connecter", command=admin_login, fg=HEADER, bg=BG, font=("Arial Black", 11)).pack(pady=10)

tk.Label(admin_panel, text="Panneau Administrateur", font=("Arial", 18, "bold"), bg=BG, fg=HEADER).pack(pady=10)

columns = ("id","name","phone","nid","room","rooms","start","end","days","total")
tree = ttk.Treeview(admin_panel, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=90)

tree.pack(fill="both", expand=True, padx=10, pady=10)

def load_data():
    tree.delete(*tree.get_children())
    for row in func.get_all_reservations():
        tree.insert("", "end", values=row)

def delete_res():
    sel = tree.selection()
    if sel:
        func.delete_reservation(tree.item(sel)["values"][0])
        load_data()

tk.Button(admin_panel, text="Actualiser", command=load_data,bg=BG, fg=HEADER, font=("Arial Black", 11)).pack( padx=10)
tk.Button(admin_panel, text="Supprimer", command=delete_res,bg=BG, fg=HEADER, font=("Arial Black", 11)).pack( padx=10)

nav = tk.Frame(win, bg=HEADER)
nav.pack(side="bottom", fill="x")

tk.Button(nav, text="Réservation", command=lambda: show_frame("customer"), bg=BG, fg=HEADER, font=("Arial Black", 10)).pack(side="left", padx=20)
tk.Button(nav, text="Vérification", command=lambda: show_frame("check"), bg=BG, fg=HEADER, font=("Arial Black", 10)).pack(side="left", padx=20)
tk.Button(nav, text="Admin", command=lambda: show_frame("admin"), bg=BG, fg=HEADER, font=("Arial Black", 10)).pack(side="left", padx=20)

show_frame("customer")
win.mainloop()