using Teacher_Service_API.Models.Database;
using Teacher_Service_API.Models.Database.Repositories;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Domain
{
    public class Teacher
    {
        private readonly CourseRepository _courseRepository = new CourseRepository(new DatabaseManager());
        public string Id { get; set; }
        public string FullName { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public List<CourseDTO> courseDTOs { get; set; }

        public Teacher(string id, string fullName, string email, string password)
        {
            Id = id;
            FullName = fullName;
            Email = email;
            Password = password;
            courseDTOs = _courseRepository.GetAllCoursesOfTeacher(email);
        }


        public CourseDTO? AddCourse(CourseDTO courseDTO)
        {
            foreach (var course in courseDTOs)
            {
                if (course.Name == courseDTO.Name)
                {
                    return null;
                }
            }
            courseDTO.Id = _courseRepository.AddCourse(Id, courseDTO).Result;
            courseDTOs.Add(courseDTO);
            return courseDTO;
        }
    }
}
