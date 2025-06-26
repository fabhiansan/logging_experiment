# DVC Experiment Tracking

## a. Komponen/arsitektur sistem
DVC (Data Version Control) bekerja di atas Git. Arsitekturnya sederhana dan kuat:
- **Metadata di Git**: File `.dvc` kecil dan `dvc.yaml` disimpan di Git. File-file ini berisi informasi tentang cara mereproduksi data atau model, tetapi bukan data itu sendiri.
- **Cache DVC**: Data besar, model, atau artefak disimpan dalam direktori `.dvc/cache` (yang diabaikan oleh Git).
- **Remote Storage**: Cache dapat disinkronkan dengan penyimpanan jarak jauh seperti Google Drive, S3, atau server SSH.

## b. Cara setup instrumentasi/pencatatan eksperimen
1.  **Instalasi**: `pip install dvc`
2.  **Inisialisasi**: `dvc init` untuk menyiapkan struktur direktori DVC dalam repositori Git.
3.  **Mendefinisikan Metrik**: Dalam file `dvc.yaml`, Anda menentukan *path* ke file metrik (biasanya JSON, YAML, atau CSV) yang dihasilkan oleh skrip pelatihan Anda.

**Contoh `dvc.yaml`:**
```yaml
metrics:
  - metrics/simple_metrics.json
  - metrics/classification_metrics.json
```

**Contoh Skrip Pelatihan (Python):**
```python
import json

# Setelah pelatihan selesai
metrics = {"accuracy": 0.95, "loss": 0.12}

with open("metrics/classification_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)
```

## c. Metadata eksperimen yang dikumpulkan
- **Metrik**: Nilai apa pun yang disimpan dalam file metrik yang ditentukan di `dvc.yaml`.
- **Parameter**: Parameter yang relevan untuk setiap tahap dapat ditentukan dalam `dvc.yaml`, memungkinkan pelacakan perubahan konfigurasi.
- **Dependensi dan Output**: DVC melacak dependensi (kode, data) dan output (model, metrik) untuk setiap tahap, memastikan reproduktifitas penuh.

## d. Visualisasi/laporan/dashboard yang disediakan
Visualisasi DVC terutama berbasis **Command-Line Interface (CLI)**, yang membuatnya cepat dan efisien untuk perbandingan langsung di terminal.
- `dvc metrics show`: Menampilkan tabel metrik dari *run* terbaru.
- `dvc metrics diff`: Membandingkan metrik antara *workspace* saat ini dan commit Git terakhir (atau commit lainnya).
- `dvc plots show`: Dapat menghasilkan plot sederhana (misalnya, kurva presisi-recall) jika data plot didefinisikan.

## e. Evaluasi umum
- **Kelebihan**: Integrasi yang sangat erat dengan Git menjadikannya alat yang luar biasa untuk **reproduktifitas**. Sangat baik untuk versioning data dan model bersama kode. Perbandingan metrik di CLI sangat cepat dan efisien.
- **Kekurangan**: Kemampuan visualisasinya tidak sekaya MLFlow atau TensorBoard. DVC lebih fokus pada pelacakan dan versioning daripada analisis visual yang mendalam.