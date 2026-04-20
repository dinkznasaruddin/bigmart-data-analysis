import kagglehub
import os
import pandas as pd
from pymongo import MongoClient
from pyspark.sql import SparkSession
# Menambahkan fungsi pembulatan (round)
from pyspark.sql.functions import col, sum as _sum, round as _round

# ==========================================
# 1. DOWNLOAD & MERGE ALL DATA
# ==========================================
print("Step 1: Mendownload dan menyiapkan data...")
path = kagglehub.dataset_download("brijbhushannanda1979/bigmart-sales-data")

df_train = pd.read_csv(os.path.join(path, 'Train.csv'))
df_test = pd.read_csv(os.path.join(path, 'Test.csv'))
df = pd.concat([df_train, df_test], ignore_index=True)

# CLEANING: Isi data penjualan kosong dengan 0
df['Item_Outlet_Sales'] = df['Item_Outlet_Sales'].fillna(0)
# CLEANING: Standarisasi Outlet_Type dan Location_Type jika ada yang kosong
df['Outlet_Type'] = df['Outlet_Type'].fillna('Unknown')
df['Outlet_Location_Type'] = df['Outlet_Location_Type'].fillna('Unknown')

print(f"✅ Data siap! Total baris: {len(df)}")

# ==========================================
# 2. STORAGE (NoSQL - MongoDB)
# ==========================================
print("\nStep 2: Mengunggah Data Mentah ke MongoDB...")
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["BigMart_Database"]
    
    # Simpan Data Mentah
    col_raw = db["sales_data"]
    col_raw.delete_many({}) 
    col_raw.insert_many(df.to_dict(orient='records'))
    print(f"✅ Tersimpan di 'sales_data': {col_raw.count_documents({})} dokumen.")
except Exception as e:
    print(f"❌ Error MongoDB: {e}")

# ==========================================
# 3. PROCESSING (MapReduce - PySpark)
# ==========================================
print("\nStep 3: Menjalankan Multi-MapReduce dengan Spark...")
spark = SparkSession.builder.appName("BigMartMultiAnalysis").config("spark.driver.bindAddress", "127.0.0.1").getOrCreate()
spark_df = spark.createDataFrame(df)

# --- MAPREDUCE 1: Berdasarkan Kategori Produk (Item_Type) ---
# Menggunakan _round untuk membulatkan 2 desimal
mr_item = spark_df.groupBy("Item_Type") \
    .agg(_round(_sum("Item_Outlet_Sales"), 2).alias("Total_Sales")) \
    .orderBy(col("Total_Sales").desc())

# --- MAPREDUCE 2: Berdasarkan Tipe Toko (Outlet_Type) ---
mr_outlet = spark_df.groupBy("Outlet_Type") \
    .agg(_round(_sum("Item_Outlet_Sales"), 2).alias("Total_Sales")) \
    .orderBy(col("Total_Sales").desc())

# --- MAPREDUCE 3: Berdasarkan Lokasi (Outlet_Location_Type) ---
mr_location = spark_df.groupBy("Outlet_Location_Type") \
    .agg(_round(_sum("Item_Outlet_Sales"), 2).alias("Total_Sales")) \
    .orderBy(col("Total_Sales").desc())

print("\n--- HASIL MR 2: PENJUALAN BERDASARKAN TIPE TOKO ---")
mr_outlet.show(truncate=False)

# ==========================================
# 4. SIMPAN HASIL KE NOSQL
# ==========================================
print("\nStep 4: Menyimpan semua hasil MapReduce ke MongoDB...")
try:
    # Simpan MR 1
    db["summary_item"].delete_many({})
    db["summary_item"].insert_many(mr_item.toPandas().to_dict(orient='records'))
    
    # Simpan MR 2
    db["summary_outlet"].delete_many({})
    db["summary_outlet"].insert_many(mr_outlet.toPandas().to_dict(orient='records'))
    
    # Simpan MR 3
    db["summary_location"].delete_many({})
    db["summary_location"].insert_many(mr_location.toPandas().to_dict(orient='records'))
    
    print("✅ Semua hasil ringkasan berhasil disimpan ke 3 koleksi berbeda!")
except Exception as e:
    print(f"❌ Error Simpan Hasil: {e}")

print("\n--- TUGAS SELESAI ---")