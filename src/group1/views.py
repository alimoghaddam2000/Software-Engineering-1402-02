from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, StudentExamRecord, Category,AudioFile
from django.conf import settings

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    categories = Category.objects.all()
    user = request.user

    # Get filter parameters
    difficulty = request.GET.get('difficulty')
    category_id = request.GET.get('category')
    taken = request.GET.get('taken')

    if difficulty:
        exams = exams.filter(difficulty=difficulty)
    if category_id:
        exams = exams.filter(category_id=category_id)
    if taken:
        if taken == 'yes':
            exams = exams.filter(studentexamrecord__student=user)
        elif taken == 'no':
            exams = exams.exclude(studentexamrecord__student=user)

    context = {
        'exams': exams,
        'categories': categories,
        'difficulty': difficulty,
        'category_id': category_id,
        'taken': taken,
    }
    return render(request, 'exam_list.html', context)

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    student = request.user

    student_exam = StudentExamRecord.objects.filter(student=student, exam=exam).first()

    if student_exam:
        return redirect('exam_result', exam_id=exam.id)
    questions = exam.question_set.all()

    if request.method == 'POST':
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            StudentExamRecord.objects.create(
                student=student,
                exam=exam,
                question=question,
                answer=answer
            )
        return redirect('exam_result', exam_id=exam.id)

    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'take_exam.html', context)

@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    student=request.user
    if request.method == 'POST':
        if 'retake_exam' in request.POST:
            StudentExamRecord.objects.filter(student=student, exam=exam).delete()
            return redirect('take_exam',exam_id=exam.id)
    student_records = StudentExamRecord.objects.filter(exam=exam, student=request.user)
    questions = exam.question_set.all()
    correct_answers = 0
    for record in student_records:
        if record.question.question_type == 'MC' and record.answer == record.question.correct_answer:
            correct_answers += 1
        elif record.question.question_type == 'TX' and record.answer.strip().lower() == record.question.correct_answer.strip().lower():
            correct_answers += 1

    total_questions = questions.count()
    grade = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    context = {
        'exam': exam,
        'student_records': student_records,
        'grade': grade,
    }
    return render(request, 'exam_result.html', context)