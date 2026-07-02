from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProcedureForm, ProcedureImageForm
from .models import Procedure, ProcedureImage


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


def procedure_detail(request, slug):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    samples = [
        {
            'id': item.id,
            'before_image': item.before_image,
            'after_image': item.after_image,
        }
        for item in procedure.gallery_items.all()
    ]
    context = {
        'procedure': procedure,
        'name': get_text(procedure, 'name', lang),
        'summary': get_text(procedure, 'summary', lang),
        'samples': samples,
    }
    if request.user.is_authenticated:
        context['image_form'] = ProcedureImageForm()
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


@login_required
def add_procedure_image(request, slug):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    if request.method == 'POST':
        form = ProcedureImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.procedure = procedure
            image.save()
            return redirect('procedure_detail', slug=procedure.slug)
    else:
        form = ProcedureImageForm()

    return render(
        request,
        'clinic/add_procedure_image.html',
        {
            'form': form,
            'procedure': procedure,
            'procedure_name': get_text(procedure, 'name', lang),
            'mode': 'create',
        },
    )


@login_required
def edit_procedure_image(request, slug, image_id):
    lang = request.session.get('lang', 'en')
    procedure = get_object_or_404(Procedure, slug=slug)
    image_item = get_object_or_404(ProcedureImage, pk=image_id, procedure=procedure)
    if request.method == 'POST':
        form = ProcedureImageForm(request.POST, request.FILES, instance=image_item)
        if form.is_valid():
            form.save()
            return redirect('procedure_detail', slug=procedure.slug)
    else:
        form = ProcedureImageForm(instance=image_item)

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
    image_item = get_object_or_404(ProcedureImage, pk=image_id, procedure=procedure)
    image_item.delete()
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
            'gallery_count': item.gallery_items.count(),
        }
        for item in procedures
    ]
    context = {'items': items}
    return render(request, 'clinic/manage_content.html', add_shared_forms(request, context))
