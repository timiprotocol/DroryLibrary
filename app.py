import streamlit as st
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import os

# Megjelenés beállítása
st.set_page_config(page_title="Drory Könyvtár AI", page_icon="📚", layout="centered")

# --- AI BEÁLLÍTÁS (A Secrets-ből olvassa) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Hiba az API kulccsal. Ellenőrizd a Streamlit Secrets beállításait!")
    st.stop()

st.title("📚 Drory AI Könyvtár")
st.write("Szia Szarah! Csak fotózd le a könyv borítóját, és én elmentem neked!")

# --- ADATBÁZIS KAPCSOLAT ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Nem sikerült kapcsolódni a Google Táblázathoz.")
    st.stop()

# --- FOTÓ KÉSZÍTÉSE ---
img_file = st.camera_input("Kamera megnyitása")

if img_file:
    with st.spinner("Az AI éppen elemzi a könyvet... 🤖"):
        try:
            # Kép beolvasása
            img = Image.open(img_file)
            
            # AI kérése: Ismerje fel a könyvet magyarul
            prompt = "Identify this book from the image. Tell me the Title and the Author in Hungarian. Format: Cím: [title], Szerző: [author]"
            response = model.generate_content([prompt, img])
            ai_text = response.text
            
            st.success("Könyv azonosítva!")
            st.info(ai_text)

            # Mentés gomb
            if st.button("💾 Mentés az adatbázisba"):
                # Táblázat beolvasása (ügyelj, hogy a Munkalap1 név stimmeljen!)
                existing_data = conn.read(worksheet="Munkalap1")
                
                # Új sor létrehozása
                new_row = pd.DataFrame([{"Cím és Szerző": ai_text, "Dátum": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}])
                
                # Összefűzés és frissítés
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(worksheet="Munkalap1", data=updated_df)
                
                st.balloons()
                st.success("Sikeresen elmentve a Google Táblázatba!")
        
        except Exception as e:
            st.error(f"Hiba történt az elemzés során: {e}")

st.divider()
st.subheader("📋 Eddig elmentett könyvek")
try:
    df = conn.read(worksheet="Munkalap1")
    st.dataframe(df, use_container_width=True)
except:
    st.write("A lista még üres.")
