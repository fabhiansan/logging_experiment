# TensorBoard: Visualisasi & Debugging Pelatihan Model

TensorBoard adalah toolkit visualisasi dari TensorFlow. Ini memungkinkan Anda untuk melihat dan memahami eksperimen, grafik model, dan metrik machine learning Anda. Ini adalah alat yang sangat diperlukan untuk **debugging** dan **optimisasi** proses pelatihan.

---

## a. Komponen & Arsitektur Sistem

Arsitektur TensorBoard sangat sederhana dan berbasis file:

1.  **Summary Writer**: Dalam kode Anda (PyTorch atau TensorFlow), Anda membuat sebuah `SummaryWriter`.
2.  **Event Files**: Penulis ini mengambil data yang Anda catat (seperti *loss*, akurasi, atau gambar) dan menuliskannya ke dalam file log biner khusus yang disebut *event files*. File-file ini biasanya disimpan dalam direktori seperti `runs/`.
3.  **TensorBoard Server**: Anda menjalankan server web lokal (`tensorboard --logdir runs`) yang membaca *event files* ini dan menyajikannya dalam dasbor interaktif di browser Anda.

Arsitektur ini membuatnya sangat portabel, karena Anda hanya perlu membagikan direktori `runs` agar orang lain dapat mereproduksi visualisasi Anda.

---

## b. Cara Setup & Instrumentasi Eksperimen

Anda dapat menggunakan TensorBoard dengan PyTorch melalui `torch.utils.tensorboard`.

1.  **Instalasi**: `pip install tensorboard`
2.  **Inisialisasi Writer**: Buat instance `SummaryWriter`, menentukan direktori log.
3.  **Pencatatan**: Gunakan metode writer seperti `add_scalar()`, `add_image()`, atau `add_histogram()` di dalam *training loop* Anda.

**Contoh Kode (PyTorch):**

```python
import torch
from torch.utils.tensorboard import SummaryWriter

# 1. Inisialisasi writer, setiap run akan berada di sub-folder unik
writer = SummaryWriter('runs/fashion_mnist_experiment_1')

# Contoh data (biasanya di dalam training loop Anda)
for epoch in range(100):
    # Hitung loss dan accuracy dari model Anda
    loss = 0.1 * (1 / (epoch + 1))
    accuracy = 1.0 - loss

    # 2. Catat metrik skalar
    # Argumen pertama adalah nama plot, kedua adalah nilai y, ketiga adalah nilai x (step)
    writer.add_scalar('Loss/train', loss, epoch)
    writer.add_scalar('Accuracy/train', accuracy, epoch)

# 3. Catat gambar (contoh: confusion matrix atau sampel gambar)
# (Anda akan membuat gambar ini menggunakan matplotlib atau PIL)
# dummy_image = torch.rand(3, 100, 100)
# writer.add_image('four_fashion_mnist_images', dummy_image)

# 4. Tutup writer setelah selesai
writer.close()
```

---

## c. Visualisasi & Dasbor yang Disediakan

Dasbor TensorBoard adalah fitur utamanya. Setiap tab dirancang untuk memvisualisasikan aspek yang berbeda dari pelatihan Anda.

### **Scalars**
Tab ini adalah yang paling sering digunakan. Ini memplot metrik sederhana seperti *loss* dan akurasi dari waktu ke waktu. Anda dapat membandingkan beberapa *run* pada plot yang sama, memperhalus kurva, dan menganalisis kinerja.

![Dasbor Skalar TensorBoard](https://www.tensorflow.org/images/tensorboard_scalars.png)

### **Graphs**
Tab ini memungkinkan Anda untuk memvisualisasikan arsitektur model Anda. Ini sangat berguna untuk memastikan model Anda dibangun seperti yang Anda harapkan dan untuk memahami aliran data.

![Dasbor Grafik TensorBoard](https://www.tensorflow.org/images/tensorboard_graphs.png)

### **Histograms & Distributions**
Tab ini memberikan pandangan mendalam tentang bagaimana distribusi bobot dan bias dalam model Anda berubah dari waktu ke waktu. Ini bisa menjadi alat yang sangat kuat untuk mendiagnosis masalah seperti *vanishing* atau *exploding gradients*.

-   **Distributions View**: Menampilkan distribusi nilai tensor pada setiap *epoch*.
-   **Histograms View**: Menampilkan bagaimana distribusi tersebut berubah dari waktu ke waktu dalam tampilan 3D.

![Dasbor Histogram TensorBoard](https://www.tensorflow.org/images/tensorboard_histograms.png)

### **Images**
Memvisualisasikan gambar yang Anda catat, seperti gambar input, *feature maps*, atau plot yang dihasilkan seperti *confusion matrix*.

---

## d. Evaluasi Umum

-   **Kelebihan**:
    -   **Visualisasi Mendalam**: Tak tertandingi untuk analisis *real-time* dan *post-hoc* dari dinamika pelatihan. Sangat baik untuk menjawab "Mengapa?"
    -   **Debugging**: Alat terbaik untuk men-debug masalah pelatihan yang kompleks dengan memvisualisasikan bobot, gradien, dan grafik komputasi.
    -   **Interaktif**: UI sangat responsif, memungkinkan Anda untuk memperbesar, menggeser, dan menjelajahi data Anda secara intuitif.
    -   **Ekosistem**: Terintegrasi dengan baik dengan PyTorch, TensorFlow, dan pustaka lainnya.

-   **Kekurangan**:
    -   **Bukan untuk Perbandingan Skala Besar**: Meskipun Anda dapat membandingkan beberapa *run*, ini menjadi tidak praktis untuk membandingkan puluhan atau ratusan *run* seperti yang bisa dilakukan MLFlow.
    -   **Tidak Ada Manajemen Siklus Hidup**: TensorBoard berfokus murni pada visualisasi dan tidak memiliki fitur untuk versioning, pengemasan, atau deployment model.