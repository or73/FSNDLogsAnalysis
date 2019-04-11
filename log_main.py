#!/usr/bin/env python3

import datetime
import time
import psycopg2  # postgres

DBNAME = 'news'


def print_table(query, field1='Rank', field2='Name', field3='Views'):
    """
    :param query: data to print
    :param field1: Column 1 title
    :param field2: Column 2 title
    :param field3: Column 3 title
    :return: do not return a value, this function prints data
    """
    try:
        cursor.execute(query)
        answer = cursor.fetchall()
        print('\t| %s \t| %s\t\t\t\t      | %s  |' % (field1, field2, field3))
        print('\t|-------+-------------------------------------+--------|')
        for i, record in enumerate(answer):
            rank = str(i + 1)
            name = str(record[0])
            views = str(record[1])
            if len(name) < 35:
                name += (' ' * (35 - len(name)))
            if len(views) < 6:
                views += (' ' * (6 - len(views)))
            print('\t| %s\t| %s | %s |' % (rank, name, views))
        print('\n')
    except Exception as e:
        print('Error in Answer 1: ', e)


def main(cursor):
    """
    :param cursor: database cursor
    :return: do not return a value, executes several queries to 'news' database
                to answer 3 questions
    """

    # 1. What are the most popular three articles of all time?
    #    Which articles have been accessed the most? Present this
    #       information as a sorted list with the most popular
    #       article at the top.
    query1 = 'SELECT articles.title, COUNT(*) AS results' \
             '  FROM articles, log' \
             '  WHERE log.status = \'200 OK\'' \
             '   AND articles.slug = substr(log.path, 10)' \
             '   GROUP BY articles.title' \
             '   ORDER BY results DESC ' \
             '   LIMIT 3;'
    # 2. Who are the most popular article authors of all time? That is,
    #       when you sum up all of the articles each author has written,
    #       which authors get the most page views? Present this as a
    #       sorted list with the most popular author at the top.
    query2 = 'SELECT authors.name, COUNT(*) AS result' \
             '  FROM log, authors, articles' \
             '  WHERE log.status = \'200 OK\'' \
             '  AND articles.slug = substr(log.path, 10)' \
             '  AND authors.id = articles.author' \
             '  GROUP BY authors.name' \
             '  ORDER BY result DESC'

    # 3. On which days did more than 1% of requests lead to errors?
    #       The log table includes a column status that indicates
    #       the HTTP status code that the news site sent to the user's browser.
    query3 = 'SELECT * ' \
             '  FROM (' \
             '  SELECT date(time), round(100.0*sum(CASE log.status ' \
             '      WHEN \'200 OK\' ' \
             '      THEN 0 ' \
             '      ELSE 1 ' \
             '      END)/count(log.status),4) AS error ' \
             '      FROM log ' \
             '      GROUP BY date(time) ' \
             '      ORDER BY error DESC) AS subq ' \
             '  WHERE error > 1;'

    print('\n\t\t---------------- QUESTION 1 ----------------')
    print('\nThe most popular three articles of all time are:\n')
    print_table(query1)

    print('\n\t\t---------------- QUESTION 2 ----------------')
    print('\nThe most popular article authors of all time are:\n')
    print_table(query2)

    print('\n\t\t---------------- QUESTION 3 ----------------')
    print('\nThe days with more than 1% of requests lead to errors are:\n')
    print_table(query3, 'Rank', 'Date', 'Error')

    db.close()


if __name__ == '__main__':
    print('\n\t\tProject: Logs Analysis\n\t\tDeveloper: Oscar Reyes\n')
    localtime = time.asctime(time.localtime(time.time()))
    print('START - program execution time stamp: ', localtime)
    print('_______________________________\n')
    # Create connection with DB
    try:
        # db = psycopg2.connect(database=DBNAME)
        db = psycopg2.connect('dbname=news')
        cursor = db.cursor()
        main(cursor)
    except Exception as e:
        print('Database connection error: ', e)
        exit()

    localtime = time.asctime(time.localtime(time.time()))
    print('\nSTOP - program execution time stamp: ', localtime)
    print('_______________________________\n')
