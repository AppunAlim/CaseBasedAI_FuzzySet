import csv


def pelayanan_buruk(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / (60 - 40)
    else:
        return 0



def pelayanan_sedang(x):
    if 40 <= x <= 60:
        return (x - 40) / (60 - 40)
    elif 60 < x <= 80:
        return (80 - x) / (80 - 60)
    else:
        return 0



def pelayanan_baik(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / (80 - 60)
    else:
        return 1



def harga_murah(x):
    if x <= 30000:
        return 1
    elif 30000 < x < 40000:
        return (40000 - x) / (40000 - 30000)
    else:
        return 0



def harga_sedang(x):
    if 30000 <= x <= 40000:
        return (x - 30000) / (40000 - 30000)
    elif 40000 < x <= 50000:
        return (50000 - x) / (50000 - 40000)
    else:
        return 0



def harga_mahal(x):
    if x <= 40000:
        return 0
    elif 40000 < x < 50000:
        return (x - 40000) / (50000 - 40000)
    else:
        return 1




def inferensi_fuzzy(pelayanan, harga):
    # Fuzzification pelayanan
    buruk = pelayanan_buruk(pelayanan)
    sedang_pelayanan = pelayanan_sedang(pelayanan)
    baik = pelayanan_baik(pelayanan)

    # Fuzzification harga
    murah = harga_murah(harga)
    sedang_harga = harga_sedang(harga)
    mahal = harga_mahal(harga)

  

    # Kelayakan rendah
    r1 = min(sedang_pelayanan, mahal)
    r2 = min(buruk, sedang_harga)
    r3 = min(buruk, mahal)

    rendah = max(r1, r2, r3)

    # Kelayakan sedang
    r4 = min(baik, mahal)
    r5 = min(sedang_pelayanan, sedang_harga)
    r6 = min(buruk, murah)

    sedang = max(r4, r5, r6)

    # Kelayakan tinggi
    r7 = min(baik, murah)
    r8 = min(baik, sedang_harga)
    r9 = min(sedang_pelayanan, murah)

    tinggi = max(r7, r8, r9)

    

    pembilang = (rendah * 40) + (sedang * 70) + (tinggi * 100)
    penyebut = rendah + sedang + tinggi

    if penyebut == 0:
        return 0

    skor = pembilang / penyebut

    return skor


# =========================== MEMBACA DATA DARI FILE CSV =====================


def baca_data(nama_file):
    data_restoran = []

    with open(nama_file, mode='r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            restoran = {
                'id': int(row['id Pelanggan']),
                'pelayanan': int(row['Pelayanan']),
                'harga': float(row['harga'])
            }

            data_restoran.append(restoran)

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


