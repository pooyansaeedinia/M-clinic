import re
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProcedureForm, SectionImageForm
from .models import GallerySection, Procedure, SectionImage


def get_text(obj, field_base, lang):
    value = getattr(obj, f'{field_base}_{lang}', '')
    if value:
        return value
    return getattr(obj, f'{field_base}_en', '')


def add_shared_forms(request, context):
    if request.user.is_authenticated and 'procedure_form' not in context:
        context['procedure_form'] = ProcedureForm()
    return context


def set_language(request, lang_code):
    if lang_code not in {'en', 'tr'}:
        lang_code = 'en'
    request.session['lang'] = lang_code
    next_url = request.GET.get('next') or reverse('home')
    return redirect(next_url)


def home(request):
    lang = request.session.get('lang', 'en')
    procedures = Procedure.objects.all()
    cards = [
        {
            'slug': item.slug,
            'name': get_text(item, 'name', lang),
            'summary': get_text(item, 'summary', lang),
            'default_image': item.default_image,
        }
        for item in procedures
    ]
    context = {'cards': cards}
    return render(request, 'clinic/home.html', add_shared_forms(request, context))


def build_gallery_sections(procedure, lang):
    sections = []
    for section in procedure.gallery_sections.all():
        before_items = []
        after_items = []
        for image in section.images.all():
            payload = {
                'id': image.id,
                'title': get_text(image, 'title', lang),
                'image': image.image,
            }
            if image.image_type == SectionImage.ImageType.BEFORE:
                before_items.append(payload)
            else:
                after_items.append(payload)
        sections.append({
            'id': section.id,
            'before_items': before_items,
            'after_items': after_items,
        })
    return sections


def procedure_detail(request, slug):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    gallery_sections = build_gallery_sections(procedure, lang)
    context = {
        'procedure': procedure,
        'name': get_text(procedure, 'name', lang),
        'summary': get_text(procedure, 'summary', lang),
        'gallery_sections': gallery_sections,
        'has_gallery': bool(gallery_sections),
    }
    return render(request, 'clinic/procedure_detail.html', add_shared_forms(request, context))


@login_required
def add_procedure(request):
    if request.method == 'POST':
        form = ProcedureForm(request.POST, request.FILES)
        if form.is_valid():
            procedure = form.save()
            return redirect('procedure_detail', slug=procedure.slug)
    else:
        form = ProcedureForm()

    return render(
        request,
        'clinic/add_procedure.html',
        {
            'form': form,
            'mode': 'create',
        },
    )


@login_required
def edit_procedure(request, slug):
    procedure = get_object_or_404(Procedure, slug=slug)
    if request.method == 'POST':
        form = ProcedureForm(request.POST, request.FILES, instance=procedure)
        if form.is_valid():
            procedure = form.save()
            return redirect('procedure_detail', slug=procedure.slug)
    else:
        form = ProcedureForm(instance=procedure)

    return render(
        request,
        'clinic/add_procedure.html',
        {
            'form': form,
            'mode': 'edit',
            'procedure': procedure,
        },
    )


