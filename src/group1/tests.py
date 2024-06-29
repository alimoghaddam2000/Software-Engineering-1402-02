from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Exam, Question,StudentExamRecord

class ExamViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.exam = Exam.objects.create(title='Test Exam', difficulty='Easy', category='General')
        self.question1 = Question.objects.create(exam=self.exam, question_text='Question 1', question_type='MC', options=['Option 1', 'Option 2', 'Option 3', 'Option 4'], correct_answer=0)
        self.question2 = Question.objects.create(exam=self.exam, question_text='Question 2', question_type='TX')

    def test_take_exam_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('take_exam', kwargs={'exam_id': self.exam.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'take_exam.html')

    def test_exam_result_view(self):
        student_exam = StudentExamRecord.objects.create(student=self.user, exam=self.exam)
        response = self.client.get(reverse('exam_result', kwargs={'student_exam_id': student_exam.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exam_result.html')

    def test_submit_exam_form(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'exam': self.exam.id,
            'student': self.user.id,
            'answers-TOTAL_FORMS': 2,
            'answers-INITIAL_FORMS': 0,
            'answers-MIN_NUM_FORMS': 0,
            'answers-MAX_NUM_FORMS': 1000,
            'answers-0-id': '',
            'answers-0-question': self.question1.id,
            'answers-0-answer': 0,  # Selecting the first option as answer for MC question
            'answers-1-id': '',
            'answers-1-question': self.question2.id,
            'answers-1-answer': 'Answer for Question 2',  # Text answer for TX question
        }
        response = self.client.post(reverse('take_exam', kwargs={'exam_id': self.exam.id}), data=form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after form submission
        # Optionally, you can assert other behaviors like message checks or data in the database