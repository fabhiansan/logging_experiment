# TensorBoard: Detail untuk Pelacakan Eksperimen

TensorBoard adalah toolkit visualisasi yang disediakan oleh TensorFlow, tetapi juga dapat digunakan dengan library lain seperti PyTorch.

## a. Komponen/Arsitektur Sistem

1.  **Event Files (Log Files)**:
    *   Program machine learning (misalnya, skrip training TensorFlow/Keras atau PyTorch) menulis data ringkasan (summary data) ke dalam file log biner yang disebut event file. File-file ini biasanya disimpan dalam direktori log.
    *   Setiap event file berisi data serial dari `tf.compat.v1.Event` protocol buffer, yang dapat mencakup skalar, histogram, gambar, audio, teks, dan data graf.

2.  **TensorBoard Server**:
    *   Sebuah aplikasi web lokal yang Anda jalankan dari command line.
    *   Server ini membaca event file dari direktori log yang ditentukan.
    *   Memproses data dan menyajikannya melalui antarmuka web.

3.  **Web UI (Dashboard)**:
    *   Antarmuka pengguna berbasis web yang diakses melalui browser (biasanya di `http://localhost:6006`).
    *   Menyediakan berbagai dashboard untuk memvisualisasikan data yang dicatat.

## b. Cara Setup Instrumentasi/Pencatatan Eksperimen

1.  **Instalasi**:
    *   Biasanya diinstal sebagai bagian dari TensorFlow:
        ```bash
        pip install tensorflow
        ```
    *   Atau secara terpisah:
        ```bash
        pip install tensorboard
        ```

2.  **Pencatatan dalam Kode Python (Contoh dengan TensorFlow 2.x)**:
    *   **Menggunakan `tf.summary.create_file_writer()`**:
        ```python
        import tensorflow as tf
        import datetime

        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        summary_writer = tf.summary.create_file_writer(log_dir)
        ```
    *   **Mencatat Skalar (misalnya, loss, accuracy)**:
        ```python
        with summary_writer.as_default():
            tf.summary.scalar('loss', loss_value, step=epoch)
            tf.summary.scalar('accuracy', accuracy_value, step=epoch)
        ```
    *   **Mencatat Histogram (misalnya, distribusi bobot)**:
        ```python
        with summary_writer.as_default():
            tf.summary.histogram('weights_layer1', model.layers[0].get_weights()[0], step=epoch)
        ```
    *   **Mencatat Gambar**:
        ```python
        # Misalkan `image_tensor` adalah tensor gambar [batch_size, height, width, channels]
        with summary_writer.as_default():
            tf.summary.image("Sample Training Image", image_tensor, max_outputs=3, step=epoch)
        ```
    *   **Mencatat Teks**:
        ```python
        with summary_writer.as_default():
            tf.summary.text("Hyperparameters", tf.convert_to_tensor(str(hyperparam_dict)), step=0)
        ```
    *   **Mencatat Graf Model (untuk TensorFlow)**:
        Biasanya dilakukan secara otomatis jika `tf.function` digunakan atau dengan `tf.summary.trace_on()` dan `tf.summary.trace_export()`.

3.  **Menggunakan Keras `TensorBoard` Callback**: Cara termudah jika menggunakan Keras.
    ```python
    from tensorflow.keras.callbacks import TensorBoard

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1) # histogram_freq=1 untuk mencatat histogram bobot setiap epoch

    model.fit(x_train, y_train, epochs=10, callbacks=[tensorboard_callback])
    ```

4.  **Untuk PyTorch**:
    *   Gunakan `torch.utils.tensorboard.SummaryWriter`:
        ```python
        from torch.utils.tensorboard import SummaryWriter
        writer = SummaryWriter('runs/my_pytorch_experiment') # Direktori log
        writer.add_scalar('Loss/train', loss_value, epoch)
        writer.add_histogram('weights/conv1', model.conv1.weight, epoch)
        writer.close()
        ```

