import streamlit as st
import pandas as pd
import joblib

# Carrega els objectes guardats
label_encoder = joblib.load('Sprint9/models/label_encoder.pkl')
one_hot_columns = joblib.load('Sprint9/models/one_hot_columns.pkl')
pca_columns = joblib.load('Sprint9/models/pca_columns.pkl')
scaler = joblib.load('Sprint9/models/standard_scaler.pkl')
pca = joblib.load('Sprint9/models/pca_model.pkl')
model = joblib.load('Sprint9/models/model_lr_final.pkl')

# Configura la interfície d'usuari
st.title("Predicció de Contractació de Dipòsits Bancaris")

# Widgets per a la entrada de dades
age = st.number_input("Edat | Age", min_value=18, max_value=100, value=28)
job = st.selectbox("Feina | Job", ['admin.', 'technician', 'services', 'management', 'retired', 'self-employed', 'student', 'unemployed', 'unknown'])
marital = st.selectbox("Estat Civil | Marital", ['married', 'single', 'divorced'])
education = st.selectbox("Educació | Education", ['primary', 'secondary', 'tertiary', 'unknown'])
default = st.selectbox("Default Creditici | Default", ['no', 'yes'])
balance = st.number_input("Balanç | Balance", value=5000)
housing = st.selectbox("Préstec Hipotecari | Housing", ['no', 'yes'])
loan = st.selectbox("Préstec Personal | Loan", ['no', 'yes'])
contact = st.selectbox("Canal de Contacte | Contact", ['unknown', 'cellular', 'telephone'])
day = st.number_input("Dia del Mes | Day", min_value=1, max_value=31, value=15)
month = st.selectbox("Mes | Month", ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
duration = st.number_input("Duració (s) | Duration", value=300)  # Inclòs però s'eliminarà després
campaign = st.number_input("Nombre de Contactes | Campaign", min_value=1, value=1)
pdays = st.number_input("Dies des de l'Últim Contacte | Pdays", value=30)
previous = st.number_input("Contactes Previs | Previous", min_value=0, value=2)
poutcome = st.selectbox("Resultat Previ | Poutcome", ['unknown', 'failure', 'success', 'other'])

# Processament de les dades
if st.button("Prediu"):
    # Crear DataFrame amb les dades d'entrada
    input_data = {
        'age': [age],
        'job': [job],
        'marital': [marital],
        'education': [education],
        'default': [default],
        'balance': [balance],
        'housing': [housing],
        'loan': [loan],
        'contact': [contact],
        'day': [day],
        'month': [month],
        'duration': [duration],
        'campaign': [campaign],
        'pdays': [pdays],
        'previous': [previous],
        'poutcome': [poutcome]
    }
    input_df = pd.DataFrame(input_data)

    # Codificar variables binàries
    binary_cols = ['default', 'housing', 'loan']
    for col in binary_cols:
        input_df[col] = label_encoder.transform(input_df[col])

    # Aplicar One-Hot Encoding
    input_encoded = pd.get_dummies(input_df, columns=['job', 'marital', 'education', 'contact', 'month', 'poutcome'], dtype=int)
    
    # Assegurar totes les columnes originals (incloent 'duration' i 'contact_unknown')
    input_encoded = input_encoded.reindex(columns=one_hot_columns, fill_value=0)

    # Estandarditzar variables numèriques (incloent 'duration')
    numeric_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']
    input_encoded[numeric_cols] = scaler.transform(input_encoded[numeric_cols])

    # Eliminar 'duration' i 'contact_unknown' (després de l'escalat)
    input_encoded = input_encoded.drop(columns=['duration', 'contact_unknown'], errors='ignore')

    # Reindexar per al PCA
    input_encoded = input_encoded.reindex(columns=pca_columns, fill_value=0)

    # Aplicar PCA i fer la predicció
    input_pca = pca.transform(input_encoded)
    prediction = model.predict(input_pca)
    
    # Mostrar resultat
    resultat = "Sí" if prediction[0] == 1 else "No"
    st.success(f"**Predicció:** {resultat}")

    # Mostrar components principals (opcional)
    st.write("### Components Principals Actius")
    st.write(pd.DataFrame(input_pca, columns=[f"CP{i+1}" for i in range(18)]))