# Hopsworks Feature Store

Hopsworks adalah platform AI Lakehouse terdistribusi kelas enterprise yang menyertakan Feature Store yang canggih dan berpusat pada Python. Hopsworks dirancang untuk mengelola data secara intensif untuk machine learning, mencakup seluruh siklus hidup ML mulai dari rekayasa fitur, training model, hingga inferensi. Platform ini bersifat modular, artinya Anda dapat menggunakannya sebagai Feature Store mandiri, untuk mengelola dan menyajikan model, atau bahkan untuk mengembangkan dan mengoperasikan pipeline fitur dan model secara keseluruhan.

Fitur utama Hopsworks Feature Store meliputi:

1.  **Manajemen Fitur Terpusat (Feature Groups)**:
    *   Fitur diorganisir ke dalam "Feature Groups". Feature Group adalah sekumpulan fitur yang dihitung bersama, seringkali dari sumber data yang sama dan dengan logika komputasi yang sama.
    *   Mendukung CRUD (Create, Read, Update, Delete) API untuk mengelola data fitur dalam Feature Groups, misalnya menggunakan Pandas DataFrame di Python.
    *   Menyimpan metadata yang kaya tentang fitur, termasuk versi, statistik, dependensi data, dan skema.

2.  **Rekayasa Fitur (Feature Engineering)**:
    *   Memungkinkan pengguna untuk mendefinisikan pipeline rekayasa fitur menggunakan Python (misalnya, dengan Spark, Pandas, atau SQL).
    *   Mendukung komputasi fitur secara batch maupun streaming.
    *   Fitur dapat divalidasi terhadap ekspektasi kualitas data.

3.  **Penyimpanan Offline dan Online Terintegrasi**:
    *   **Offline Store**: Digunakan untuk menyimpan volume besar data fitur historis untuk training model dan analisis. Hopsworks menggunakan Apache Hudi di atas HDFS atau penyimpanan cloud (seperti S3) untuk offline store-nya, yang memungkinkan manajemen data yang efisien (misalnya, pembaruan, penghapusan, dan perjalanan waktu).
    *   **Online Store**: Dirancang untuk penyajian fitur dengan latensi sangat rendah dan throughput tinggi untuk aplikasi online. Hopsworks menggunakan RonDB (versi cloud-native dari MySQL Cluster) sebagai online store-nya, yang dikenal karena ketersediaan dan kinerjanya yang tinggi.
    *   Sinkronisasi antara offline dan online store dikelola oleh platform.

4.  **Penyajian Fitur (Feature Serving)**:
    *   Menyediakan API Python (HSFS - Hopsworks Feature Store client library) untuk mengambil fitur:
        *   Untuk membuat dataset training (dari offline store) dengan kemampuan join *point-in-time* yang akurat untuk menghindari kebocoran data.
        *   Untuk mengambil vektor fitur (dari online store) untuk inferensi model secara real-time.

5.  **Manajemen Versi dan Tata Kelola Data (Data Governance)**:
    *   Secara otomatis mengontrol versi fitur dan skema fitur.
    *   Menyediakan fitur tata kelola data seperti kontrol akses berbasis peran, audit, dan pelacakan silsilah data (data lineage).

6.  **Integrasi dengan Ekosistem AI/ML**:
    *   Terintegrasi dengan baik dengan berbagai library dan framework ML (seperti TensorFlow, PyTorch, Scikit-learn, Spark ML).
    *   Mendukung berbagai lingkungan komputasi (on-premise, cloud).

7.  **Skalabilitas dan Ketersediaan Tinggi**:
    *   Dibangun di atas arsitektur terdistribusi untuk menangani dataset dan beban kerja skala besar.
    *   Online store (RonDB) dirancang untuk ketersediaan tinggi (high availability).

Secara singkat, Hopsworks Feature Store bertujuan untuk:
*   **Menyediakan platform terpadu untuk seluruh siklus hidup data ML**.
*   **Memfasilitasi kolaborasi antara tim data engineering dan data science**.
*   **Memastikan kualitas, konsistensi, dan reproduktifitas fitur**.
*   **Menyajikan fitur dengan kinerja tinggi untuk aplikasi AI real-time**.
*   **Menyederhanakan MLOps dengan manajemen fitur yang kuat**.
