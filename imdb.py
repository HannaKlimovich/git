import re
import collections
import argparse
import json
import csv

try:
    list_db = open(r'ratings.list', 'r', encoding='ISO-8859-1')  # r by default
    ratings = open(r'ratings.txt', 'r+', encoding='ISO-8859-1')
    years = open(r'years.txt', 'r+', encoding='ISO-8859-1')  # ?????????? w+=create
    top = open(r'top250_movies.txt', 'r+', encoding='ISO-8859-1')  # ?????????
    js = open(r'json_sample.json', 'w+', encoding='ISO-8859-1')
    cs = open(r'csvsample.csv', 'w+', encoding='ISO-8859-1')



except FileNotFoundError:
    print('File is not found!')

else:
    strg = list_db.read()  # all info from list
    start = strg.find('New  Distribution  Votes  Rank  Title') + len(
        'New  Distribution  Votes  Rank  Title\n')  # start of top-250
    end = strg.find('\nBOTTOM 10 MOVIES (1500+ VOTES)')  # end of top-250
    strg = strg[start:end]  # top-250


    def func_years(strg):
        """
        Returns list with extracted years from doc.
        """
        all_years = []
        for num, line in enumerate(strg.splitlines()):
            year_st = line.find('(')
            year = int(line[year_st + 1:year_st + 5])  # year
            all_years.append(year)
        return all_years


    def func_rates(strg):
        """
        Returns list with extracted rates from doc.
        """
        all_rates = []
        for num, line in enumerate(strg.splitlines()):
            rat_st = re.search('\d+\.+\d', line)  # where ratings start
            all_rates.append(rat_st[0])
        return all_rates


    def func_titles(strg):
        """
        Returns list with extracted titles from doc.
        """
        all_titles = []
        for num, line in enumerate(strg.splitlines()):
            beg = re.search('\d+\.+\d', line)  # where ratings start
            end = line.find('(')  # where years start
            title = line[beg.end():end].strip()  # title names
            all_titles.append(title)
        return all_titles


    def hist_titles(all_titles):
        """
        Returns formatted titles, that are ready for writing in a file.
        """
        all_titles_wr = []
        for num in range(250):
            all_titles_wr.append('{num}) {title} \n'.format(num=num + 1, title=all_titles[num]))
        return all_titles_wr


    def hist_rates(all_rates, all_titles):
        """
        Returns list with rating histogram, that are ready for writing in a file.
        """
        all_rates_hist = []
        for i in range(250):
            title = all_titles[i]
            seq = int(float(all_rates[i]) * 10)
            all_rates_hist.append('{rate:<92} {number} {title} \n'.format(rate=seq * '+', number=seq / 10, title=title))
        return all_rates_hist


    def hist_year(all_years):
        """
        Returns list with year histogram, that are ready for writing in a file.
        """
        all_years_hist = []
        c = collections.Counter()
        for y in all_years:
            c[y] += 1
        d = dict(c.most_common())
        for key, value in d.items():
            all_years_hist.append('{0}   {1}    ({2})\n'.format(key, '+' * value, value))
        return all_years_hist


    def file_write(f_name, obj):  # FORMAT
        """
        Writes objects to file.
        """
        for i in obj:
            f_name.write(i)
        return


    def all_files():
        """
        Task4.
        """
        file_write(years, hist_year(func_years(strg)))
        file_write(top, hist_titles(func_titles(strg)))
        file_write(ratings, hist_rates(func_rates(strg), func_titles(strg)))
        return


    def f_arg_year():
        print('--------------YEAR--------------')
        for item in range(250):
            z = ('{year} {title}'.format(year=list_dic[item]['year'], title=list_dic[item]['title']))
            print(z)
            output_f.append(z+'\n')

        if str(args.format).lower() == 'json':
            list_for_js = []
            for i in list_dic:
                js_d = {}
                js_d['title'] = i['title']
                js_d['year'] = i['year']
                list_for_js.append(js_d)
            a = json.dumps(list_for_js, separators=(',\n  ', ':'))
            js.write(a)
            print('Your year json is ready.')

        if str(args.format).lower() == 'csv':
            csv_writer = csv.writer(cs, delimiter=' ',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)  # btw symbols, words
            for i in list_dic:
                csv_writer.writerow(i['title'] + ' ' + str(i['year']))
            print('Your year csv is ready.')


    def f_arg_rate():
        print('--------------RATE--------------')
        for item in range(250):
            z = ('{rate} {title}'.format(rate=list_dic[item]['rate'], title=list_dic[item]['title']))
            print(z)
            output_f.append(z+'\n')

        if str(args.format).lower() == 'json':
            print('Your rate json is ready.')
            list_for_js = []
            for i in list_dic:
                js_d = {}
                js_d['title'] = i['title']
                js_d['rate'] = i['rate']
                list_for_js.append(js_d)
            a = json.dumps(list_for_js, separators=(',\n  ', ':'))
            js.write(a)

        if str(args.format).lower() == 'csv':
            csv_writer = csv.writer(cs, delimiter=' ',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)  # btw symbols, words
            for i in list_dic:
                csv_writer.writerow(i['title'] + ' ' + str(i['rate']))
            print('Your rate csv is ready.')
        else:
            print('Sorry, incorrect input!')


    def f_arg_all():
        print('--------------ALL INFO--------------')
        for item in range(250):
            z = ('{title} |{rate}| ({year})'.format(title=list_dic[item]['title'], rate=list_dic[item]['rate'],
                                                    year=list_dic[item]['year']))
            print(z)
            output_f.append(z+'\n')

        if str(args.format).lower() == 'json':
            print('Your all info json is ready.')
            list_for_js = []
            for i in list_dic:
                js_d = {}
                js_d['title'] = i['title']
                js_d['rate'] = i['rate']
                js_d['year'] = i['year']
                list_for_js.append(js_d)
            a = json.dumps(list_for_js, separators=(',\n  ', ':'))
            js.write(a)

        if str(args.format).lower() == 'csv':
            list_for_csv = []
            csv_writer = csv.writer(cs, delimiter=' ',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)  # btw symbols, words
            for i in list_dic:
                csv_writer.writerow(i['title'] + ' |' + str(i['rate']) + '| (' + str(i['year']) + ')')
            print('Your all info csv is ready.')


    def f_hist_year():
        print('--------------YEAR RATING--------------')
        for i in hist_year(func_years(strg)):
            print(i)
            output_f.append(i+'\n')


    def f_hist_rate():
        print('--------------HISTOGRAM RATING--------------')
        for i in hist_titles(func_titles(strg)):
            print(i)
            output_f.append(i+'\n')


    # ---------------------------------------PARSING---------------------------------------
    parser = argparse.ArgumentParser()
    ######################
    list_dic = []

    for item in range(250):
        list_dic.append(
            {'title': func_titles(strg)[item], 'rate': func_rates(strg)[item],
             'year': func_years(strg)[item]})  ##отд перменная

    ###########################
    parser.add_argument('--year', action='store_true', help='Displays Top250 movies titles with year')
    parser.add_argument('--rate', action='store_true', help='Displays Top250 movies titles with rate')
    parser.add_argument('--all', action='store_true', help='Displays Top250 movies titles with rate')
    parser.add_argument('--histogram_rating', action='store_true', help='Displays Top250 movies titles with rate')
    parser.add_argument('--histogram_year', action='store_true', help='Displays Top250 movies year histogram')
    parser.add_argument('--output', action='store', help='')
    parser.add_argument('--format', action='store', help='JSON/CSV')

    args = parser.parse_args()
    output_f = []


    if args.year:
        f_arg_year()

    if args.rate:
        f_arg_rate()

    if args.all:
        f_arg_all()

    if args.histogram_rating:
        f_hist_rate()

    if args.histogram_year:
        f_hist_year()

    if getattr(args, 'output') != None:
        file_res = open(getattr(args, 'output'), 'w')
        file_write(file_res, output_f)
        """for i in range(len(output_f)):
            file_res.write(output_f[i] + '\n')"""
        file_res.close()

    list_db.close()
    ratings.close()
    years.close()
    top.close()
    js.close()
    cs.close()
