
from django.contrib import admin
from .models import User, Attendance

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name', 'registered_date')
    search_fields = ('userid', 'name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'status')
    list_filter = ('date', 'status')
    search_fields = ('user__userid', 'user__name')
