from django.shortcuts import render

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import models

import json

from WebLabeler.utils.converter import TimeConverter

# Create your views here.
def test(request):
    return render(request, 'WebLabeler/test.html', {
    })


# login / logout
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('front'))
    return render(request, 'WebLabeler/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('front'))


#
def front(request):
    return render(request, 'WebLabeler/front.html', {
    })


@login_required(login_url='/WebLabeler/login/')
def list_page(request, media_page):
    page_item_size = 10
    max_pages_size = 10
    media_count = models.Media.objects.count()
    if not media_count:
        media_count = 0
    max_page = int(round(media_count / page_item_size + 0.5))

    page_cur = int(media_page)
    pages_start = page_cur - int(max_pages_size/2)
    if pages_start < 1:
        pages_start = 1

    pages_end = pages_start + max_pages_size
    if pages_end > max_page:
        pages_start += (max_page - pages_end)
        pages_end = max_page

    if pages_start < 1:
        pages_start = 1

    pages = []
    for i in range(pages_start, pages_end+1):
        pages = pages + [i]

    medias = models.Media.objects.all().order_by('-pk')[(page_cur - 1) * page_item_size:page_cur * page_item_size]

    return render(request, 'WebLabeler/list.html',
                  {'medias' : medias, 'pages' : pages, 'page_cur' : page_cur})


@login_required(login_url='/WebLabeler/login/')
def browse_media(request, media_id):
    media = models.Media.objects.get(pk=media_id)
    info = models.ContentInformation.objects.get(media__pk=media_id)
    shots = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum')

    return render(request, 'WebLabeler/browse.html',
                  {'media' : media,
                   'info': info,
                   'shots': shots,
                   })


@login_required(login_url='/WebLabeler/login/')
def edit_media_sbd_manual(request, media_id):
    media = models.Media.objects.get(pk=media_id)
    info = models.ContentInformation.objects.get(media__pk=media_id)

    shots = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum')[:5]
    max_shots = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum').count()

    return render(request, 'WebLabeler/media_edit_sbd_manual.html',
                  {'media' : media,
                   'info': info,
                   'shots': shots,
                   'max_shots': max_shots,
                   })


def edit_media_sbd_add_shots(request):
    print request.POST
    media_pk = request.POST['mediaPK']

#    try:
    timecode_lines = request.POST['timecodes'].split('\r\n')
    for timecode_line in timecode_lines:
        timecode = timecode_line.split('\t')
        print timecode[0], timecode[1]
        models.Shot.add_shot_by_timecode(media_id=media_pk, startTimecode=timecode[0], endTimecode=timecode[1])
    models.Shot.reorder_shots(media_id=media_pk)
#    except:
#        return HttpResponseRedirect(reverse('front'))
    return HttpResponseRedirect(request.POST['requestURL'])


@login_required(login_url='/WebLabeler/login/')
def edit_media_person(request, media_id):
    media = models.Media.objects.get(pk=media_id)
    info = models.ContentInformation.objects.get(media__pk=media_id)

    shots = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum')[:5]
    max_shots = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum').count()

    return render(request, 'WebLabeler/media_edit_person.html',
                  {'media' : media,
                   'info': info,
                   'shots': shots,
                   'max_shots': max_shots,
                   })


@login_required(login_url='/WebLabeler/login/')
def edit_media_person_page(request, media_id, shot_num):
    media = models.Media.objects.get(pk=media_id)
    info = models.ContentInformation.objects.get(media__pk=media_id)

    shot = models.Shot.objects.get(media__pk=media_id, shotNum=shot_num)
    shot_max = models.Shot.objects.filter(media__pk=media_id).order_by('shotNum').count()

    return render(request, 'WebLabeler/media_edit_person_page.html',
                  {'media' : media,
                   'info': info,
                   'shot': shot,
                   'shot_num': shot_num,
                   'shot_max': shot_max,
                   })



@login_required(login_url='/WebLabeler/login/')
def upload(request):
    return render(request, 'WebLabeler/upload.html', {
    })


def util_image_ajax(request):
    response_datas = []

    if request.GET['name'] == 'getFrameURL':
        response_data = {}
        mediaNum = int(request.GET['mediaNum'])
        frameNum = int(request.GET['frameNum'])
        response_data['tagID'] = request.GET['tagID']
        response_data['URL'] = models.get_frame_url(mediaNum, frameNum)

    response_datas.append(response_data)

    return HttpResponse(json.dumps(response_datas), content_type="application/json")