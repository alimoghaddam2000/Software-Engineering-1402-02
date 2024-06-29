using MySql.Data.MySqlClient;
using MySqlX.XDevAPI.Common;
using Org.BouncyCastle.Utilities;
using System.Xml.Linq;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Database.Repositories
{
    public class ExamRepository
    {
        private readonly DatabaseManager _databaseManager = new DatabaseManager();

        public string AddExam(ExamDTO examDTO)
        {
            var query = "insert into exams(id, name, subjects, courseId) values (@id, @name, @subjects, @courseId)";
            var id = Guid.NewGuid().ToString();
            using(var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@id",id);
                command.Parameters.AddWithValue("@name", examDTO.Name);
                command.Parameters.AddWithValue("@subjects", examDTO.Subjects);
                command.Parameters.AddWithValue("@courseId", examDTO.CourseId);
                command.ExecuteNonQuery();
            }
            return id;
        }

        public List<ExamDTO> GetAllExamsOfCourse(string courseId)
        {
            var result = new List<ExamDTO>();
            var query = "select * from exams where courseId = @courseId";
            using(var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@courseId",courseId);
                using(var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var id = reader.GetString("id");
                        var name = reader.GetString("name");
                        var subjects = reader.GetString("subjects");
                        result.Add(new ExamDTO(courseId,id,name,subjects));
                    }
                }
            }
            return result;
        }

        public ExamDTO GetExamById(string id)
        {
            var query = "select * from exams where id = @id";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@id", id);
                using (var reader = command.ExecuteReader())
                {
                    if(reader.Read())
                    {
                        var courseId = reader.GetString("courseId");
                        var name = reader.GetString("name");
                        var subjects = reader.GetString("subjects");
                        return new ExamDTO(courseId, id, name, subjects);
                    }
                }
                return new ExamDTO("", "", "", "");
            }
        }
    }
}
