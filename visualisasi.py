import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Koneksi ke MongoDB
print("Menghubungkan ke MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
db = client["BigMart_Database"]
collection = db["sales_data"] # Kita ambil data mentah yang berisi 14rb baris

# 2. Ambil data dan jadikan Pandas DataFrame
data = list(collection.find())
if not data:
    print("❌ Data tidak ditemukan. Pastikan main_process.py sudah dijalankan sebelumnya.")
else:
    print("✅ Data berhasil ditarik! Memproses visualisasi...")
    df = pd.DataFrame(data)

    # Mengatur gaya background grafik ala Seaborn
    sns.set_theme(style="whitegrid")

    # 3. Setup Canvas (Dashboard) berukuran 2 Baris x 2 Kolom
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Analisis Eksploratif Big Data (EDA) - Big Mart Sales', fontsize=20, fontweight='bold')

    # ==========================================
    # GRAFIK 1: Histogram Distribusi Penjualan
    # (Mirip dengan grafik distplot di file PDF Kaggle)
    # ==========================================
    sns.histplot(df['Item_Outlet_Sales'], bins=50, kde=True, ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Distribusi Total Penjualan', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Item Outlet Sales (Nilai Penjualan)')
    axes[0, 0].set_ylabel('Frekuensi')

    # ==========================================
    # GRAFIK 2: Scatter Plot - Harga vs Penjualan
    # (Mirip dengan grafik titik-titik di PDF Kaggle)
    # ==========================================
    sns.scatterplot(x='Item_MRP', y='Item_Outlet_Sales', hue='Item_Fat_Content', 
                    alpha=0.6, data=df, ax=axes[0, 1], palette='Set1')
    axes[0, 1].set_title('Korelasi: Harga Barang (MRP) vs Penjualan', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Harga Maksimal Retail (Item_MRP)')
    axes[0, 1].set_ylabel('Total Penjualan')

    # ==========================================
    # GRAFIK 3: Boxplot - Sebaran Penjualan per Tipe Toko
    # ==========================================
    sns.boxplot(x='Outlet_Type', y='Item_Outlet_Sales', data=df, ax=axes[1, 0], palette='Set2')
    axes[1, 0].set_title('Sebaran Penjualan Berdasarkan Jenis Toko', fontsize=14, fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=15)
    axes[1, 0].set_xlabel('Tipe Toko')
    axes[1, 0].set_ylabel('Total Penjualan')

    # ==========================================
    # GRAFIK 4: Barplot - Rata-rata Penjualan per Tier Lokasi
    # ==========================================
    sns.barplot(x='Outlet_Location_Type', y='Item_Outlet_Sales', data=df, ax=axes[1, 1], palette='viridis')
    axes[1, 1].set_title('Rata-rata Penjualan per Tier Lokasi', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Tier Lokasi Kota')
    axes[1, 1].set_ylabel('Rata-rata Penjualan')

    # Merapikan jarak antar grafik agar tidak bertumpuk
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    print("✅ Menampilkan Dashboard...")
    plt.show()