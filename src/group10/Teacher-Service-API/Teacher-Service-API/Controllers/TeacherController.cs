using Microsoft.AspNetCore.Mvc;
using Teacher_Service_API.Models.Database.Repositories;
using Teacher_Service_API.Models.DTOs;
using Teacher_Service_API.Models.Validators;

namespace Teacher_Service_API.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class TeacherController : ControllerBase
    {
        private readonly TeacherRepository _teacherRepository;

        public TeacherController(TeacherRepository teacherRepository)
        {
            _teacherRepository = teacherRepository;
        }

        [HttpPost("SignUpWithEmail")]
        public IActionResult SignUpWithEmail(EmailSignUpInfo signUpInfo)
        {
            var validator = new EmailSignUpInfoValidator(signUpInfo);
            var validationResult = validator.Validate();
            if (validationResult)
            {
                var id = _teacherRepository.AddTeacherAsync(signUpInfo).Result;
                return CreatedAtAction(nameof(GetTeacherById), new { id = id }, new { id = id });
            }
            else
            {
                return BadRequest("wrong-regex");
            }
        }

        [HttpPost("email-check/{email}")]
        public IActionResult IsEmailDuplicated(string email)
        {
            if (_teacherRepository.IsEmailUsedBefore(email).Result)
            {
                return BadRequest("duplicate-email");
            }
            else
            {
                return Ok();
            }
        }

        [HttpPost("SignInWithEmail")]
        public IActionResult SignInWithEmail([FromBody]EmailSignInInfo signInInfo)
        {
            var validator = new EmailSignInInfoValidator(signInInfo, _teacherRepository);
            var validationResult = validator.Validate();
            if (validationResult)
            {
                var name = _teacherRepository.GetNameByEmail(signInInfo.Email);
                return Ok(name);
            }
            else
            {
                return Unauthorized();
            }
        }


        [HttpGet("{id}")]
        public IActionResult GetTeacherById(string id)
        {
            var teacher = _teacherRepository.GetTeacherById(id);
            if (teacher.Email == "")
            {
                return BadRequest();
            }
            else
            {
                return Ok(teacher);
            }
        }
    }
}
