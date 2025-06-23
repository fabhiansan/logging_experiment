# DVC (Data Version Control): Detail untuk Pelacakan Eksperimen

DVC adalah alat open-source untuk versioning data, pipeline machine learning, dan eksperimen, yang bekerja di atas Git.

## a. Komponen/Arsitektur Sistem

1.  **Integrasi Git**: DVC tidak menggantikan Git, tetapi melengkapinya. Kode, konfigurasi DVC, dan *metafile* disimpan di Git.
2.  **`.dvc` Metafiles**: File kecil berformat YAML yang disimpan di Git. Metafile ini berisi informasi tentang file data atau direktori yang dilacak DVC, termasuk:
    *   Hash MD5 dari konten file/direktori.
    *   Lokasi file dalam cache DVC.
    *   Informasi remote (jika data disimpan di penyimpanan jarak jauh).
3.  **Cache DVC (`.dvc/cache`)**:
    *   Direktori lokal (biasanya di dalam proyek, dan di-gitignore) tempat DVC menyimpan salinan konten file data yang dilacak.
    *   Struktur berbasis konten (content-addressable storage), artinya file dengan konten yang sama hanya disimpan sekali.
    *   Memungkinkan checkout versi data yang berbeda dengan cepat tanpa mengunduh ulang jika sudah ada di cache.
4.  **Remote Storage**: Lokasi untuk menyimpan data besar yang tidak ingin dimasukkan ke Git. DVC mendukung berbagai jenis remote:
    *   Lokal (direktori lain di sistem file).
    *   Cloud: AWS S3, Google Cloud Storage, Azure Blob Storage, Alibaba Cloud OSS.
    *   Jaringan: SSH, HDFS, HTTP.
5.  **`dvc.yaml`**: File utama untuk mendefinisikan pipeline ML.
    *   Mendefinisikan **stages** (tahapan) dalam pipeline.
    *   Setiap stage memiliki:
        *   `cmd`: Perintah yang akan dijalankan.
        *   `deps`: Dependensi (file kode, file data yang dilacak DVC, parameter).
        *   `outs`: Output (file data yang dilacak DVC, metrik, plot).
        *   `params`: Parameter yang dilacak dari file `params.yaml` atau file lain.
        *   `metrics`: File yang berisi metrik (misalnya, JSON, CSV).
        *   `plots`: File yang berisi data untuk plot (misalnya, JSON, CSV, gambar).
6.  **`dvc.lock`**: File yang dihasilkan DVC untuk mengunci versi dependensi dan output setiap stage, memastikan reproduktifitas.
7.  **`params.yaml` (Konvensi)**: File untuk menyimpan parameter eksperimen.
8.  **DVC Experiments**: Fitur untuk menjalankan, melacak, dan membandingkan variasi eksperimen (perubahan kode, data, atau parameter) tanpa harus membuat banyak cabang Git secara manual.

## b. Cara Setup Instrumentasi/Pencatatan Eksperimen

1.  **Instalasi**:
    ```bash
    pip install dvc dvc[s3] # Contoh jika menggunakan S3 sebagai remote, sesuaikan dengan remote Anda
    ```

2.  **Inisialisasi Proyek**:
    *   Pastikan Anda berada dalam repositori Git.
    *   Inisialisasi DVC:
        ```bash
        dvc init
        git commit -m "Initialize DVC" # Commit file konfigurasi DVC
        ```

3.  **Melacak Data**:
    ```bash
    dvc add path/to/your/data.csv
    git add path/to/your/data.csv.dvc .gitignore # .gitignore akan otomatis diupdate oleh dvc add
    git commit -m "Add raw data"
    ```

4.  **Mengatur Remote Storage (Opsional, tapi direkomendasikan untuk data besar/kolaborasi)**:
    ```bash
    dvc remote add -d myremote s3://my-bucket/my-project-data # -d untuk default remote
    git add .dvc/config
    git commit -m "Configure S3 remote"
    dvc push # Mengunggah data ke remote
    ```

5.  **Mendefinisikan Pipeline (`dvc.yaml`)**:
    *   Buat file `params.yaml` (contoh):
        ```yaml
        # params.yaml
        featurize:
          max_features: 5000
        train:
          n_estimators: 100
          learning_rate: 0.1
        ```
    *   Buat stage dalam `dvc.yaml` (misalnya, `dvc stage add ...` atau edit manual):
        ```yaml
        # dvc.yaml
        stages:
          process_data:
            cmd: python src/process_data.py data/raw.csv data/processed.csv
            deps:
              - src/process_data.py
              - data/raw.csv
            outs:
              - data/processed.csv
          train_model:
            cmd: python src/train.py data/processed.csv model.pkl --lr ${train.learning_rate}
            deps:
              - src/train.py
              - data/processed.csv
              - params.yaml: # Melacak parameter spesifik
                - train.learning_rate
            params:
              - train.learning_rate # Membuat parameter tersedia untuk substitusi ${}
            outs:
              - model.pkl
            metrics:
              - metrics.json: # File metrik yang dihasilkan skrip train.py
                  cache: false # Biasanya metrik tidak perlu di-cache DVC
        ```
    *   Jalankan pipeline: `dvc repro`
    *   Commit perubahan: `git add dvc.yaml dvc.lock metrics.json params.yaml && git commit -m "Define and run pipeline"`

