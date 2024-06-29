using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Teacher_Service_API.Models.Database.Repositories;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class QuestionController : ControllerBase
    {
        private readonly QuestionRepository _questionRepository;

        public QuestionController(QuestionRepository questionRepository)
        {
            _questionRepository = questionRepository;
        }

        [HttpPost("add-question")]
        public IActionResult AddQustionToExam(QuestionDTO question)
        {
            Console.WriteLine(question.Option1);
            _questionRepository.AddQuestion(question);
            return Ok();
        }

        [HttpGet("retrieve-questions/{testId}")]
        public IActionResult GetQuestionsOfTest(string testId)
        {            
            var questions = _questionRepository.GetQuestionsOfExam(testId);
            return Ok(questions);
        }
    }
}
