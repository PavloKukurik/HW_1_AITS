from flask import Flask, request, jsonify, abort

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Novel"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian"
    },
    {
        "id": 3,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Novel"
    },
    {
        "id": 4,
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "year": 1988,
        "genre": "Science"
    },
    {
        "id": 5,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "year": 1954,
        "genre": "Fantasy"
    },
    {
        "id": 6,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "genre": "Novel"
    },
    {
        "id": 7,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "year": 1951,
        "genre": "Novel"
    }
]


def get_new_id():
    if books:
        return max(book["id"] for book in books) + 1
    return 1


@app.route("/books", methods=["GET"])
def get_books():
    author = request.args.get("author")
    year = request.args.get("year")
    genre = request.args.get("genre")

    filtered_books = books

    if author:
        filtered_books = [book for book in filtered_books if book["author"] == author]
    if year:
        try:
            year_int = int(year)
            filtered_books = [book for book in filtered_books if book["year"] == year_int]
        except ValueError:
            abort(400, description="Invalid year format")
    if genre:
        filtered_books = [book for book in filtered_books if book["genre"] == genre]

    return jsonify(filtered_books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def add_book():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    data = request.get_json()
    # Перевірка наявності необхідних полів
    for field in ["title", "author", "year", "genre"]:
        if field not in data:
            abort(400, description=f"Missing field: {field}")

    try:
        year_int = int(data["year"])
    except ValueError:
        abort(400, description="Year must be an integer")

    new_book = {
        "id": get_new_id(),
        "title": data["title"],
        "author": data["author"],
        "year": year_int,
        "genre": data["genre"]
    }
    books.append(new_book)
    return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
