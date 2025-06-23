# MLflow: Detail untuk Pelacakan Eksperimen

MLflow adalah platform open-source untuk mengelola siklus hidup machine learning secara end-to-end.

## a. Komponen/Arsitektur Sistem

MLflow terdiri dari beberapa komponen utama:

1.  **MLflow Tracking**:
    *   **Tracking Server**: Sebuah server (bisa lokal atau jarak jauh) yang mencatat dan menyajikan metadata eksperimen.
    *   **Backend Store**: Tempat metadata eksperimen (parameter, metrik, tag, dll.) disimpan. Bisa berupa file lokal, database SQLAlchemy-compatible (seperti SQLite, PostgreSQL, MySQL), atau layanan Databricks.
    *   **Artifact Store**: Tempat artefak (file output, model, plot, data) disimpan. Bisa berupa direktori lokal, NFS, atau penyimpanan cloud seperti AWS S3, Azure Blob Storage, Google Cloud Storage.
    *   **UI (User Interface)**: Antarmuka web untuk melihat, mencari, dan membandingkan eksperimen dan run.
    *   **API & CLI**: Antarmuka pemrograman (Python, R, Java, REST) dan command-line untuk berinteraksi dengan MLflow.

2.  **MLflow Projects**: Format untuk mengemas kode data science secara reusable dan reproducible.
3.  **MLflow Models**: Format standar untuk mengemas model machine learning yang dapat digunakan di berbagai alat hilir.
4.  **MLflow Model Registry**: Repositori terpusat untuk mengelola siklus hidup model MLflow, termasuk versioning dan transisi tahap.

Untuk pelacakan eksperimen, fokus utama adalah pada komponen MLflow Tracking.

## b. Cara Setup Instrumentasi/Pencatatan Eksperimen

1.  **Instalasi**:
    ```bash
    pip install mlflow
    ```

2.  **Konfigurasi Tracking Server (Opsional, default lokal)**:
    *   Untuk pelacakan lokal, MLflow akan menyimpan data di direktori `mlruns` di direktori kerja Anda.
    *   Untuk server jarak jauh, Anda perlu mengatur `MLFLOW_TRACKING_URI` environment variable atau menggunakan `mlflow.set_tracking_uri("your-server-uri")` dalam kode.

3.  **Pencatatan dalam Kode Python**:
    *   **Memulai Run**:
        ```python
        import mlflow

        with mlflow.start_run(run_name="My Experiment Run") as run:
            # Kode eksperimen Anda di sini
            run_id = run.info.run_id
            experiment_id = run.info.experiment_id
            print(f"Run ID: {run_id}")
            # ... (lanjut ke pencatatan parameter, metrik, artefak)
        ```
    *   **Mencatat Parameter**:
        ```python
        mlflow.log_param("learning_rate", 0.01)
        mlflow.log_params({"epochs": 10, "batch_size": 32})
        ```
    *   **Mencatat Metrik**: Metrik dapat dicatat beberapa kali (misalnya, per epoch).
        ```python
        mlflow.log_metric("accuracy", 0.95)
        mlflow.log_metric("loss", 0.12, step=1) # 'step' untuk melacak metrik seiring waktu
        ```
    *   **Mencatat Artefak**: File apa pun (model, gambar, data).
        ```python
        # Mencatat file lokal
        mlflow.log_artifact("path/to/my_model.pkl", artifact_path="models")
        # Mencatat direktori
        mlflow.log_artifacts("path/to/output_images", artifact_path="images")
        ```
    *   **Mencatat Model (Flavors)**: MLflow memiliki "flavors" untuk berbagai library ML.
        ```python
        # Contoh dengan scikit-learn
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        # ... (training model)
        mlflow.sklearn.log_model(model, "sklearn-model")

        # Contoh dengan PyTorch
        # mlflow.pytorch.log_model(pytorch_model, "pytorch-model")
        ```
    *   **Mengatur Tag**:
        ```python
        mlflow.set_tag("data_version", "v2.1")
        ```

4.  **Menjalankan MLflow UI**:
    ```bash
    mlflow ui
    ```
    Secara default, UI akan berjalan di `http://localhost:5000`.

## c. Metadata Eksperimen yang Dikumpulkan

MLflow mengumpulkan berbagai metadata untuk setiap run:

*   **Run ID**: Pengidentifikasi unik untuk setiap run.
*   **Experiment ID**: Pengidentifikasi unik untuk eksperimen tempat run berada.
*   **Source Name**: Nama file atau proyek tempat run dijalankan.
*   **Source Version**: Commit hash Git jika dijalankan dari repositori Git.
*   **Entry Point**: Perintah atau fungsi yang dieksekusi.
*   **Start & End Time**: Waktu mulai dan selesai run.
*   **User ID**: Pengguna yang menjalankan eksperimen.
*   **Parameters**: Pasangan key-value dari parameter input.
*   **Metrics**: Pasangan key-value dari metrik output, bisa dengan histori (step).
*   **Artifacts**: File output apa pun yang disimpan (model, plot, file data). Lokasi URI ke artifact store.
*   **Tags**: Pasangan key-value tambahan untuk anotasi (misalnya, versi data, catatan kustom).
*   **Model Information**: Jika model dicatat, metadata spesifik model (misalnya, flavor, signature, environment).

## d. Visualisasi/Laporan/Dashboard yang Disediakan

MLflow UI menyediakan visualisasi dan laporan yang komprehensif:

*   **Daftar Eksperimen**: Menampilkan semua eksperimen yang dilacak.
*   **Tabel Run**: Untuk setiap eksperimen, menampilkan tabel run dengan kolom yang dapat disesuaikan (parameter, metrik). Memungkinkan sorting dan filtering.
*   **Halaman Detail Run**:
    *   Ringkasan parameter, metrik (nilai akhir).
    *   Plot interaktif untuk metrik yang dicatat dengan `step` (misalnya, kurva loss/accuracy).
    *   Browser artefak untuk melihat dan mengunduh artefak yang disimpan.
    *   Informasi model yang dicatat.
    *   Tag.
*   **Perbandingan Run**: Pilih beberapa run untuk membandingkan parameter dan metrik secara berdampingan. UI juga dapat membuat plot perbandingan untuk metrik.
*   **Pencarian**: Kemampuan untuk mencari run berdasarkan parameter, metrik, atau tag.
*   **Model Registry UI**: Jika digunakan, antarmuka untuk mengelola versi model, tahap, dan anotasi.

## e. Evaluasi Umum Perbandingan

*   **Kelebihan**:
    *   **Framework-agnostic**: Dapat digunakan dengan library ML apa pun dan bahasa pemrograman (Python, R, Java).
    *   **Komprehensif**: Mencakup pelacakan, proyek, model, dan registri model.
    *   **Reproducibility**: Membantu mereproduksi eksperimen dengan mencatat kode, parameter, dan dependensi.
    *   **Skalabilitas**: Dapat berjalan lokal atau dengan backend dan artifact store terpusat untuk tim.
    *   **UI yang Baik**: Antarmuka pengguna yang intuitif untuk eksplorasi dan perbandingan.
    *   **Open-source dan Komunitas Aktif**.
*   **Kekurangan**:
    *   Untuk proyek yang sangat sederhana, mungkin terasa sedikit berlebihan.
    *   Memerlukan server yang berjalan (bahkan `mlflow ui` adalah server) untuk melihat visualisasi, tidak seperti TensorBoard yang bisa membaca file log statis (meskipun TensorBoard juga menjalankan server).
    *   Manajemen dependensi untuk MLflow Projects bisa memerlukan perhatian ekstra.