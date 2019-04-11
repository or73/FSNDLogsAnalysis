#!/usr/bin/env python3

import datetime
import time
import psycopg2  # postgres

DBNAME = 'news'


def print_table(data):
    print('table')
    for i, record in enumerate(data):
        print('Rank{rank}: '.format(rank=i + 1))
        print(' \'{name}\' has had {views} views.'.format(name=record[0], views=record[1]))


def main(cursor):

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
             '  ORDER BY restuls DESC'

    # 3. On which days did more than 1% of requests lead to errors?
    #       The log table includes a column status that indicates
    #       the HTTP status code that the news site sent to the user's browser.
    query3 = 'SELECT * ' \
             '  FROM (' \
             '  SELECT date(time), round(100.0*sum(CASE log.status ' \
             '                                      WHEN \'200 OK\' ' \
             '                                      THEN 0 ' \
             '                                      ELSE 1 END)/count(log.status),4) AS error ' \
             '      FROM log ' \
             '      GROUP BY date(time) ' \
             '      ORDER BY error DESC) AS subq ' \
             '  WHERE error > 1;'
    try:

        cursor.execute(query1)
        answer1 = cursor.fetchall()
    except Exception as e:
        print('Error in Answer 1: ', e)

    try:
        cursor.execute(query2)
        answer2 = cursor.fetchall()
    except Exception as e:
        print('Error in Answer 2: ', e)

    try:
        cursor.execute(query3)
        answer3 = cursor.fetchall()
    except Exception as e:
        print('Error in Answer 3: ', e)

    print('The most popular three articles of all time are:')
    print_table(answer1)

    print('The most popular article authors of all itme are:')
    print_table(answer2)

    print('The days with more than 1% of requests lead to errors are:')
    print_table(answer3)

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
        print('1.')
        # cursor = db.cursor()
        # print('2.')
        # main(cursor)
    except Exception as e:
        print('Database connection error: ', e)
        exit()

    localtime = time.asctime(time.localtime(time.time()))
    print('\nSTOP - program execution time stamp: ', localtime)
    print('_______________________________\n')

