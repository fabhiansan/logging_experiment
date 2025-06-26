import torch
import torch.nn as nn
import numpy as np
import mlflow
from torch.utils.tensorboard import SummaryWriter
import json
import os

# --- 1. Konfigurasi & Parameter ---
LEARNING_RATE = 0.01
EPOCHS = 100

# --- 2. Buat Data Sintetis ---
# y = 2x + 1 + noise
X_numpy = np.random.rand(100, 1).astype(np.float32)
y_numpy = 2 * X_numpy + 1 + np.random.randn(100, 1).astype(np.float32) * 0.1

X_train = torch.from_numpy(X_numpy)
y_train = torch.from_numpy(y_numpy)

# --- 3. Definisikan Model PyTorch ---
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

model = LinearRegression()

# --- 4. Tentukan Loss dan Optimizer ---
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)

# --- 5. Setup Logging ---

# Setup MLFlow
mlflow.start_run(run_name="simple_linear_regression")
mlflow.log_param("learning_rate", LEARNING_RATE)
mlflow.log_param("epochs", EPOCHS)

# Setup TensorBoard
# Ini akan membuat direktori 'runs/simple_linear_regression'
writer = SummaryWriter('runs/simple_linear_regression')

print("Memulai pelatihan model sederhana...")

# --- 6. Training Loop ---
for epoch in range(EPOCHS):
    # Forward pass
    outputs = model(X_train)
    loss = criterion(outputs, y_train)

    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Logging ke semua platform
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item():.4f}')
        
        # Log ke MLFlow
        mlflow.log_metric("loss", loss.item(), step=epoch)

        # Log ke TensorBoard
        writer.add_scalar("Loss/train", loss.item(), epoch)

# --- 7. Selesaikan Logging ---

# Tutup writer TensorBoard
writer.close()

# Simpan metrik akhir untuk DVC
final_metrics = {'final_loss': loss.item()}
os.makedirs("metrics", exist_ok=True)
with open("metrics/simple_metrics.json", "w") as f:
    json.dump(final_metrics, f, indent=4)

print("Metrik akhir disimpan untuk DVC di metrics/simple_metrics.json")

# Akhiri run MLFlow
mlflow.end_run()

print("Pelatihan selesai. Semua log telah disimpan.")
