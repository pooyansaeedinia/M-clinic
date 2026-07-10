"""Serialization and validation helpers for portal chat-template CMS APIs."""

from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import ChatTemplateLanguage, ChatTemplateSection
from .validators import validate_language_image_upload


def language_to_dict(language, *, include_sections=False):
    section_count = getattr(language, 'section_count', None)
    if section_count is None:
        section_count = language.sections.count()
    data = {
        'id': language.pk,
        'name': language.name,
        'code': language.code,
        'language_name': language.language_name,
        'image_url': language.image_url,
        'has_image': bool(language.image),
        'sort_order': language.sort_order,
        'is_active': language.is_active,
        'section_count': section_count,
        'subtitle': language.subtitle,
        'created_at': language.created_at.isoformat(),
        'updated_at': language.updated_at.isoformat(),
    }
    if include_sections:
        data['sections'] = [
            section_to_dict(section) for section in language.sections.all()
        ]
    return data


def section_to_dict(section):
    return {
        'id': section.pk,
        'language_id': section.language_id,
        'title': section.title,
        'body': section.body,
        'template_type': section.template_type,
        'sort_order': section.sort_order,
        'is_active': section.is_active,
        'category': section.category,
        'tags': section.tags,
        'created_at': section.created_at.isoformat(),
        'updated_at': section.updated_at.isoformat(),
    }


def parse_language_payload(data, *, instance=None):
    errors = {}
    name = (data.get('name') or '').strip()
    language_name = (data.get('language_name') or '').strip()
    code = (data.get('code') or '').strip().lower()

    if not name:
        errors['name'] = 'Name is required.'
    if not code:
        code = slugify(name) if name else ''
    if not code:
        errors['code'] = 'Code is required.'
    elif not slugify(code):
        errors['code'] = 'Use letters, numbers, or hyphens only.'
    else:
        code = slugify(code)

    qs = ChatTemplateLanguage.objects.filter(code=code)
    if instance is not None:
        qs = qs.exclude(pk=instance.pk)
    if code and qs.exists():
        errors['code'] = 'A language with this code already exists.'

    sort_order = data.get('sort_order', instance.sort_order if instance else 0)
    try:
        sort_order = int(sort_order)
        if sort_order < 0:
            raise ValueError
    except (TypeError, ValueError):
        errors['sort_order'] = 'Sort order must be a non-negative integer.'

    is_active = data.get('is_active', True if instance is None else instance.is_active)
    if isinstance(is_active, str):
        is_active = is_active.lower() in {'1', 'true', 'yes', 'on'}

    clear_image = data.get('clear_image', False)
    if isinstance(clear_image, str):
        clear_image = clear_image.lower() in {'1', 'true', 'yes', 'on'}

    if errors:
        return None, errors

    return {
        'name': name,
        'code': code,
        'language_name': language_name,
        'sort_order': sort_order,
        'is_active': bool(is_active),
        'clear_image': bool(clear_image),
    }, None


def validate_language_image_file(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        validate_language_image_upload(uploaded_file)
    except ValidationError as exc:
        message = '; '.join(exc.messages) if hasattr(exc, 'messages') else str(exc)
        return message
    return None


def parse_section_payload(data, *, instance=None, language=None):
    errors = {}
    title = (data.get('title') or '').strip()
    body = (data.get('body') or '').strip()
    if not title:
        errors['title'] = 'Title is required.'
    if not body:
        errors['body'] = 'Message text is required.'

    sort_order = data.get('sort_order', instance.sort_order if instance else 0)
    try:
        sort_order = int(sort_order)
        if sort_order < 0:
            raise ValueError
    except (TypeError, ValueError):
        errors['sort_order'] = 'Sort order must be a non-negative integer.'

    is_active = data.get('is_active', True if instance is None else instance.is_active)
    if isinstance(is_active, str):
        is_active = is_active.lower() in {'1', 'true', 'yes', 'on'}

    category = (data.get('category') or '').strip()
    template_type = (
        data.get('template_type')
        or (instance.template_type if instance else ChatTemplateSection.TemplateType.MESSAGE)
    )
    valid_types = {choice.value for choice in ChatTemplateSection.TemplateType}
    if template_type not in valid_types:
        errors['template_type'] = 'Invalid template type.'

    if language is None and instance is not None:
        language = instance.language
    if language is None:
        errors['language'] = 'Language is required.'

    if errors:
        return None, errors

    return {
        'language': language,
        'title': title,
        'body': body,
        'template_type': template_type,
        'sort_order': sort_order,
        'is_active': bool(is_active),
        'category': category,
    }, None
