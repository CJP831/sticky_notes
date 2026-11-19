from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import StickyNoteForm
from .models import StickyNote


class StickyNoteListView(ListView):
    model = StickyNote
    context_object_name = 'notes'
    ordering = ['-updated_at']


class StickyNoteDetailView(DetailView):
    model = StickyNote
    context_object_name = 'note'


class StickyNoteCreateView(CreateView):
    model = StickyNote
    form_class = StickyNoteForm
    success_url = reverse_lazy('sticky_note_list')


class StickyNoteUpdateView(UpdateView):
    model = StickyNote
    form_class = StickyNoteForm
    success_url = reverse_lazy('sticky_note_list')


class StickyNoteDeleteView(DeleteView):
    model = StickyNote
    success_url = reverse_lazy('sticky_note_list')
