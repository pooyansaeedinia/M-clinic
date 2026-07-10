import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import ChatTemplateLanguage, ChatTemplateSection
from .portal import (
    PORTAL_PASSWORD,
    PORTAL_SESSION_KEY,
    PORTAL_USERNAME,
    ensure_default_languages,
    is_portal_authenticated,
    languages_queryset,
    portal_login_required,
)
from .portal_templates import (
    language_to_dict,
    parse_language_payload,
    parse_section_payload,
    section_to_dict,
    validate_language_image_file,
)
from .validators import ALLOWED_LANGUAGE_IMAGE_ACCEPT


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _error_response(message, *, status=400, errors=None):
    payload = {'ok': False, 'error': message}
    if errors:
        payload['errors'] = errors
    return JsonResponse(payload, status=status)


def _language_request_payload(request):
    content_type = (request.content_type or '').lower()
    if 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
        data = {key: request.POST.get(key) for key in request.POST.keys()}
        return data, request.FILES.get('image')
    data = _json_body(request)
    if data is None:
        return None, None
    return data, None


def _apply_language_image(language, image_file, *, clear_image=False):
    if clear_image and language.image:
        language.image.delete(save=False)
        language.image = None
    if image_file is not None:
        if language.image:
            language.image.delete(save=False)
        language.image = image_file
    return language


@require_http_methods(['GET', 'POST'])
def portal_login(request):
    if is_portal_authenticated(request):
        return redirect(reverse('portal_dashboard'))

    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if username == PORTAL_USERNAME and password == PORTAL_PASSWORD:
            request.session[PORTAL_SESSION_KEY] = True
            return redirect(reverse('portal_dashboard'))
        error = 'Invalid username or password.'

    return render(request, 'portal/login.html', {'error': error})


@portal_login_required
def portal_dashboard(request):
    ensure_default_languages()
    languages = languages_queryset()
    return render(
        request,
        'portal/dashboard.html',
        {
            'languages': languages,
            'language_image_accept': ALLOWED_LANGUAGE_IMAGE_ACCEPT,
        },
    )


@portal_login_required
def portal_language(request, code):
    language = get_object_or_404(ChatTemplateLanguage, code=code)
    sections = language.sections.all()
    return render(
        request,
        'portal/language.html',
        {
            'language': language,
            'sections': sections,
        },
    )


@portal_login_required
@require_http_methods(['POST'])
def portal_logout(request):
    request.session.pop(PORTAL_SESSION_KEY, None)
    return redirect(reverse('portal_login'))


@portal_login_required
@require_http_methods(['GET', 'POST'])
def portal_api_languages(request):
    if request.method == 'GET':
        languages = languages_queryset()
        return JsonResponse(
            {
                'ok': True,
                'languages': [language_to_dict(lang) for lang in languages],
            }
        )

    data, image_file = _language_request_payload(request)
    if data is None:
        return _error_response('Invalid request body.')

    payload, errors = parse_language_payload(data)
    if errors:
        return _error_response('Validation failed.', errors=errors)

    image_error = validate_language_image_file(image_file)
    if image_error:
        return _error_response('Validation failed.', errors={'image': image_error})

    clear_image = payload.pop('clear_image', False)
    language = ChatTemplateLanguage(
        name=payload['name'],
        code=payload['code'],
        language_name=payload['language_name'],
        sort_order=payload['sort_order'],
        is_active=payload['is_active'],
    )
    # Save once so upload_to can use code, then attach image.
    language.save()
    _apply_language_image(language, image_file, clear_image=clear_image)
    language.save()
    return JsonResponse(
        {'ok': True, 'language': language_to_dict(language)},
        status=201,
    )


@portal_login_required
@require_http_methods(['GET', 'PATCH', 'PUT', 'POST', 'DELETE'])
def portal_api_language_detail(request, pk):
    language = get_object_or_404(ChatTemplateLanguage, pk=pk)

    if request.method == 'GET':
        return JsonResponse(
            {
                'ok': True,
                'language': language_to_dict(language, include_sections=True),
            }
        )

    if request.method == 'DELETE':
        if language.image:
            language.image.delete(save=False)
        language.delete()
        return JsonResponse({'ok': True})

    data, image_file = _language_request_payload(request)
    if data is None:
        return _error_response('Invalid request body.')

    # Allow POST as a multipart-friendly update alias.
    payload, errors = parse_language_payload(data, instance=language)
    if errors:
        return _error_response('Validation failed.', errors=errors)

    image_error = validate_language_image_file(image_file)
    if image_error:
        return _error_response('Validation failed.', errors={'image': image_error})

    clear_image = payload.pop('clear_image', False)
    for field, value in payload.items():
        setattr(language, field, value)
    language.save()
    _apply_language_image(language, image_file, clear_image=clear_image)
    language.save()
    return JsonResponse({'ok': True, 'language': language_to_dict(language)})


@portal_login_required
@require_http_methods(['GET', 'POST'])
def portal_api_language_sections(request, pk):
    language = get_object_or_404(ChatTemplateLanguage, pk=pk)

    if request.method == 'GET':
        sections = language.sections.all()
        return JsonResponse(
            {
                'ok': True,
                'sections': [section_to_dict(section) for section in sections],
            }
        )

    data = _json_body(request)
    if data is None:
        return _error_response('Invalid JSON body.')

    payload, errors = parse_section_payload(data, language=language)
    if errors:
        return _error_response('Validation failed.', errors=errors)

    section = ChatTemplateSection.objects.create(**payload)
    return JsonResponse(
        {'ok': True, 'section': section_to_dict(section)},
        status=201,
    )


@portal_login_required
@require_http_methods(['GET', 'PATCH', 'PUT', 'DELETE'])
def portal_api_section_detail(request, pk):
    section = get_object_or_404(ChatTemplateSection, pk=pk)

    if request.method == 'GET':
        return JsonResponse({'ok': True, 'section': section_to_dict(section)})

    if request.method == 'DELETE':
        section.delete()
        return JsonResponse({'ok': True})

    data = _json_body(request)
    if data is None:
        return _error_response('Invalid JSON body.')

    payload, errors = parse_section_payload(data, instance=section)
    if errors:
        return _error_response('Validation failed.', errors=errors)

    for field, value in payload.items():
        setattr(section, field, value)
    section.save()
    return JsonResponse({'ok': True, 'section': section_to_dict(section)})
