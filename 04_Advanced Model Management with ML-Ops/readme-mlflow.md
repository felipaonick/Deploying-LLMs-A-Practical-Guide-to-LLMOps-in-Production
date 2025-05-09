# Section 4 - Model Management & ML-Ops


Below is a guide and Bash commands to set up MLflow on an Ubuntu system. This setup includes installing MLflow, setting up a backend store for experiments and runs, and launching the MLflow UI.

### MLflow Setup Guide for Ubuntu

#### Prerequisites:
- Python 3.6 or higher
- Pip (Python package installer)
- Ubuntu system (or a similar Linux distribution)




### Step 1: Create custom user (optional)

Setting up a custom user for MLflow and a dedicated Python environment is a good practice, especially for ensuring that the MLflow service runs securely and isolated from other system processes. Here's how you can set it up on an Ubuntu system:

1. **Create the User**:
   Open a terminal and run the following command to create a new user called `mlflow`.
   ```bash
   sudo adduser mlflow
   ```

2. **Grant Sudo Privileges (Optional)**:
   If this user needs to perform administrative tasks, you can grant it sudo privileges. Otherwise, you can skip this step.
   ```bash
   sudo usermod -aG sudo mlflow
   ```

### Step 2: Install Python and Create an Environment

1. **Switch to the mlflow User**:
   Switch to the new user account.
   ```bash
   su - mlflow
   ```

2. **Install Python3 and Pip**:
   Ensure Python3 and Pip are installed. Most Ubuntu versions come with Python3 by default, but you might need to install pip.
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

3. **Install Virtualenv**:
   Virtualenv is a tool to create isolated Python environments.
   ```bash
   pip3 install virtualenv
   or 
   sudo apt install python3-virtualenv
   ```

4. **Create a Virtual Environment**:
   Create a new directory for the MLflow server and navigate into it. Then create a virtual environment.
   ```bash
   mkdir ~/mlflow_server
   cd ~/mlflow_server
   virtualenv mlflow_env
   ```

5. **Activate the Virtual Environment**:
   Before installing MLflow and other dependencies, activate the virtual environment.
   ```bash
   source mlflow_env/bin/activate
   ```

### Step 3: Install MLflow
With the virtual environment activated, install MLflow. If you want to ensure compatibility, use the same versions I use in the course. If you'd like to use the latest, make sure to use matching versions for the other libraries.

```bash
pip install mlflow==2.7.1
```


### Step 4: Install Backend Store (Optional)
MLflow uses a tracking server to log experiment data. By default, it logs to the local filesystem, but for more robust use, you may want to set up a database like MySQL or SQLite.

**For SQLite (Simpler Option):**
- SQLite comes pre-installed on many systems, including Ubuntu.
- Decide on a directory where you want your SQLite database to reside
```bash
cd ~/mlflow_server
mkdir metrics_store
```

**For MySQL:**
- Install MySQL Server:
  ```bash
  sudo apt update
  sudo apt install mysql-server
  ```
- Secure your installation and set up your user (follow the prompt after the command):
  ```bash
  sudo mysql_secure_installation
  ```
- Log into MySQL to create a database for MLflow:
  ```bash
  sudo mysql -u root -p
  ```
- Once inside MySQL, create a database:
  ```mysql
  CREATE DATABASE mlflow_db;
  EXIT;
  ```

### Step 5: Set Backend Store for MLflow
- **For SQLite**, you'll use a URI like: `sqlite:////home/mlflow/mlflow_server/metrics_store/mlflow.db`
- **For MySQL**, the URI will be: `mysql://<username>:<password>@localhost/mlflow_db`


### Step 6: Install Artifact Store
The artifact store is where MLflow saves model artifacts like models and plots. You can use S3, Azure Blob Storage, Google Cloud Storage, or even a shared filesystem.

- **For local storage (simplest for getting started)**, use a local directory.
```bash
cd ~/mlflow_server
mkdir artifact_store
```




### Step 7: Launch MLflow Tracking Server
Open a terminal and run the following command, replacing the URIs with your chosen backend and artifact store paths:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow-artifacts


mlflow server --backend-store-uri sqlite:////home/mlflow/mlflow_server/metrics_store/mlflow.db --default-artifact-root file:///home/mlflow/mlflow_server/artifact_store/
```

Replace `sqlite:///mlflow.db` with your MySQL URI if you're using MySQL, and adjust `./mlflow-artifacts` to the path where you want artifacts stored.

### Step 8: Accessing the MLflow UI
- Once the tracking server is running, it will display a URL, typically `http://127.0.0.1:5000`. Open this URL in a web browser to access the MLflow UI.
- You can now navigate the UI to see your experiments, runs, metrics, and artifacts.
```bash
ssh -L 5000:localhost:5000 remote
```


#### Additional Tips:
- **Service**: For a more permanent setup, you might want to set up MLflow to run as a service or use a process manager like `supervisor` to manage the server process.
- **Security**: If you're setting this up on a cloud server or an exposed machine, ensure you configure proper security settings, including firewalls and authentication for the MLflow server.

### Conclusion
You now have MLflow set up on your Ubuntu system with a backend store for tracking experiments and an artifact store for saving model artifacts. You can start running experiments and tracking them using the MLflow Python library, and all your experiment details will be accessible through the MLflow UI.