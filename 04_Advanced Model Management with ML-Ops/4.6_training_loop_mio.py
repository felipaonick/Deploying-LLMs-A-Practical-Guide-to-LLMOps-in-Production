import mlflow
import torch
from datasets import load_dataset
from torch.utils.data import DataLoader
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast
from torch.optim import AdamW
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from tqdm import tqdm
import os


# Define Parameters
params = {
    "model_name": "distilbert-base-uncased",
    "learning_rate": 5e-5,
    "batch_size": 16,
    "num_epochs": 3,
    "dataset_name": "ag_news",
    "task_name": "sequence_classification_final",
    "log_steps": 100,
    "max_seq_length": 128,
    "output_dir": "models/distilbert_ag-news",
}


# Mlflow setup
# ci colleghiamo al server e creiamo un experiment
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment(f"{params['task_name']}")

# Start run
run = mlflow.start_run(run_name=f"{params['model_name']}-{params['dataset_name']}")

# carichiamo i parametri 
mlflow.log_params(params=params)

# Load dataset
dataset = load_dataset(params['dataset_name'])

tokenizer = DistilBertTokenizerFast.from_pretrained(params['model_name'])

def tokenize(batch):
    return tokenizer(batch['text'], padding="max_length", truncation=True, max_length=params['max_seq_length'])


train_subset_size = min(20_000, len(dataset['train']))
test_subset_size = min(20_000, len(dataset['test']))

train_dataset = dataset['train'].shuffle(seed=42).select(range(train_subset_size)).map(tokenize, batched=True)
test_dataset = dataset['test'].shuffle(seed=42).select(range(test_subset_size)).map(tokenize, batched=True)

# salviamo i nostri datasets sul disco 
# ci consentirà di registrarli ad MLflow come artifacts
# li salviamo come .parquet files perchè è un formato molto robusto
# ma si potrbbero slavare anche come JSON o qualsiasi altro formato compatibile
train_dataset.to_parquet("data/train.parquet")
test_dataset.to_parquet("data/test.parquet")

# load datasets
# dopo che abbiamo slavato i datasets sul disco li possiamo registrare su MLflow come 
#artifacts
mlflow.log_artifact('data/train.parquet', artifact_path='datasets')
mlflow.log_artifact("data/test.parquet", artifact_path="datasets")

# per velocizzare un po il training creiamo dei data loaders per i nostri datasets
# questo ci consente di streammare i data alla training pipeline più efficientemente
train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

train_loader = DataLoader(train_dataset, batch_size=params['batch_size'], shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=params['batch_size'], shuffle=False)

# get labels
# vediamo che le news del dataset sono labellati con "World", "Sports", "Business", "Sci/Tech"
labels = dataset['train'].features['label'].names

# Define model 
# utilizziamo gli stessi parametri di configurazione che abbiamo
# già registrato in MLflow 
model = DistilBertForSequenceClassification.from_pretrained(params['model_name'], num_labels=len(labels))
model.config.id2label = {i: label for i, label in enumerate(labels)}
params["id2label"] = model.config.id2label

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)

# Define optimizer 
optimizer = AdamW(model.parameters(), lr=params['learning_rate'])


# Evaluation function
# durante il training implementeremo una evaluation alla fine di ciascuna epoch 
# in tal modo sapremo come la performance del nostro modello evolve metre si addestra
# creiamo una funzione custom dove passiamo un batch di inputs per il modello 
# ed ottenendo i labels predetti dal modello calcoliamo alcune metriche.
def evaluate_model(model, dataloader, device):
    model.eval()
    predictions, true_labels = [], []

    with torch.no_grad():
        for batch in dataloader:
            inputs, masks, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch['label'].to(device)

            # forward pass 
            outputs = model(inputs, attention_mask=masks)
            logits = outputs.logits
            _, predicted_labels = torch.max(logits, dim=1)

            predictions.extend(predicted_labels.cpu().detach().numpy())
            true_labels.extend(labels.cpu().detach().numpy())

    # calculate metrics
    # utilizziamo le metriche classiche per un task di classificazione
    # accuracy, F1 precision e recall
    acc = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predictions, average="macro")

    return acc, precision, recall, f1


# Trainig loop
# facciamo un semplice training loop, preparando gli inputs e poi li passiamo 
# al modello, calcolando la loss
# infine facciamo un backward pass prima di ciascun learninf step

with tqdm(total=params['num_epochs'] * len(train_loader), desc=f"Epoch [1/{params['num_epochs']}] - (Loss: N/A) - Steps") as pbar:
    for epoch in range(params["num_epochs"]):
        running_loss = 0.0
        for i, batch in enumerate(train_loader, 0):
            inputs, masks, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(inputs, attention_mask=masks, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # ora che abbiamo la loss la tracciamo per evitare overflowing
            # tracciamo ad ogni step ovvero ogni 100 steps come definito nei params
            # quindi ogni 100 batch ciasuno contenente 16 righe del train dataset
            # dunque ogni 1600 esempi tracciamo la loss
            if i and i % params["log_steps"] == 0:
                avg_loss = running_loss / params['log_steps']

                pbar.set_description(f"Epoch [{epoch + 1}/{params['num_epochs']}] - (Loss: {avg_loss:.3f}) - Steps")
                mlflow.log_metric("loss", avg_loss, step=epoch*len(train_loader)+i)
                running_loss = 0.0
            
            pbar.update(1)

        # Evaluate model
        # valutiamo il modello dopo ciascuna epoca usando il metodo che abiamo già scritto
        # gli passiamo il modello ed i dati e lasciamo che calcoli le metriche del modello sul
        # dataset di test
        acc, precision, recall, f1 = evaluate_model(model, test_loader, device)

        print("Epoch: {}, Accuracy: {}, Precision: {}, Recall: {}, F1: {}".format(epoch, acc, precision, recall, f1))

        # Log Metrics
        # dopo che abbiamo ottenuto le metriche dobbiamo tracciarle in MLflow
        # per avere le performance del nostro modello registrate
        mlflow.log_metrics({"accuracy": acc, "precision": precision, "recall": recall, "f1": f1})


        # l'ultima cosa che dobbiamo aggiungere è la progress bar
        # in modo che possiamo vedere cosa accade durante il traning
        # la progress bar nel training sono essenziali dato che forniscono 
        # un feedback visivo immediato
        
# Save model
# salviamo il modello in artifact
# Log model to MLflow through built-in PyTorch method
# mlflow.pytorch.log_model(model, "model")

# Log model to MLflow through custom method
# salviamo il modello sul disco
os.makedirs(params['output_dir'], exist_ok=True)
model.save_pretrained(params['output_dir'])
tokenizer.save_pretrained(params['output_dir'])

mlflow.log_artifacts(params['output_dir'], artifact_path="custom_model")

# ora con il modello loggato come artifact, l'ultima cosa che dobbiamo fare è
# registrarlo come un effettivo modello. Lo facciamo cosicchè poi mlflow lo tratti come tale
# vediamo infatti che lo tratta come un modello e non come una semplice directory

# ciò che rende speciali i modelli e diversi dagli artifacts è che essi possono vivere
# nel model registry. Ciò significa che possono essere versionati, allestiti e integrati in altri runs e pipelines
model_uri = f"runs:/{run.info.run_id}/model"
mlflow.register_model(model_uri, "agnews-transformer")

print('Finished Training')

# End run
mlflow.end_run()


