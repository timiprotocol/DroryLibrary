import streamlit as st
import requests

st.set_page_config(page_title="Anya Könyvtára", page_icon="📚")

st.title("📚 Könyvtár Regisztráló")

# Bevitel: lehet ISBN vagy akár a könyv címe is!
query = st.text_input("Írd be az ISBN kódot vagy a könyv címét:")

if query:
    st.info(f"Keresés: {query}...")
    
    # Tisztítás: ha csak számok és szóközök vannak, ISBN-ként kezeljük
    clean_query = query.replace("-", "").replace(" ", "")
    
    # Google Books API keresés (univerzális kereső)
    url = f"https://www.googleapis.com/books/v1/volumes?q={clean_query}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            # Kilistázzuk az első 3 találatot, hogy anyu választhasson, ha több van
            st.write("Ezeket találtam, válaszd ki a megfelelőt:")
            
            for item in data["items"][:3]:
                book_info = item["volumeInfo"]
                title = book_info.get("title", "Ismeretlen cím")
                authors = ", ".join(book_info.get("authors", ["Ismeretlen szerző"]))
                thumb = book_info.get("imageLinks", {}).get("thumbnail", "")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if thumb:
                        st.image(thumb)
                with col2:
                    st.markdown(f"**{title}**")
                    st.write(f"Szerző: {authors}")
                    if st.button(f"Mentés: {title[:20]}...", key=item["id"]):
                        with open("konyvtar.csv", "a", encoding="utf-8") as f:
                            f.write(f"{title};{authors}\n")
                        st.success(f"Elmentve: {title}")
                        st.balloons()
        else:
            st.error("Sajnos így sem találtam meg. Próbáld meg csak a könyv címét beírni!")
            
    except Exception as e:
        st.error(f"Hiba történt: {e}")

st.divider()
st.subheader("📚 Mentett könyvek")
try:
    with open("konyvtar.csv", "r", encoding="utf-8") as f:
        rows = f.readlines()
        for row in reversed(rows):
            st.text(f"📖 {row.strip()}")
except FileNotFoundError:
    st.info("Még üres a lista.")
