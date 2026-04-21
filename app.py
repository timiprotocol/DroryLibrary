import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Anyu Könyvtára", page_icon="📚")

st.title("📚 Könyv Adatbázis")

# Kapcsolat létrehozása a Google Táblázattal
conn = st.connection("gsheets", type=GSheetsConnection)

# Meglévő adatok beolvasása
existing_data = conn.read(worksheet="Sheet1", usecols=[0, 1], ttl=5)
existing_data = existing_data.dropna(how="all")

st.write("Illeszd be a könyv adatait:")

# Adatbevitel (a Pixel telefonon itt tud beilleszteni a Lens-ből)
uj_cim = st.text_input("Könyv címe:")
uj_szerzo = st.text_input("Szerző:")

if st.button("💾 Mentés az adatbázisba"):
    if uj_cim:
        # Új sor előkészítése
        new_row = pd.DataFrame([{"Cím": uj_cim, "Szerző": uj_szerzo}])
        
        # Hozzáadás a táblázathoz
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success(f"'{uj_cim}' elmentve az adatbázisba!")
        st.balloons()
        st.rerun() # Frissíti az oldalt, hogy látszódjon az új könyv
    else:
        st.error("A címet kötelező megadni!")

st.divider()
st.subheader("📋 A jelenlegi könyvtár:")
st.dataframe(existing_data, use_container_width=True)