5.  **Menjalankan TensorBoard UI**:
    ```bash
    tensorboard --logdir logs/fit # atau direktori log yang sesuai
    ```
    Akses UI di `http://localhost:6006`.

## c. Metadata Eksperimen yang Dikumpulkan

TensorBoard dirancang untuk mengumpulkan berbagai jenis data visualisasi:

*   **Scalars**: Nilai tunggal yang berubah seiring waktu (step/epoch), seperti loss, accuracy, learning rate.
*   **Histograms**: Distribusi nilai tensor dari waktu ke waktu, berguna untuk melacak bobot, bias, atau aktivasi.
*   **Distributions**: Mirip histogram, tetapi dengan lebih banyak detail statistik.
*   **Images**: Gambar yang dicatat selama training (misalnya, input sampel, filter yang dipelajari, output generator di GAN).
*   **Audio**: Klip audio.
*   **Text**: Pesan teks atau informasi kualitatif.
*   **Graphs**: Struktur komputasi model (untuk TensorFlow, ini bisa interaktif).
*   **Embeddings**: Proyeksi data berdimensi tinggi ke ruang 2D/3D (misalnya, embedding kata).
*   **Hyperparameters**: Pelacakan berbagai set hyperparameter dan metrik terkait untuk perbandingan.
*   **Profiling Data (melalui TensorFlow Profiler)**: Detail kinerja eksekusi operasi pada CPU/GPU/TPU.

## d. Visualisasi/Laporan/Dashboard yang Disediakan

TensorBoard UI menyediakan beberapa dashboard utama:

*   **Scalars Dashboard**: Plot garis interaktif untuk semua metrik skalar yang dicatat. Memungkinkan smoothing, perbandingan antar run.
*   **Histograms Dashboard**: Visualisasi histogram yang berubah seiring waktu (misalnya, bagaimana distribusi bobot berubah per epoch).
*   **Distributions Dashboard**: Mirip histogram, menunjukkan bagaimana distribusi nilai berubah.
*   **Images Dashboard**: Menampilkan gambar yang dicatat pada step yang berbeda.
*   **Audio Dashboard**: Memutar klip audio yang dicatat.
*   **Text Dashboard**: Menampilkan data teks.
*   **Graphs Dashboard**: Memvisualisasikan graf komputasi model. Untuk TensorFlow, ini bisa interaktif, memungkinkan eksplorasi node dan dependensi.
*   **Embeddings Projector**: Alat untuk memvisualisasikan embedding berdimensi tinggi menggunakan PCA, t-SNE, dll.
*   **HParams Dashboard**: Membandingkan hasil (metrik) dari berbagai kombinasi hyperparameter.
*   **Profiler Dashboard**: Menganalisis kinerja training, mengidentifikasi bottleneck.

## e. Evaluasi Umum Perbandingan

*   **Kelebihan**:
    *   **Visualisasi yang Kaya**: Sangat baik untuk memvisualisasikan berbagai aspek training model, terutama untuk deep learning.
    *   **Real-time Monitoring**: Dapat memantau metrik saat training berlangsung.
    *   **Debugging Model**: Membantu memahami perilaku internal model (bobot, gradien).
    *   **Integrasi Erat dengan TensorFlow/Keras**: Sangat mudah digunakan dalam ekosistem ini.
    *   **Dukungan untuk PyTorch dan Library Lain**: Melalui `SummaryWriter`.
    *   **Profiler yang Kuat**: Untuk analisis kinerja mendalam.
*   **Kekurangan**:
    *   Fokus utamanya adalah pada *visualisasi* data training, bukan manajemen eksperimen yang komprehensif seperti MLflow (misalnya, pelacakan artefak generik atau versioning model yang eksplisit).
    *   Kurang cocok untuk melacak parameter eksperimen non-numerik secara terstruktur seperti MLflow.
    *   Meskipun dapat membandingkan run, antarmuka perbandingannya mungkin tidak sefleksibel MLflow untuk parameter dan metrik arbitrer.
    *   Tidak memiliki konsep bawaan untuk "proyek" atau "registri model" seperti MLflow.