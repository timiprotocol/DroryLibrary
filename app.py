import streamlit as st

st.set_page_config(page_title="Anyu Könyvtára", page_icon="📚")

# Ez a rész felel azért, hogy az adatok ne vesszenek el frissítéskor
if 'konyvek' not in st.session_state:
    st.session_state.konyvek = []

st.title("📚 Könyvtár Mentés Teszt")

# Adatbevitel
cime = st.text_input("Könyv címe:")
szerzo = st.text_input("Szerző:")

if st.button("Hozzáadás a listához"):
    if cime:
        # Új könyv hozzáadása a memóriához
        uj_konyv = {"cim": cime, "szerzo": szerzo}
        st.session_state.konyvek.append(uj_konyv)
        st.success(f"Sikeresen hozzáadva: {cime}")
        st.balloons()
    else:
        st.error("A címet kötelező kitölteni!")

st.divider()
st.subheader("📋 Regisztrált könyvek listája")

# Itt jelenítjük meg a listát
if st.session_state.konyvek:
    for i, konyv in enumerate(reversed(st.session_state.konyvek)):
        st.info(f"{len(st.session_state.konyvek) - i}. {konyv['cim']} (Szerző: {konyv['szerzo']})")
else:
    st.write("Még nincs semmi a listában.")
