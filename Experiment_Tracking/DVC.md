# DVC (Data Version Control): Reproducibilitas Berbasis Git

DVC adalah sistem kontrol versi sumber terbuka untuk proyek machine learning. Filosofi utamanya adalah memperluas Git, memungkinkan Anda untuk mengelola data besar, model, dan metrik dengan alur kerja yang sama seperti Anda mengelola kode.

**DVC bukan pengganti Git.** Ia bekerja *bersama* Git untuk memberikan solusi versioning yang lengkap.

---

## a. Arsitektur & Cara Kerja

DVC secara cerdas memisahkan metadata dari data besar.

![Arsitektur DVC](https://dvc.org/img/flow- DVC-git-files.png)

1.  **Git**: Melacak semua file kode dan file metadata `.dvc` yang kecil.
2.  **Pointer `.dvc`**: Ketika Anda menambahkan file besar (seperti `data.csv`) ke DVC, DVC menggantinya dengan file teks kecil (`data.csv.dvc`). File ini bertindak sebagai *pointer* ke data sebenarnya dan berisi hash unik dari konten data.
3.  **Cache DVC**: Data besar yang sebenarnya dipindahkan ke direktori tersembunyi `.dvc/cache`. Struktur ini dioptimalkan untuk efisiensi penyimpanan.
4.  **Remote Storage**: Anda dapat mengonfigurasi DVC untuk mendorong (*push*) cache ini ke penyimpanan jarak jauh seperti Google Drive, S3, GCS, atau server SSH Anda sendiri.

Alur kerja ini berarti repositori Git Anda tetap kecil dan cepat, sementara data besar Anda tetap di-versioning dan dapat diakses.

---

## b. Alur Kerja & Instrumentasi

Tidak seperti MLFlow atau TensorBoard, **DVC tidak memerlukan instrumentasi kode di dalam skrip pelatihan Anda**. Sebaliknya, Anda mendefinisikan alur kerja Anda dalam file `dvc.yaml`.

### Alur Kerja Dasar (Versioning Data)

1.  **Inisialisasi**: `dvc init` (membuat direktori `.dvc`)
2.  **Menambahkan Data**: `dvc add path/to/your/data.csv`
    -   Ini membuat `data.csv.dvc` dan menambahkan data ke cache.
3.  **Commit ke Git**: `git add data.csv.dvc .gitignore` dan `git commit`
4.  **Push Data (Opsional)**: `dvc push` (mengunggah cache ke remote storage)

### Alur Kerja Eksperimen

Anda mendefinisikan *stage* (tahapan) dalam file `dvc.yaml`. Setiap stage adalah langkah dalam pipeline Anda (misalnya, `preprocess`, `train`, `evaluate`).

**Contoh `dvc.yaml`:**
```yaml
stages:
  train:
    cmd: python train.py
    deps:
      - train.py
      - data/features.csv
    params:
      - n_estimators
      - max_depth
    outs:
      - model.pkl
    metrics:
      - metrics.json: 
          cache: false # Metrik adalah file kecil, tidak perlu di-cache DVC
```

-   `cmd`: Perintah yang akan dijalankan.
-   `deps`: Dependensi (file kode atau data). DVC akan menjalankan ulang stage ini jika dependensi berubah.
-   `params`: Hyperparameter yang dilacak dari file `params.yaml`.
-   `outs`: Output yang dihasilkan (model, file, dll.).
-   `metrics`: File metrik yang akan dilacak.

Untuk menjalankan pipeline, Anda menggunakan: `dvc exp run`

---

## c. Visualisasi & Perbandingan

DVC unggul dalam perbandingan berbasis teks di terminal, yang cepat dan efisien.

### Membandingkan Eksperimen

Perintah `dvc exp show` menampilkan tabel dari semua eksperimen yang telah Anda jalankan, lengkap dengan parameter dan metriknya.

![dvc exp show](https://dvc.org/img/exp-show-table.png)

### Melihat Perbedaan Metrik

Perintah `dvc metrics diff` memberikan perbandingan yang jelas antara metrik dari *workspace* Anda saat ini dengan commit Git sebelumnya.

```sh
$ dvc metrics diff
Path           Metric    HEAD      workspace    Change
metrics.json   accuracy  0.925     0.951        0.026
metrics.json   loss      0.153     0.101       -0.052
```

---

## d. Evaluasi Umum

-   **Kelebihan**:
    -   **Reproducibilitas Terbaik**: Dengan mem-versioning kode, data, parameter, dan metrik bersama-sama, DVC menjamin reproduktifitas yang sesungguhnya.
    -   **Berbasis Git**: Alur kerjanya terasa alami bagi siapa saja yang sudah terbiasa dengan Git.
    -   **Efisien**: Tidak menyimpan duplikat data. Bekerja dengan baik untuk file data yang sangat besar.
    -   **Agnostik Bahasa & Framework**: Karena bekerja di luar kode Anda, ini dapat digunakan dengan bahasa atau pustaka apa pun.

-   **Kekurangan**:
    -   **Kurva Pembelajaran**: Membutuhkan pemahaman tentang konsep Git dan DVC itu sendiri.
    -   **Kurang Visual**: Meskipun ada beberapa ekstensi untuk plot, kekuatan utamanya ada di terminal, bukan di dasbor web yang kaya seperti MLFlow atau TensorBoard.