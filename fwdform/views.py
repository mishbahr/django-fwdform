# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect, render_to_response
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .akismet import Akismet
from .exceptions import EmptyFormError, FwdFormError
from .forms import FwdFormModelForm
from .helpers import get_next_url, send_mail
from .models import FwdForm, Site

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500


def handle_error(message, reason=None, status=HTTP_400_BAD_REQUEST,
                 json_response=False, extra_context=None):

    default_errors = {
        HTTP_400_BAD_REQUEST: 'badRequest',
        HTTP_404_NOT_FOUND: 'notFound',
        HTTP_500_INTERNAL_SERVER_ERROR: 'internalError',
    }

    if reason is None:  # pragma: no cover
        reason = default_errors.get(status, '')

    context = {
        'status': status,
        'code': status,
        'reason': reason,
        'message': force_text(message),
    }

    if extra_context is not None:
        context.update(extra_context)

    if json_response:
        return JsonResponse(context, status=status)
    return render_to_response('fwdform/error.html', context, status=status)


@csrf_exempt
@require_POST
def create_or_update_form(request, hashid):
    json_response = True

    try:
        site = Site.objects.get_by_hashid(hashid=hashid)
    except Site.DoesNotExist:
        message = _('Site does not exist.')
        return handle_error(message, status=HTTP_404_NOT_FOUND, json_response=json_response)

    data = {
        'site': site.id,
        'name': request.POST.get('name'),
        'recipients': request.POST.get('recipients'),
        'next': request.POST.get('next')
    }

    data = dict((k, v) for k, v in six.iteritems(data) if v)
    error_message = _('Make sure all fields are entered and valid.')

    form_id = request.POST.get('hashid', None)
    if form_id is not None:
        try:
            form_instance = FwdForm.objects.get_by_hashid(hashid=form_id)
        except FwdForm.DoesNotExist:  # pragma: no cover
            form_instance = None

        if not form_instance or not form_instance.site == site:
            message = _('Form does not exists.')
            return handle_error(message, status=HTTP_404_NOT_FOUND, json_response=json_response)

        form = FwdFormModelForm(data, instance=form_instance, partial=True)
        if not form.is_valid():  # pragma: no cover
            return handle_error(
                error_message,
                reason='validationError',
                status=HTTP_400_BAD_REQUEST,
                extra_context={'errors': json.loads(form.errors.as_json())},
                json_response=json_response
            )

        form.save()

        return JsonResponse({}, status=HTTP_204_NO_CONTENT)

    form = FwdFormModelForm(data)
    if not form.is_valid():  # pragma: no cover
        return handle_error(
            error_message,
            reason='validationError',
            status=HTTP_400_BAD_REQUEST,
            extra_context={'errors': json.loads(form.errors.as_json())},
            json_response=json_response
        )

    form_instance = form.save()
    return JsonResponse({'hashid': form_instance.hashid}, status=HTTP_201_CREATED)


@csrf_exempt
@require_POST
def forward_form(request, hashid):
    json_response = request.is_ajax()

    try:
        form = FwdForm.objects.get_by_hashid(hashid=hashid)
    except FwdForm.DoesNotExist:  # pragma: no cover
        message = _('We couldn\'t find the form you\'re trying to send to.')
        return handle_error(message, status=HTTP_404_NOT_FOUND, json_response=json_response)

    is_spam = request.POST.get('_gotcha', False)
    site = form.site
    if not is_spam and site.akismet_key:  # pragma: no cover
        akismet = Akismet(api_key=site.akismet_key, site_url=site.domain)
        is_spam = akismet.is_spam(request)

    if not is_spam:
        try:
            send_mail(request, form)
        except EmptyFormError:
            message = _('Looks like you forgot to complete the form. Please try again.')
            return handle_error(message, reason='emptyForm', status=HTTP_400_BAD_REQUEST,
                                json_response=json_response)
        except FwdFormError, e:  # pragma: no cover
            return handle_error(str(e), status=HTTP_500_INTERNAL_SERVER_ERROR,
                                json_response=json_response)
    else:
        form.spam_count = F('spam_count') + 1
        form.save()

    redirect_url = request.build_absolute_uri(reverse('fwdform:thank_you'))
    next_url = get_next_url(request.META.get('HTTP_REFERER', ''), request.POST.get('_next', ''))

    urls = (next_url, form.thankyou_url, )
    redirect_url = next((url for url in urls if url not in (None, '', )), redirect_url)

    if request.is_ajax():  # pragma: no cover
        return JsonResponse({'next': redirect_url}, status=HTTP_200_OK)

    return redirect(redirect_url)


@require_GET
def thank_you(request):
    return render_to_response('fwdform/thankyou.html', {})
