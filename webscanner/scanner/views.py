import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Target
from .utils.sqlmap_client import start_sqlmap_scan
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from .sql_injection_checker import test_sql_injection




def format_vulnerabilities(raw_data):
    vulnerabilities = []
    for item in raw_data:
        vuln_type = item.get("type", "Unknown")
        vulnerabilities.append({
            "type": vuln_type,
            "description": get_description(vuln_type),
            "severity": get_severity(vuln_type)
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
        return "Ошибка базы данных позволяет определить структуру SQL-запроса."
    elif "boolean" in vuln_type or "blind" in vuln_type:
        return "Слепая SQL-инъекция с использованием логических выражений."
    elif "union" in vuln_type:
        return "UNION-инъекция позволяет извлечь данные из других таблиц."
    elif "time" in vuln_type:
        return "SQL-инъекция с задержкой времени, возможна без вывода ошибки."
    return "Общая или неизвестная SQL-инъекция."


def check_sql(request, pk):
    target = get_object_or_404(Target, pk=pk)
    base_url = target.url
    results = test_sql_injection(base_url)

    # Отобразим в шаблоне
    return render(request, 'scanner/sql_results.html', {
        'target': target,
        'results': results
    })



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

    for vuln in vulns:
        vuln_type = vuln.get("type", "")
        vuln["severity"] = get_severity(vuln_type)
        vuln["description"] = get_description(vuln_type)

    sqli_results = []
    if "?" in target.url:
        sqli_results = test_sql_injection(target.url)

    return render(request, 'scanner/report.html', {
        'target': target,
        'vulnerabilities': vulns,
        'sqli_results': sqli_results,  # ← добавили
    })



def export_pdf(request, target_id):
    target = Target.objects.get(id=target_id)
    raw_result = target.report or {}
    vulnerabilities = format_vulnerabilities(raw_result.get('data', []))
    sqli_results = test_sql_injection(target.url)

    html_string = render_to_string('scanner/pdf_template.html', {
        'target': target,
        'vulnerabilities': vulnerabilities,
        'sqli_results': sqli_results  # ← добавили
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="scan_report_{target_id}.pdf"'
    return response

