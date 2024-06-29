
using MySql.Data.MySqlClient;
using System.Data.SqlClient;

namespace Teacher_Service_API.Models.Database
{
    public class DatabaseManager
    {
        private readonly string _connectionString;
        public DatabaseManager()
        {
            _connectionString = "server=127.0.0.1;uid=root;pwd=sqlpassword;database=test-schema";
        }

        public MySqlConnection GetConnection()
        {
            return new MySqlConnection(_connectionString);
        }
    }
}
