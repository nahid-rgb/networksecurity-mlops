# NetworkSecurity-MLOps

An end-to-end **Machine Learning and MLOps project** for detecting phishing websites.

The project covers the complete journey from **data ingestion and model training to experiment tracking, API development, Dockerization, CI/CD, and cloud deployment**.

**Live Demo:** https://networksecurity-mlops.onrender.com

---

## Project Overview

The project follows an end-to-end MLOps workflow:

1. **Project Setup & Packaging** — Set up the Python project, GitHub repository, virtual environment, and package structure using `setup.py`.
2. **Logging & Exception Handling** — Added centralized logging and custom exception handling for easier debugging.
3. **ETL & Data Ingestion** — Pulls phishing website data from MongoDB Atlas and prepares it for the ML pipeline.
4. **Data Validation** — Validates incoming data against the expected schema and checks for data drift.
5. **Data Transformation** — Handles missing values and prepares the numerical features for machine learning.
6. **Model Training & Evaluation** — Trains multiple ML models, performs hyperparameter tuning with `GridSearchCV`, and selects the best-performing model.
7. **MLflow & DagsHub** — Tracks experiments locally with MLflow and remotely through DagsHub.
8. **Model Pushing** — Saves the trained model and preprocessor and synchronizes required model/artifact files with Hugging Face Hub.
9. **FastAPI & Prediction** — Provides `/train`, `/train/status`, and `/predict` endpoints for training, monitoring, and prediction.
10. **Dockerization** — Packages the complete application and its dependencies into a Docker image.
11. **GitHub Actions CI/CD** — Automatically builds the Docker image and pushes it to Docker Hub whenever changes are pushed to `main`.
12. **Docker Hub** — Stores the Docker image used for deployment.
13. **Render Deployment** — Deploys the Docker image as a live FastAPI application.

---

## MLOps Architecture

```text
                         MongoDB Atlas
                              │
                              ▼
                       Data Ingestion
                              │
                              ▼
                       Data Validation
                              │
                              ▼
                    Data Transformation
                              │
                              ▼
                 Model Training & Evaluation
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
              MLflow                 Model / Artifacts
                 │                         │
                 ▼                         ▼
              DagsHub                Hugging Face Hub

                       Model + Application              
                              │
                              ▼
                           FastAPI
                              │
                              ▼
                            Docker
                              │
                              ▼
                       GitHub Actions(CI/CD)
                              │
                              ▼
                         Docker Hub
                              │
                              ▼
                           Render
                              │
                              ▼
                         Live API
```

---

# Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Database | MongoDB Atlas |
| Experiment Tracking | MLflow |
| Remote MLflow Tracking | DagsHub |
| Model/Artifact Sync | Hugging Face Hub |
| API | FastAPI |
| API Server | Uvicorn |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Container Registry | Docker Hub |
| Deployment | Render |

### AWS Note

**AWS S3, Amazon ECR, and EC2** these AWS services were not used in this implementation because the required resources are paid. Instead, this project uses **Hugging Face, Docker Hub, and Render** as the alternative workflow.

---

# Dataset

## Domain

**Phishing Website Detection**

The project uses a dataset containing approximately **11,000 labeled website samples**.

The data is stored in **MongoDB Atlas** and is pulled fresh from MongoDB when the training pipeline runs rather than relying on a static local CSV as the primary training source.

The MongoDB collection used by the project is:

```text
phishing_data
```

---

## Target Column

The target column is:

```text
Result
```

The **original dataset** represents the two classes using:

```text
-1
1
```

During the **Data Transformation** stage, these labels are converted into a simpler binary representation:

```text
0 → Legitimate website
1 → Phishing website
```

Therefore, after transformation, the machine learning model works with:

```text
0 = Legitimate
1 = Phishing
```

This conversion happens during the data transformation process.

---

## Input Features

The dataset contains **30 numerical website-related features**.

These features describe different characteristics of a website, including URL structure, SSL information, domain properties, redirects, external links, JavaScript behavior, DNS information, traffic, and search-engine information.

The features are already represented numerically, so the pipeline can process them directly without requiring text encoding.

Missing values are handled during Data Transformation using **KNNImputer**.

