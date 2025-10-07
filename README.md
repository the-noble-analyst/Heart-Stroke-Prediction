# Heart Disease Prediction App

A machine learning web application built with Streamlit that predicts a patient's risk of heart disease based on health parameters.

## 🚀 Features
- Predicts the likelihood of heart disease using a trained KNN classifier.
- Interactive Streamlit UI for real-time input and predictions.
- Fully preprocessed dataset with outlier handling and feature engineering.
- EDA with visualizations (box plots, violin plots, heatmaps).
- Trained multiple models: Logistic Regression, KNN, Naive Bayes, SVM, Decision Tree.
- Achieved up to **88.6% accuracy** with the KNN model.

## 📊 Dataset
- Source: `heart.csv`
- Records: 918
- Features: Age, Gender, Chest Pain Type, RestingBP, Cholesterol, MaxHR, etc.

## ⚙️ Tech Stack
- Python (Pandas, NumPy, Scikit-learn, Seaborn)
- Streamlit (for web UI)
- Together AI api key for AI chatbot integration
- Joblib (for saving model, scaler, and feature schema)

## 🛠 How it Works
1. **Data Preprocessing**:
   - Replaced 0s in `Cholesterol` and `RestingBP` with mean values.
   - One-hot encoded categorical variables.
   - Standardized numerical features using `StandardScaler`.

2. **Model Training**:
   - Split data into train/test sets using `train_test_split`.
   - Trained 5 ML models and evaluated using accuracy and F1-score.
   - Selected KNN for deployment.

3. **Deployment**:
   - Saved trained KNN model and scaler using `joblib`.
   - Built a Streamlit app to collect input and make predictions with AI chatbot integration.
   - App ensures proper feature ordering and scaling for inference.
   - 

## 📦 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
