import sys
import os
import hashlib
import json
import requests

from requests.exceptions import HTTPError


def issue_request(method, url, headers, data=None, binary=False):
    if data is not None and not binary:
        data = json.dumps(data)

    response = requests.request(method, url, headers=headers, data=data)

    try:
        response.raise_for_status()
        try:
            data = json.loads(response.text)
        except ValueError:
            data = response.content
    except HTTPError as error:
        print('Caught an HTTPError: {}'.format(error.message))
        print('Body:\n', response.text)
        raise

    return data


class Figshare:
    """ A Python interface to Figshare"""
    def __init__(self, token):
        self.baseurl = "https://api.figshare.com/v2"
        self.token = token

    def endpoint(self, link):
        return self.baseurl + link

    def get_headers(self, token=None):
        """ HTTP header information. """
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = 'token {0}'.format(token)

        return headers

    def create_article(self, title, description, defined_type, tags, categories):
        """ Create a new Figshare article."""
        if isinstance(categories, int):
            categories = [categories]

        data = {'title': title,
                'description': description,
                'defined_type': defined_type,
                'categories': categories,
                'tags': tags}

        url = self.endpoint("/account/articles")
        headers = self.get_headers(self.token)
        response = self.issue_request('POST', url, headers=headers, data=data)
        response = json.loads(response.body_string())

        if "error" not in response.keys():
            article_id = int(response["location"].split("/")[-1])
        else:
            article_id = None
        return article_id

    def update_article(self, article_id, **kwargs):
        """ Updates an article with a given article_id. """
        allowed = {'title', 'description', 'defined_type', 'tags', 'categories'}
        valid_keys = set(kwargs.keys()).intersection(set(allowed))
        body = {}

        for key in valid_keys:
            body[key] = kwargs[key]

        url = self.endpoint('/account/articles/{0}'.format(str(article_id)))
        headers = self.get_headers(token=self.token)
        response = issue_request('PUT', url, headers=headers,
                                 data=json.dumps(body))
        response = json.loads(response.text)
        return response

    def get_article_details(self, article_id, private=False):
        """ Return the details of an article with a given article ID. """
        if private:
            url = self.endpoint('/account/articles/{}'.format(str(article_id)))
        else:
            url = self.endpoint('/articles/{}'.format(str(article_id)))
        headers = self.get_headers(self.token)
        response = issue_request('GET', url, headers=headers)
        details = json.loads(response.body_string())
        return details

    def list_files(self, article_id):
        """ List all the files associated with a given article. """
        url = self.endpoint('/account/articles/{}/files'.format(article_id))
        headers = self.get_headers(self.token)
        response = issue_request('GET', url, headers=headers)
        files = json.loads(response.body_string())
        return files

    def get_file_details(self, article_id, file_id):
        """ Get the details about a file associated with a given article. """
        path = '/account/articles/{0}/files/{1}'.format(article_id, file_id)
        url = self.endpoint(path)
        response = issue_request('GET', url,
                                 headers=self.get_headers(token=self.token))
        response = json.loads(response.body_string())
        return response