| Feature | What it represents |
|---|---|
| `having_IP_Address` | Whether the URL uses an IP address instead of a domain |
| `URL_Length` | Whether the URL has suspicious or unusual length |
| `Shortining_Service` | Whether a URL-shortening service is used |
| `having_At_Symbol` | Presence of `@` in the URL |
| `double_slash_redirecting` | Suspicious use of `//` for redirection |
| `Prefix_Suffix` | Suspicious use of `-` in the domain |
| `having_Sub_Domain` | Presence/level of subdomains |
| `SSLfinal_State` | SSL certificate/security characteristics |
| `Domain_registeration_length` | Domain registration duration |
| `Favicon` | Favicon/domain relationship |
| `port` | Use of ports associated with the website |
| `HTTPS_token` | Suspicious use of HTTPS-related tokens |
| `Request_URL` | External resources requested by the page |
| `URL_of_Anchor` | External/different-domain links in anchors |
| `Links_in_tags` | External links in HTML tags |
| `SFH` | Server Form Handler behavior |
| `Submitting_to_email` | Whether form data is submitted to an email |
| `Abnormal_URL` | Whether the URL shows abnormal domain behavior |
| `Redirect` | Redirect behavior |
| `on_mouseover` | Suspicious mouse-over JavaScript behavior |
| `RightClick` | Whether right-click is disabled |
| `popUpWidnow` | Presence of suspicious pop-up windows |
| `Iframe` | Use of iframe elements |
| `age_of_domain` | Domain age |
| `DNSRecord` | DNS record availability |
| `web_traffic` | Website traffic/popularity information |
| `Page_Rank` | Page ranking information |
| `Google_Index` | Whether the website is indexed by Google |
| `Links_pointing_to_page` | Number of links pointing to the page |
| `Statistical_report` | Presence in known phishing-related reports |

---

# Data Pipeline

The data pipeline follows:

```text
MongoDB Atlas
      ↓
Data Ingestion
      ↓
Data Validation
      ↓
Data Transformation
      ↓
Model Training
```

### Data Ingestion

Connects to MongoDB Atlas and retrieves the dataset required for training.

### Data Validation

Checks the incoming data against the expected schema and performs data-drift validation.

### Data Transformation

Prepares the data for machine learning, including handling missing values with `KNNImputer` and converting the target labels from the original `-1/1` representation into `0/1`.

---

# Model Training

The model-training component evaluates multiple machine learning models.

Hyperparameter tuning is performed using:

```text
GridSearchCV
```

The general process is:

```text
Multiple Models
      ↓
Hyperparameter Search
      ↓
Model Evaluation
      ↓
Best Model
      ↓
Save Model + Preprocessor
```

The best-performing model is selected based on the project's evaluation process rather than permanently assuming one specific algorithm will always be the best.

---

# MLflow & DagsHub

## MLflow

MLflow is used to track machine learning experiments.

It helps record information such as:

- Model parameters
- Evaluation metrics
- Experiment runs
- Model-related information

## DagsHub

DagsHub is used as the remote repository for MLflow experiment tracking.

This allows the experiment information to be accessed remotely rather than keeping everything only on the local machine.

---

# Model & Artifact Management

The trained model and preprocessing object are saved locally:

```text
final_model/
├── model.pkl
└── preprocessor.pkl
```

The project also synchronizes required model/artifact files with **Hugging Face Hub**.

The Hugging Face authentication token is supplied through an environment variable:

```text
HUGGINGFACE_TOKEN
```

Credentials are never stored directly in the source code.

---

# FastAPI Application

The FastAPI application is located in:

```text
app.py
```

The application is created with:

```python
app = FastAPI()
```

For local development, start the application with:

```cmd
uvicorn app:app --reload
```

The local API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## `GET /`

The root endpoint redirects visitors to:

```text
/docs
```

FastAPI automatically provides an interactive API documentation page at `/docs`, powered by **Swagger UI**.

It allows the API endpoints to be viewed and tested directly from the browser.

---

## `GET /train`

Starts the machine learning training pipeline.

The project originally ran the entire training pipeline directly inside this endpoint. Since training can take several minutes, the browser had to wait for the complete training process.

On Render's free tier, this long-running request could result in:

```text
502 Bad Gateway
```

even though the training process itself was still running.

The endpoint was therefore changed to use FastAPI's `BackgroundTasks`.

The current flow is:

