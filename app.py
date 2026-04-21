import streamlit as st
import requests

st.set_page_config(page_title="Anya Könyvtára", page_icon="📚")

st.title("📚 Könyvtár Regisztráló")

# Manuális bevitel - a Pixel billentyűzetén van mikrofon is, ha diktálni szeretné!
barcode = st.text_input("Szkenneld be vagy írd be a vonalkódot (ISBN):")

if barcode:
    # Tisztítsuk meg a bevitelt (csak számok maradjanak)
    clean_barcode = "".join(filter(str.isdigit, barcode))
    
    st.info(f"Keresés folyamatban: {clean_barcode}...")
    
    # Google Books API használata
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{clean_barcode}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            title = book_info.get("title", "Ismeretlen cím")
            authors = ", ".join(book_info.get("authors", ["Ismeretlen szerző"]))
            thumbnail = book_info.get("imageLinks", {}).get("thumbnail", "")

            st.success("Könyv megtalálva!")
            st.subheader(f"📖 {title}")
            st.write(f"**Szerző:** {authors}")
            
            if thumbnail:
                st.image(thumbnail)
            
            if st.button("Mentés a listába"):
                with open("konyvtar.csv", "a", encoding="utf-8") as f:
                    f.write(f"{clean_barcode};{title};{authors}\n")
                st.balloons()
                st.success("Elmentve a könyvtárba!")
        else:
            st.warning("Ezt a könyvet nem találtam a Google rendszerében. Próbáld meg kézzel beírni a listába?")
            
    except Exception as e:
        st.error(f"Hiba történt: {e}")

st.divider()
st.subheader("📚 Saját Könyvtár Lista")

try:
    with open("konyvtar.csv", "r", encoding="utf-8") as f:
        rows = f.readlines()
        if not rows:
            st.info("Még nincs mentett könyv.")
        else:
            for row in reversed(rows): # A legújabb legyen elöl
                st.text(f"✅ {row.strip()}")
except FileNotFoundError:
    st.info("A lista még üres. Kezdj el szkennelni!")
