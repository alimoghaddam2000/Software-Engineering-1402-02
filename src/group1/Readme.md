# English Listening Exam Management System

## Overview

This project is part of an English learning website, focusing on the listening section. It allows administrators to create and manage listening exams, associate audio files with these exams, and create questions related to the audio content. Students can take these listening exams, and their responses are recorded for analysis.

## Features

- **Listening Exam Management**: Create and manage listening exams with different difficulty levels and categories.
- **Audio Files**: Upload and associate audio files with listening exams.
- **Question Types**: Support for multiple choice and text answer questions related to the audio content.
- **Student Exam Records**: Track students' answers and performance in listening exams.
- **Filtering**: Filter exams by difficulty, category, and whether the student has taken them.

## Models

### Exam

- `title`: CharField
- `description`: TextField
- `difficulty`: CharField (choices: Easy, Medium, Hard)
- `category`: ForeignKey (to Category)
- `date_created`: DateTimeField (auto_now_add=True)

### AudioFile

- `exam`: ForeignKey (to Exam, related_name='audio_files')
- `audio_file`: FileField
- `description`: TextField (optional)

### Question

- `exam`: ForeignKey (to Exam)
- `question_text`: TextField
- `question_type`: CharField (choices: Multiple Choice, Text Answer)
- `options`: JSONField (optional)
- `correct_answer`: TextField

### StudentExamRecord

- `student`: ForeignKey (to User)
- `exam`: ForeignKey (to Exam)
- `question`: ForeignKey (to Question)
- `answer`: TextField
- `date_taken`: DateTimeField (auto_now_add=True)

## Views

### `exam_list`

Fetches and filters the list of listening exams based on difficulty, category, and whether the student has taken them.

```python
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
            exams = exams.filter(studentexamrecord__student=user).distinct()
        elif taken == 'no':
            exams = exams.exclude(studentexamrecord__student=user).distinct()

    context = {
        'exams': exams,
        'categories': categories,
        'difficulty': difficulty,
        'category_id': category_id,
        'taken': taken,
    }
    return render(request, 'exam_list.html', context)
```

## Setup Instructions

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/english-listening-exam-management.git
   cd english-listening-exam-management
   ```

2. **Create and activate a virtual environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Apply the migrations**:

   ```sh
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```sh
   python manage.py runserver
   ```

7. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **Admin Panel**: Log in to the admin panel at `http://127.0.0.1:8000/admin/` to manage listening exams, audio files, and questions.
- **Exam List**: Students can view the list of listening exams and filter them based on difficulty, category, and whether they have taken them.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