```text
Browser
   ↓
GET /train
   ↓
"Training started"
   ↓
Browser gets immediate response
   ↓
Training continues in background
```

---

## `GET /train/status`

Checks the current training status.

Possible states are:

```text
idle
running
completed
failed
```

Example:

```json
{
  "status": "running"
}
```

After training finishes:

```json
{
  "status": "completed"
}
```

This endpoint provides a simple way to monitor the long-running training operation.

### BackgroundTasks limitation

`BackgroundTasks` is suitable for this learning project because it avoids introducing additional infrastructure such as Celery and Redis.

However, it is **not a production-grade job queue**.

If the Render service restarts, shuts down, or is interrupted while training is running, the background task can also be interrupted.

For a larger production system, a dedicated worker/job-queue architecture would be more appropriate.

---

## `POST /predict`

Accepts a CSV file containing website features and generates predictions using the saved model and preprocessor.

The process is:

```text
CSV File
   ↓
Load Preprocessor
   ↓
Load Model
   ↓
Transform Input
   ↓
Generate Prediction
   ↓
Add predicted_column
   ↓
Return Results
```

The generated prediction file is saved as:

```text
prediction_output/output.csv
```

---

# Docker

The application is packaged using Docker.

The Dockerfile uses Python 3.12:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update && pip install -r requirements.txt

CMD ["python3", "app.py"]
```

The Docker image contains:

```text
Application Code
+
Python Runtime
+
Python Dependencies
+
Application Configuration
```

This allows the same application environment to be used locally and during deployment.

---

# GitHub Actions CI/CD

GitHub Actions is used to automate the Docker build and delivery process.

The current workflow runs whenever code is pushed to:

```text
main
```

The deployment workflow is:

```text
GitHub
   ↓
Push to main
   ↓
GitHub Actions
   ↓
Continuous Integration
   ├── Checkout
   ├── Lint placeholder
   └── Test placeholder
   ↓
Continuous Delivery
   ├── Login to Docker Hub
   ├── Docker Build
   └── Docker Push
   ↓
Docker Hub
   ↓
Render
```

### Current CI Note

The current lint and test steps are placeholders:

```yaml
- name: Lint code
  run: echo "Linting repository"

- name: Run unit tests
  run: echo "Running unit tests"
```

They currently demonstrate the CI structure but do not perform actual linting or unit-test execution yet.

---

# GitHub Secrets

GitHub Actions authenticates with Docker Hub using two repository secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The workflow uses:

```yaml
username: ${{ secrets.DOCKERHUB_USERNAME }}
password: ${{ secrets.DOCKERHUB_TOKEN }}
```

The Docker Hub token is an **access token**, not the Docker Hub account password.

The actual token value is never stored in the repository.

---

# Docker Hub

After the GitHub Actions workflow successfully builds the Docker image, it pushes the image to Docker Hub.

The image is:

```text
nahidocker19/networksecurity-mlops:latest
```

The meaning is:

```text
nahidocker19
      ↓
Docker Hub username

networksecurity-mlops
      ↓
Repository/image name

latest
      ↓
Image tag
```

---

# Render Deployment

Render deploys the Docker image stored on Docker Hub.

The deployed image is:

```text
docker.io/nahidocker19/networksecurity-mlops:latest
```

The live application is available at:

```text
Live demo: https://networksecurity-mlops.onrender.com
```

---

# Render Environment Variables

The application requires the following environment variables on Render:

```text
MONGO_DB_URL
HUGGINGFACE_TOKEN
DAGSHUB_TOKEN
```

These are configured through Render's Environment Variables section.

Their actual values should never be committed to GitHub.

---

# Local Environment Variables

For local development, the required secrets are stored in a `.env` file:

```text
MONGO_DB_URL=your_mongodb_connection_string
HUGGINGFACE_TOKEN=your_huggingface_token
DAGSHUB_TOKEN=your_dagshub_token
```

The `.env` file is excluded from Git using `.gitignore`.

---

# Running Locally

## 1. Activate the environment

Using Command Prompt:

```cmd
conda activate venv
```

## 2. Install dependencies

```cmd
pip install -r requirements.txt
```

## 3. Start FastAPI

```cmd
uvicorn app:app --reload
```

## 4. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# Running with Docker

Build the image:

```cmd
docker build -t networksecurity-mlops .
```

Run it locally:

```cmd
docker run -p 8000:8000 --env-file .env networksecurity-mlops
```

Then open:

```text
http://localhost:8000/docs
```

---

# Git Workflow

The project uses Git and GitHub for source-code version control.

Typical workflow:

```text
Modify Code
    ↓
