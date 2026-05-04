import csv

def linear_up(x, a, b):
    if x <= a: return 0
    if x >= b: return 1
    return (x - a) / (b - a)

def linear_down(x, a, b):
    if x <= a: return 1
    if x >= b: return 0
    return (b - x) / (b - a)

def segitiga(x, a, b, c):
    if x <= a or x >= c: return 0
    if a < x <= b: return (x - a) / (b - a)
    if b < x < c: return (c - x) / (c - b)
    return 0

# setiap variabel func fuzzifikasi dipisah jadi lebih modular dan mudah dipahami
def fuzzify_pelayanan(x):
    return {
        'buruk': linear_down(x, 40, 60),
        'sedang': segitiga(x, 40, 60, 80),
        'baik': linear_up(x, 60, 80)
    }

def fuzzify_harga(x):
    return {
        'murah': linear_down(x, 30000, 40000),
        'sedang': segitiga(x, 30000, 40000, 50000),
        'mahal': linear_up(x, 40000, 50000)
    }

def inferensi_fuzzy(pelayanan_val, harga_val):
    p = fuzzify_pelayanan(pelayanan_val)
    h = fuzzify_harga(harga_val)

    # Aturan dikelompokin untuk setiap skor
    r_rendah = [
        min(p['sedang'], h['mahal']),
        min(p['buruk'], h['sedang']),
        min(p['buruk'], h['mahal'])
    ]
    skor_rendah = max(r_rendah)

    r_sedang = [
        min(p['baik'], h['mahal']),
        min(p['sedang'], h['sedang']),
        min(p['buruk'], h['murah'])
    ]
    skor_sedang = max(r_sedang)

    r_tinggi = [
        min(p['baik'], h['murah']),
        min(p['baik'], h['sedang']),
        min(p['sedang'], h['murah'])
    ]
    skor_tinggi = max(r_tinggi)

    # Defuzzification (Sugeno Style)
    pembilang = (skor_rendah * 40) + (skor_sedang * 70) + (skor_tinggi * 100)
    penyebut = skor_rendah + skor_sedang + skor_tinggi

    return pembilang / penyebut if penyebut != 0 else 0


# =========================== MEMBACA DATA DARI FILE CSV =====================


def baca_data(nama_file):
    data_restoran = []
    try:
        with open(nama_file, mode='r', encoding='utf-8-sig') as file: # utf-8-sig untuk handle BOM excel
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    data_restoran.append({
                        'id': int(row['id Pelanggan']),
                        'pelayanan': int(row['Pelayanan']),
                        'harga': float(row['harga'])
                    })
                except (ValueError, KeyError):
                    continue # Skip baris yang datanya cacat
    except FileNotFoundError:
        print(f"Error: File {nama_file} tidak ditemukan.")
    return data_restoran



# ===================== PROSES UTAMA PROGRAM ===========================


def proses_fuzzy(data_restoran):
    hasil = []

    for restoran in data_restoran:
        skor = inferensi_fuzzy(
            restoran['pelayanan'],
            restoran['harga']
        )

        hasil.append({
            'id': restoran['id'],
            'pelayanan': restoran['pelayanan'],
            'harga': restoran['harga'],
            'skor': round(skor, 2)
        })

    return hasil


# =================== MENYIMPAN OUTPUT KE FILE CSV ==========================


def simpan_hasil(data, nama_file):
    with open(nama_file, mode='w', newline='') as file:
        fieldnames = ['id', 'pelayanan', 'harga', 'skor']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            writer.writerow(item)


# ===================== MAIN PROGRAM =======================

# Nama file input
file_input = 'excel.csv'

# Nama file output
file_output = 'peringkat_restoran.csv'

# Membaca data restoran
restoran = baca_data(file_input)

# Memproses fuzzy logic
hasil_fuzzy = proses_fuzzy(restoran)

# Mengurutkan berdasarkan skor tertinggi
hasil_fuzzy.sort(key=lambda x: x['skor'], reverse=True)

# Mengambil 5 restoran terbaik
top_5 = hasil_fuzzy[:5]

# Menampilkan hasil
print('===== 5 RESTORAN TERBAIK =====')
print()

for i, restoran in enumerate(top_5, start=1):
    print(f"Peringkat {i}")
    print(f"ID Restoran : {restoran['id']}")
    print(f"Pelayanan   : {restoran['pelayanan']}")
    print(f"Harga       : {restoran['harga']}")
    print(f"Skor        : {restoran['skor']}")
    print('-----------------------------')

# Menyimpan hasil ke file CSV
simpan_hasil(top_5, file_output)

print()
print('Hasil berhasil disimpan ke file :', file_output)