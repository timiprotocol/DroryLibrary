import streamlit as st
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import io

st.set_page_config(page_title="Drory Könyvtár AI", page_icon="📚")

# --- AI BEÁLLÍTÁS ---
# Ide kell majd az API kulcsod az AI Studióból!
os_api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=os_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📚 Drory AI Könyvtár")

# --- ADATBÁZIS KAPCSOLAT ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FOTÓ KÉSZÍTÉSE ---
st.subheader("Fényképezd le a könyv borítóját!")
img_file = st.camera_input("Kamera megnyitása")

if img_file:
    st.info("AI elemzés folyamatban... 🤖")
    
    # Kép előkészítése az AI-nak
    img = Image.open(img_file)
    
    # AI kérése: Ismerje fel a könyvet
    prompt = "Identify this book from the image. Provide the Title, Author, and ISBN if possible in this format: Title: [title], Author: [author], ISBN: [isbn]"
    response = model.generate_content([prompt, img])
    
    # Adatok kinyerése a válaszból
    ai_text = response.text
    st.write("AI válasza:", ai_text)

    # Egyszerű mentés gomb
    if st.button("Mentés a Google Táblázatba"):
        # Itt elmentjük a táblázatba (feltételezve, hogy a Munkalap1 létezik)
        existing_data = conn.read(worksheet="Munkalap1")
        new_row = pd.DataFrame([{"Cím": ai_text, "Dátum": pd.Timestamp.now()}])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Munkalap1", data=updated_df)
        st.success("Sikeresen elmentve!")
        st.balloons()

st.divider()
st.subheader("📋 Eddigi könyvek listája")
try:
    df = conn.read(worksheet="Munkalap1")
    st.dataframe(df)
except:
    st.info("Még nincs mentett adat a táblázatban.")
