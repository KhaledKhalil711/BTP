from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ContactMessage
from .forms import ContactForm, InscriptionForm


class ContactMessageModelTest(TestCase):
    """Test cases for ContactMessage model."""

    def setUp(self):
        """Set up test data."""
        self.contact = ContactMessage.objects.create(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="Test message content"
        )

    def test_contact_message_creation(self):
        """Test that a contact message is created correctly."""
        self.assertEqual(self.contact.name, "Test User")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(self.contact.subject, "Test Subject")
        self.assertEqual(self.contact.message, "Test message content")
        self.assertIsNotNone(self.contact.sent_at)

    def test_contact_message_str(self):
        """Test the string representation of contact message."""
        expected = f"{self.contact.name} - {self.contact.subject}"
        self.assertEqual(str(self.contact), expected)

    def test_email_field_validation(self):
        """Test that email field validates email format."""
        invalid_contact = ContactMessage(
            name="Test",
            email="invalid-email",
            subject="Test",
            message="Test"
        )
        with self.assertRaises(Exception):
            invalid_contact.full_clean()


class ContactFormTest(TestCase):
    """Test cases for ContactForm."""

    def test_contact_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Inquiry',
            'message': 'This is a test message'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_missing_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_contact_form_invalid_email(self):
        """Test form with invalid email."""
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test',
            'message': 'Test message'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contact_form_save(self):
        """Test that form saves correctly."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test',
            'message': 'Test message'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')


class InscriptionFormTest(TestCase):
    """Test cases for InscriptionForm."""

    def test_inscription_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = InscriptionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_inscription_form_password_mismatch(self):
        """Test form with mismatched passwords."""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!'
        }
        form = InscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_inscription_form_missing_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = InscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)


class ViewsTestCase(TestCase):
    """Test cases for views."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_index_view(self):
        """Test that index view returns 200."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_formation_view(self):
        """Test that formation view returns 200."""
        response = self.client.get(reverse('formation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/formation.html')

    def test_livrables_view(self):
        """Test that livrables view returns 200."""
        response = self.client.get(reverse('livrables'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/livrables.html')

    def test_contact_view_get(self):
        """Test that contact view GET returns 200 and form."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_view_post_valid(self):
        """Test contact view with valid POST data."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(ContactMessage.objects.count(), 1)
        contact = ContactMessage.objects.first()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')

    def test_contact_view_post_invalid(self):
        """Test contact view with invalid POST data."""
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email'
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 200)  # No redirect on error
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_inscription_view_get(self):
        """Test that inscription view GET returns 200 and form."""
        response = self.client.get(reverse('inscription'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/inscription.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], InscriptionForm)

    def test_inscription_view_post_valid(self):
        """Test inscription view with valid POST data."""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('inscription'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_inscription_view_post_invalid(self):
        """Test inscription view with invalid POST data."""
        form_data = {
            'username': 'newuser',
            'password1': 'pass',
            'password2': 'different'
        }
        response = self.client.post(reverse('inscription'), data=form_data)
        self.assertEqual(response.status_code, 200)  # No redirect on error
        self.assertEqual(User.objects.count(), 0)


class IntegrationTestCase(TestCase):
    """Integration tests for the application."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_registration_and_login_flow(self):
        """Test complete user registration flow."""
        # Register a new user
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('inscription'), data=form_data)
        self.assertEqual(response.status_code, 302)

        # Verify user is created
        new_user = User.objects.get(username='newuser')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_contact_message_submission_flow(self):
        """Test complete contact message submission flow."""
        # Submit contact form
        form_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Business Inquiry',
            'message': 'I would like to discuss a project.'
        }
        response = self.client.post(reverse('contact'), data=form_data)

        # Verify redirect
        self.assertEqual(response.status_code, 302)

        # Verify message is saved
        message = ContactMessage.objects.get(email='jane@example.com')
        self.assertEqual(message.name, 'Jane Doe')
        self.assertEqual(message.subject, 'Business Inquiry')
