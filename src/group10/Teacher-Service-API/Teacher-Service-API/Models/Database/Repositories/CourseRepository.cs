using MySql.Data.MySqlClient;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Database.Repositories
{
    public class CourseRepository
    {
        private readonly DatabaseManager _databaseManager;
        public CourseRepository(DatabaseManager databaseManager)
        {
            _databaseManager = databaseManager;
        }

        public Task<string> AddCourse(string teacherId, CourseDTO newCourse)
        {
            var query = "Insert Into Courses(TeacherId, Id, Name, Description, Objectives) VALUES (@TeacherId, @Id, @Name, @Description, @Objectives)";
            var id = Guid.NewGuid().ToString();
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@TeacherId", teacherId);
                command.Parameters.AddWithValue("@Id", id);
                command.Parameters.AddWithValue("@Name", newCourse.Name);
                command.Parameters.AddWithValue("@Description", newCourse.Description);
                command.Parameters.AddWithValue("@Objectives", newCourse.Objectives);
                command.ExecuteNonQuery();
            }
            return Task.FromResult(id);
        }


        public List<CourseDTO> GetAllCoursesOfTeacher(string teacherId)
        {
            var query = "Select * From Courses Where teacherId = @teacherId";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@teacherId", teacherId);
                using (var reader = command.ExecuteReader())
                {
                    var result = new List<CourseDTO>();
                    while (reader.Read())
                    {
                        var id = reader.GetString("Id");
                        var name = reader.GetString("Name");
                        var description = reader.GetString("Description");
                        var objectives = reader.GetString("Objectives");
                        result.Add(new CourseDTO(id, description, name, objectives));
                    }

                    return result;
                }
            }
        }

        //test
        public CourseDTO GetCourseById(string id)
        {
            var query = "Select * From Courses Where Id = @id";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@id", id);
                using (var reader = command.ExecuteReader())
                {
                    reader.Read();
                    var name = reader.GetString("Name");
                    var description = reader.GetString("Description");
                    var objectives = reader.GetString("Objectives");
                    return new CourseDTO(id, description, name, objectives);
                }
            }
        }

        public List<VideoMetaData> GetCourseVideosMetaData(string courseId)
        {
            var result = new List<VideoMetaData>();
            var query = "Select videoId,title From videos Where courseId = @courseId";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@courseId", courseId);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var videoId = reader.GetString("videoId");
                        var title = reader.GetString("Title");
                        result.Add(new VideoMetaData(videoId, title));
                    }
                }
            }
            return result;
        }

        public Task DeleteCourse(CourseDTO newCourse)
        {
            throw new NotImplementedException();
        }

        public Task UpdateCourse(CourseDTO newCourse)
        {
            throw new NotImplementedException();
        }
    }
}
