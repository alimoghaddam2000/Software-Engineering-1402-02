namespace Teacher_Service_API.Models.DTOs
{
    public class ExamDTO(string courseId, string id, string name, string subjects)
    {
        public string CourseId { get; set; } = courseId;
        public string Id { get; set; } = id;
        public string Name { get; set; } = name;
        public string Subjects { get; set; } = subjects;
    }
}
