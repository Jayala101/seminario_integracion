# invoices/services/pdf.py
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

def render_pdf_from_template(template_path, context, filename):
    html = render_to_string(template_path, context)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result, encoding='utf-8')
    if pisa_status.err:
        # fallback: devolver HTML si falla PDF
        return HttpResponse(html)
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"{filename}\"'
    return response
