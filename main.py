#!/usr/bin/env python3
"""
Skrip gabungan:
1. Memodifikasi file data.txt:
   - Membuat backup file asli (data.txt.bak) 📦
   - Menambahkan awalan "tma " pada setiap baris yang diawali dengan "user=" ✨
2. Menjalankan skrip utama untuk claim token 🚀.
"""

import shutil
import requests
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.text import Text
from datetime import datetime
import pytz
import logging
import concurrent.futures
import signal
import sys
from urllib.parse import unquote

# --- Fungsi Modifikasi File data.txt ---
def modify_data_file():
    """
    Memodifikasi file data.txt dengan menambahkan "tma " di awal baris
    yang dimulai dengan "user=".
    Membuat backup file asli sebagai data.txt.bak.
    """
    input_file = "data.txt"
    backup_file = "data.txt.bak"
    temp_file = "data_modified.txt"
    
    try:
        shutil.copyfile(input_file, backup_file)
    except Exception as e:
        print(f"❌ Error membuat backup file: {e}")
        sys.exit(1)
    
    with open(input_file, "r") as f_in, open(temp_file, "w") as f_out:
        for line in f_in:
            # Cek apakah baris (tanpa spasi di awal) dimulai dengan "user="
            if line.lstrip().startswith("user="):
                new_line = "tma " + line
            else:
                new_line = line
            f_out.write(new_line)
    
    # Ganti file asli dengan file yang telah dimodifikasi
    shutil.move(temp_file, input_file)
    print(f"✅ Modifikasi selesai. File asli dibackup sebagai '{backup_file}'. 😊")

# --- Konfigurasi Logging dan Console ---
logging.basicConfig(
    filename="claim_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console = Console()
tz = pytz.timezone("Europe/London")

# --- Banner Tampilan ---
red_lines = [
    "███╗   ███╗    █████╗     ███╗   ██╗    █████╗  ",
    "████╗ ████║   ██╔══██╗   ████╗  ██║   ██╔══██╗ ",
    "██╔████╔██║   ███████║   ██╔██╗ ██║   ███████║ "
]
white_lines = [
    "██║╚██╔╝██║   ██╔══██║   ██║╚██╗██║   ██╔══██║ ",
    "██║ ╚═╝ ██║   ██║  ██║   ██║ ╚████║   ██║  ██║ ",
    "╚═╝     ╚═╝   ╚═╝  ╚═╝   ╚═╝  ╚═══╝   ╚═╝  ╚═╝"
]
red_text = "[red]" + "\n".join(red_lines) + "[/red]"
white_text = "[white]" + "\n".join(white_lines) + "[/white]"
banner_text = red_text + "\n" + white_text
banner_aligned = Align.center(banner_text)
console.print(Panel(banner_aligned, border_style="green", title="[bold red]Spell Bot Claim Mana 🚀[/bold red]"))

# --- Fungsi-Fungsi Pendukung ---
def extract_username_from_token(token):
    """
    Mengekstrak username dari token yang telah di URL decode.
    Contoh: jika token mengandung substring "username":"NekoSakurako",
    fungsi ini akan mengembalikan "NekoSakurako".
    """
    decoded = unquote(token)
    marker = 'username":"'
    start = decoded.find(marker)
    if start == -1:
        return None
    start += len(marker)
    end = decoded.find('"', start)
    if end == -1:
        return None
    return decoded[start:end]

def validate_token(token):
    """
    Memvalidasi token dengan memanggil endpoint /user.
    Mengembalikan tuple (True, user_data) jika valid, atau (False, None) jika tidak.
    """
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': token,
        'origin': 'https://wallet.spell.club',
        'referer': 'https://wallet.spell.club/',
    }
    try:
        user_response = requests.get('https://wallet-api.spell.club/user', headers=headers, timeout=10)
        if user_response.status_code == 200:
            user_data = user_response.json()
            return True, user_data
        else:
            return False, None
    except Exception as e:
        logging.error(f"❌ Error validasi token: {e}")
        return False, None

