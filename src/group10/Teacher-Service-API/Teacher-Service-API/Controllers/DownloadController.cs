using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Teacher_Service_API.Models.Database.Repositories;

namespace Teacher_Service_API.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class DownloadController(ImageFileRepository imageFileRepository,VideoFileRepository videoFileRepository) : ControllerBase
    {
        private readonly ImageFileRepository _imageFileRepository = imageFileRepository;
        private readonly VideoFileRepository _videoFileRepository = videoFileRepository;

        [HttpGet("course-poster/get/{courseId}")]
        public IActionResult DownloadCoursePosterFile(string courseId)
        {
            var fileBytes = _imageFileRepository.GetCoursePoster(courseId);
            if (fileBytes.Length == 0)
            {
                return BadRequest();
            }
            var contentType = "application/octet-stream";
            return File(fileBytes, contentType);
        }

        [HttpGet("course-video/get/{videoId}")]
        public IActionResult DownloadCourseVideo(string videoId)
        {
            var fileBytes = _videoFileRepository.GetCourseVideo(videoId);
            if (fileBytes.Length == 0)
            {
                return BadRequest();
            }
            var contentType = "application/octet-stream";
            return File(fileBytes, contentType);
        }
    }
}
