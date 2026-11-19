from django.urls import path

from .views import (
    StickyNoteCreateView,
    StickyNoteDeleteView,
    StickyNoteDetailView,
    StickyNoteListView,
    StickyNoteUpdateView,
)

urlpatterns = [
    path('', StickyNoteListView.as_view(), name='sticky_note_list'),
    path('notes/create/', StickyNoteCreateView.as_view(),
         name='sticky_note_create'),
    path('notes/<int:pk>/', StickyNoteDetailView.as_view(),
         name='sticky_note_detail'),
    path('notes/<int:pk>/edit/', StickyNoteUpdateView.as_view(),
         name='sticky_note_update'),
    path('notes/<int:pk>/delete/', StickyNoteDeleteView.as_view(),
         name='sticky_note_delete'),
]
