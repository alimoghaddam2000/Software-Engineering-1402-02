namespace Teacher_Service_API.Models.DTOs
{
    public class CourseDTO(string id, string description, string name, string objectives)
    {        

        public string Id { get; set; } = id;
        public string Description { get; set; } = description;
        public string Name { get; set; } = name;
        public string Objectives { get; set; } = objectives;
    }
}
