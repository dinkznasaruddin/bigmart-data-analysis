import kagglehub
import os
import pandas as pd

# 1. Download dataset Big Mart Sales
# Dataset ini adalah salah satu yang paling populer untuk latihan data processing
path = kagglehub.dataset_download("brijbhushannanda1979/bigmart-sales-data")

print("Lokasi folder:", path)

# 2. Daftar file di folder tersebut
files = os.listdir(path)
print("File yang ditemukan:", files)

# 3. Baca file train.csv (biasanya ini yang datanya paling lengkap)
train_file = os.path.join(path, 'Train.csv')

if os.path.exists(train_file):
    df = pd.read_csv(train_file)
    
    print("\n" + "="*30)
    print("HASIL PENGECEKAN DATASET")
    print("="*30)
    print(f"Jumlah Baris: {df.shape[0]}")
    print(f"Jumlah Kolom: {df.shape[1]}")
    print(f"Daftar Kolom: {df.columns.tolist()}")
    
    # Validasi kriteria tugas
    if df.shape[0] >= 15000:
        print("\n✅ Dataset memenuhi syarat (> 15.000 baris).")
    else:
        # Jika kurang, kita bisa menggabungkan dengan file Test.csv
        test_file = os.path.join(path, 'Test.csv')
        if os.path.exists(test_file):
            df_test = pd.read_csv(test_file)
            df_total = pd.concat([df, df_test])
            print(f"⚠️ Data Train saja hanya {len(df)} baris.")
            print(f"✅ Setelah digabung Train + Test: {len(df_total)} baris. (AMAN)")
            df = df_total # Gunakan yang sudah digabung
else:
    print("File Train.csv tidak ditemukan, pastikan nama filenya benar.")