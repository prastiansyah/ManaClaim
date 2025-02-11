# Spell Bot Claim Mana 🚀

Skrip ini menggabungkan dua fungsi utama:
1. **Modifikasi File `data.txt`**  
   - Membuat backup file asli sebagai `data.txt.bak` ✅  
   - Menambahkan awalan `tma ` pada setiap baris yang diawali dengan `user=`
2. **Proses Claim Token Otomatis**  
   - Melakukan validasi token sebelum melakukan claim token melalui API Spell Club  
   - Menampilkan status dan informasi token secara interaktif dengan [rich](https://github.com/Textualize/rich) 🌟  
   - Menjalankan proses claim secara paralel menggunakan multi-threading ⚡  
   - Menampilkan hitungan mundur sebelum claim berikutnya ⏳  

## Fitur Utama
- **Backup Otomatis:** File asli `data.txt` akan di-backup menjadi `data.txt.bak` 📦
- **Validasi Token:** Token dicek validitasnya sebelum melakukan claim 🚦
- **Interaksi yang Keren:** Tampilan interaktif dengan rich, termasuk banner dan live countdown 😃
- **Multi-threading:** Proses claim untuk beberapa token dilakukan secara paralel untuk mempercepat eksekusi 🔥
- **Logging:** Setiap aktivitas dan error akan dicatat di file `claim_log.log` 📜

## Cara Penggunaan
1. **Pastikan Python Terinstall**  
   Pastikan kamu menggunakan Python di sistem kamu 🐍

2. **Instal Dependencies**  
   Jalankan perintah berikut untuk menginstal paket yang diperlukan:
   ```bash
   pip install -r requirements.txt
3. Siapkan File Token
   Buat file data.txt di direktori yang sama dengan skrip.
   Masukkan token (satu token per baris) ke dalam file tersebut 📄
4. Jalankan Skrip
   Jalankan skrip menggunakan:
   ```bash
    python bot.py
6. Nikmati Otomatisasi Claim Token! 😎

## Konfigurasi
   File Token: data.txt
   Backup File: data.txt.bak
   Log: claim_log.log
## Dependencies
   requests 📡
   rich 🌈
   pytz ⏰

## Kontribusi
   Kontribusi dan saran sangat kami sambut! Jangan ragu untuk fork repository ini dan mengajukan pull request jika kamu memiliki perbaikan atau fitur baru 😊
