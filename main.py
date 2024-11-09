from database.chroma_handler import generate_data, rag_query, get_chroma
from parser.parser import get_bestiary
from api import app


def main() -> None:
    # get_bestiary()
    # db = generate_data()
    # db = get_chroma()
    app.run(host='0.0.0.0', port=8000)
    return


if __name__ == '__main__':
    main()
