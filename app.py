import streamlit as st
import requests

st.set_page_config(page_title="Anya Könyvtára", page_icon="📚")

st.title("📚 Könyvtár Regisztráló")

# Segítség anyunak
st.info("Tipp: Az ISBN szám általában 978-al kezdődik a könyv hátulján.")

barcode = st.text_input("Írd be a vonalkódot (ISBN):")

if barcode:
    # 1. TISZTÍTÁS: Vegyük ki a kötőjeleket és szóközöket, csak a szám maradjon
    clean_barcode = "".join(filter(str.isdigit, barcode))
    
    if len(clean_barcode) < 10:
        st.warning("Ez a kód túl rövidnek tűnik. Az ISBN általában 10 vagy 13 számjegyből áll.")
    else:
        st.info(f"Keresés: {clean_barcode}...")
        
        # 2. KERESÉS: Több irányból is megpróbáljuk
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{clean_barcode}"
        
        try:
            response = requests.get(url)
            data = response.json()

            if "items" in data:
                book_info = data["items"][0]["volumeInfo"]
                title = book_info.get("title", "Ismeretlen cím")
                authors = ", ".join(book_info.get("authors", ["Ismeretlen szerző"]))
                thumbnail = book_info.get("imageLinks", {}).get("thumbnail", "")

                st.success("Megvan!")
                st.subheader(f"📖 {title}")
                st.write(f"**Szerző:** {authors}")
                
                if thumbnail:
                    st.image(thumbnail)
                
                if st.button("Mentés a listába"):
                    with open("konyvtar.csv", "a", encoding="utf-8") as f:
                        f.write(f"{clean_barcode};{title};{authors}\n")
                    st.balloons()
                    st.success("Elmentve!")
            else:
                # 3. HIBAKEZELÉS: Ha nincs az adatbázisban
                st.error("Sajnos ez a könyv nincs a Google adatbázisában.")
                st.write("Próbálj meg rákeresni a címére kézzel:")
                st.write(f"https://www.google.com/search?q=ISBN+{clean_barcode}")
                
        except Exception as e:
            st.error(f"Hálózati hiba történt: {e}")

st.divider()
st.subheader("📚 Eddigi könyvek")
try:
    with open("konyvtar.csv", "r", encoding="utf-8") as f:
        rows = f.readlines()
        for row in reversed(rows):
            st.text(f"✅ {row.strip()}")
except FileNotFoundError:
    st.info("Még üres a lista.")
