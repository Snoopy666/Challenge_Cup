from django.shortcuts import render
from labeled_data.models import User, LabelId, Data, Label
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


MAX_NUM_LABEL = 3
law_list = [
    ('抢夺', 0),
    ('抢劫', 1),
    ('滥伐林木', 2),
    ('故意伤害', 3),
    ('故意杀人', 4),
    ('容留他人吸毒', 5)
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
                labels = [(label.name, label.label_id) for label in LabelId.objects.filter(crit=nwuser.labeling.crit)]
                return render(request, 'index.html', {
                    'logined': True,
                    'is_label': True,
                    'active': nwuser.labeling.crit,
                    'user_name': nwuser.name,
                    'law_list': law_list,
                    'law_article': json.dumps(nwuser.labeling.data),
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
        if user.allowed_crit != -1 and user.allowed_crit != bid:
            return HttpResponse(
                json.dumps({'status': 'err', 'reason': 'Permission denied.'}),
                content_type="application/json")
        try:

            nwlabel = Data.objects.filter(
                Q(crit=bid) & Q(num_labeled__lt=MAX_NUM_LABEL)
                & ~Q(pk__in= user.label_set.all().values('data'))
                )[0]
        except IndexError as e:
            return HttpResponse(
                json.dumps({'status': 'err', 'reason': 'no unlabeled data.'}),
                content_type="application/json")
        nwlabel.num_labeled += 1
        nwlabel.num_labeling += 1
        nwlabel.save()

        if user.labeling is not None:
            user.labeling.num_labeled -= 1
            user.labeling.num_labeling -= 1
            user.labeling.save()
            user.labeling = None
        user.labeling = nwlabel
        user.save()
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
            user.labeling.num_labeled -= 1
            user.labeling.num_labeling -= 1
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
            Label(data=user.labeling, label=label, author=user).save()
            user.labeling.num_labeling -= 1
            user.labeling.save()
            user.labeling = None
            user.num_labeled += 1
            user.save()
            return HttpResponse(
                json.dumps({'status': 'ok'}),
                content_type="application/json")
    return HttpResponseBadRequest()