git add
    ↓
git commit
    ↓
git push
    ↓
GitHub Actions
```

Example:

```cmd
git add .
git commit -m "Update application"
git push origin main
```

A push to `main` automatically triggers the GitHub Actions workflow.

---

# Project Structure

```text
NetworkSecurity-MLOps/
│
├── .github/
│   └── workflows/
│       └── <workflow>.yml
│
├── networksecurity/
│   ├── __init__.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── constant/
│   │   ├── __init__.py
│   │   └── training_pipeline/
│   │       └── __init__.py
│   │
│   ├── entity/
│   │   ├── __init__.py
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   │
│   ├── exception/
│   │   ├── __init__.py
│   │   └── exception.py
│   │
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logger.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── training_pipeline.py
│   │   └── batch_prediction.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── main_utils/
│   │   │   ├── __init__.py
│   │   │   └── utils.py
│   │   │
│   │   └── ml_utils/
│   │       ├── __init__.py
│   │       ├── metric/
│   │       │   ├── __init__.py
│   │       │   └── classification_metric.py
│   │       │
│   │       └── model/
│   │           ├── __init__.py
│   │           └── estimator.py
│   │
│   └── cloud/
│       ├── __init__.py
│       ├── huggingface_auth.py
│       └── huggingface_syncer.py
│
├── data_schema/
│   └── schema.yaml
│
├── final_model/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── prediction_output/
│   └── output.csv
│
├── templates/
│   └── index.html
│
├── Artifacts/
├── logs/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── setup.py
├── .gitignore
├── .dockerignore
└── README.md
```

> **Note:** `Artifacts/` and `logs/` are generated during execution. The exact contents of generated directories can change depending on the training run.

---

# `.gitignore`

The project keeps secrets, virtual-environment files, generated artifacts, logs, and Python cache files out of Git:

```gitignore
# Virtual environment
venv/

# Environment variables / secrets
.env

# Generated ML artifacts
Artifacts/

# Logs
logs/

# Python cache
__pycache__/
*.pyc
```

The prediction output is intentionally kept in the repository for this project.

---

# Security

Never commit sensitive credentials such as:

```text
.env
MongoDB connection strings
MongoDB passwords
Docker Hub access tokens
DagsHub tokens
Hugging Face tokens
API keys
```

Use environment variables and GitHub/Render secrets instead.

---

# Complete Project Flow

The complete project can be viewed as two connected flows.

## ML Flow

```text
MongoDB Atlas
      ↓
Data Ingestion
      ↓
Data Validation
      ↓
Data Transformation
      ↓
Model Training
      ↓
Hyperparameter Tuning
      ↓
Model Evaluation
      ↓
MLflow
      ↓
DagsHub
      ↓
Model/Artifact Pushing
      ↓
Hugging Face
      ↓
FastAPI
```

## Deployment Flow

```text
Developer
     ↓
git push origin main
     ↓
GitHub
     ↓
GitHub Actions
     ↓
CI
     ↓
Docker Build
     ↓
Docker Hub
     ↓
Render
     ↓
Live FastAPI Application
```

Together:

```text
                 MACHINE LEARNING FLOW
                         │
                         ▼
                    Trained Model
                         │
                         ▼
                      FastAPI
                         │
                         ▼
                       Docker
                         │
                         ▼
                 GitHub Actions
                         │
                         ▼
                    Docker Hub
                         │
                         ▼
                       Render
                         │
                         ▼
                    Live API
```

The deployed FastAPI application provides the following endpoints:

```text
GET  /
GET  /train
GET  /train/status
POST /predict
```

The original AWS-based deployment stages were replaced with accessible alternatives for this implementation.

## Acknowledgment

Built by following Krish Naik's *End-to-End MLOps Bootcamp* (Udemy), adapted throughout to use free-tier alternatives (MongoDB Atlas, DagsHub, Hugging Face Hub, Docker Hub, Render) in place of AWS services, with additional debugging, refactoring, and background-task handling done independently.
