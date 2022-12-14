from sys import maxsize
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

import os
from django.core.exceptions import ValidationError
import magic

# VIDEO-----VALIDATORS------START

def validate_is_mp4(file):
    valid_mime_types = ['video/mp4', 'video/mpeg',]
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type. Acceptable files are .MPEG and .MP4 only')
    valid_file_extensions = ['.MP4', '.mp4', '.mpeg', '.MPEG',]
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension. Acceptable files are .MP4 .MPEG')

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



class State(models.Model):
    name = models.CharField(max_length=25)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name 




class SituationReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_video')
    title = models.CharField(max_length=75)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='video_state')
    lga = models.CharField(max_length=20)
    ward = models.CharField(max_length=20)
    polling_unit = models.CharField(max_length=20)
    video = models.FileField(upload_to="report_video/%Y/%m/%d/", validators=(validate_is_mp4, validate_file_size,))
    brief_description = models.TextField(max_length=150, null=True, blank=True)
    published = models.BooleanField(default=False)
    main = models.BooleanField(default=False)
    like = models.ManyToManyField(User, related_name='like_blog_post', blank=True)
    dislike = models.ManyToManyField(User, related_name='blog_post', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def total_downvote(self):
        return self.dislike.count()

    def total_upvote(self):
        return self.like.count()


    def __str__(self):
        return '{} || by ====> {}'.format(self.video, self.user)

    def get_absolute_url(self):
        return reverse("dashboard")



class ViewCount(models.Model):
    video = models.ForeignKey(SituationReport, related_name='View_counts', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50, null=True)
    session = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.ip_address}'