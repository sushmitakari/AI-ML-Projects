# 🚗 Predictive Maintenance - Capstone Project

This repository contains the complete end-to-end Machine Learning, MLOps, and Streamlit deployment solution for **Capstone Project 3: Predictive Maintenance (Engine Health Diagnostics)**.

---

## 📁 Google Colab Notebooks

| Notebook File | Milestone Scope | Sections Covered |
| :--- | :--- | :--- |
| **`Predictive_Maintenance_Interim_Submission.ipynb`** | **Interim Submission (40 Pts)** | 1. Data Registration<br>2. Exploratory Data Analysis (EDA)<br>3. Data Preparation<br>4. Model Building with Experimentation Tracking<br>5. Detailed Interim Observations |
| **`Predictive_Maintenance_Final_Submission.ipynb`** | **Final Submission (60 Pts)** | All 8 Sections: Data Registration, EDA, Data Prep, Model Building & Tracking, Model Deployment (Streamlit), GitHub Actions CI/CD Pipeline, Output Evaluation, Actionable Insights |

---

## 📂 Project Structure

```text
CapStone_Project/
├── Predictive_Maintenance_Interim_Submission.ipynb  # 🚀 Interim Submission Notebook
├── Predictive_Maintenance_Final_Submission.ipynb    # 🏆 Final Submission Notebook
├── app.py                                          # 🌐 Streamlit Web Application
├── requirements.txt                                # 📦 Project Dependencies
├── engine_data.csv                                 # 📊 Raw Sensor Telemetry Dataset
├── data/
│   ├── engine_data.csv                             # Master Registered Dataset
│   ├── train.csv                                   # Prepared Training Split (80%)
│   └── test.csv                                    # Prepared Testing Split (20%)
├── models/
│   ├── best_model.pkl                              # Champion Model Artifact (AdaBoost/Random Forest)
│   └── experiment_results.json                     # Logged Hyperparameters & Experiment Metrics
├── src/
│   ├── data_registration.py                        # Script 1: Schema & Data Integrity Validation
│   ├── data_preparation.py                         # Script 2: Data Cleaning & Stratified Splitting
│   └── model_training.py                           # Script 3: ML Training, Grid Search CV & Model Export
├── .github/
│   └── workflows/
│       └── pipeline.yml                            # ⚙️ GitHub Actions Automated CI/CD Workflow
└── README.md                                       # Documentation & Guide
```

---

## 🚀 Running on Google Colab

1. **Open Google Colab:** [colab.research.google.com](https://colab.research.google.com)
2. **Upload Notebook:** Click **File** > **Upload notebook** and choose either:
   - `Predictive_Maintenance_Interim_Submission.ipynb` (for Interim milestone)
   - `Predictive_Maintenance_Final_Submission.ipynb` (for Final milestone)
3. **Upload Dataset:** Upload `engine_data.csv` to the session files (or run the built-in ingestion cell).
4. **Run All Cells:** Click **Runtime** > **Run all** (`Ctrl + F9` / `Cmd + F9`).
5. **Convert to HTML (Mandatory Submission Format):**
   Run the following in a code cell at the end of the notebook:
   ```python
   !jupyter nbconvert --to html Predictive_Maintenance_Interim_Submission.ipynb
   ```
   or
   ```python
   !jupyter nbconvert --to html Predictive_Maintenance_Final_Submission.ipynb
   ```
