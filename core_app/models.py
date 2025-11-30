from django.db import models

from django.db import models

class User(models.Model):
    userid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    image = models.BinaryField(null=True, blank=True)   # store raw image bytes (BLOB)
    registered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userid} - {self.name}"

class Attendance(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    capture_image = models.BinaryField(null=True, blank=True)  # BLOB of captured image
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # to be updated after compare

    def __str__(self):
        user_repr = self.user.userid if self.user else "Unknown"
        return f"{user_repr} | {self.date} {self.time} | {self.status}"
