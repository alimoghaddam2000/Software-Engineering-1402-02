namespace Teacher_Service_API.Models.DTOs
{
    public class QuestionDTO(string testId,
        string question,
        string category,
        string option1,
        string option2,
        string option3,
        string option4
        )
    {
        public string TestId { get; set; } = testId;
        public string Question { get; set; } = question;
        public string Category { get; set; } = category;
        public string Option1 { get; set; } = option1;
        public string Option2 { get; set; } = option2;
        public string Option3 { get; set; } = option3;
        public string Option4 { get; set; } = option4;
    }
}
