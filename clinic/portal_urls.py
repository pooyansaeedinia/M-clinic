from django.urls import path

from . import portal_views

urlpatterns = [
    path('', portal_views.portal_login, name='portal_login'),
    path('dashboard/', portal_views.portal_dashboard, name='portal_dashboard'),
    path(
        'language/<slug:code>/',
        portal_views.portal_language,
        name='portal_language',
    ),
    # Backward-compatible alias for older country URLs.
    path(
        'country/<slug:code>/',
        portal_views.portal_language,
        name='portal_country',
    ),
    path('logout/', portal_views.portal_logout, name='portal_logout'),
    path(
        'api/languages/',
        portal_views.portal_api_languages,
        name='portal_api_languages',
    ),
    path(
        'api/languages/<int:pk>/',
        portal_views.portal_api_language_detail,
        name='portal_api_language_detail',
    ),
    path(
        'api/languages/<int:pk>/sections/',
        portal_views.portal_api_language_sections,
        name='portal_api_language_sections',
    ),
    path(
        'api/sections/<int:pk>/',
        portal_views.portal_api_section_detail,
        name='portal_api_section_detail',
    ),
]
