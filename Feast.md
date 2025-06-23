# Feast (Feature Store for AI/ML)

Feast adalah feature store open-source yang dirancang untuk menyederhanakan dan menstandardisasi cara fitur machine learning didefinisikan, disimpan, ditemukan, dan disajikan. Tujuannya adalah untuk memungkinkan tim ML membangun dan menerapkan model ke produksi lebih cepat dan lebih andal. Feast berfokus pada penyediaan antarmuka yang konsisten untuk mengakses fitur baik untuk training model (offline) maupun untuk inferensi (online).

Fitur dan konsep utama dalam Feast meliputi:

1.  **Definisi Fitur Terpusat (Feature Repository)**:
    *   Pengguna mendefinisikan objek-objek Feast seperti `Entity`, `FeatureView`, dan `DataSource` menggunakan kode Python dalam sebuah repositori Feast. Repositori ini bertindak sebagai satu sumber kebenaran (single source of truth) untuk definisi fitur.
    *   `Entity`: Merepresentasikan objek bisnis inti yang menjadi subjek prediksi (misalnya, pelanggan, driver, produk).
    *   `DataSource`: Menunjuk ke sumber data mentah tempat nilai fitur dapat ditemukan (misalnya, tabel di data warehouse, file Parquet di cloud storage, atau stream data).
    *   `FeatureView`: Mendefinisikan sekumpulan fitur yang logis dan bagaimana mereka terkait dengan entitas dan sumber data. `FeatureView` dapat mencakup transformasi sederhana atau merujuk pada fitur yang sudah ada.

2.  **Penyimpanan Offline (Offline Store)**:
    *   Digunakan untuk menyimpan data fitur historis dalam volume besar, yang biasanya diperlukan untuk training model atau analisis batch.
    *   Feast dapat membaca data dari berbagai data warehouse (seperti BigQuery, Snowflake, Redshift) atau sistem file (seperti S3, GCS, HDFS) yang berfungsi sebagai offline store.
    *   Memungkinkan pengguna untuk membuat dataset training dengan melakukan join *point-in-time* yang benar antara entitas dan nilai fitur historis, menghindari kebocoran data (data leakage).

3.  **Penyimpanan Online (Online Store)**:
    *   Digunakan untuk menyajikan nilai fitur terbaru dengan latensi rendah untuk inferensi model secara real-time.
    *   Feast mendukung berbagai database online seperti Redis, DynamoDB, Google Cloud Datastore, dan lainnya.
    *   Pengguna dapat memuat (materialize) fitur dari offline store ke online store secara berkala.

4.  **Penyajian Fitur (Feature Serving)**:
    *   Feast menyediakan SDK Python untuk mengambil fitur:
        *   `get_historical_features()`: Untuk mengambil data fitur historis dari offline store untuk membuat dataset training atau validasi.
        *   `get_online_features()`: Untuk mengambil vektor fitur terbaru dari online store untuk satu atau lebih entitas saat inferensi.

5.  **Konsistensi Training-Serving**:
    *   Dengan menggunakan definisi fitur yang sama untuk mengambil data training dan data inferensi, Feast membantu memastikan konsistensi dan mengurangi *training-serving skew*.

6.  **Materialisasi Fitur**:
    *   Perintah `feast materialize` digunakan untuk menghitung dan memuat nilai fitur dari offline store ke online store, menjaga data di online store tetap *fresh*. `feast materialize-incremental` hanya memuat data yang lebih baru dari materialisasi sebelumnya.

7.  **Integrasi dan Ekstensibilitas**:
    *   Feast dirancang untuk menjadi modular dan dapat diintegrasikan dengan berbagai komponen dalam tumpukan MLOps (misalnya, platform orkestrasi alur kerja, sistem pemantauan model).

Secara singkat, Feast membantu Anda:
*   **Menstandardisasi definisi dan manajemen fitur**.
*   **Menyediakan akses yang konsisten ke fitur untuk training dan serving**.
*   **Memudahkan pembuatan dataset training yang benar secara point-in-time**.
*   **Menyajikan fitur dengan latensi rendah untuk inferensi online**.
*   **Meningkatkan kolaborasi dan penggunaan kembali fitur dalam tim ML**.
