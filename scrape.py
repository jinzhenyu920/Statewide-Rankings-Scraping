#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup

base_url = 'https://www.ncdc.noaa.gov/cag/statewide/rankings/'


def extract_params():
    response = request.urlopen(base_url)
    html_doc = response.read().decode('utf8')

    soup = BeautifulSoup(html_doc, features='html.parser')
    params = dict()
    for label in soup.find(id='required').findAll('label'):
        params[label.text.replace(':', '')] = dict()

    for k, v in params.items():
        for option in soup.find(id=k.lower()).findAll('option'):
            v[option.text] = option.get('value')

    return params


def get_xml_url(params):
    file_name = '{}-{}-{}{}'.format(
        params['State'], params['Parameter'],
        params['Year'], params['Month'].zfill(2)
    )
    return ''.join([base_url, file_name, '.xml'])


if __name__ == '__main__':
    params = {
        'Parameter': 'Average Temperature',
        'Year': '2016',
        'Month': 'August',
        'State': 'Virginia'
    }

    param_dict = extract_params()
    for k, v in params.items():
        params[k] = param_dict[k][v]

    url = get_xml_url(params)
    print(url)
