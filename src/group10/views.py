from django.contrib.auth import login
from django.contrib.auth.models import User
import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
import base64

from .forms import SignUpForm, SignInForm, CourseForm, VideoForm, ExamForm, QuestionForm


def index_page(request):
    name = ""
    authenticated = is_authenticated(request)
    if authenticated:
        name = get_name(request)
    signup_form = SignUpForm()
    signin_form = SignInForm()

    context = {
        'is_authenticated': authenticated,
        'name': name,
        'signup_form': signup_form,
        'signin_form': signin_form,
    }
    return render(request, template_name='group10/html_files/index.html', context=context)


def signup(request):
    signup_form = SignUpForm(request.POST)
    if signup_form.is_valid():
        name = signup_form.cleaned_data.get('name')
        email = signup_form.cleaned_data.get('email')
        password = signup_form.cleaned_data.get('password')

        url_str = "https://localhost:7071/teacher/SignUpWithEmail"
        response = requests.post(url_str, json={'email': email, 'password': password, 'FullName': name}, verify=False)

        if response.status_code == 201:
            response = redirect(reverse('index_page'))
            response.set_cookie('username', email, max_age=3600)
            response.set_cookie('name', name, max_age=3600)
            return response
        return redirect(reverse('index_page'))
    else:
        context = {
            'signup_form': signup_form,
            'signin_form': SignInForm(),
            'is_authenticated': False,
        }
        return render(request, 'group10/html_files/index.html', context=context)


def signin(request):
    signup_in = SignInForm(request.POST)
    if signup_in.is_valid():

        print("))))))))))))))))))))))))))))))))))))))))))))))))))))))))0")
        email = signup_in.cleaned_data.get('email')
        password = signup_in.cleaned_data.get('password')

        url_str = "https://localhost:7071/teacher/SignInWithEmail"
        response = requests.post(url_str, json={'email': email, 'password': password}, verify=False)

        if response.status_code == 200:
            name = response.text.strip()
            response = redirect(reverse('index_page'))
            response.set_cookie('username', email, max_age=3600)
            response.set_cookie('name', name, max_age=3600)
            return response
        return redirect(reverse('index_page'))
    else:
        context = {
            'signup_form': SignUpForm(),
            'signin_form': signup_in,
            'is_authenticated': False,
        }
        return render(request, 'group10/html_files/index.html', context=context)


def courses(request):
    if is_authenticated(request):
        email = get_email(request)
        url = f"https://localhost:7071/Course/get-teacher-courses/{email}"
        courses = []
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            for course_data in data:
                course = Course(
                    name=course_data['name'],
                    description=course_data['description'],
                    objectives=course_data['objectives'],
                    id=course_data['id']
                )
                image_data = get_course_poster(request, course.id)
                course.set_image(image_data)

                courses.append(course)
        name = get_name(request)
        context = {
            'is_authenticated': True,
            'name': name,
            'courses': courses
        }

        return render(request, 'group10/html_files/courses.html', context=context)
    else:
        return redirect(reverse("index_page"))


class Video:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.video_file = None

    def set_video_file(self, video_file):
        self.video_file = video_file


def course_page(request, id):
    if is_authenticated(request):

        course = get_course_details(request, id)
        image_url = get_course_poster(request, id)

        exams = []
        url = f'https://localhost:7071/exam/retrieve-exams/{id}'
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            exam_data = response.json()
            for exam in exam_data:
                exam_id = exam["id"]
                exam_name = exam["name"]
                exam_subjects = exam["subjects"]
                exam = Exam(name=exam_name, subjects=exam_subjects, course_id=id, exam_id=exam_id)
                exams.append(exam)
        course_videos = []
        url = f'https://localhost:7071/course/get_videos_metadata/{id}'
        response = requests.get(url, verify=False)
        video_title = "default title"
        if response.status_code == 200:
            video_metadata = response.json()
            for metadata in video_metadata:
                video_id = metadata["id"]
                video_title = metadata["title"]
                video = Video(id=video_id, title=video_title)
                video_fetch_url = f'https://localhost:7071/download/course-video/get/{video_id}'
                video_response = requests.get(video_fetch_url, verify=False)
                if video_response.status_code == 200:
                    video_data = video_response.content
                    video_data_base64 = base64.b64encode(video_data).decode('utf-8')
                    video.set_video_file(video_data_base64)
                    course_videos.append(video)

        name = get_name(request)

        form = VideoForm()
        context = {
            'name': name,
            'is_authenticated': True,
            'course': course,
            'image_url': image_url,
            'course_videos': course_videos,
            'form': form,
            'exams': exams
        }

        return render(request, 'group10/html_files/course_page.html', context=context)
    else:
        return redirect(reverse("index_page"))


class Course:
    def __init__(self, name, description, objectives, id):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.id = id
        self.image_data = None

    def set_image(self, image_data):
        self.image_data = image_data


C_SHARP_SERVER_URL = "http://your-csharp-server/api/courses/"


