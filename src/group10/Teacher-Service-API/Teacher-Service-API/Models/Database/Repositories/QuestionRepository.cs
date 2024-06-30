using MySql.Data.MySqlClient;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Database.Repositories
{
    public class QuestionRepository
    {
        private readonly DatabaseManager _databaseManager = new DatabaseManager();

        public void AddQuestion(QuestionDTO questionDTO)
        {
            var query = "insert into questions(testId,question,category,option1,option2,option3,option4) values (@testId,@question,@category,@option1,@option2,@option3,@option4)";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@testId", questionDTO.TestId);
                command.Parameters.AddWithValue("@question", questionDTO.Question);
                command.Parameters.AddWithValue("@category", questionDTO.Category);
                command.Parameters.AddWithValue("@option1", questionDTO.Option1);
                command.Parameters.AddWithValue("@option2", questionDTO.Option2);
                command.Parameters.AddWithValue("@option3", questionDTO.Option3);
                command.Parameters.AddWithValue("@option4", questionDTO.Option4);
                command.ExecuteNonQuery();
            }
        }

        public List<QuestionDTO> GetQuestionsOfExam(string testId)
        {
            var result = new List<QuestionDTO>();
            var query = "select * from questions where testId = @testId";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@testId",testId);
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var question = reader.GetString(1);
                        var category = reader.GetString(2);
                        var option1 = reader.GetString(3);
                        var option2 = reader.GetString(4);
                        var option3 = reader.GetString(5);
                        var option4 = reader.GetString(6);
                        result.Add(new QuestionDTO(testId, question, category, option1, option2, option3, option4));
                    }
                }
            }
            return result;
        }
    }
}
