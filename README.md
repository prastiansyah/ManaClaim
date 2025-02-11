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
1. **Pastikan Python 3 Terinstall**  
   Pastikan kamu menggunakan Python 3 di sistem kamu 🐍

2. **Instal Dependencies**  
   Jalankan perintah berikut untuk menginstal paket yang diperlukan:
   ```bash
   pip install -r requirements.txt