def create_course(request):
    if is_authenticated(request):
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course_data = {
                    'name': form.cleaned_data['name'],
                    'description': form.cleaned_data['description'],
                    'objectives': form.cleaned_data['objectives'],
                }

                email = get_email(request)
                url = f"https://localhost:7071/Course/add-course/{email}"
                response = requests.post(url,
                                         json={'id': "", 'name': course_data["name"],
                                               'description': course_data["description"],
                                               'objectives': course_data["objectives"]},
                                         verify=False)
                course_id = response.text.strip()
                image = form.cleaned_data['image'].read()

                url = f"https://localhost:7071/upload/course-poster/{course_id}"
                files = {'posterFile': image}
                response = requests.post(url, files=files, verify=False)

                return redirect(reverse('courses'))
        else:
            form = CourseForm()

        name = get_name(request)
        context = {
            'name': name,
            'is_authenticated': True,
            'form': form
        }

        return render(request, 'group10/html_files/create_course.html', context=context)

    else:
        return redirect(reverse("index_page"))


def add_video(request, id):
    if is_authenticated(request):
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video_data = {
                    'course_id': id,
                    'title': form.cleaned_data['title'],
                    'video': form.cleaned_data['video'].read()
                }
                video_file = video_data['video']
                url = f"https://localhost:7071/upload/course-videos/{video_data['course_id']}/{video_data['title']}"
                files = {'file': video_file}
                requests.post(url, files=files, verify=False)
                return redirect(reverse('course_page', args=[id]))
        else:
            form = VideoForm()
        return redirect(reverse('course_page', args=[id]))
    else:
        return redirect(reverse("index_page"))


def is_authenticated(request):
    username = request.COOKIES.get('username')
    name = request.COOKIES.get('name')
    if username and name:
        return True
    return False


def get_name(request):
    return request.COOKIES.get('name')


def get_email(request):
    return request.COOKIES.get('username')


def logout(request):
    response = redirect(reverse('index_page'))
    response.delete_cookie('username')
    response.delete_cookie('name')
    return response


def get_course_poster(request, course_id):
    api_url = f'https://localhost:7071/Download/course-poster/get/{course_id}'
    response = requests.get(api_url, verify=False)

    print(response.status_code)

    if response.status_code == 200:
        image_data = response.content

        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        return image_data_base64
    else:
        return "Image not found"


def get_course_details(request, course_id):
    api_url = f'https://localhost:7071/Course/get-course/{course_id}'
    response = requests.get(api_url, verify=False)
    if response.status_code == 200:
        course_data = response.json()
        return Course(name=course_data['name'], description=course_data['description'],
                      objectives=course_data['objectives'], id=course_data['id'])
    else:
        return Course(name="course name", description='description',
                      objectives='objectives', id='id')


def create_exam(request, course_id):
    if is_authenticated(request):
        if request.method == 'POST':
            form = ExamForm(request.POST)
            if form.is_valid():
                exam_data = {
                    'courseId': course_id,
                    'Id': '',
                    'Name': form.cleaned_data['name'],
                    'Subjects': form.cleaned_data['subjects'],
                }

                url = f"https://localhost:7071/exam/add-exam"
                response = requests.post(url, json=exam_data, verify=False)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(response.status_code)
                return redirect(reverse('course_page', args=[course_id]))
        else:
            form = ExamForm()

        name = get_name(request)
        context = {
            'name': name,
            'is_authenticated': True,
            'form': form,
            'course_id': course_id
        }

        return render(request, 'group10/html_files/create_exam.html', context=context)
    else:
        return redirect(reverse("index_page"))


def exam_page(request, exam_id):
    if is_authenticated(request):
        url = f'https://localhost:7071/exam/get-exam/{exam_id}'
        print("11111111111111111111111111111111111111111111111111111111111111")
        response = requests.get(url, verify=False)

        exam_json = response.json()

        exam = Exam(name=exam_json['name'],subjects= exam_json['subjects'], course_id=exam_json['courseId'],exam_id= exam_json['id'])

        questions = []

        url = f'https://localhost:7071/question/retrieve-questions/{exam_id}'
        response = requests.get(url, verify=False)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
        print(response.status_code)
        json_data=response.json()

        for question in json_data:

            questions.append(
                Question(test_id=question['testId'],question= question['question'],option1= question['option1'], option2=question['option2'],
                        option3= question['option3'], option4=question['option4'],category= question['category']))
        name = get_name(request)

        context = {
            'name': name,
            'is_authenticated': True,
            'course_id': exam.course_id,
            'exam': exam,
            'questions': questions
        }

        return render(request, 'group10/html_files/exam_page.html', context=context)
    else:
        return redirect(reverse("index_page"))


def add_question(request, exam_id):
    if is_authenticated(request):
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                question_data = {
                    'testId': exam_id,
                    'question': form.cleaned_data['question'],
                    'option1': form.cleaned_data['option1'],
                    'option2': form.cleaned_data['option2'],
                    'option3': form.cleaned_data['option3'],
                    'option4': form.cleaned_data['option4'],
                    'category': form.cleaned_data['category'],
                }

                url = "https://localhost:7071/question/add-question"
                response = requests.post(url,json=question_data, verify=False)
                return redirect(reverse('exam_page', args=[exam_id]))
        else:
            form = QuestionForm()

        name = get_name(request)
        context = {
            'name': name,
            'is_authenticated': True,
            'form': form,
            'exam_id': exam_id
        }

        return render(request, 'group10/html_files/add_question.html', context)
    else:
        return redirect(reverse("index_page"))


class Exam:
    def __init__(self, name, subjects, course_id, exam_id):
        self.name = name
        self.subjects = subjects
        self.course_id = course_id
        self.exam_id = exam_id


class Question:
    def __init__(self, test_id, question, option1, option2, option3, option4, category):
        self.test_id = test_id
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.category = category
