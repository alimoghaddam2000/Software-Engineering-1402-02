using System.Text.RegularExpressions;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Validators
{
    public class EmailSignUpInfoValidator(EmailSignUpInfo emailSignUpInfo) : IValidator
    {
        private readonly EmailSignUpInfo _emailSignUpInfo = emailSignUpInfo ?? throw new ArgumentNullException();
        private bool CheckEmailRegex(string email)
        {
            return Regex.IsMatch(email, @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$");
        }
        private bool CheckPasswordRegex(string password)
        {
            return Regex.IsMatch(password, @"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,15}$");

        }
        
        public bool Validate()
        {
            return CheckEmailRegex(emailSignUpInfo.Email) && CheckPasswordRegex(emailSignUpInfo.Password);
        }        
    }
}
