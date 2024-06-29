namespace Teacher_Service_API.Models.DTOs
{
    public class EmailSignInInfo(string email, string password)
    {
        public string Email { get; set; } = email;
        public string Password { get; set; } = password;
    }
}
