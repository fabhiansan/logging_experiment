# Tensorboard Experiment Tracking

## a. Komponen/arsitektur sistem
TensorBoard bekerja dengan membaca file log yang dihasilkan selama proses pelatihan. 
- **Summary Writer**: Dalam kode Anda (misalnya, Python), Anda membuat `SummaryWriter` yang menulis data (metrik, gambar, dll.) ke direktori log yang ditentukan (misalnya, direktori `runs/`).
- **Log Files**: File-file ini berisi data dalam format protobuf yang dioptimalkan untuk dibaca oleh TensorBoard.
- **TensorBoard UI**: Server web lokal yang membaca dari direktori log dan menyajikan data dalam dasbor interaktif.

## b. Cara setup instrumentasi/pencatatan eksperimen
1.  **Instalasi**: `pip install tensorboard` (biasanya sudah terinstal bersama TensorFlow atau PyTorch).
2.  **Membuat Writer**: Inisialisasi `SummaryWriter` dari `torch.utils.tensorboard` (untuk PyTorch) atau `tf.summary` (untuk TensorFlow), dengan menunjuk ke direktori log.
3.  **Pencatatan**:
    - `writer.add_scalar("tag", nilai_skalar, global_step)`: Mencatat nilai numerik tunggal pada langkah tertentu (misalnya, *loss* per *epoch*).
    - `writer.add_image("tag", array_gambar, global_step)`: Mencatat gambar (misalnya, *confusion matrix*).
    - `writer.add_histogram("tag", nilai, global_step)`: Mencatat distribusi nilai.

**Contoh Kode (PyTorch):**
```python
from torch.utils.tensorboard import SummaryWriter
import numpy as np

# Buat writer yang akan menulis ke direktori 'runs/my_experiment'
writer = SummaryWriter('runs/my_experiment')

# Catat metrik skalar dari waktu ke waktu
for epoch in range(100):
    loss = 0.1 * epoch
    writer.add_scalar('Loss/train', loss, epoch)

# Catat sebuah gambar (misalnya, gambar acak)
random_image = np.random.rand(3, 64, 64)
writer.add_image('My Image', random_image, 0)

writer.close()
```

## c. Metadata eksperimen yang dikumpulkan
- **Skalar**: Metrik numerik yang dilacak dari waktu ke waktu. Ini adalah kasus penggunaan yang paling umum.
- **Gambar**: Plot statis atau gambar yang relevan dengan pelatihan.
- **Histogram**: Distribusi bobot atau bias model dari waktu ke waktu.
- **Graph**: Visualisasi dari arsitektur model (grafik komputasi).
- **Teks**: Catatan teks atau informasi lainnya.

## d. Visualisasi/laporan/dashboard yang disediakan
TensorBoard unggul dalam visualisasi dinamis dari **satu kali proses pelatihan**.
- **Plot Time-Series**: Grafik interaktif yang indah untuk semua skalar yang dicatat, memungkinkan Anda untuk memperbesar, memperkecil, dan menghaluskan kurva.
- **Image Viewer**: Menampilkan semua gambar yang Anda catat, dengan slider untuk menavigasi melalui berbagai langkah.
- **Graph Explorer**: Memungkinkan Anda menjelajahi arsitektur model secara interaktif.
- **Distribution dan Histogram**: Visualisasi detail dari distribusi bobot dan bias.

## e. Evaluasi umum
- **Kelebihan**: Alat visualisasi terbaik untuk menganalisis dinamika pelatihan secara mendalam. Plot skalar dan penampil gambar sangat informatif dan interaktif. Sangat mudah diintegrasikan dengan PyTorch dan TensorFlow.
- **Kekurangan**: Tidak dirancang untuk membandingkan banyak *run* yang berbeda secara efisien seperti MLFlow. Setiap *run* biasanya dilihat secara terpisah, meskipun perbandingan dasar dimungkinkan.