#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import os

import cv2
from django.conf import settings
from django.db import models
from django.utils import timezone

from WebLabeler.utils import extract_mp3
from WebLabeler.utils.converter import TimeConverter


def get_media_path(media):
    new_name = u'medias/' + \
               unicode(media.pk) + u'/'
    return new_name


def get_frame_url(mediaNum, frameNum):
    media = Media.objects.get(pk=mediaNum)

    # make path
    base_name = u"frame" + unicode(frameNum) + u".jpg"
    framePath = get_media_path(media) + u"frames/"
    frameURL = framePath + \
               unicode(os.path.basename(base_name))
    framePath = os.path.join(settings.MEDIA_ROOT, framePath)
    frameFilepath = os.path.join(settings.MEDIA_ROOT, frameURL)

    # make frame path
    if not os.path.exists(framePath):
        os.makedirs(framePath)

    # check file exist
    if not os.path.isfile(frameFilepath):
        safepath = media.localFile.path.encode('utf-8')
        vidcap = cv2.VideoCapture(safepath)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNum)
        success, image = vidcap.read()
        if success:
            print u"make new capture: " + frameFilepath
            cv2.imwrite(frameFilepath, image)
        else:
            print u"!!!FAILURE!!! make new capture: " + frameFilepath

    return frameURL


# Create your models here.
class Media(models.Model):
    programName = models.CharField(max_length=255)
    thumbnail = models.FileField(upload_to='medias/_temp/thumbnail/', blank=True)
    audioFile = models.FileField(upload_to='medias/_temp/', blank=True)
    localFile = models.FileField(upload_to='medias/_temp/')
    registerDateTime = models.DateTimeField(default=timezone.now)
    lastSavedDateTime = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return unicode(self.programName)

    def update_localPath(self):
        # Make Media Path
        initial_path = self.localFile.path
        new_name = get_media_path(self) + \
                   unicode(os.path.basename(self.localFile.name))
        new_path = os.path.join(settings.MEDIA_ROOT, new_name)

        # Check Path
        if initial_path != new_path:
            # Move the file on the filesystem
            if os.path.isfile(initial_path):
                self.localFile.name = new_name
                os.renames(initial_path, new_path)

        # Make Thumbnail Path
        # Warning!!! (need to refine code)
        initial_path = self.thumbnail.path
        new_name = get_media_path(self) + \
                   unicode(os.path.basename(self.thumbnail.name))
        new_path = os.path.join(settings.MEDIA_ROOT, new_name)

        # Check Path
        if initial_path != new_path:
            # Move the file on the filesystem
            if os.path.isfile(initial_path):
                self.thumbnail.name = new_name
                os.renames(initial_path, new_path)

        # Make Audio Path
        # Warning!!! (need to refine code)
        if self.audioFile:
            initial_path = self.audioFile.path
            new_name = get_media_path(self) + \
                       unicode(os.path.basename(self.audioFile.name))
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            # Check Path
            if initial_path != new_path:
                # Move the file on the filesystem
                if os.path.isfile(initial_path):
                    self.audioFile.name = new_name
                    os.renames(initial_path, new_path)
                else:
                    self.audioFile.name = ""
                # print u'rename from: ' + initial_path
                # print u'rename to: ' + new_path

    def make_audioFile(self):
        if not self.audioFile:
            media_path = self.localFile.path
            media_name = os.path.splitext(media_path)
            media_name = os.path.split(media_name[0])
            #print media_path, type(media_path)
            new_name = u'medias/_temp/' + \
                       media_name[1] + u".mp3"
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            #print new_path, type(new_path)
            ret = extract_mp3.extract(media_path, new_path)
            #print ret
            if ret:
                self.audioFile.name = new_name


    def make_thumbnail(self):
        if not self.thumbnail:
            safepath = self.localFile.path.encode('utf-8')
            vidcap = cv2.VideoCapture(safepath)
            success, image = vidcap.read()
            if success:
                # Make Path
                new_name = u'medias/_temp/' + \
                           u'thumb.jpg'
                new_path = os.path.join(settings.MEDIA_ROOT, new_name)

                cv2.imwrite(new_path, image)
                self.thumbnail.name = new_name

    def make_contentsInformation(self):
        info = ContentInformation.objects.filter(media__pk=self.pk).first()
        if not info:
            new_info = ContentInformation(media=self)
            new_info.save()

    def save(self, *args, **kwargs):
        self.lastSavedDateTime = timezone.now()
        # Call standard save first. (because in creation time, has no PK)
        super(Media, self).save(*args, **kwargs)
        self.make_contentsInformation()
        self.make_thumbnail()
        #self.make_audioFile()
        self.update_localPath()

        super(Media, self).save()

    '''






    def reset_to_uploaded(self):
        print u'RESET ' + self.programName + u'(' + unicode(self.pk) + u')'
        #scenes = Scene.objects.filter(media__pk=self.pk)
        shots = Shot.objects.filter(media__pk=self.pk)
        #scene_tags = SceneTag.objects.filter(media__pk=self.pk)
        #shot_tags = ShotTag.objects.filter(media__pk=self.pk)

        #for shot_tag in shot_tags:
        #    shot_tag.delete()
        #for scene_tag in scene_tags:
        #    scene_tag.delete()
        #for scene in scenes:
        #    scene.delete()
        for shot in shots:
            shot.delete()
        self.status = status_default()
        self.save()
'''


