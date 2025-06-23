# Feathr

Feathr adalah sebuah *feature store* open-source yang awalnya dikembangkan dan digunakan secara internal di LinkedIn selama lebih dari enam tahun sebelum dirilis sebagai proyek open-source dan di-host oleh LF AI & Data Foundation. Feathr dirancang untuk menjadi platform rekayasa data dan AI yang terpadu, skalabel, dan berkinerja tinggi untuk kebutuhan enterprise.

Tujuan utama dari feature store seperti Feathr adalah untuk menyediakan tempat terpusat untuk menyimpan, mengelola, menemukan, dan menyajikan fitur-fitur machine learning. Ini membantu mengatasi beberapa tantangan umum dalam siklus hidup ML, seperti:

*   **Duplikasi Upaya**: Tim yang berbeda seringkali membuat ulang fitur yang sama.
*   **Konsistensi Fitur**: Memastikan bahwa fitur yang sama digunakan secara konsisten antara training dan penyajian (inferensi) model, untuk menghindari *training-serving skew*.
*   **Penemuan Fitur**: Memudahkan data scientist untuk menemukan dan menggunakan kembali fitur yang sudah ada.
*   **Skalabilitas dan Kinerja**: Menyediakan fitur dengan latensi rendah untuk aplikasi real-time dan throughput tinggi untuk training model.

Fitur dan konsep utama dalam Feathr meliputi:

1.  **Definisi Fitur Terpusat**:
    *   Feathr memungkinkan pengguna untuk mendefinisikan fitur menggunakan konfigurasi atau kode (seringkali berbasis Python). Definisi ini mencakup bagaimana fitur dihitung dari sumber data mentah.
    *   Mendukung berbagai jenis fitur, termasuk fitur berbasis window (misalnya, jumlah transaksi dalam 7 hari terakhir), fitur turunan (misalnya, rasio klik), dan embedding.

2.  **Transformasi Fitur**:
    *   Menyediakan kemampuan untuk melakukan transformasi pada data mentah untuk menghasilkan fitur. Ini bisa melibatkan agregasi, join, atau fungsi yang ditentukan pengguna (UDF).

3.  **Penyimpanan Fitur**:
    *   Fitur yang telah dihitung dapat disimpan dalam penyimpanan offline (untuk training model batch, seringkali menggunakan sistem file terdistribusi seperti HDFS atau Azure Data Lake Storage) dan penyimpanan online (untuk penyajian fitur dengan latensi rendah, seringkali menggunakan database NoSQL seperti Redis atau Azure Cosmos DB).

4.  **Penyajian Fitur (Feature Serving)**:
    *   Menyediakan API untuk mengambil fitur baik untuk training model (mengambil data historis dalam jumlah besar) maupun untuk inferensi online (mengambil fitur terbaru untuk entitas tertentu dengan cepat).

5.  **Manajemen Materialisasi Fitur**:
    *   Mengelola proses penghitungan dan pembaruan fitur secara berkala agar tetap *fresh*.

6.  **Integrasi dengan Ekosistem Data**:
    *   Dirancang untuk berintegrasi dengan berbagai sumber data (misalnya, data stream, data warehouse) dan platform komputasi (seperti Spark, Databricks). Feathr juga memiliki integrasi yang kuat dengan Azure.

7.  **Penemuan dan Berbagi Fitur**:
    *   Dengan adanya repositori fitur terpusat, tim dapat lebih mudah berbagi dan menggunakan kembali fitur, yang meningkatkan produktivitas dan konsistensi.

Secara singkat, Feathr bertujuan untuk:
*   **Menyederhanakan dan mempercepat rekayasa fitur**.
*   **Meningkatkan kolaborasi dan penggunaan kembali fitur**.
*   **Memastikan konsistensi fitur antara training dan serving**.
*   **Menyediakan platform yang skalabel dan berkinerja tinggi untuk manajemen fitur**.
