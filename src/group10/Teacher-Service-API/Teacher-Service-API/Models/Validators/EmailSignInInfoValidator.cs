using Teacher_Service_API.Models.Database.Repositories;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Validators
{
    public class EmailSignInInfoValidator(EmailSignInInfo emailSignInInfo, TeacherRepository teacherRepository) : IValidator
    {
        private readonly EmailSignInInfo _emailSignInInfo = emailSignInInfo;
        private readonly TeacherRepository _teacherRepository = teacherRepository;

        public bool Validate()
        {
            return
                _teacherRepository.AreEmailAndPasswordMatch(_emailSignInInfo).Result;               
        }
    }
}
