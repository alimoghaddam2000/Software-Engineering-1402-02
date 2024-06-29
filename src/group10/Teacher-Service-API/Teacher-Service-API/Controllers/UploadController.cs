using Microsoft.AspNetCore.Mvc;
using Teacher_Service_API.Models.Database.Repositories;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class UploadController(ImageFileRepository imageFileRepository, VideoFileRepository videoFileRepository) : ControllerBase
    {
        private readonly ImageFileRepository _imageFileRepository = imageFileRepository;
        private readonly VideoFileRepository _videoFileRepository = videoFileRepository;

        [HttpPost("course-poster/{courseId}")]
        public async Task<IActionResult> UploadCoursePosterFile(string courseId, IFormFile posterFile)
        {
            if (posterFile == null || posterFile.Length == 0)
            {
                return BadRequest();
            }
            await _imageFileRepository.AddCoursePosterFileAsync(courseId, posterFile);
            return Ok();
        }


        [HttpPost("course-videos/{courseId}/{description}")]
        [RequestSizeLimit(1_000_000_000)]
        public async Task<IActionResult> UploadCourseVideo(string courseId, string description, IFormFile file)
        {
            if (file == null || file.Length == 0)
            {
                return BadRequest();
            }
            await _videoFileRepository.AddCourseVideoFileAsync(courseId, description, file);
            return Ok();
        }
    }
}
