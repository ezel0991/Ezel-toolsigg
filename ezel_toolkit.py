
import os
import time
import socket
import requests
import platform
import pyfiglet
import subprocess
import hashlib
import qrcode
import psutil
from colorama import Fore, Style, init
from getpass import getpass

init(autoreset=True)

KULLANICI_ADI = "ezel"
SIFRE = "1234"

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def loading_bar():
    print(Fore.YELLOW + "Yükleniyor: ", end="")
    for _ in range(30):
        print(Fore.GREEN + "█", end="", flush=True)
        time.sleep(0.01)
    print(Fore.CYAN + " [Tamamlandı]")

def giris_ekrani():
    temizle()
    ascii_art = pyfiglet.figlet_format("LOGIN")
    print(Fore.CYAN + ascii_art)
    for _ in range(3):
        kullanici = input(Fore.YELLOW + "Kullanıcı Adı: ")
        sifre = getpass(Fore.YELLOW + "Şifre: ")
        if kullanici == KULLANICI_ADI and sifre == SIFRE:
            loading_bar()
            print(Fore.GREEN + "\nGiriş Başarılı. Hoşgeldin Ezel!")
            time.sleep(1)
            return True
        else:
            print(Fore.RED + "Hatalı giriş! Tekrar dene...\n")
            time.sleep(1)
    print(Fore.RED + "Çok fazla hatalı deneme. Çıkılıyor...")
    exit()

def banner():
    ascii_art = pyfiglet.figlet_format("EZEL TOOLKIT")
    print(Fore.GREEN + ascii_art)

def ip_konum():
    ip = input("IP Adresi (boş bırak kendi IP): ")
    if not ip:
        ip = requests.get("https://api64.ipify.org").text
    url = f"https://ipapi.co/{ip}/json/"
    data = requests.get(url).json()
    print(Fore.YELLOW + f"""
IP: {ip}
Ülke: {data.get('country_name')}
Şehir: {data.get('city')}
İnternet Sağlayıcı: {data.get('org')}
Saat Dilimi: {data.get('timezone')}
""")

def hava_durumu():
    sehir = input("Şehir: ")
    url = f"http://wttr.in/{sehir}?format=3"
    response = requests.get(url)
    print(Fore.CYAN + response.text)

def motivasyon_al():
    url = "https://api.quotable.io/random"
    veri = requests.get(url).json()
    print(Fore.MAGENTA + f'"{veri["content"]}"\n— {veri["author"]}')

def kripto_fiyat():
    kisa_ad = input("Kripto kodu (BTC, ETH...): ").lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={kisa_ad}&vs_currencies=usd"
    response = requests.get(url).json()
    fiyat = response.get(kisa_ad, {}).get("usd")
    if fiyat:
        print(Fore.GREEN + f"{kisa_ad.upper()} Fiyatı: ${fiyat}")
    else:
        print(Fore.RED + "Geçersiz kripto adı.")

def dunya_saati():
    ulke = input("Ülke/Şehir kodu (Europe/Istanbul): ")
    url = f"http://worldtimeapi.org/api/timezone/{ulke}"
    response = requests.get(url).json()
    if "datetime" in response:
        print(Fore.CYAN + f"Şimdiki zaman: {response['datetime']}")
    else:
        print(Fore.RED + "Zaman bilgisi alınamadı.")

def ping_test():
    hedef = input("Ping atılacak adres (ör: google.com): ")
    komut = ["ping", "-n" if os.name == "nt" else "-c", "4", hedef]
    sonuc = subprocess.run(komut, capture_output=True, text=True)
    print(Fore.GREEN + sonuc.stdout)

def traceroute():
    hedef = input("Traceroute yapılacak adres: ")
    komut = "tracert" if os.name == "nt" else "traceroute"
    sonuc = subprocess.run([komut, hedef], capture_output=True, text=True)
    print(Fore.YELLOW + sonuc.stdout)

def port_tarama():
    hedef = input("Hedef IP/Domain: ")
    print(Fore.CYAN + f"{hedef} adresindeki açık portlar taranıyor (1-1024)...\n")
    for port in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((hedef, port)) == 0:
            print(Fore.GREEN + f"Port {port} açık")
        s.close()

def sistem_bilgileri():
    print(Fore.CYAN + "Sistem Bilgileri:\n")
    print(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    print(f"İşlemci: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
    print(f"Uptime: {round(time.time() - psutil.boot_time()) // 60} dk")

def qr_olustur():
    veri = input("QR koduna dönüştürülecek metin/link: ")
    img = qrcode.make(veri)
    img.show()
    print(Fore.GREEN + "QR kod görseli açıldı.")

def sifrele():
    metin = input("Şifrelenecek veri: ")
    print("[1] MD5\n[2] SHA256")
    secim = input("Seçim: ")
    if secim == "1":
        print("MD5:", hashlib.md5(metin.encode()).hexdigest())
    elif secim == "2":
        print("SHA256:", hashlib.sha256(metin.encode()).hexdigest())
    else:
        print("Geçersiz seçim.")

def menu():
    while True:
        temizle()
        banner()
        print(Fore.BLUE + """
[1] IP'den Konum Bul
[2] Hava Durumu
[3] Motivasyon Sözü
[4] Kripto Fiyatı
[5] Dünya Saati
[6] Ping Testi
[7] Traceroute
[8] Port Taraması
[9] Sistem Bilgileri
[10] QR Kod Oluştur
[11] Şifreleme Aracı
[0] Çıkış
""" + Style.RESET_ALL)
        secim = input(Fore.WHITE + "Seçiminiz: " + Style.RESET_ALL)
        temizle()
        if secim == "1":
            ip_konum()
        elif secim == "2":
            hava_durumu()
        elif secim == "3":
            motivasyon_al()
        elif secim == "4":
            kripto_fiyat()
        elif secim == "5":
            dunya_saati()
        elif secim == "6":
            ping_test()
        elif secim == "7":
            traceroute()
        elif secim == "8":
            port_tarama()
        elif secim == "9":
            sistem_bilgileri()
        elif secim == "10":
            qr_olustur()
        elif secim == "11":
            sifrele()
        elif secim == "0":
            print(Fore.RED + "Çıkılıyor...")
            break
        else:
            print(Fore.RED + "Geçersiz seçim!")
        input(Fore.WHITE + "\nDevam etmek için Enter'a bas...")

if __name__ == "__main__":
    giris_ekrani()
    menu()
