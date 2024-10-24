from database.chroma_handler import generate_data, rag_query, get_chroma


def main() -> None:
    # db = generate_data()
    db = get_chroma()
    query = input('Enter your query: ')
    print(rag_query(query, db))
    return


if __name__ == '__main__':
    main()