class ContentInformation(models.Model):
    media = models.ForeignKey(Media)
    # fileFormat = models.CharField(max_length=255)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    framerate = models.FloatField(default=0)
    duration = models.DurationField(default=0)

    def __unicode__(self):
        return unicode(self.media)

    def save(self, *args, **kwargs):
        safepath = self.media.localFile.path.encode('utf-8')
        vidcap = cv2.VideoCapture(safepath)
        self.framerate = vidcap.get(cv2.CAP_PROP_FPS)
        self.width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = datetime.timedelta(seconds=count/self.framerate) # BUG!!!!!
        super(ContentInformation, self).save()


class Shot(models.Model):
    media = models.ForeignKey(Media)
    shotNum = models.IntegerField(default=0)
    startFrame = models.IntegerField(default=0)
    endFrame = models.IntegerField(default=0)
    startTimestamp = models.CharField(max_length=255, blank=True)
    endTimestamp = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        name = unicode(self.media.programName) + u' SHOT(' + unicode(self.shotNum) + u')'
        return name

    def make_timestamp(self, frame, framerate):
        tc = TimeConverter(frame_rate=framerate)
        tc.set_framenum(frame)
        return tc.get_timestamp()

    def save(self, *args, **kwargs):
        info = ContentInformation.objects.get(media__pk=self.media.pk)
        self.startTimestamp = self.make_timestamp(frame=self.startFrame, framerate=info.framerate)
        self.endTimestamp = self.make_timestamp(frame=self.endFrame, framerate=info.framerate)
        super(Shot, self).save(*args, **kwargs)

    @classmethod
    def add_shot(request, media_id, startFrame, endFrame):
        safe_margin = 2
        media = Media.objects.get(pk=media_id)
        new_shot = Shot(media=media, shotNum=0, startFrame=startFrame + safe_margin, endFrame=endFrame - safe_margin)
        new_shot.save()

    @classmethod
    def add_shot_by_timecode(request, media_id, startTimecode, endTimecode):
        print "start timecode add"
        info = ContentInformation.objects.get(media__pk=media_id)
        tc = TimeConverter(frame_rate=info.framerate)
        tc.set_timecode(startTimecode)
        startFrame = tc.get_framenum()
        tc.set_timecode(endTimecode)
        endFrame = tc.get_framenum()
        Shot.add_shot(media_id=media_id, startFrame=startFrame, endFrame=endFrame)

    @classmethod
    def reorder_shots(request, media_id):
        shots = Shot.objects.filter(media__pk=media_id).order_by('startFrame')
        shotNum = 0
        for shot in shots:
            shotNum += 1
            if shot.shotNum != shotNum:
                shot.shotNum = shotNum
                shot.save()
