import os
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render,redirect
import pdfkit
import subprocess
from .models import temp_table
from django.db.models import Count, Q

REPORTS_DIR = "D:/gtn/reports"
OUTPUT_DIR = os.path.join(REPORTS_DIR, "output")
HTML_REPORT_PATH = os.path.join(OUTPUT_DIR, "generated_report.html")


from django.db.models import Count, Q
from django.shortcuts import render
from .models import temp_table

def home(request):
    group_by = request.GET.get('group_by', 'Plantcode')  # Default: Group by Plantcode

    # Group data dynamically based on selected filter (Plantcode or Shiftcode)
    grouped_data = (
        temp_table.objects.values(group_by)
        .annotate(
            total_employees=Count('EmpID', distinct=True),
            total_present=Count('EmpID', filter=Q(Attn='P')),
            total_absent=Count('EmpID', filter=Q(Attn='AB')),
            total_leave=Count('EmpID', filter=Q(Status='L')),
            total_weekoff=Count('EmpID', filter=Q(Status='WO')),
        )
        .order_by(group_by)
    )

    # Overall statistics
    total_employees = temp_table.objects.count()
    present_employees = temp_table.objects.filter(Attn="P").count()
    absent_employees = temp_table.objects.filter(Attn="AB").count()
    leave_employees = temp_table.objects.filter(Status="L").count()
    weekoff_employees = temp_table.objects.filter(Status="WO").count()
    in_count = temp_table.objects.filter(Status="In").count()
    out_count = temp_table.objects.filter(Status="Out").count()

    # Prepare grouped statistics for the bar chart
    grouped_chart_data = {
        "labels": [],
        "total": [],
        "present": [],
        "absent": [],
        "leave": [],
        "weekoff": [],
    }

    # Populate chart data dynamically
    for record in grouped_data:
        label = record[group_by]
        grouped_chart_data["labels"].append(label)
        grouped_chart_data["total"].append(record['total_employees'])
        grouped_chart_data["present"].append(record['total_present'])
        grouped_chart_data["absent"].append(record['total_absent'])
        grouped_chart_data["leave"].append(record['total_leave'])
        grouped_chart_data["weekoff"].append(record['total_weekoff'])

    context = {
        "grouped_data": grouped_data,
        "group_by": group_by,
        "total_employees": total_employees,
        "present_employees": present_employees,
        "absent_employees": absent_employees,
        "leave_employees": leave_employees,
        "weekoff_employees": weekoff_employees,
        "grouped_chart_data": grouped_chart_data,
        "in_count": in_count,
        "out_count": out_count,
    }

    return render(request, "home.html", context)



def get_employee_details(request):
    """Fetch employee details for the selected group and category."""
    group_by = request.GET.get('group_by')  # Either Plantcode or Shiftcode
    group_value = request.GET.get('group_value')  # Specific group (e.g., 'HK')
    category = request.GET.get('category')  # 'total', 'present', or 'absent'

    if not group_by or not group_value:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    # Base query filtered by group
    employees = temp_table.objects.filter(**{group_by: group_value})

    # Filter further based on category
    if category == 'present':
        employees = employees.filter(Attn='P')
    elif category == 'absent':
        employees = employees.filter(Attn='AB')

    employee_list = list(employees.values('EmpID', 'Biorefno', 'Plantcode', 'Shiftcode', 'Attndt', 'Status'))

    return JsonResponse({'employees': employee_list})


def reports(request):
    plantcodes = temp_table.objects.values_list('Plantcode', flat=True).distinct()
    shiftcodes = temp_table.objects.values_list('Shiftcode', flat=True).distinct()
    Statuses = temp_table.objects.values_list('Status', flat=True).distinct()

    context = {
        'plantcodes': plantcodes,
        'shiftcodes': shiftcodes,
        'Statuses': Statuses
    }
    return render(request, 'reportbox.html', context)

def generate_report(request):
    try:
        plantcode_filter = request.GET.get('plantcode', "").strip()
        shiftcode_filter = request.GET.get('shiftcode', "").strip()
        status_filter = request.GET.get('Status', "").strip()

        if not plantcode_filter and not shiftcode_filter and not status_filter:
            return HttpResponse("Error: Please select at least one filter.", status=400)

        os.chdir(REPORTS_DIR)

        classpath = (
            ".;D:/gtn/reports/jasperreports-6.20.0.jar;"
            "D:/gtn/reports/mysql-connector-j-8.0.33.jar;"
            "D:/gtn/reports/commons-logging-1.2.jar;"
            "D:/gtn/reports/commons-digester-2.1.jar;"
            "D:/gtn/reports/commons-collections4-4.4.jar;"
            "D:/gtn/reports/commons-beanutils-1.9.4.jar"
        )

        java_command = [
            "java",
            "-cp", classpath,
            "GenerateReport",
            plantcode_filter if plantcode_filter else "ALL",
            shiftcode_filter if shiftcode_filter else "ALL",
            status_filter if status_filter else "ALL"
        ]

        process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return HttpResponse(f"Error running the report:\n{stderr.decode('utf-8')}\n{stdout.decode('utf-8')}", status=500)

        return redirect('view_report')

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def view_report(request):
    """Render the generated HTML report."""
    # Path to the generated HTML report
    html_report_path = "D:/gtn/reports/output/generated_report.html"

    if os.path.exists(html_report_path):
        with open(html_report_path, "r", encoding="utf-8") as file:
            report_content = file.read()
        return render(request, "view_report.html", {"report_content": report_content})
    else:
        return HttpResponse("Report not found.", status=404)


def download_pdf(request):
    # Configure pdfkit to use the downloaded wkhtmltopdf binary
    config = pdfkit.configuration(wkhtmltopdf=r'D:\gtn\tools\wkhtmltopdf\bin\wkhtmltopdf.exe')


    # Path to your HTML file (you can use a local file or HTML string)
    html_path = "D:/gtn/reports/output/generated_report.html"  # Update with the actual path
    
    # If the HTML is stored as a string (optional)
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Generate PDF from HTML content (you can also directly provide the HTML string here)
    pdf = pdfkit.from_string(html_content, False, configuration=config)

    # Return the PDF as a downloadable response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated_report.pdf"'
    return response