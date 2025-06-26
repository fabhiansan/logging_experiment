import mlflow
import numpy as np
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.datasets import load_breast_cancer
from torch.utils.tensorboard import SummaryWriter

# --- 1. Konfigurasi & Parameter ---
MAX_DEPTH = 5
TEST_SIZE = 0.3
RANDOM_STATE = 42

# --- 2. Muat Dataset ---
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

# --- 3. Setup Logging ---

# Setup MLFlow
# Hardcode the absolute path for the tracking URI as a last resort
tracking_uri_path = "/Users/fabhiantom/Downloads/logging_experiment/mlruns"
os.environ["MLFLOW_TRACKING_URI"] = "file://" + tracking_uri_path
mlflow.start_run(run_name="decision_tree_classifier")
mlflow.log_param("max_depth", MAX_DEPTH)
mlflow.log_param("random_state", RANDOM_STATE)

# Setup TensorBoard
writer = SummaryWriter('runs/decision_tree_classifier')

print("Memulai pelatihan model klasifikasi...")

# --- 4. Latih Model ---
model = DecisionTreeClassifier(max_depth=MAX_DEPTH, random_state=RANDOM_STATE)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# --- 5. Hitung Metrik ---
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')

metrics = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}

print("Metrik:", json.dumps(metrics, indent=2))

# Log metrik ke MLFlow & TensorBoard
mlflow.log_metrics(metrics)
for key, value in metrics.items():
    writer.add_scalar(f'Metrics/{key}', value, 0)

# --- 6. Buat dan Log Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap='Blues')
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix')
plt.tight_layout()

# Simpan plot sebagai file gambar
cm_image_path = "plots/confusion_matrix.png"
os.makedirs("plots", exist_ok=True)
plt.savefig(cm_image_path)
plt.close(fig)

print(f"Confusion matrix disimpan di {cm_image_path}")

# Log artifact ke MLFlow (dinonaktifkan karena masalah lingkungan eksekusi)
# mlflow.log_artifact(cm_image_path, artifact_path="plots")

# Log gambar ke TensorBoard
# Membaca gambar sebagai array numpy untuk TensorBoard
from PIL import Image
image_array = np.array(Image.open(cm_image_path))
writer.add_image('Plots/ConfusionMatrix', image_array, 0, dataformats='HWC')

# --- 7. Selesaikan Logging ---

# Tutup writer TensorBoard
writer.close()

# Simpan metrik untuk DVC
os.makedirs("metrics", exist_ok=True)
with open("metrics/classification_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Metrik klasifikasi disimpan untuk DVC.")

# Akhiri run MLFlow
mlflow.end_run()

print("Pelatihan selesai. Semua log dan plot telah disimpan.")
