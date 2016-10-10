# -*- coding: utf-8 -*-
from myparser import Parser
import csv

title = ['"company_name"','"company_short_description"','"Company_description"','"homepage"','"sector"','"founded"','"business_model"','"amount_raised"','"funding_stage"','"employees"','"products"','"products_stage"','"tags"','"address"','"offices_abroad"','"geographical_market"','"target_markets"','"patent"','"tim_member_1"','"tim_member_2"','"tim_member_3"','"funding_round_type"','"funding_round_sum"','"funding_round_investor"','"funding_rounds_date"','"funding_round_type_1"','"funding_round_sum_1"','"funding_round_investor_1"','"funding_rounds_date_1"','"facebook"','"twitter"','"linkedin"','"url_source"','"Similar companies 1"','"Similar companies 2"','"Similar companies 3"']

items = ['get_company_name','get_company_short_description','get_company_description','get_homepage',
 'get_sector','get_founded','get_business_model','get_amount_raised','get_funding_stage',
 'get_employees','get_products','get_product_stage','get_tags','get_address','get_offices_abroad',
 'get_geographical_markets','get_target_markets','get_patent','get_tim_member_1','get_tim_member_2',
 'get_tim_member_3','get_funding_round_type','get_funding_round_sum','get_funding_round_investor',
 'get_funding_rounds_date','get_funding_round_type_1','get_funding_round_sum_1','get_funding_round_investor_1',
 'get_funding_rounds_date_1','get_facebook','get_twitter','get_linkedin','get_url_source','get_similar_link']
    

with open('urls.txt', 'r') as in_file, open('combined_file.csv', 'w') as outcsv, open('log_file.log', 'w') as log_file:
    writer = csv.writer(outcsv)
    writer.writerow(title)

    for i, url in enumerate(in_file.readlines()):
        try:
            parser = Parser(url)
            result = []
            log = str(i) + ' parse page: ' + url
            print log
            log_file.write(log+'')
            for item in items:
                to_call = getattr(parser, item)
                call = to_call()
                if isinstance(call,tuple):
                    for v in call:
                        result.append((v or '-'))
                else:
                    result.append((call or '-'))
            log_file.write('Done ' +'\n\n')
        except Exception, e:
            print e
            log_file.write('ERROR - ' str(e)+'\n\n')
        
        writer = csv.writer(outcsv)
        writer.writerow(result)

