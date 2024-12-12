# Procés de Recol·lecció de Dades

## 1. Fonts de Dades

### Identificació de Fonts
Les dades emprades provenen de registres interns d’una entitat bancària que ha dut a terme diverses campanyes de màrqueting telefònic. També s’utilitza la base de dades històrica de clients, que conté informació demogràfica, financera i històrics de comunicacions anteriors.

### Descripció de les Fonts
- **Base de dades de clients**: Conté informació personal (edat, ocupació, estat civil, nivell educatiu), dades sobre crèdits (préstecs hipotecaris i personals) i saldos mitjans anuals.
- **Registres d’activitats de campanyes de màrqueting**: Inclou els contactes efectuats durant una campanya específica.

---

## 2. Mètodes de Recol·lecció de Dades

### Procediments i Eines Utilitzades
**Integració amb sistemes interns**:  
Les dades dels clients provenen directament del CRM (HubSpot) del banc, que conté totes les dades històriques dels clients, que ja es tenien prèviament a la campanya, i és on es registren les noves dades adquirides a través de les trucades telefòniques.

### Freqüència de Recol·lecció
- **Dades històriques**: Es mantenen estables tret d’actualitzacions puntuals.
- **Noves dades**: S’afegeixen diàriament a través d’una rutina de descàrrega automàtica utilitzant l’API de HubSpot.

### Scripts de Descàrrega
Una vegada es configura HubSpot per accedir i extreure dades de forma programada, es genera el següent script personalitzat en Python. A més a més, s’utilitza el planificador `cron` (en Linux) per descarregar les dades cada dia a les 23:59h.


```python
import requests
import pandas as pd
from datetime import datetime

# clau API de HubSpot
API_KEY = "TEVA_CLAU_API"
URL = f"https://api.hubapi.com/contacts/v1/lists/all/contacts/all?hapikey={API_KEY}"

def export_hubspot_data():
    # fem la petició GET
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        
        # processem les dades
        contacts = []
        for contact in data.get("contacts", []):
            contacts.append({
                "age": contact["properties"].get("age", {}).get("value", ""),
                "job": contact["properties"].get("job", {}).get("value", ""),
                "marital": contact["properties"].get("marital", {}).get("value", ""),
                # afegir les altres variables restants
            })

        # convertim dades (diccionari) a un dataframe de pandas
        df = pd.DataFrame(contacts)
        
        # desa el dataframe a un fitxer CSV
        filename = f"hubspot_contacts_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"Dades exportades a {filename}")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    export_hubspot_data()
```

---

## 3. Format i Estructura de les Dades

### Tipus de Dades Recopilades
- **Numèrics**: `age`, `balance`, `duration`, `campaign`, `pdays`, `previous`
- **Categòrics**: `job`, `marital`, `education`, `contact`, `poutcome`
- **Binàries**: `default`, `housing`, `loan`, `y`
- **Date**: `day_of_week`, `month`

### Format d'Emmagatzematge
- Les dades s’exporten a fitxers CSV directament des de HubSpot per facilitar el seu ús en anàlisi i models predictius. Els fitxers contenen una primera fila amb els noms de les columnes i dades delimitades per comes (,).

---

## 4. Limitacions de les Dades

### Qualitat i Precisió
- Variables com `job`, `marital`, `education`, `contact` o `poutcome` poden contenir la categoria “unknown”.
- La variable `pdays` pot tenir el valor `-1`, indicant que el client no va ser contactat anteriorment.

### Diferents Dates d'Actualització
- Les dades històriques i les dades adquirides durant la campanya poden no estar perfectament sincronitzades. L’estat civil, per exemple, pot haver variat sense que això s’hagi tingut en compte a l’exportar les dades des del CRM.

---

## 5. Consideracions sobre Dades Sensibles

### Tipus de Dades Sensibles
Donat que es tracta d’un projecte per un banc, les dades més sensibles són les personals (`age`, `job`, `marital` i `education`). Les dades financeres, que en altres contextos es considerarien sensibles, en aquest cas no s’hi consideren.

### Mesures de Protecció
- **Anonimització**: Eliminació d’identificadors directes dels clients.
- **Accés Restringit**: Només el personal autoritzat té accés a les dades.
- **Compliment amb Normatives**: GDPR i altres estàndards aplicables.