@login_required
def delete_procedure(request, slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    procedure = get_object_or_404(Procedure, slug=slug)
    procedure.delete()
    return redirect('manage_content')


FIELD_PATTERN = re.compile(r'^s(\d+)_(b|a)(\d+)_(title_en|title_tr|image)$')
KIND_MAP = {'b': 'before', 'a': 'after'}


def collect_upload_items(post_data, files_data):
    items = defaultdict(dict)
    for key, value in post_data.items():
        match = FIELD_PATTERN.match(key)
        if not match or match.group(4) != 'title_en':
            continue
        section_idx = int(match.group(1))
        kind = match.group(2)
        image_idx = int(match.group(3))
        items[(section_idx, kind, image_idx)]['title_en'] = value.strip()

    for key, value in post_data.items():
        match = FIELD_PATTERN.match(key)
        if not match or match.group(4) != 'title_tr':
            continue
        section_idx = int(match.group(1))
        kind = match.group(2)
        image_idx = int(match.group(3))
        items[(section_idx, kind, image_idx)]['title_tr'] = value.strip()

    for key, uploaded in files_data.items():
        match = FIELD_PATTERN.match(key)
        if not match or match.group(4) != 'image':
            continue
        section_idx = int(match.group(1))
        kind = match.group(2)
        image_idx = int(match.group(3))
        items[(section_idx, kind, image_idx)]['image'] = uploaded

    return items


def save_nested_gallery(procedure, post_data, files_data):
    items = collect_upload_items(post_data, files_data)
    if not items:
        return 0

    sections = defaultdict(lambda: {'before': [], 'after': []})
    for (section_idx, kind, image_idx), payload in items.items():
        image_file = payload.get('image')
        if not image_file:
            continue
        title_en = payload.get('title_en', '').strip() or f'Image {image_idx + 1}'
        title_tr = payload.get('title_tr', '').strip()
        kind_key = KIND_MAP.get(kind, kind)
        sections[section_idx][kind_key].append({
            'title_en': title_en,
            'title_tr': title_tr,
            'image': image_file,
        })

    created_sections = 0
    for section_idx in sorted(sections.keys()):
        section_data = sections[section_idx]
        if not section_data['before'] and not section_data['after']:
            continue

        gallery_section = GallerySection.objects.create(procedure=procedure)
        created_sections += 1

        for item in section_data['before']:
            SectionImage.objects.create(
                section=gallery_section,
                title_en=item['title_en'],
                title_tr=item['title_tr'],
                image=item['image'],
                image_type=SectionImage.ImageType.BEFORE,
            )

        for item in section_data['after']:
            SectionImage.objects.create(
                section=gallery_section,
                title_en=item['title_en'],
                title_tr=item['title_tr'],
                image=item['image'],
                image_type=SectionImage.ImageType.AFTER,
            )

    return created_sections


@login_required
def add_procedure_image(request, slug):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    if request.method == 'POST':
        created = save_nested_gallery(procedure, request.POST, request.FILES)
        if created:
            return redirect('procedure_detail', slug=procedure.slug)

    return render(
        request,
        'clinic/add_procedure_image.html',
        {
            'procedure': procedure,
            'procedure_name': get_text(procedure, 'name', lang),
            'mode': 'create',
        },
    )


@login_required
def edit_procedure_image(request, slug, image_id):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    image_item = get_object_or_404(
        SectionImage,
        pk=image_id,
        section__procedure=procedure,
    )
    if request.method == 'POST':
        form = SectionImageForm(request.POST, request.FILES, instance=image_item)
        if form.is_valid():
            form.save()
            return redirect('procedure_detail', slug=procedure.slug)
    else:
        form = SectionImageForm(instance=image_item)

    return render(
        request,
        'clinic/add_procedure_image.html',
        {
            'form': form,
            'procedure': procedure,
            'procedure_name': get_text(procedure, 'name', lang),
            'mode': 'edit',
            'image_item': image_item,
        },
    )


@login_required
def delete_procedure_image(request, slug, image_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    procedure = get_object_or_404(Procedure, slug=slug)
    image_item = get_object_or_404(
        SectionImage,
        pk=image_id,
        section__procedure=procedure,
    )
    section = image_item.section
    image_item.delete()
    if not section.images.exists():
        section.delete()
    return redirect('procedure_detail', slug=procedure.slug)


@login_required
def manage_content(request):
    lang = request.session.get('lang', 'en')
    procedures = Procedure.objects.all()
    items = [
        {
            'slug': item.slug,
            'name': get_text(item, 'name', lang),
            'default_image': item.default_image,
            'gallery_count': SectionImage.objects.filter(section__procedure=item).count(),
        }
        for item in procedures
    ]
    context = {'items': items}
    return render(request, 'clinic/manage_content.html', add_shared_forms(request, context))
