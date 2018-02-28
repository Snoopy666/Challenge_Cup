from django.shortcuts import render
from labeled_data.models import User, LabelId, Data
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

law_list = [
    ('罪名1', 0),
    ('罪名2', 1),
    ('罪名3', 2),
    ('罪名4', 3),
    ('罪名5', 4),
    ('罪名6', 5),
    ('罪名7', 6),
    ('罪名8', 7)
]


@require_http_methods(["GET"])
def index(request, **kwargs):
    user = request.session.get('user', None)
    if user is None:
        return render(request, 'index.html', { 'logined': False })
    else:
        try:
            nwuser = User.objects.get(pk=user)

            if nwuser.labeling is None:
                return render(request, 'index.html', {
                    'logined': True,
                    'is_label': False,
                    'user_name': nwuser.name,
                    'law_list': law_list
                })
            else:
                labels = [(label.name. label.label_id) for label in LabelId.objects.filter(crit=nwuser.labeling.crit)]
                return render(request, 'index.html', {
                    'logined': True,
                    'is_label': True,
                    'active': nwuser.labeling.crit,
                    'user_name': nwuser.name,
                    'law_list': law_list,
                    'law_article': nwuser.labeling.data,
                    'labels': labels
                })

        except User.DoesNotExist as err:    # User not found
            request.session['user'] = None
            return render(request, 'index.html', {'logined': False})


@csrf_exempt
@require_http_methods(["POST"])
def login(request, **kwargs):
    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST.get('name', ''))
            request.session['user'] = user.pk
            return HttpResponse(
                json.dumps({'status': 'ok', 'reason': user.name}),
                content_type="application/json")
        except User.DoesNotExist as e:
            return HttpResponse(
                json.dumps({'status': 'err', 'reason': 'user not found'}),
                content_type="application/json")
    return HttpResponseBadRequest()


def getUser(uid):
    if uid is None:
        return None
    try:
        nwuser = User.objects.get(pk=uid)
        return nwuser
    except User.DoesNotExist as err:
        return None


@csrf_exempt
@require_http_methods(["POST"])
def changeCrit(request, **kwargs):
    bid = request.POST.get('bid', None)
    user = getUser(request.session.get('user', None))

    if request.method == 'POST' and (bid is not None) and (user is not None):
        try:
            nwlabel = Data.objects.filter(crit=bid, status='U')[0]
        except IndexError as e:
            return HttpResponse(
                json.dumps({'status': 'err', 'reason': 'no unlabeled data'}),
                content_type="application/json")
        nwlabel.status = 'I'
        nwlabel.save()
        if user.labeling is not None:
            user.labeling.status = 'U'
            user.labeling.save()
            user.labeling = None
            user.save()
        user.labeling = nwlabel
        return HttpResponse(
                json.dumps({'status': 'ok', 'reason': nwlabel.pk}),
                content_type="application/json")
    return HttpResponseBadRequest()


@csrf_exempt
@require_http_methods(["POST"])
def quit(request, **kwargs):
    user = getUser(request.session.get('user', None))

    if request.method == 'POST' and (user is not None):
        if user.labeling is not None:
            user.labeling.status = 'U'
            user.labeling.save()
            user.labeling = None
            user.save()
        return HttpResponse(
            json.dumps({'status': 'ok'}),
            content_type="application/json")
    return HttpResponseBadRequest()


@csrf_exempt
@require_http_methods(["POST"])
def save(request, **kwargs):
    user = getUser(request.session.get('user', None))
    data = request.POST.get('data', '')
    label = request.POST.get('label', '')
    if request.method == 'POST' and (user is not None) and (user.labeling is not None):
        if user.labeling.data == data and len(data) == len(label):
            user.labeling.status = 'L'
            user.labeling.label = label
            user.labeling.save()
            user.labeling = None
            user.save()
            return HttpResponse(
                json.dumps({'status': 'ok'}),
                content_type="application/json")
    return HttpResponseBadRequest()