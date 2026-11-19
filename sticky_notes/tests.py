from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import StickyNoteForm
from .models import StickyNote


class StickyNoteListTests(TestCase):
    def setUp(self):
        self.note = StickyNote.objects.create(
            title='First', content='Initial content')

    def test_empty_list_shows_empty_state(self):
        self.note.delete()

        response = self.client.get(reverse('sticky_note_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No sticky notes yet...')
        self.assertEqual(list(response.context['notes']), [])

    def test_list_orders_notes_by_most_recently_updated(self):
        second_note = StickyNote.objects.create(
            title='Second', content='More recent content')
        StickyNote.objects.filter(pk=self.note.pk).update(
            updated_at=timezone.now() - timedelta(days=1))

        response = self.client.get(reverse('sticky_note_list'))

        self.assertEqual(
            [note.pk for note in response.context['notes']],
            [second_note.pk, self.note.pk],
        )

    def test_list_shows_note_and_edit_and_delete_actions(self):
        response = self.client.get(reverse('sticky_note_list'))

        self.assertContains(response, 'First')
        self.assertContains(response, reverse(
            'sticky_note_detail', args=[self.note.pk]))
        self.assertContains(response, reverse(
            'sticky_note_update', args=[self.note.pk]))
        self.assertContains(response, reverse(
            'sticky_note_delete', args=[self.note.pk]))


class StickyNoteCreateTests(TestCase):
    def test_create_form_is_displayed(self):
        response = self.client.get(reverse('sticky_note_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Sticky Note')
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="content"')

    def test_create_note(self):
        response = self.client.post(
            reverse('sticky_note_create'),
            {'title': 'Created', 'content': 'Created content'},
        )
        self.assertRedirects(response, reverse('sticky_note_list'))
        self.assertTrue(StickyNote.objects.filter(
            title='Created', content='Created content').exists())

    def test_invalid_create_does_not_save_note(self):
        response = self.client.post(
            reverse('sticky_note_create'),
            {'title': '   ', 'content': '   '},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title',
                             'This field is required.')
        self.assertFormError(response.context['form'], 'content',
                             'This field is required.')
        self.assertEqual(StickyNote.objects.count(), 0)


class StickyNoteDetailTests(TestCase):
    def setUp(self):
        self.note = StickyNote.objects.create(
            title='First', content='Initial content')

    def test_read_note(self):
        response = self.client.get(
            reverse('sticky_note_detail', args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First')
        self.assertContains(response, 'Initial content')
        self.assertContains(response, reverse('sticky_note_update',
                                              args=[self.note.pk]))

    def test_missing_note_returns_404(self):
        response = self.client.get(
            reverse('sticky_note_detail', args=[self.note.pk + 1]))

        self.assertEqual(response.status_code, 404)


class StickyNoteUpdateTests(TestCase):
    def setUp(self):
        self.note = StickyNote.objects.create(
            title='First', content='Initial content')

    def test_update_form_is_prefilled(self):
        response = self.client.get(
            reverse('sticky_note_update', args=[self.note.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['title'], 'First')
        self.assertEqual(
            response.context['form'].initial['content'], 'Initial content')

    def test_update_note(self):
        response = self.client.post(
            reverse('sticky_note_update', args=[self.note.pk]),
            {'title': 'Updated', 'content': 'Updated content'},
        )
        self.assertRedirects(response, reverse('sticky_note_list'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated')
        self.assertEqual(self.note.content, 'Updated content')

    def test_invalid_update_does_not_change_note(self):
        response = self.client.post(
            reverse('sticky_note_update', args=[self.note.pk]),
            {'title': '   ', 'content': 'Updated content'},
        )

        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'First')
        self.assertEqual(self.note.content, 'Initial content')

    def test_missing_note_returns_404(self):
        response = self.client.get(
            reverse('sticky_note_update', args=[self.note.pk + 1]))

        self.assertEqual(response.status_code, 404)


class StickyNoteDeleteTests(TestCase):
    def setUp(self):
        self.note = StickyNote.objects.create(
            title='First', content='Initial content')

    def test_delete_confirmation_does_not_delete_note(self):
        response = self.client.get(
            reverse('sticky_note_delete', args=[self.note.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete Sticky Note?')
        self.assertContains(response, 'First')
        self.assertTrue(StickyNote.objects.filter(pk=self.note.pk).exists())

    def test_delete_note_on_post(self):
        response = self.client.post(
            reverse('sticky_note_delete', args=[self.note.pk]))
        self.assertRedirects(response, reverse('sticky_note_list'))
        self.assertFalse(StickyNote.objects.filter(pk=self.note.pk).exists())

    def test_missing_note_returns_404(self):
        response = self.client.get(
            reverse('sticky_note_delete', args=[self.note.pk + 1]))

        self.assertEqual(response.status_code, 404)


class StickyNoteFormTests(TestCase):
    def test_form_rejects_blank_title_and_content(self):
        form = StickyNoteForm(data={'title': '   ', 'content': '   '})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)

    def test_form_strips_title_and_content(self):
        form = StickyNoteForm(
            data={'title': '  My note  ', 'content': '  Note content  '})
        self.assertTrue(form.is_valid())
        note = form.save()
        self.assertEqual(note.title, 'My note')
        self.assertEqual(note.content, 'Note content')

    def test_form_accepts_maximum_title_length(self):
        form = StickyNoteForm(data={
            'title': 'T' * 200,
            'content': 'Note content',
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_title_over_maximum_length(self):
        form = StickyNoteForm(data={
            'title': 'T' * 201,
            'content': 'Note content',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
