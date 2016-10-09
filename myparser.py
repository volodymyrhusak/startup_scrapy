# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json


class Parser:

    def __init__(self, url):
        self.url = 'http://' + url.strip()
        response = requests.get(self.url, timeout=100, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.content
        print response.status_code
        print response.url
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_company_name(self):
        result = self.soup.find('h1', class_="company__title page-title").text
        return result.encode('utf-8')

    def get_company_short_description(self):
        result = self.soup.find('div', class_='company__short-description')
        return result.get_text().strip().strip('\n').encode('utf-8')

    def get_company_description(self):
        return self.soup.find('div', class_="company__description").text.replace('\n', '').encode('utf-8')

    def get_homepage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Homepage') != -1:
                return li.find('a').text.encode('utf-8')

    def get_sector(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Sector') != -1:
                return li.find('a').text.encode('utf-8')

    def get_founded(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Founded') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_business_model(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Business Model') != -1:
                return li.find('a').text.encode('utf-8')

    def get_funding_stage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Funding Stage') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_amount_raised(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Amount Raised') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_employees(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Employees') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_products(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Products') != -1:
                result = li.find('div', class_="company-parameters__value").text
                result = result.replace('\n', '').replace(' ', '')
                return result.encode('utf-8')

    def get_product_stage(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Product Stage') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_patent(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Patent') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def get_geographical_markets(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Geographical Markets') != -1:
                result = li.find('div', class_="company-parameters__value").text
                result = result.replace('\n', '').replace(' ', '')
                return result.encode('utf-8')

    def get_tags(self):
        tags = list()
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Tags') != -1:
                for tag in li.find_all('a', class_="tags__tag "):
                    tags.append(tag.text)
                return ', '.join(tags).encode('utf-8')

    def get_target_markets(self):
        tags = list()
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Target Markets') != -1:
                for tag in li.find_all('a', class_="tags__tag "):
                    tags.append(tag.text)
                return ', '.join(tags).encode('utf-8')

    def get_address(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Address') != -1:
                result = li.find('div', class_="company-parameters__value")
                return result.text.strip().strip('\n').encode('utf-8')

    def get_offices_abroad(self):
        for li in self.soup.find_all('li', class_="company-parameters__one"):
            if str(li).find('Offices abroad') != -1:
                return li.find('div', class_="company-parameters__value").text.encode('utf-8')

    def _get_team(self):
        lst = [u'-',u'-',u'-']
        team = self.soup.find('div', class_='company-team') 
        for i, person in enumerate(team.find_all('div', class_='company-team__info')[0:2]):
            name = person.find('div', class_='company-team__name').get_text()
            position = person.find('div', class_='company-team__position').get_text()
            if name and position:
                lst[i] = name + ', ' + position
        return lst

    def get_tim_member_1(self):
        return self._get_team()[0].encode('utf-8')

    def get_tim_member_2(self):
        return self._get_team()[1].encode('utf-8')

    def get_tim_member_3(self):
        return self._get_team()[2].encode('utf-8')

    def get_funding_round_type(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 0:
            item = self.soup.find_all('div', class_='company-fundings__one')[0]
            return item.find('h3', class_='company-fundings__round round__data').text.encode('utf-8')
        return u'-'

    def get_funding_round_sum(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 0:
            item = self.soup.find_all('div', class_='company-fundings__one')[0]
            item = item.find('span', class_='company-fundings__sum-currency round__data')
            return item.text.strip().strip('\n').encode('utf-8')
        return u'-'

    def get_funding_round_investor(self):
        investors = []
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 0:
            item = self.soup.find_all('div', class_='company-fundings__one')[0]
            for investor in item.find_all('li', class_='company-fundings__investor round__data'):
                investors.append(investor.text.strip('\n').strip())
            return ', '.join(investors).encode('utf-8')
        return u'-'

    def get_funding_rounds_date(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 0:
            item = self.soup.find_all('div', class_='company-fundings__one')[0]
            return item.find('p', class_="company-fundings__date round__data").text.encode('utf-8')
        return u'-'

    def get_funding_round_type_1(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 1:
            item = self.soup.find_all('div', class_='company-fundings__one')[1]
            return item.find('h3', class_='company-fundings__round round__data').text.encode('utf-8')
        return u'-'

    def get_funding_round_sum_1(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 1:
            item = self.soup.find_all('div', class_='company-fundings__one')[1]
            item = item.find('span', class_='company-fundings__sum-currency round__data')
            return item.text.strip().strip('\n').encode('utf-8')
        return u'-'

    def get_funding_round_investor_1(self):
        investors = []
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 1:
            item = self.soup.find_all('div', class_='company-fundings__one')[1]
            for investor in item.find_all('li', class_='company-fundings__investor round__data'):
                investors.append(investor.text.strip('\n').strip())
            return ', '.join(investors).encode('utf-8')
        return u'-'

    def get_funding_rounds_date_1(self):
        if len(self.soup.find_all('div', class_='company-fundings__one')) > 1:
            item = self.soup.find_all('div', class_='company-fundings__one')[1]
            return item.find('p', class_="company-fundings__date round__data").text.encode('utf-8')
        return u'-'

    def get_facebook(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('facebook.com') != -1:
                return l.get('href').encode('utf-8')

    def get_twitter(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('twitter.com') != -1:
                return l.get('href').encode('utf-8')

    def get_linkedin(self):
        for l in self.soup.find_all('a', class_="social-networks__link"):
            if l.get('href').find('linkedin.com') != -1:
                return l.get('href').encode('utf-8')

    def get_url_source(self):
        return self.url.strip().encode('utf-8')

    def get_similar_link(self):
        comp = self.url.split('/')[-1].strip()
        link = 'http://finder.startupnationcentral.org/similar/%s'%comp
        # print link
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        data = response.content.decode('utf-8')
        # print data
        data = json.loads(data)
        similar = []
        for i in data:
            similar.append('finder.startupnationcentral.org/c/' + i['url'])
        return (similar[0].encode('utf-8'),similar[1].encode('utf-8'),similar[2].encode('utf-8'))

if __name__ == '__main__':
    parser = Parser('finder.startupnationcentral.org/c/syneron-medical')
    print(parser.get_tim_member_1())
