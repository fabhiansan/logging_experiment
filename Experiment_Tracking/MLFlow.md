# Laporan Analisis: Manajemen Siklus Hidup Machine Learning Menggunakan MLFlow

## 1. Pendahuluan

MLFlow adalah platform sumber terbuka yang dirancang untuk mengelola siklus hidup machine learning secara end-to-end. Platform ini menyediakan serangkaian alat terintegrasi untuk mengatasi tantangan dalam pelacakan eksperimen, reproduktifitas, deployment, dan manajemen model. MLFlow terdiri dari empat komponen utama: MLFlow Tracking, MLFlow Projects, MLFlow Models, dan MLFlow Model Registry. Dokumen ini menyajikan analisis mendalam mengenai setiap komponen dan kapabilitasnya.

---

## 2. Komponen 1: MLFlow Tracking

MLFlow Tracking adalah komponen inti yang berfungsi sebagai API dan antarmuka pengguna untuk mencatat dan memvisualisasikan data eksperimen.

-   **2.1. Arsitektur Sistem**: Arsitektur MLFlow Tracking dirancang untuk fleksibilitas, mendukung eksekusi lokal maupun terdistribusi.
    ![Diagram Arsitektur MLFlow](https://mlflow.org/docs/latest/_images/tracking-server.png)
    -   **Tracking Server**: Entitas pusat yang menerima dan menyimpan data eksperimen.
    -   **Backend Store**: Penyimpanan untuk metadata (parameter, metrik). Dapat berupa sistem file lokal atau database relasional (misalnya, PostgreSQL).
    -   **Artifact Store**: Penyimpanan untuk file besar (model, plot). Dapat berupa direktori lokal atau penyimpanan cloud (misalnya, S3, GCS).

-   **2.2. Implementasi Pencatatan**: MLFlow mendukung dua mode utama untuk instrumentasi kode:
    -   **Manual Logging**: Memberikan kontrol eksplisit kepada pengguna untuk mencatat data menggunakan API seperti `mlflow.log_param()`, `mlflow.log_metric()`, dan `mlflow.log_artifact()`.
    -   **Autologging**: Menyediakan fungsionalitas pencatatan otomatis untuk pustaka populer (misalnya, Scikit-learn, TensorFlow, PyTorch) dengan satu panggilan fungsi (`mlflow.sklearn.autolog()`), yang secara signifikan mengurangi kode boilerplate.

-   **2.3. Antarmuka Visualisasi**: Dasbor web interaktif (`mlflow ui`) adalah fitur sentral untuk analisis.
    -   **Tampilan Eksperimen**: Menyajikan tabel ringkasan dari semua *run*, yang dapat disortir dan difilter berdasarkan parameter dan metrik.
        ![Tampilan Daftar Run MLFlow](https://mlflow.org/docs/latest/_images/tracking-ui-page.png)
    -   **Fitur Perbandingan**: Memungkinkan perbandingan visual dari beberapa *run* untuk menganalisis dampak hyperparameter terhadap kinerja model.
        ![Tampilan Perbandingan Run MLFlow](https://mlflow.org/docs/latest/_images/parallel-coordinates-plot.png)

---

## 3. Komponen 2: MLFlow Projects

Komponen ini bertujuan untuk meningkatkan reproduktifitas dengan mengemas kode dalam format standar. Hal ini dicapai melalui file konfigurasi `MLproject` yang mendefinisikan dependensi (misalnya, file `conda.yaml`) dan titik masuk eksekusi.

**Contoh `MLproject`:**
```yaml
name: My Project
conda_env: conda.yaml
entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
    command: "python train.py --alpha {alpha}"
```
Eksekusi proyek dilakukan melalui perintah `mlflow run`.

---

## 4. Komponen 3 & 4: MLFlow Models dan Model Registry

Kedua komponen ini berfokus pada standardisasi dan manajemen siklus hidup model pasca-pelatihan.

-   **4.1. MLFlow Models**: Mendefinisikan format pengemasan standar ("flavor") yang memungkinkan model untuk digunakan di berbagai platform deployment (misalnya, sebagai fungsi Python, kontainer Docker, atau di Azure ML).

-   **4.2. MLFlow Model Registry**: Menyediakan repositori terpusat untuk versioning, staging, dan anotasi model.
    ![Siklus Hidup Model Registry](https://mlflow.org/docs/latest/_images/model-registry.png)
    Siklus hidup model di dalam registry umumnya meliputi tahap-tahap berikut: `Staging`, `Production`, dan `Archived`, yang memfasilitasi tata kelola model (governance) yang terstruktur.

---

## 5. Evaluasi dan Kesimpulan

-   **5.1. Keunggulan**:
    -   **Manajemen End-to-End**: Menyediakan solusi terintegrasi dari eksperimen hingga deployment.
    -   **Skalabilitas Perbandingan**: Sangat efektif untuk membandingkan sejumlah besar eksperimen.
    -   **Fleksibilitas**: Agnostik terhadap pustaka machine learning dan dapat di-deploy di berbagai lingkungan.

-   **5.2. Keterbatasan**:
    -   **Sensitivitas Lingkungan**: Fungsionalitas, terutama pencatatan artefak, dapat dipengaruhi oleh konfigurasi dan perizinan lingkungan eksekusi.
    -   **Visualisasi Pelatihan**: Meskipun mampu memplot metrik, tingkat interaktivitas untuk analisis dinamika pelatihan tidak sedalam yang ditawarkan oleh TensorBoard.