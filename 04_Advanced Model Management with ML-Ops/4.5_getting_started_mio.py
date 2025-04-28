"""
Siamo il Client che comunica con MLFlow Server
che abbiamo già lanciato ed è in esecuzione su http://localhost:5000
in questo caso sia MLFlow server che client sono in locale
"""

import mlflow
import numpy as np
import pandas as pd
import plotly.express as px

mlflow.set_tracking_uri("http://localhost:5000")

# creiamo un experiment
experiment_id = mlflow.create_experiment("My new Experiment_finale")

# creiamo un run ovvero una iterazione all'interno dell'experiment
# i run tracciano tutti i cambiamenti o modifiche che facciamo sui dati o parametri
run = mlflow.start_run(experiment_id=experiment_id, run_name="First run")


# loggin parameters
mlflow.log_param("learning_rate", 0.01)
mlflow.log_param("batch_size", 32)

num_epochs = 10

mlflow.log_param("num_epochs", num_epochs)

# logging metrics
# diversamente dai parametri le metriche sono time-based o step-based (training)
for epoch in range(num_epochs):
    mlflow.log_metric("accuracy", np.random.random(), step=epoch)
    mlflow.log_metric("loss", np.random.random(), step=epoch)


# Logging a time-series metric
for t in range(100):
    metric_value = np.sin(t * np.pi / 50)
    mlflow.log_metric("time_series_metric", metric_value, step=t)

# Logging artefacts
# sono qualsiasi tipo di file grandi come datasets, modelli, logs o custom files

# Generate a confusion matrix
confusion_matrix = np.random.randint(0, 100, size=(5, 5))  # 5x5 matrix

labels = ["Class A", "Class B", "Class C", "Class D", "Class E"]
df_cm = pd.DataFrame(confusion_matrix, index=labels, columns=labels)

# Plot confusion matrix using Plotly Express
fig = px.imshow(df_cm, text_auto=True, labels=dict(x="Predicted Label", y="True Label"), x=labels, y=labels, title="Confusion Matrix")

# Save the figure as an HTML file
html_file = "confusion_matrix.html"
fig.write_html(html_file)

# Log the HTML file with MLflow
mlflow.log_artifact(html_file, "data")


# Logging Models

from transformers import AutoModelForSeq2SeqLM

# Initialize a model from Hugging Face Transformers
model = AutoModelForSeq2SeqLM.from_pretrained("TheFuzzyScientist/T5-base_Amazon-product-reviews")


# Log the model in MLflow
mlflow.pytorch.log_model(model, "transformer_model")


# fine del run
mlflow.end_run()