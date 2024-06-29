namespace Teacher_Service_API.Models.DTOs
{
    public class EmailSignUpInfo(string email, string password, string fullName)
    {
        public string Email { get; set; } = email;
        public string Password { get; set; } = password;
        public string FullName { get; set; } = fullName;        
    }
}
