from django import forms

from .models import StickyNote


class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        fields = ['title', 'content']
        labels = {
            'title': 'Note title',
            'content': 'Note content',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'sticky-note-title',
                'placeholder': 'Enter a title',
                'maxlength': 200,
            }),
            'content': forms.Textarea(attrs={
                'class': 'sticky-note-content',
                'placeholder': 'Write your note here...',
                'rows': 8,
            }),
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if not title:
            raise forms.ValidationError('A note title cannot be blank.')
        return title

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise forms.ValidationError('A note cannot be blank.')
        return content
