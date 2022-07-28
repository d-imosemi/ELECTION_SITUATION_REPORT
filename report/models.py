from sys import maxsize
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

import os
import magic
from django.core.exceptions import ValidationError


# VIDEO-----VALIDATORS------START

def validate_is_mp4(file):
    valid_mime_types = ['video/mp4', 'video/mpeg',]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.MP4', '.mp4', '.mpeg', '.MPEG',]
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension. Acceptable files are .MP4')

def validate_file_size(value):
    filesize= value.size
    
    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value

# VIDEO------VALIDATORS-------END



class DailyInspiration(models.Model):
    quote = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.quote   


class HeaderTitle(models.Model):
    title = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title 


# for authenticity sake, you must say your location in your video else it won't be published


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=50)
    candidate_image = models.ImageField(upload_to="candidate_image/%Y/%m/%d/")
    candidate_party = models.CharField(max_length=50)
    know_more = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.candidate_name 


# UPLOAD .MP4 AND MPEG-4 ONLY AND MAXIMUM SIZE OF VIDEO IS 10MB 
# CLICK THE LINK TO FREELY REDUCE THE SIZE of YOUR VIDEO  https://www.freeconvert.com/video-compressor

class SituationReport(models.Model):
    STATE = (
        ('F.C.T', 'F.C.T'),
        ('Abia', 'Abia'),
        ('Adamawa', 'Adamawa'),
       ('Akwa Ibom', ' Akwa Ibom'),
        ('Anambra', 'Anambra'),
        ('Bauchi', 'Bauchi'),
        ('Bayelsa', 'Bayelsa'),
        ('Benue', 'Benue'),
        ('Borno', 'Borno'),
        ('Cross River', 'Cross River'),
        ('Delta', 'Delta'),
        ('Ebonyi', 'Ebonyi'),
        ('Edo', 'Edo'),
        ('Ekiti', 'Ekiti'),
        ('Enugu', 'Enugu'),
        ('Gombe', 'Gombe'),
        ('Imo', 'Imo'),
        ('Jigawa', 'Jigawa'),
        ('Kaduna', 'Kaduna'),
        ('Kano', 'Kano'),
        ('Katsina', 'Katsina'),
        ('Kebbi', 'Kebbi'),
        ('Kogi', 'Kogi'),
        ('Kwara', 'Kwara'),
        ('Lagos', 'Lagos'),
        ('Nasarawa', 'Nasarawa'),
        ('Niger', 'Niger'),
        ('Ogun', 'Ogun'),
        ('Ondo', 'Ondo'),
        ('Osun', 'Osun'),
        ('Oyo', 'Oyo'),
        ('Plateau', 'Plateau'),
        ('Rivers', 'Rivers'),
        ('Sokoto', 'Sokoto'),
        ('Taraba', 'Taraba'),
        ('Yobe', 'Yobe'),
        ('Zamfara', 'Zamfara'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE)
    lga = models.CharField(max_length=20)
    ward = models.CharField(max_length=20)
    polling_unit = models.CharField(max_length=20)
    video = models.FileField(upload_to="report_video/%Y/%m/%d/", validators=(validate_is_mp4, validate_file_size,))
    brief_description = models.TextField(max_length=150, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return '{} || by ====> {}'.format(self.video, self.user)

    def get_absolute_url(self):
        return reverse("dashboard")