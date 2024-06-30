using MySql.Data.MySqlClient;
using Teacher_Service_API.Models.Domain;
using Teacher_Service_API.Models.DTOs;

namespace Teacher_Service_API.Models.Database.Repositories
{
    public class TeacherRepository(DatabaseManager databaseManager)
    {
        private readonly DatabaseManager _databaseManager = databaseManager;

        public Task<string> AddTeacherAsync(EmailSignUpInfo emailSignUpInfo)
        {
            var query = "Insert into teachers(Id, FullName, Email, Password) VALUES (@Id, @FullName, @Email, @Password)";
            var id = Guid.NewGuid().ToString();
            using (var connection = _databaseManager.GetConnection())
            {
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@Id", id);
                command.Parameters.AddWithValue("@FullName", emailSignUpInfo.FullName);
                command.Parameters.AddWithValue("@Email", emailSignUpInfo.Email);
                command.Parameters.AddWithValue("@Password", emailSignUpInfo.Password);
                connection.Open();
                command.ExecuteNonQuery();
            }
            return Task.FromResult(id);
        }

        public Task<bool> AreEmailAndPasswordMatch(EmailSignInInfo emailLoginInfo)
        {
            var query = "SELECT * From teachers WHERE Email = @Email AND Password = @Password";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@Email", emailLoginInfo.Email);
                command.Parameters.AddWithValue("@Password", emailLoginInfo.Password);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return Task.FromResult(true);
                    }
                }
                return Task.FromResult(false);
            }
        }

        public string GetNameByEmail(string email)
        {
            var query = "SELECT FullName FROM teachers WHERE Email = @email";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@Email", email);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        var name = reader.GetString("FullName");
                        return name;
                    }
                }
                return "";
            }
        }        

        public string GetIdByEmail(string email)
        {
            var query = "SELECT Id FROM teachers WHERE Email = @email";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@Email", email);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        var id = reader.GetString("Id");
                        return id;
                    }
                }
                return "";
            }
        }

        public Task<bool> IsEmailUsedBefore(string email)
        {
            var query = $"SELECT email FROM teachers WHERE email = @email";

            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query, connection);
                command.Parameters.AddWithValue("@email", email);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return Task.FromResult(true);
                    }
                    else
                    {
                        return Task.FromResult(false);
                    }
                }
            }

        }
        public Teacher GetTeacherById(string id)
        {
            var query = "Select * From teachers Where Id = @id";
            using (var connection = _databaseManager.GetConnection())
            {
                connection.Open();
                var command = new MySqlCommand(query,connection);
                command.Parameters.AddWithValue("@id", id);
                using (var reader = command.ExecuteReader())
                {
                    reader.Read();
                    var fullName = reader["FullName"].ToString() ?? "";
                    var email = reader["Email"].ToString() ?? "";
                    var password = reader["password"].ToString() ?? "";
                    return new Teacher(id, fullName, email, password);
                }
            }
        }

        public Task RemoveTeacherAsync(string id)
        {
            //logic to remove from database
            throw new NotImplementedException();
        }

        public Task UpdateTeacherAsync(TeacherDTO teacherDTO)
        {
            //logic to update the teacher in database
            throw new NotImplementedException();
        }
    }
}
