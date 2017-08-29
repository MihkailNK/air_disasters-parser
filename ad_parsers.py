from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse

# Proto-class
class ADParser(object):
    def __init__(self, decsription, url):
        self.description = decsription
        self.page = None
        self.soup = None
        self.url = url # "http://www.airdisaster.ru/database.php?id="
        self.get_soup()

    def get_soup(self):
        self.page = urllib.request.urlopen(self.url + str(self.description))
        self.soup = BeautifulSoup(self.page, 'lxml')

    def html_rus(self, st):
        st = st.replace('\xa0', '')
        st = st.replace('?', 'no data')
        return st  # encoding.smart_str(st, encoding='windows-1251', errors='ignore')

# Parse and return the victims count from page
class DisasterParser(ADParser):
    def __init__(self, decsription):
        super().__init__(decsription, "http://www.airdisaster.ru/database.php?id=")

    def get_statistic(self):
        stat_result = {'v_passengers': 0, 'v_personal': 0, 'v_onland': 0, 'passengers': 0, 'personal': 0, 'total':0}
        c_table = self.soup.findAll('table')
        c_tbody = c_table[2].find("tbody")
        table_static =c_tbody.findAll("tbody")[3]
        table_static_body = table_static.findAll('tbody')
        rows =table_static_body[1].find_all('tr')
        for row in rows:
            cols = row.findAll('td')
            col_description = self.html_rus(cols[0].text.upper())
            # Air crew statistics
            if 'экипаж'.upper() in col_description:
                stat_result['v_personal'] = self.html_rus(cols[2].text)
                stat_result['personal'] = self.html_rus(cols[1].text)
            # Passengers statictic
            elif 'пассажир'.upper() in col_description:
                stat_result['v_passengers'] = self.html_rus(cols[2].text)
                stat_result['passengers'] = self.html_rus(cols[1].text)
            # Victims on land
            elif 'земл'.upper() in col_description:
                stat_result['v_onland'] = self.html_rus(cols[2].text)
        # Total count from page
        table_total = table_static_body[2].findAll('td')
        col_description = self.html_rus(table_total[0].text.lower())
        if 'всего погибших' in col_description:
            stat_result['total'] = self.html_rus(table_total[1].text)
        return stat_result

    # Parse the data string from the page
    def get_date(self):
        # tbody =  table[2].find("tbody")
        c_table = self.soup.findAll('table')
        c_tbody = c_table[2].tbody.findAll("tbody")
        c_tr = c_tbody[0].find_all('tr')
        c_td = c_tr=c_tr[3].find_all('td')[2].find_all('b')
        for r in c_td:
            if 'Дата:' in r.text:
                disaster_date =self.html_rus(r.nextSibling).split(' ')
                if len(disaster_date) > 2:
                    yy = disaster_date[2]
                    mm = self._parse_month_num(disaster_date[1])
                    dd = disaster_date[0]
                    result = dict(y=yy, m=mm, d=dd)
                    return result
        return dict(y='No data', m='No data', d='No data')

    def _parse_month_num(self, month):
        months = dict(янв=1, фев=2, мар=3, апр=4, май=5, мая=5, июн=6, июл=7, авг=8, сен=9, окт=10, ноя=11, дек=12)
        month_key = month[0:3].lower()
        if month_key in months:
            return months[month_key]


# Parse and return the list of id of current year
class YearParser(ADParser):
    def __init__(self, decsription):
        super().__init__(decsription, "http://www.airdisaster.ru/database.php?y=")

    def get_disasters_ids(self):
        find_result = self.soup.findAll("td", {"class": "tdh2"})
        crash_id_list = list()
        for mysoup in find_result:
            for a in mysoup.find_all('a', href=True):
                link = str(a['href'])
                crash_id_list.append(link[len("/database.php?id="):])
        return crash_id_list


