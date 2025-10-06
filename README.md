# DataAudit.io - MVP

## Description
Small MVP that accepts dataset uploads (CSV / Excel), runs an automated data quality & EDA pipeline and returns a downloadable report (HTML + optional PDF summary).

## Quick start (local)
1. Create virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

Notes:
- `pdfkit` conversion requires `wkhtmltopdf` installed on the host if you want full HTML->PDF conversion.
- For production / payments, configure Stripe and SendGrid credentials in `.env`.
