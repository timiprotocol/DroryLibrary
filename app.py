import streamlit as st
import requests

st.set_page_config(page_title="Anya Könyvtára", page_icon="📚")

st.title("📚 Könyvtár Regisztráló")
st.write("Írd be a vonalkódot vagy használd a szkennert!")

# Egyszerűbb beviteli mező az első teszthez
barcode = st.text_input("Vonalkód (ISBN):")

if barcode:
    st.info(f"Keresés: {barcode}")
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            title = book_info.get("title", "Ismeretlen cím")
            authors = ", ".join(book_info.get("authors", ["Ismeretlen szerző"]))
            thumbnail = book_info.get("imageLinks", {}).get("thumbnail", "")

            st.subheader(f"📖 {title}")
            st.write(f"**Szerző:** {authors}")
            if thumbnail:
                st.image(thumbnail)
            
            if st.button("Mentés a listába"):
                with open("konyvtar.csv", "a", encoding="utf-8") as f:
                    f.write(f"{barcode};{title};{authors}\n")
                st.success("Könyv elmentve!")
                st.balloons()
        else:
            st.warning("Nem találtam ilyen könyvet. Próbáld másik kóddal!")
    except Exception as e:
        st.error(f"Hiba történt a keresés közben: {e}")

st.divider()
st.subheader("Már regisztrált könyvek")
try:
    with open("konyvtar.csv", "r", encoding="utf-8") as f:
        rows = f.readlines()
        for row in rows:
            st.text(row.strip())
except FileNotFoundError:
    st.info("Még nincs mentett könyv.")
