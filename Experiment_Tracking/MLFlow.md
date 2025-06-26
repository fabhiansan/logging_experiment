# MLFlow Experiment Tracking

## a. Komponen/arsitektur sistem
MLFlow Tracking terdiri dari beberapa komponen utama:
- **Tracking Server**: Sebuah server (bisa lokal atau jarak jauh) yang mencatat semua informasi. Secara default, ia berjalan secara lokal dan menyimpan data di direktori `mlruns`.
- **Backend Store**: Tempat metadata seperti parameter dan metrik disimpan. Bisa berupa file lokal atau database seperti PostgreSQL.
- **Artifact Store**: Tempat file besar seperti model, plot, atau dataset disimpan. Bisa berupa direktori lokal (misalnya, di dalam `mlruns`) atau penyimpanan cloud seperti S3 atau GCS.
- **UI**: Antarmuka web untuk melihat, membandingkan, dan menganalisis hasil eksperimen.

## b. Cara setup instrumentasi/pencatatan eksperimen
1.  **Instalasi**: `pip install mlflow`
2.  **Memulai Eksperimen**: Eksperimen dicatat dalam sebuah *run* yang diawali dengan `mlflow.start_run()`.
3.  **Pencatatan**: 
    - `mlflow.log_param("nama_param", nilai)`: Mencatat parameter konfigurasi.
    - `mlflow.log_metric("nama_metrik", nilai, step=x)`: Mencatat metrik numerik. `step` bersifat opsional dan berguna untuk melacak metrik dari waktu ke waktu (misalnya, per epoch).
    - `mlflow.log_artifact("path/ke/file")`: Mencatat file (plot, model, dll.) sebagai artefak.

**Contoh Kode:**
```python
import mlflow

# Atur nama eksperimen
mlflow.set_experiment("My Experiment")

with mlflow.start_run(run_name="My First Run"):
    # Catat parameter
    mlflow.log_param("learning_rate", 0.01)

    # Catat metrik
    mlflow.log_metric("accuracy", 0.95)

    # Catat artefak (misalnya, file teks)
    with open("output.txt", "w") as f:
        f.write("Hello, MLFlow!")
    mlflow.log_artifact("output.txt", artifact_path="notes")
```

## c. Metadata eksperimen yang dikumpulkan
- **Parameter**: Pasangan kunci-nilai dari konfigurasi yang digunakan dalam *run* (misalnya, *learning rate*, ukuran *batch*).
- **Metrik**: Nilai numerik yang dapat berubah seiring waktu (misalnya, *loss*, *accuracy*).
- **Artefak**: File apa pun yang dihasilkan, seperti model yang telah dilatih, plot, atau file data.
- **Tag dan Catatan**: Metadata tambahan yang dapat diedit pengguna untuk mengatur dan mendeskripsikan *run*.
- **Source Code**: Referensi ke commit Git dari kode yang dijalankan untuk memastikan reproduktifitas.

## d. Visualisasi/laporan/dashboard yang disediakan
MLFlow UI menyediakan dasbor yang kuat untuk:
- **Melihat Daftar Eksperimen**: Semua eksperimen yang telah Anda jalankan.
- **Membandingkan Run**: Memilih beberapa *run* dan membandingkan parameter dan metrik mereka secara berdampingan dalam bentuk tabel dan plot.
- **Melihat Detail Run**: Melihat semua parameter, metrik (termasuk plot time-series), dan artefak untuk satu *run*.
- **Melihat Artefak**: Pratinjau atau mengunduh artefak yang disimpan.

## e. Evaluasi umum
- **Kelebihan**: Sangat baik untuk manajemen siklus hidup ML secara keseluruhan. Kemampuan untuk membandingkan puluhan *run* secara bersamaan adalah fitur utamanya. Terintegrasi dengan baik dengan banyak pustaka ML populer (fitur `autolog`).
- **Kekurangan**: Seperti yang kita alami, bisa sangat sensitif terhadap konfigurasi lingkungan eksekusi, yang terkadang menyebabkan error yang tidak terduga saat mencatat artefak jika *path* tidak dapat diakses.