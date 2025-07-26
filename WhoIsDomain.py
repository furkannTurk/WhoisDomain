import whois
import tkinter as tk
import socket

from datetime import datetime
from tkinter import ttk, messagebox


lang = "en"

texts = {
    "en": {
        "title": "Domain Whois Lookup",
        "select_language": "Select Language:",
        "query": "Query",
        "enter_domain": "Enter a domain name (e.g. google.com): ",
        "is_registered": "Is it registered: ",
        "yes": "Yes",
        "no": "No",
        "creation_date": "Creation Date: ",
        "expiration_date": "Expiration Date: ",
        "days_left": "Days until expiration: ",
        "registrar": "Registrar: ",
        "name_servers": "Name Servers: ",
        "private": "Is the credential private?: ",
        "error": "Error: ",
        "press_enter": "Press Enter to return to the menu...",
        "valid_domain": "Please enter a valid domain...",
        "date_notfound": "Expiration date not found.",
    },
    "tr": {
        "title": "Domain Whois Sorgulama",
        "select_language": "Dil Seçin:",
        "query": "Sorgula",
        "enter_domain": "Domain adını girin (örn. google.com): ",
        "is_registered": "Kayıtlı mı: ",
        "yes": "Evet",
        "no": "Hayır",
        "creation_date": "Kayıt Tarihi: ",
        "expiration_date": "Bitiş Tarihi: ",
        "days_left": "Kalan Gün Sayısı: ",
        "registrar": "Kayıt Eden: ",
        "name_servers": "Name Serverlar: ",
        "private": "Kimlik Bilgisi Gizli mi?: ",
        "error": "Hata: ",
        "press_enter": "Menüye dönmek için Enter'a basın...",
        "valid_domain": "Lütfen geçerli bir domain giriniz...",
        "date_notfound": "Bitiş tarihi bulunamadı.",
    }
}

def days_left(expiration_date):
    if not expiration_date:
        return texts[lang]["date_notfound"]

    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    if isinstance(expiration_date, str):
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                expiration_date = datetime.strptime(expiration_date, fmt)
                break
            except ValueError:
                continue
        else:
            return "?"

    now = datetime.now()
    diff = expiration_date - now

    if diff.days < 0:
        return texts[lang]["no"]
    else:
        return f"{diff.days}"
def format_date(date_obj):
    if not date_obj:
        return "N/A"
    # Eğer listeyse ilk elemanı al
    if isinstance(date_obj, list):
        date_obj = date_obj[0]
    # datetime objesini sadece YYYY-AA-GG olarak string yap
    return date_obj.strftime("%Y-%m-%d")
def sorgula(domain):
    try:
        w = whois.whois(domain)
        ip_address = "Not found"
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            pass

        result = ""
        result += f"{texts[lang]['is_registered']} {texts[lang]['yes'] if w.domain_name else texts[lang]['no']}\n"
        result += "\n"
        result += f"Ip: {ip_address}\n\n"
        result += f"{texts[lang]['creation_date']}{format_date(w.creation_date)}\n\n"
        result += f"{texts[lang]['expiration_date']}{format_date(w.expiration_date)}\n\n"
        result += f"{texts[lang]['days_left']}{days_left(w.expiration_date)}\n\n"
        result += f"{texts[lang]['registrar']}{w.registrar}\n\n"
        result += f"{texts[lang]['name_servers']}{w.name_servers}\n\n"
        result += f"{texts[lang]['private']}{texts[lang]['yes'] if w.status and 'clientTransferProhibited' in w.status else texts[lang]['no']}\n\n"
        return result
    except Exception as e:
        return f"{texts[lang]['error']} {e}"

# UI'dan çağrılır
def query_domain():
    domain = domain_entry.get()
    result_box.delete("1.0", tk.END)

    if not domain.strip():
        messagebox.showwarning("Warning", texts[lang]["valid_domain"])
        return

    result = sorgula(domain)
    result_box.insert(tk.END, result)

# Terminal için ayrı çalışabilir
def menu():
    domain = input(f"{texts[lang]['enter_domain']}")
    if domain == "":
        print(f"{texts[lang]['valid_domain']}")
        menu()
    else:
        result = sorgula(domain)
        print(result)
        input(f"{texts[lang]['press_enter']}")
        menu()

def change_language(event):
    global lang
    lang = lang_var.get()
    update_ui_texts()

def update_ui_texts():
    t = texts[lang]
    window.title(t["title"])
    lang_label.config(text=t["select_language"])
    domain_label.config(text=t["enter_domain"])
    query_button.config(text=t["query"])

# --- UI Kurulumu ---
window = tk.Tk()
window.title(texts[lang]["title"])
window.geometry("1000x600")  # Genişlik x Yükseklik
window.resizable(False, False)
window.configure(bg="#714329")#543200

lang_var = tk.StringVar(value=lang)
lang_label = tk.Label(window, text=texts[lang]["select_language"],bg="#B9937B")
lang_label.pack(pady=5)

lang_menu = ttk.Combobox(window, textvariable=lang_var, values=["en", "tr"], state="readonly")
lang_menu.bind("<<ComboboxSelected>>", change_language)
lang_menu.pack()

domain_label = tk.Label(window, text=texts[lang]["enter_domain"] ,bg="#B9937B")
domain_label.pack(pady=5)

domain_entry = tk.Entry(window, width=40)
domain_entry.pack()

query_button = tk.Button(window, text=texts[lang]["query"], command=query_domain, bg="#B9937B")
query_button.pack(pady=10)

title_font = ("Arial", 15, "bold")

result_box = tk.Text(window, height=17, width=60,bg="#B08463" ,fg="#FFFFFF", font=title_font)
result_box.pack(pady=10)

window.mainloop()

# İstersen terminali de çalıştır:
# menu()
