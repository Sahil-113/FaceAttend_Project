import io
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import User, Attendance
from openpyxl import Workbook
from .compare import compare_faces
from datetime import datetime

# Home page
def home_view(request):
    return render(request, 'home.html')

# Registration page
def registration_page(request):
    return render(request, 'registration.html')

# Attendance page
def attendance_page(request):
    return render(request, 'attendance.html')


# Registration submit (expects multipart/form-data with 'userid','name' and 'image' file)
@csrf_exempt
@require_http_methods(["POST"])
def register_submit(request):
    userid = request.POST.get('userid')
    name = request.POST.get('name')
    img_file = request.FILES.get('image')

    if not userid or not name:
        return JsonResponse({'status': 'error', 'message': 'userid and name are required'}, status=400)

    if not img_file:
        return JsonResponse({'status': 'error', 'message': 'Image not received'}, status=400)

    try:
        img_bytes = img_file.read()
        user, created = User.objects.update_or_create(
            userid=userid,
            defaults={'name': name, 'image': img_bytes}
        )
        return JsonResponse({'status': 'success', 'message': 'Registration Successful'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Server error: ' + str(e)}, status=500)


# Attendance submit (expects 'userid' and 'image')
@csrf_exempt
@require_http_methods(["POST"])
def attendance_submit(request):
    print("POST DATA:", request.POST)
    print("FILES:", request.FILES)

    userid = request.POST.get('userid')
    if not userid:
        return JsonResponse({'status': 'error', 'message': 'userid is required'}, status=400)

    img_file = request.FILES.get("captured_image")
    if not img_file:
        return JsonResponse({'status': 'error', 'message': 'Image not received'}, status=400)

    # Read captured image bytes
    captured_bytes = img_file.read()

    # Find registered user
    user = User.objects.filter(userid=userid).first()
    if user is None:
        return JsonResponse({"status": "error", "message": "User not registered"}, status=400)

    registered_bytes = user.image

    # Compare faces
    match = compare_faces(registered_bytes, captured_bytes)

    if not match:
        return JsonResponse({"status": "error", "message": "Face mismatch"}, status=400)

    # Save attendance (IMPORTANT FIX → user= instead of userid=)
    Attendance.objects.create(
        user=user,
        capture_image=captured_bytes,
        status="Present"
    )

    return JsonResponse({"status": "success", "message": "Attendance recorded"})




# Excel download
def download_attendance(request):
    # Query attendance joined with user
    qs = Attendance.objects.select_related('user').order_by('date', 'time')

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    ws.append(['User ID', 'Name', 'Date', 'Time', 'Status'])

    for att in qs:
        uid = att.user.userid if att.user else ''
        name = att.user.name if att.user else ''
        ws.append([uid, name, att.date.strftime('%Y-%m-%d'), att.time.strftime('%H:%M:%S'), att.status])

    # Save workbook to in-memory bytes
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename=attendance_{ts}.xlsx'
    return response
