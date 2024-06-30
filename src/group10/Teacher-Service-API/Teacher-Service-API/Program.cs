
using Microsoft.AspNetCore.Http.Features;
using Teacher_Service_API.Models.Database;
using Teacher_Service_API.Models.Database.Repositories;

namespace Teacher_Service_API
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();            

            builder.Services.AddSingleton<TeacherRepository>();
            builder.Services.AddSingleton<DatabaseManager>();
            builder.Services.AddSingleton<CourseRepository>();
            builder.Services.AddSingleton<ImageFileRepository>();
            builder.Services.AddSingleton<VideoFileRepository>();
            builder.Services.AddSingleton<ExamRepository>();
            builder.Services.AddSingleton<QuestionRepository>();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            //app.UseHttpsRedirection();

            app.UseAuthorization();


            app.MapControllers();

            app.Run();
        }
    }
}
