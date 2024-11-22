from flask import Flask, request, jsonify, make_response, render_template
from database.chroma_handler import rag_query, get_chroma

app = Flask(__name__)
db = get_chroma()
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    # data = request.get_json(force=True)
    # query_json = data.get('query', '')
    query = request.form.get('query')
    # if not query:
    #     return make_response({'error': 'Empty query'}, 400)

    response = rag_query(query, db)
    return render_template('response.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)
