# BigMart Sales Big Data Analysis

 iProject big data untuk melakukan analisis data penjualan BigMart menggunakan teknologi NoSQL (MongoDB) dan distributed computing (Apache Spark).

## 📋 Daftar Isi
- [Deskripsi Project](#deskripsi-project)
- [Struktur Project](#struktur-project)
- [Requirements](#requirements)
- [Instalasi](#instalasi)
- [Cara Menggunakan](#cara-menggunakan)
- [Pipeline Data](#pipeline-data)
- [Output](#output)

## 🎯 Deskripsi Project

Project ini memproses dataset BigMart Sales (14,000+ baris data penjualan) menggunakan:
- **Data Collection**: Download dataset dari Kaggle
- **Data Storage**: Penyimpanan ke MongoDB (NoSQL database)
- **Data Processing**: MapReduce operations menggunakan Apache Spark
- **Data Visualization**: Exploratory Data Analysis (EDA) dengan matplotlib & seaborn

Dataset berisi informasi tentang penjualan produk di berbagai outlet dengan atribut seperti harga, tipe item, lokasi toko, dan total penjualan.

## 📁 Struktur Project

```
tugas2-bigdata/
├── downlod-kaggle.py      # Script untuk download dataset dari Kaggle
├── main.py                # Script untuk ETL & MapReduce processing
├── visualisasi.py         # Script untuk membuat visualisasi data
└── README.md             # Dokumentasi project (file ini)
```

### File-file Penting

| File | Fungsi |
|------|--------|
| `downlod-kaggle.py` | Mengunduh BigMart Sales dataset dari Kaggle kagglehub API |
| `main.py` | Melakukan data cleaning, penyimpanan ke MongoDB, dan MapReduce analysis menggunakan Spark |
| `visualisasi.py` | Membuat 4 visualisasi EDA (Histogram, Scatter Plot, Boxplot, Bar Chart) |

## 📦 Requirements

- Python 3.8+
- Jupyter Notebook (opsional, untuk development)
- Teknologi yang digunakan:
  - **kagglehub**: Download dataset dari Kaggle
  - **pandas**: Data manipulation & processing
  - **pyspark**: Distributed computing & MapReduce
  - **pymongo**: Koneksi ke MongoDB
  - **matplotlib & seaborn**: Visualisasi data

## 🔧 Instalasi

### 1. Clone/Setup Project
```bash
cd tugas2-bigdata
```

### 2. Install Python Dependencies
```bash
pip install kagglehub pandas pyspark pymongo matplotlib seaborn
```

### 3. Setup Kaggle API (Jika belum ada)
- Buat akun di [Kaggle.com](https://kaggle.com)
- Download file `kaggle.json` dari settings akun Anda
- Letakkan file tersebut di: `~/.kaggle/kaggle.json`
- Set permission: `chmod 600 ~/.kaggle/kaggle.json` (Linux/Mac)

### 4. Setup MongoDB
Pastikan MongoDB berjalan di `localhost:27017`:

**Option A: Menggunakan Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: Local MongoDB Installation**
- Install MongoDB dari [mongodb.com](https://www.mongodb.com/try/download/community)
- Jalankan MongoDB service

## 🚀 Cara Menggunakan

### Step 1: Verify Dataset (Opsional)
Untuk mengecek apakah dataset memenuhi syarat (>15,000 baris):
```bash
python3 downlod-kaggle.py
```

**Output yang diharapkan:**
```
✅ Dataset memenuhi syarat (> 15.000 baris).
```

### Step 2: Download & Process Data
Jalankan script utama untuk ETL dan MapReduce:
```bash
python3 main.py
```

**Proses yang terjadi:**
1. Download dataset BigMart Sales dari Kaggle
2. Merge file Train.csv dan Test.csv
3. Data cleaning (missing values)
4. Simpan data mentah ke MongoDB
5. Jalankan 4 MapReduce operations menggunakan Spark:
   - Penjualan berdasarkan Item Type
   - Penjualan berdasarkan Outlet Type
   - Penjualan berdasarkan Location Type
   - Top 10 Item dengan penjualan tertinggi

### Step 3: Visualisasi Data
Buat EDA visualizations dari data yang sudah diproses:
```bash
python3 visualisasi.py
```

**Output:**
- Dashboard dengan 4 grafik:
  1. **Histogram**: Distribusi total penjualan
  2. **Scatter Plot**: Korelasi harga vs penjualan
  3. **Boxplot**: Sebaran penjualan per jenis toko
  4. **Bar Chart**: Penjualan berdasarkan lokasi toko

## 🔄 Pipeline Data

```
┌─────────────────────────────────────────────────────────────────┐
│                    BIGMART SALES ANALYSIS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  downlod-kaggle.py    main.py               visualisasi.py      │
│  ┌────────────────┐   ┌─────────────────┐   ┌──────────────┐    │
│  │ Download from  │   │ ETL & MapReduce │   │ Visualisasi  │    │
│  │ Kaggle API     │──▶│ with Spark      │──▶│ & Dashboard  │    │
│  │                │   │ + MongoDB Store │   │              │    │
│  └────────────────┘   └─────────────────┘   └──────────────┘    │
│                                                                 │
│  Dataset: BigMart Sales (14,000+ rows)                          │
│  Output: Analysis reports & Visualization                       │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Output

### Data dalam MongoDB
Koleksi `sales_data` berisi dokumen-dokumen dengan struktur:
```json
{
  "_id": ObjectId,
  "Item_Identifier": "FDA15",
  "Item_Weight": 9.3,
  "Item_Fat_Content": "Low Fat",
  "Item_Type": "Dairy",
  "Item_MRP": 249.8,
  "Outlet_Identifier": "OUT049",
  "Outlet_Establishment_Year": 1999,
  "Outlet_Size": "Medium",
  "Outlet_Location_Type": "Tier 1",
  "Outlet_Type": "Supermarket Type1",
  "Item_Outlet_Sales": 3735.138
}
```

### Analisis MapReduce
Hasil dari 4 MapReduce operations disimpan dalam koleksi terpisah:
- `analysis_by_item_type`: Aggregasi penjualan per kategori produk
- `analysis_by_outlet_type`: Aggregasi penjualan per jenis toko
- `analysis_by_location`: Aggregasi penjualan per lokasi
- `top_items`: Top 10 produk dengan penjualan tertinggi

### Visualisasi
File output grafik berupa file PNG atau ditampilkan secara interaktif.

## 🐛 Troubleshooting

### Error: "MongoDB connection refused"
- Pastikan MongoDB service sudah berjalan
- Cek dengan: `mongosh` atau `mongo`

### Error: "Kaggle API not found"
- Pastikan `kaggle.json` sudah di-setup di `~/.kaggle/`
- Jalankan ulang script

### Error: "Spark not found"
- Install PySpark: `pip install pyspark`
- Pastikan Java sudah installed (Spark memerlukan Java)

### Error: "No module named 'pymongo'"
- Install PyMongo: `pip install pymongo`

## 📝 Catatan Penting

- Dataset akan diunduh dari Kaggle secara otomatis
- Folder cache Kaggle biasanya di `~/.cache/kagglehub/`
- MongoDB harus berjalan untuk menyimpan dan membaca data
- Spark membutuhkan memory yang cukup; jika error heap memory, jalankan dengan:
  ```bash
  SPARK_LOCAL_IP=127.0.0.1 python3 main.py
  ```
  
**Last Updated**: April 2026
