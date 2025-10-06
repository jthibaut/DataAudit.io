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
            report_html = analyze_dataset(input_path, tmp_dir)
            st.success("Rapport HTML généré ✅")

            # Show basic preview (iframe)
            st.markdown("**Aperçu du rapport (HTML)**")
            with open(report_html, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=600, scrolling=True)

            # Offer download
            with open(report_html, "rb") as f:
                st.download_button("Télécharger le rapport (HTML)", f, file_name=os.path.basename(report_html))

            # Generate small PDF summary (ReportLab) and offer download
            pdf_path = os.path.join(tmp_dir, "summary_report.pdf")
            generate_summary_pdf(report_html, pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("Télécharger le résumé (PDF)", f, file_name="rapport_resume.pdf")

            st.info("Pour automatiser emailing et paiements, configurez Stripe/SendGrid et déployez le backend FastAPI.")

        except Exception as e:
            st.error(f"Erreur pendant l'analyse : {e}")