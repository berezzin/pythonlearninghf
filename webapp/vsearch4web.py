import time

import mysql.connector.errors
from flask import Flask, render_template, request, escape, session, copy_current_request_context
from vsearch import search4letters
from dbcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in
from threading import Thread

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'mypassword',
                          'database': 'vsearchlogDB'
                          }


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search letters page')


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    @copy_current_request_context
    def log_request(req: 'flask request', res: str):
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""
            time.sleep(10)
            cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,
                                  res))

    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results'
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except CredentialsError as err:
        print(f'User-id/password is incorrect. Error: {str(err)}')
    except Exception as err:
        print(f'****** Logging error is: {err}')
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results, )


@app.route('/viewlog')
@check_logged_in
def view_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            content = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=content)
    except CredentialsError as err:
        print(f'User-id/password is incorrect. Error: {str(err)}')
    except ConnectionError as err:
        print(f'Is your database switched on? Error: {str(err)}')
    except SQLError as err:
        print(f'Is your query correct? Error: {str(err)}')
    except Exception as err:
        print(f'***** Logging error is : {str(err)}')


@app.route('/login')
def do_login():
    session['logged_in'] = True
    return 'You are logged in'


@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    return 'You are logged out'


app.secret_key = 'ItsMySecret'

if __name__ == '__main__':
    app.run(debug=True)
