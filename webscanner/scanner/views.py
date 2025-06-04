import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Target
from .utils.sqlmap_client import start_sqlmap_scan


def format_vulnerabilities(raw_data):
    vulnerabilities = []
    for item in raw_data:
        vulnerabilities.append({
            "type": item.get("type", "Unknown"),
            "description": item.get("title", "No description"),
            "severity": get_severity(item.get("type", ""))
        })
    return vulnerabilities


def get_severity(vuln_type):
    vuln_type = str(vuln_type).lower()
    if "error" in vuln_type:
        return "High"
    elif "boolean" in vuln_type or "blind" in vuln_type:
        return "Medium"
    elif "union" in vuln_type:
        return "High"
    elif "time" in vuln_type:
        return "High"
    return "Low"


def get_description(vuln_type):
    vuln_type = str(vuln_type).lower()
    if "error" in vuln_type:
        return "Ошибка SQL-запроса, позволяющая извлечь информацию о базе данных."
    elif "boolean" in vuln_type or "blind" in vuln_type:
        return "Слепая SQL-инъекция, основанная на логических условиях."
    elif "union" in vuln_type:
        return "SQL-инъекция через объединение нескольких запросов (UNION)."
    elif "time" in vuln_type:
        return "SQL-инъекция, выявляемая через задержку выполнения (time-based)."
    return "Общая или неизвестная SQL-инъекция."


def home(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            target, created = Target.objects.get_or_create(url=url)
            return redirect('scan', pk=target.pk)

    targets = Target.objects.all().order_by('-created_at')
    return render(request, 'scanner/home.html', {'targets': targets})


def scan(request, pk):
    target = get_object_or_404(Target, pk=pk)

    # Запуск сканирования через sqlmap API
    result = start_sqlmap_scan(target.url)

    # Сохраняем результат
    if result:
        target.report = result
        target.save()

    return redirect('report', pk=pk)


def report(request, pk):
    target = get_object_or_404(Target, pk=pk)
    result = target.report or {}
    vulns = result.get("data", [])

    # Добавим поле severity к каждой уязвимости
    for vuln in vulns:
        vuln_type = vuln.get("type", "")
        vuln["severity"] = get_severity(vuln_type)
        vuln["description"] = get_description(vuln_type)

    return render(request, 'scanner/report.html', {
        'target': target,
        'vulnerabilities': vulns,
    })


def export_pdf(request, pk):
    target = get_object_or_404(Target, pk=pk)
    raw_result = target.report or {}
    vulnerabilities = format_vulnerabilities(raw_result.get('data', []))

    template_path = 'scanner/pdf_template.html'
    context = {'target': target, 'vulnerabilities': vulnerabilities}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Ошибка генерации PDF', status=500)
    return response
