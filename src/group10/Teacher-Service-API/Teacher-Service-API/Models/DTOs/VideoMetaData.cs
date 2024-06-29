namespace Teacher_Service_API.Models.DTOs
{
    public class VideoMetaData(string id, string title)
    {
        public string Id { get; set; } = id;
        public string Title { get; set; } = title;
    }
}
