# Perbandingan Tools Pelacakan Eksperimen: MLFlow vs TensorBoard vs DVC

Berikut adalah perbandingan antara MLFlow, TensorBoard, dan DVC berdasarkan kriteria yang umum digunakan dalam pelacakan eksperimen machine learning.

| Fitur Kunci                                 | MLFlow                                                                 | TensorBoard                                                              | DVC (Data Version Control)                                                   |
| :------------------------------------------ | :--------------------------------------------------------------------- | :----------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| **a. Komponen/Arsitektur Sistem**           | Tracking Server, Backend Store (DB/file), Artifact Store (file/cloud), UI, API/CLI. Komponen Proyek, Model, Registri. | Event Files (logs), TensorBoard Server (pembaca log), Web UI.               | Metafile `.dvc`, Cache DVC, Integrasi Git, Remote Storage, `dvc.yaml` (pipeline), `dvc.lock`. |
| **b. Cara Setup & Instrumentasi**           | `pip install mlflow`, `mlflow.start_run()`, `log_param()`, `log_metric()`, `log_artifact()`, `log_model()`. Atur `MLFLOW_TRACKING_URI`. Jalankan `mlflow ui`. | `pip install tensorboard` (atau dg TensorFlow). `tf.summary` API atau Keras/PyTorch callback. Jalankan `tensorboard --logdir`. | `pip install dvc`, `dvc init`, `dvc add`, `dvc remote add`, `dvc.yaml` (stages), `dvc exp run`. DVCLive untuk live logging. |
| **c. Metadata Eksperimen Dikumpulkan**      | Parameter, metrik (dg histori), artefak (model, file), versi kode (Git), run/exp ID, waktu, user, tag, info model. | Skalar (loss, acc), histogram (bobot), gambar, teks, audio, graf model, embedding, hyperparameter, data profiling. | Versi data (hash), versi kode (Git), definisi pipeline, parameter, metrik (dari file), artefak output, plot, info eksperimen. |
| **d. Visualisasi/Laporan/Dashboard**        | UI Web: tabel run, detail run, plot metrik interaktif, browser artefak, perbandingan run, UI registri model. | UI Web: plot skalar, histogram, distribusi, gambar, audio, teks, visualizer graf, proyektor embedding, dashboard HParams, profiler. | CLI: `dvc exp show` (tabel), `metrics/params show`, `plots show` (render plot dari data, bisa HTML/Vega-Lite). DVC Studio (produk terpisah) untuk UI web. |
| **e. Evaluasi Umum (Kelebihan/Kekurangan)** | **(+)**: Framework-agnostic, komprehensif, reproduktifitas, skalabel, UI baik. **(-)**: Mungkin overkill utk proyek simpel, UI perlu server. | **(+)**: Visualisasi kaya (DL), real-time, debug model, integrasi TF/Keras baik, profiler. **(-)**: Fokus visualisasi, kurang di manajemen eksperimen umum, tidak ada registri model. | **(+)**: Versioning data/pipeline kuat, integrasi Git, language-agnostic, `dvc exp` efisien, DVCLive. **(-)**: Kurva belajar curam, visualisasi bawaan terbatas (perlu DVC Studio utk UI kaya), fokus versioning. |

## Ringkasan dan Kapan Menggunakan Masing-masing

*   **MLFlow**:
    *   **Gunakan jika**: Anda membutuhkan solusi manajemen siklus hidup ML yang komprehensif, dari pelacakan hingga penerapan. Sangat baik jika Anda bekerja dengan berbagai library ML dan membutuhkan platform terpusat untuk tim. Cocok untuk reproduktifitas eksperimen dan versioning model formal.
    *   **Fokus**: Manajemen eksperimen menyeluruh, reproduktifitas, versioning model, dan pelaporan.

*   **TensorBoard**:
    *   **Gunakan jika**: Fokus utama Anda adalah pada visualisasi mendalam dan real-time dari proses training model deep learning (misalnya, metrik, bobot, gradien, graf model). Sangat berguna saat menggunakan TensorFlow/Keras, tetapi juga mendukung PyTorch.
    *   **Fokus**: Visualisasi detail training, debugging model, dan profiling kinerja.

*   **DVC**:
    *   **Gunakan jika**: Prioritas utama Anda adalah versioning dataset besar dan pipeline machine learning yang kompleks, serta memastikan reproduktifitas penuh dengan alur kerja berbasis Git. `dvc exp` sangat berguna untuk mengelola banyak iterasi eksperimen.
    *   **Fokus**: Versioning data dan pipeline, reproduktifitas, integrasi Git, manajemen eksperimen berbasis kode.

## Bisakah Digunakan Bersama?

Ya, tools ini dapat saling melengkapi:

*   **DVC + MLFlow**: DVC dapat menangani versioning data dan pipeline, sementara MLFlow menangani pelacakan parameter/metrik yang lebih detail, visualisasi UI, dan registri model. Anda bisa memiliki stage DVC yang menjalankan skrip yang mencatat ke MLFlow.
*   **DVC + TensorBoard**: DVC dapat mengontrol versi data/kode/pipeline, dan output dari stage training (event file TensorBoard) dapat menjadi artefak yang dilacak DVC. Anda kemudian bisa menggunakan TensorBoard untuk memvisualisasikan log dari eksperimen tertentu yang dikelola DVC.
*   **MLFlow + TensorBoard**: MLFlow dapat mencatat event file TensorBoard sebagai artefak, memungkinkan Anda mengakses visualisasi TensorBoard dari dalam UI MLFlow untuk run tertentu.

Pemilihan tergantung pada kebutuhan spesifik proyek Anda, skala tim, dan aspek mana dari siklus hidup ML yang paling ingin Anda tingkatkan. Untuk tugas kuliah ini, mencoba ketiganya akan memberikan pemahaman yang baik tentang kekuatan masing-masing.