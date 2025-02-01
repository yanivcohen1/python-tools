from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/db_name'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:yanivc77@localhost/alchemy"
)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define the models
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", backref=db.backref("books", lazy=True))


# Define the Marshmallow schemas
class AuthorSchema(SQLAlchemySchema):
    class Meta:
        model = Author

    id = auto_field()
    name = auto_field()


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book

    id = auto_field()
    title = auto_field()
    author_id = auto_field()
    author = fields.Nested(AuthorSchema)


author_schema = AuthorSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Perform an inner join query
@app.route("/books_with_authors") # , methods=["GET"]
def get_books_with_authors():
    # Perform an inner join query
    result = db.session.query(Book).join(Author).all()
    books_with_authors = books_schema.dump(result)
    return jsonify(books_with_authors)


@app.route("/add_book", methods=["POST"])
def add_book():
    try:
        data = request.get_json()
        book_data = book_schema.load(data)
        new_book = Book(title=book_data["title"], author_id=book_data["author_id"])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(book_schema.dump(new_book)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/get_book/<int:book_id>') # http://127.0.0.1:5000/get_book/2
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/get_book2') # http://127.0.0.1:5000/get_book2?book_id=2
def get_book2():
    book_id = request.args.get('book_id', type=int)
    if book_id is None:
        return jsonify({'error': 'book_id query parameter is required'}), 400
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))

@app.route('/find_book_by_name')# GET /find_book_by_name?book_name=The Great Gatsby
def find_book_by_name():
    book_name = request.args.get('book_name')
    if book_name is None:
        return jsonify({'error': 'book_name query parameter is required'}), 400
    book = Book.query.filter_by(title=book_name).first_or_404()
    return jsonify(book_schema.dump(book))

# GET /find_books_by_author_name?author_name=F. Scott Fitzgerald
@app.route('/find_books_by_author_name')
def find_books_by_author_name():
    author_name = request.args.get('author_name')
    if author_name is None:
        return jsonify({'error': 'author_name query parameter is required'}), 400
    author: Author = Author.query.filter_by(name=author_name).first_or_404()
    books = Book.query.filter_by(author_id=author.id).all()
    # return jsonify(book_schema.dump(books, many=True))
    return jsonify(books_schema.dump(books))


if __name__ == "__main__":
    # with app.app_context():
    #     # Create the tables
    #     db.create_all()

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

    app.run(debug=True)
