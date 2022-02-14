from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector as connector
from dbcm import UseDatabase

app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search letters page')


def log_request(req: 'flask request', res: str):
    # with open('vsearch.log', 'a') as file:
    #     print(req.form, req.remote_addr, req.user_agent, res, file=file, sep='|')
    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'mypassword',
                'database': 'vsearchlogDB'
                }

    with UseDatabase(dbconfig) as cursor:
        _SQL = """insert into log
        (phrase, letters, ip, browser_string, results)
        values
        (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res))


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results, )

@app.route('/viewlog')
def view_log() -> 'html':
    with open('vsearch.log') as file:
        content = []
        for line in file:
            request_array = []
            for item in line.split('|'):
                request_array.append(escape(item))
            content.append(request_array)
        titles = ('Form data', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=content)


if __name__ == '__main__':
    app.run(debug=True)
