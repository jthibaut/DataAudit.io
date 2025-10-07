import streamlit as st
import tempfile
import os
from pipeline.analyze import analyze_dataset
from pipeline.report import generate_summary_pdf
from utils.file_utils import save_uploaded_file

st.set_page_config(page_title="DataAudit.io - MVP", layout="centered")

st.title("🧠 DataAudit.io — Audit automatique de dataset")
st.write("Téléversez un fichier CSV ou Excel. Le rapport HTML sera généré automatiquement.")

uploaded_file = st.file_uploader("Choisir un fichier", type=["csv", "xlsx"])
email = st.text_input("Email (optionnel, pour recevoir le rapport)")

if uploaded_file:
    with st.spinner("Analyse en cours — ceci peut prendre quelques secondes..."):
        tmp_dir = tempfile.mkdtemp()
        input_path = save_uploaded_file(uploaded_file, tmp_dir)

        try:
            # === Étape 1 : Génération du rapport HTML via ydata_profiling ===
            report_html = analyze_dataset(input_path, tmp_dir)
            st.success("Rapport HTML généré ✅")

            # === Étape 2 : Affichage d’un aperçu HTML ===
            st.markdown("**Aperçu du rapport (HTML)**")
            with open(report_html, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=600, scrolling=True)

            # === Paiement ===
            if st.button("Payer et recevoir le rapport par email", key="pay_button_main"):
                response = requests.post("https://dataaudit-backend.onrender.com/create-checkout-session", json={"email": email, "file_url": hosted_report_url},)
                checkout_url = response.json().get("url")
                if checkout_url:
                    st.markdown(f"[👉 Accéder au paiement]({checkout_url})")

            # === Étape 3 : Téléchargement du rapport HTML complet ===
#            with open(report_html, "rb") as f:
#                st.download_button("Télécharger le rapport (HTML)", f, file_name=os.path.basename(report_html), mime="text/html")

            # # === Étape 4 : Génération du résumé PDF (version ReportLab) ===
            # summary_text = """
            # Rapport de DataAudit.io
            # ------------------------
            # Fichier analysé : {uploaded_file.name}

            # Ce rapport contient une analyse automatisée du dataset :
            # - Statistiques descriptives
            # - Analyse de distribution
            # - Corrélations et valeurs manquantes
            # - Avertissements éventuels

            # Rapport complet disponible au format HTML.
            # """
            # pdf_bytes = generate_summary_pdf(summary_text)

            # st.download_button(
            #     "📄 Télécharger le résumé (PDF)",
            #     data=pdf_bytes,
            #     file_name="rapport_resume.pdf",
            #     mime="application/pdf"
            # )

            # st.info("📬 Prochaine étape : automatiser l’envoi d’email et le paiement (Stripe + SendGrid).")
            
        except Exception as e:
            st.error(f"Erreur pendant l'analyse : {e}")

            import requests

