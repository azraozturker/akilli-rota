"""Akilli Rota projesinin Streamlit sitesi."""
import streamlit as st

st.set_page_config(page_title="Akıllı Rota", layout="wide")

st.title("Akıllı Rota Gerçeklemesi")
st.write(
    "Çelebi İHA takımı, Proje 8. Engellerden kaçan rota, "
    "rota sadeleştirme, rüzgâr altında sapma düzeltmesi ve "
    "hareketli hedefe yaklaşma."
)

rota_sekmesi, kontrol_sekmesi = st.tabs(["Rota", "Kontrol"])

with rota_sekmesi:
    st.info("Bu sekme hazırlanıyor.")

with kontrol_sekmesi:
    st.info("Bu sekme hazırlanıyor.")