def upgradeclaim(token, akunke, total_akun):
    """
    Melakukan proses claim dengan validasi token terlebih dahulu.
    Jika token valid, akan dilakukan request claim ke API.
    """
    is_valid, user_data = validate_token(token)
    if not is_valid:
        msg = (f"[{datetime.now(tz).strftime('%H:%M:%S')}] Akun [{akunke}/{total_akun}] "
               "=> Token tidak valid ❌. Melewati proses claim.")
        console.print(f"[bold red]{msg}[reset]")
        logging.warning(msg)
        return

    # Mengutamakan username dari respons user; jika tidak ada, diambil dari token.
    username = user_data.get('username') or user_data.get('name')
    if not username:
        username = extract_username_from_token(token)
    if not username:
        username = 'N/A'

    balance = user_data.get('balance', 0)
    msg_valid = (f"[{datetime.now(tz).strftime('%H:%M:%S')}] Akun [{akunke}/{total_akun}] "
                 f"=> Token valid untuk user: {username} 👍")
    console.print(f"[bold green]{msg_valid}[reset]")
    logging.info(msg_valid)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': token,
        'origin': 'https://wallet.spell.club',
        'referer': 'https://wallet.spell.club/',
    }
    params = {'batch_mode': 'true'}

    try:
        response = requests.post('https://wallet-api.spell.club/claim', params=params, headers=headers, timeout=10)
        retry_count = 0
        # Jika terjadi error 500, lakukan retry dengan exponential backoff
        while response.status_code == 500 and retry_count < 5:
            sleep_time = 2 ** (retry_count + 1)
            sleep(sleep_time)
            response = requests.post('https://wallet-api.spell.club/claim', params=params, headers=headers, timeout=10)
            retry_count += 1

        if response.status_code == 200:
            # Perbarui data user untuk mendapatkan informasi terbaru
            user_response = requests.get('https://wallet-api.spell.club/user', headers=headers, timeout=10)
            if user_response.status_code == 200:
                user_data = user_response.json()
                username = user_data.get('username') or user_data.get('name')
                if not username:
                    username = extract_username_from_token(token)
                if not username:
                    username = 'N/A'
                balance = user_data.get('balance', balance)
            else:
                balance = 0

            msg_success = (f"[{datetime.now(tz).strftime('%H:%M:%S')}] Akun [{akunke}/{total_akun}] "
                           f"=> Claim berhasil 🎉! Username: {username} | Balance: {balance / 1000000} MANA")
            console.print(f"[bold green]{msg_success}[reset]")
            logging.info(msg_success)
        else:
            try:
                error_msg = response.json().get('message', 'No message')
            except Exception:
                error_msg = "No message"
            msg_fail = (f"[{datetime.now(tz).strftime('%H:%M:%S')}] Akun [{akunke}/{total_akun}] "
                        f"=> Claim gagal ❌: {response.status_code} {error_msg}")
            console.print(f"[bold red]{msg_fail}[reset]")
            logging.error(msg_fail)
    except Exception as e:
        msg_exception = (f"[{datetime.now(tz).strftime('%H:%M:%S')}] Akun [{akunke}/{total_akun}] "
                         f"=> Exception ⚠️: {e}")
        console.print(f"[bold red]{msg_exception}[reset]")
        logging.exception(msg_exception)

def countdown(total_seconds):
    """
    Menampilkan hitungan mundur secara live menggunakan rich.live.
    Total waktu dihitung mundur dari total_seconds (dalam detik).
    """
    with Live(console=console, refresh_per_second=1) as live:
        for remaining in range(total_seconds, -1, -1):
            minutes = remaining // 60
            seconds = remaining % 60
            current_time = datetime.now(tz).strftime('%H:%M:%S')
            text = Text(f"[{current_time}] ⏳ Menunggu {minutes} menit {seconds} detik untuk claim lagi", style="bold blue")
            live.update(text)
            sleep(1)

def signal_handler(sig, frame):
    """
    Menangani sinyal untuk graceful shutdown.
    """
    msg = "👋 Graceful shutdown requested. Exiting..."
    console.print(f"[bold red]{msg}[reset]")
    logging.info(msg)
    sys.exit(0)

# Setup signal handling untuk graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- Eksekusi Awal: Modifikasi File data.txt ---
modify_data_file()

# Membaca token dari file data.txt (satu token per baris)
with open("data.txt", "r") as file:
    token_list = [line.strip() for line in file if line.strip()]

total_akun = len(token_list)

def main_loop():
    """
    Loop utama yang menjalankan proses claim secara berkala untuk tiap token.
    Setelah semua token diproses, akan ditampilkan countdown selama 6 jam (21600 detik).
    """
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i, token in enumerate(token_list, start=1):
                futures.append(executor.submit(upgradeclaim, token, i, total_akun))
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.exception(f"❌ Exception in thread: {e}")

        # Hitung mundur selama 6 jam (21600 detik)
        countdown(21600)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        msg = "👋 KeyboardInterrupt detected. Shutting down gracefully."
        console.print(f"[bold red]{msg}[reset]")
        logging.info(msg)
        sys.exit(0)
