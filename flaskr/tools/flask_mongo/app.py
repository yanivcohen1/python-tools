import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS, cross_origin

from flask_restful import Api
from flaskr.tools.flask_mongo.resources.errors import errors
from flaskr.tools.flask_mongo.database.db import initialize_db
from flaskr.tools.flask_mongo.database.models import Course, Student

app = Flask(__name__)
# app.config.from_envvar('ENV_FILE_LOCATION') # variable from (run.bat) // read from config file
current_location = os.path.dirname(os.path.abspath(__file__))
app.config.from_pyfile(current_location + '/.env.test') # read from config file
print("SECRET_KEY:" + app.config["JWT_SECRET_KEY"]) # read from config file a key
print("config read all keys:")
print(app.config) # read from config file all keys
mail = Mail(app)

api = Api(app, errors=errors)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)

# imports requiring app and mail
from flaskr.tools.flask_mongo.resources.routes import initialize_routes
initialize_routes(api)

# not from restAPI
# @app.get('/test-app')
# @app.post('/test-app')
@app.route('/test-app', methods=['GET'])
def testApp():
    # return jsonify({'name': 'alice',
    #                'email': 'alice@outlook.com'})
    # query = Movie.objects()
    from flaskr.tools.flask_mongo.database.models import Movie
    movies:list[Movie] = Movie.objects() # pylint: disable=no-member
    print(movies[0].embeds[0].name) # yan1
    print(movies[1].embeds[0].name) # yan2
    return movies.to_json()

if __name__ == "__main__":
    with app.app_context():
    #     # Create the tables
    #     db.create_all()

    #     # Insert initial users
    #     user1 = User(id=1, username="yaniv",
    #                  password=bcrypt.generate_password_hash("yaniv_P").decode('utf-8'))
    #     user2 = User(id=2, username="yaniv2",
    #                  password=bcrypt.generate_password_hash("yaniv2_P").decode('utf-8'))
    #     user3 = User(id=3, username="yaniv3",
    #                  password=bcrypt.generate_password_hash("yaniv3_P").decode('utf-8'))
    #     db.session.add_all([user1, user2, user3])
    #     db.session.commit()

    #     # Insert initial data
    #     author1 = Author(id=1, name="F. Scott Fitzgerald")
    #     author2 = Author(id=2, name="George Orwell")
    #     author3 = Author(id=3, name="Jane Austen")

    #     db.session.add_all([author1, author2, author3])
    #     db.session.commit()

    #     book1 = Book(id=1, title="The Great Gatsby", author_id=author1.id)
    #     book2 = Book(id=2, title="1984", author_id=author2.id)
    #     book3 = Book(id=3, title="Pride and Prejudice", author_id=author3.id)

    #     db.session.add_all([book1, book2, book3])
    #     db.session.commit()

    #   # for meny to meny
    #     course1: Course = Course(name="Math").save()
    #     course2: Course = Course(name="Science").save()
    #     student1: Student = Student(name="Alice", courses=[course1, course2]).save()
    #     student2: Student = Student(name="Bob", courses=[course1]).save()
    #     course1.update(push_all__students=[student1, student2])
    #     course2.update(push__students=student2)

        # Get Anna’s courses
        # Paginate Student query instead of fetching first
        # Set pagination parameters
        page_number = 1  # example page number
        page_size = 10   # example page size
        student_pages = Student.objects(name="Alice").skip((page_number - 1) * page_size).limit(page_size)  # pylint: disable=no-member
        print(f"Retrieved {student_pages.count()} student(s) on page {page_number}")
        # Iterate through the page of students and print their courses
        for student in student_pages:
            print(f"{student.name} courses: {[course.name for course in student.courses]}")

        # Get all students in Math
        math: Course = Course.objects(name="Math").first() # pylint: disable=no-member
        print(f"Students in Math: {[student.name for student in math.students]}")

    app.run(debug=True, port=5000)
