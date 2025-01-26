# Projecte-Machine-Learning
Repositori creat pel curs de Machine Learning de Barcelona Activa

---

# Documentació del Procés de Deploy

## Models i Arxius Carregats per Streamlit

Els següents models i arxius són essencials per al funcionament de l'aplicació:

| **Arxiu/Model**               | **Descripció**                                                                |
|-------------------------------|-------------------------------------------------------------------------------|
| `label_encoder.pkl`           | Codificador de variables binàries (`default`, `housing`, `loan`)              |
| `one_hot_columns.pkl`         | Llista de columnes generades després del One-Hot Encoding (inclou `duration`) |
| `pca_columns.pkl`             | Columnes utilitzades després d'eliminar `duration` i `contact_unknown`        |
| `standard_scaler.pkl`         | Estandarditzador de variables numèriques                                      |
| `pca_model.pkl`               | Model PCA amb 18 components principals                                        |
| `model_lr_final.pkl`          | Model entrenat de Regressió Logística per a prediccions                       |

---

## Arxius de Configuració

#### `requirements.txt`
Conté les dependències de Python necessàries:
```python
streamlit==1.40.1
scikit-learn==1.5.2
pandas==2.2.3
joblib==1.4.2
numpy==1.26.0
setuptools==70.0.0
wheel==0.43.0
scipy==1.14.1
python-dateutil==2.9.0
```

#### `runtime.txt`
Especifica la versió de Python que s'utilitzarà per a l'aplicació.
```python
python-version=3.11.10
```

#### `setup.sh`
Script per a configuracions addicionals:
```bash
#!/bin/bash
apt-get update && apt-get install -y python3-distutils
```

## Procés de Deploy

### 1. Preparació Local
1. **Instal·lar les dependències**:
   ```bash
   pip install -r requirements.txt

2. **Provar localment**:
   ```bash
   streamlit run app.py
   ```

## 2. Vinculació amb GitHub

1. **Crear un repositori públic** a GitHub amb tots els arxius necessaris:
   - `app.py`: El codi principal de l'aplicació Streamlit.
   - `requirements.txt`: Les dependències de Python necessàries.
   - Arxius `.pkl`: Models i objectes de preprocessament (`label_encoder.pkl`, `one_hot_columns.pkl`, `pca_columns.pkl`, `standard_scaler.pkl`, `pca_model.pkl`, `model_lr_final.pkl`).
   - Arxius de configuració opcionals: `runtime.txt` i `setup.sh`.

2. **Assegurar que el repositori sigui públic**, ja que Streamlit Sharing requereix accés públic per desplegar l'aplicació.

---

## 3. Desplegament a Streamlit Sharing

1. **Executar l'aplicació en local** per verificar que tot funcioni correctament:
   ```bash
   streamlit run app.py
   ```

2. **Crear un compte a Streamlit**. Iniciar sessió amb el compte de GitHub per vincular-lo.

3. **Vincular el compte de GitHub a Streamlit Sharing**. Això permetrà a Streamlit accedir als repositoris.

4. Realitzar un `git push` del codi al repositori de GitHub. Assegurar-se que tots els arxius necessaris (com `app.py`, `requirements.txt` i els arxius `.pkl`) estiguin inclosos.

5. Configurar l'aplicació a Streamlit Sharing:
   - **Repository**: Seleccionar el repositori de GitHub
   - **Branch**: Triar la branca on s'ha fet el push
   - **Main file path**: Indicar el camí de l'arxiu principal de l'aplicació (`app.py`)

6. **Clicar "Deploy"** per iniciar el procés de desplegament. Streamlit començarà a configurar l'entorn i a instal·lar les dependències.

7. Resoldre els errors que puguin aparèixer durant el desplegament. Aquests errors solen estar relacionats amb dependències faltants, arxius no trobats o versions incompatibles de Python. Consultar els logs per obtenir més informació i corregir els problemes al codi local abans de fer un nou `git push`.

8. Un cop resolts els errors, l'aplicació s'executarà correctament a Streamlit Sharing. S'hi podrà accedir mitjançant l'enllaç proporcionat per la plataforma.

---

## 4. Resolució d'Errors Comuns

Durant el procés de desplegament, poden aparèixer alguns errors comuns.

### **Error: "ModuleNotFoundError"**
- **Causa**: Falta una llibreria a l'entorn de desplegament.
- **Solució**: Afegeix la llibreria faltant al fitxer `requirements.txt` i fes un nou `git push`.

### **Error: "File not found: \*.pkl"**
- **Causa**: Els arxius `.pkl` no es troben al directori correcte o no s'han pujat al repositori.
- **Solució**: Assegura’t que els arxius `.pkl` estiguin al directori arrel del repositori i fes un nou `git push`.

### **Error: "Python version mismatch"**
- **Causa**: La versió de Python utilitzada localment no coincideix amb la del servidor de Streamlit.
- **Solució**: Especifica la versió correcta de Python al fitxer `runtime.txt` (per exemple, `python-3.10.12`).
