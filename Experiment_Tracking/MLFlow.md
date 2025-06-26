# MLFlow: Panduan Lengkap untuk Manajemen Siklus Hidup ML

MLFlow adalah platform sumber terbuka yang dirancang untuk mengelola seluruh siklus hidup machine learning, mulai dari eksperimen hingga deployment. Ini bukan hanya alat pelacakan; ini adalah suite terintegrasi yang terdiri dari empat komponen utama.

1.  **MLFlow Tracking**: Untuk melacak eksperimen, mencatat parameter, metrik, dan artefak.
2.  **MLFlow Projects**: Untuk mengemas kode ML dalam format yang dapat direproduksi.
3.  **MLFlow Models**: Format standar untuk mengemas model yang dapat digunakan di berbagai alat deployment.
4.  **MLFlow Model Registry**: Penyimpanan model terpusat untuk mengelola seluruh siklus hidup model.

---

## 1. MLFlow Tracking: Melacak & Membandingkan Eksperimen

Ini adalah komponen yang paling sering digunakan dan menjadi inti dari MLFlow.

### a. Arsitektur & Komponen

MLFlow Tracking memiliki arsitektur fleksibel yang memungkinkan kolaborasi dan skalabilitas.

![Diagram Arsitektur MLFlow](https://mlflow.org/docs/latest/_images/tracking-server.png)

-   **Tracking Server**: Pusat dari MLFlow. Server ini mencatat semua data yang dikirim oleh klien MLFlow.
-   **Backend Store**: Tempat metadata (parameter, metrik) disimpan. Bisa berupa file lokal atau database SQL.
-   **Artifact Store**: Tempat file besar (model, plot) disimpan. Bisa berupa direktori lokal atau penyimpanan cloud (S3, GCS).

### b. Instrumentasi Kode: Manual vs. Autologging

**Pendekatan 1: Manual Logging (Kontrol Penuh)**

Anda memiliki kontrol penuh atas apa yang dicatat dan kapan.

```python
import mlflow
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

mlflow.set_experiment("House Price Prediction")

with mlflow.start_run(run_name="Random Forest n_estimators=100"):
    # Catat Parameter
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    # Latih model
    X, y = make_regression(n_features=4, n_informative=2)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = RandomForestRegressor(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    # Catat Metrik
    mlflow.log_metric("r2_score", score)

    # Catat Model
    mlflow.sklearn.log_model(model, "model")
```

**Pendekatan 2: Autologging (Cepat & Mudah)**

Untuk pustaka populer (Scikit-learn, TensorFlow, PyTorch, dll.), MLFlow dapat secara otomatis mencatat semuanya untuk Anda hanya dengan satu baris kode.

```python
import mlflow
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

# Aktifkan autologging untuk scikit-learn
mlflow.sklearn.autolog()

mlflow.set_experiment("House Price Prediction")

with mlflow.start_run():
    # Tidak perlu log_param, log_metric, atau log_model manual!
    X, y = make_regression(n_features=4, n_informative=2)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = RandomForestRegressor(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
```

### c. Visualisasi di UI

Jalankan `mlflow ui` di terminal untuk meluncurkan dasbor.

-   **Tampilan Daftar Eksperimen**: Halaman utama untuk menyortir dan memfilter semua *run* Anda.
    ![Tampilan Daftar Run MLFlow](https://mlflow.org/docs/latest/_images/tracking-ui-page.png)

-   **Tampilan Perbandingan Run**: Fitur andalan untuk membandingkan hyperparameter dan metrik secara visual.
    ![Tampilan Perbandingan Run MLFlow](https://mlflow.org/docs/latest/_images/parallel-coordinates-plot.png)

---

## 2. MLFlow Projects: Reproducibility

Komponen ini mengemas kode Anda dalam format standar sehingga dapat dijalankan kembali oleh siapa saja di platform apa pun. Ini dicapai dengan file `MLproject`.

**Contoh `MLproject` file:**
```yaml
name: My Awesome Project

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
      l1_ratio: {type: float, default: 0.1}
    command: "python train.py --alpha {alpha} --l1_ratio {l1_ratio}"
```

Anda dapat menjalankan proyek ini dengan: `mlflow run . -P alpha=0.4`

---

## 3. MLFlow Models & Model Registry: Deployment & Governance

-   **MLFlow Models**: Menyediakan format standar ("flavor") untuk menyimpan model yang dapat dipahami oleh berbagai alat deployment.
-   **Model Registry**: Sebuah repositori terpusat untuk mengelola siklus hidup model Anda.

![Siklus Hidup Model Registry](https://mlflow.org/docs/latest/_images/model-registry.png)

**Siklus Hidup Model:**
1.  **Registrasi**: Setelah menemukan model yang bagus dari eksperimen, Anda mendaftarkannya ke Registry.
2.  **Versioning**: Setiap model baru yang didaftarkan dengan nama yang sama akan membuat versi baru (Version 1, Version 2, dst.).
3.  **Staging**: Anda dapat mempromosikan versi model ke berbagai tahap: `Staging`, `Production`, atau `Archived`.
4.  **Deployment**: Aplikasi Anda dapat secara terprogram mengambil model versi `Production` terbaru untuk inferensi.

**Contoh Kode Mendaftarkan Model:**
```python
# Di dalam run MLFlow Anda...
result = mlflow.register_model(
    "runs:/{}/model".format(mlflow.active_run().info.run_id),
    "MyProductionModel"
)
```

---

## Evaluasi & Kapan Menggunakannya

-   **Gunakan MLFlow Tracking ketika**: Anda perlu menjalankan banyak eksperimen dan dengan mudah membandingkannya untuk menemukan model terbaik.
-   **Gunakan MLFlow Projects ketika**: Anda perlu berbagi kode Anda dengan orang lain atau menjalankannya kembali di lingkungan produksi dengan cara yang dapat direproduksi.
-   **Gunakan MLFlow Model Registry ketika**: Anda memiliki alur kerja deployment yang formal dan perlu mengelola versi model yang disajikan kepada pengguna.