6.  **Melacak Eksperimen (`dvc exp`)**:
    *   Jalankan eksperimen dengan variasi:
        ```bash
        dvc exp run --set-param train.n_estimators=200 # Menjalankan dengan parameter berbeda
        dvc exp run --queue --set-param train.learning_rate=0.05 # Menambahkan ke antrian
        dvc exp run --all # Menjalankan semua eksperimen dalam antrian
        ```
    *   Tampilkan hasil eksperimen:
        ```bash
        dvc exp show
        ```
        Ini akan menampilkan tabel parameter dan metrik untuk setiap eksperimen.
    *   Terapkan eksperimen terbaik ke workspace:
        ```bash
        dvc exp apply <experiment_id>
        git commit -m "Apply best experiment <experiment_id>"
        ```

7.  **DVCLive (Untuk logging metrik/parameter secara live dari Python)**:
    *   Instalasi: `pip install dvclive`
    *   Dalam kode Python:
        ```python
        from dvclive import Live

        with Live() as live:
            # ... (training loop)
            live.log_param("learning_rate", lr)
            live.log_metric("accuracy", acc, step=epoch)
            live.log_artifact("model.pt")
            # Gambar dan plot juga bisa dicatat
            live.log_image("roc_curve.png", "plots/roc.png")
            live.next_step() # Pindah ke step berikutnya jika dalam loop
        ```
    *   DVCLive akan membuat file metrik/parameter yang dapat dilacak oleh DVC.

## c. Metadata Eksperimen yang Dikumpulkan

DVC, terutama dengan `dvc exp`, mengumpulkan:

*   **Versi Kode**: Commit Git yang terkait dengan setiap eksperimen.
*   **Versi Data**: Hash dari data input yang digunakan (melalui file `.dvc`).
*   **Parameter**: Nilai parameter yang digunakan, biasanya dari `params.yaml` atau di-override melalui `dvc exp run`.
*   **Metrik**: Nilai metrik yang dihasilkan oleh pipeline, dari file metrik (misalnya, `metrics.json`).
*   **Artefak Output**: Versi dari file output (model, data yang diproses) yang dilacak DVC.
*   **Definisi Pipeline**: Struktur `dvc.yaml` dan `dvc.lock` yang mendefinisikan bagaimana eksperimen dijalankan.
*   **Plot**: Data untuk plot (misalnya, kurva presisi-recall, matriks kebingungan) yang dapat dirender oleh `dvc plots show`.
*   **Timestamp dan Nama Eksperimen**: DVC menghasilkan nama unik untuk setiap eksperimen dan mencatat kapan dijalankan.

## d. Visualisasi/Laporan/Dashboard yang Disediakan

DVC berfokus pada antarmuka command-line untuk sebagian besar visualisasi dan laporan:

*   **`dvc exp show`**: Menampilkan tabel di terminal yang membandingkan parameter dan metrik antar eksperimen.
*   **`dvc metrics show`**: Menampilkan metrik dari berbagai commit/eksperimen.
*   **`dvc params diff`**: Menunjukkan perbedaan parameter antar commit/eksperimen.
*   **`dvc plots show`**: Merender plot dari data yang disimpan (misalnya, file JSON/CSV/TSV yang berisi data untuk plot). Dapat menghasilkan file HTML statis atau menampilkan plot di editor (jika terintegrasi). Mendukung template Vega-Lite.
*   **DVC Studio**: Produk terpisah dari Iterative.ai yang menyediakan UI web untuk memvisualisasikan dan mengelola proyek DVC, termasuk eksperimen, data, dan model. Ini adalah tambahan, bukan bagian inti dari DVC open-source.
*   **Ekstensi VS Code**: Menyediakan beberapa integrasi UI untuk DVC di dalam editor.

## e. Evaluasi Umum Perbandingan

*   **Kelebihan**:
    *   **Versioning Data dan Pipeline yang Kuat**: Ini adalah kekuatan utama DVC. Sangat baik untuk reproduktifitas.
    *   **Integrasi Git yang Mulus**: Menggunakan alur kerja Git yang sudah dikenal.
    *   **Language/Framework Agnostic**: Dapat digunakan dengan skrip atau alat apa pun.
    *   **Manajemen Eksperimen yang Efisien**: `dvc exp` memungkinkan iterasi cepat tanpa mengotori histori Git.
    *   **Skalabilitas Penyimpanan**: Data besar disimpan di remote, bukan di Git.
    *   **DVCLive**: Memudahkan logging metrik dan parameter secara real-time.
*   **Kekurangan**:
    *   **Kurva Belajar yang Lebih Curam**: Memahami konsep DVC dan bagaimana ia berinteraksi dengan Git memerlukan waktu.
    *   **Visualisasi Bawaan Terbatas**: UI bawaan tidak sekaya MLflow atau TensorBoard untuk eksplorasi metrik interaktif. `dvc plots` bagus tapi memerlukan setup template plot. DVC Studio mengatasi ini tetapi merupakan produk terpisah.
    *   Lebih fokus pada *reproduktifitas pipeline dan versioning* daripada *eksplorasi visual mendalam* dari metrik training secara real-time seperti TensorBoard.
    *   Setup awal bisa lebih terlibat dibandingkan hanya menambahkan beberapa baris `mlflow.log_metric`.