import requests

version = '0.1'
user_agent = 'wikipy/' + version + '(https://github.com/tomshen/wikipy)'
headers = {'User-Agent': user_agent}

def getJSON(endpoint, payload):
    payload['format'] = 'json'
    return requests.get(endpoint, params=payload, headers=headers).json()

class Wiki:
    def __init__(self, endpoint='http://en.wikipedia.org/w/api.php'):
        self.endpoint = endpoint

    def getPage(self, title):
        return Page(self.endpoint, title)

    def getJSON(self, payload):
        return getJSON(self.endpoint, payload)

class Page:
    def __init__(self, endpoint, title):
        if '://' in endpoint:
            head, tail = endpoint.split('://')
            domain = head + '://' + tail[:tail.index('/')]
        else:
            domain = endpoint.split('/')[0]
        raw_payload = {'action': 'query',
                       'titles': title,
                       'prop': 'revisions',
                       'rvprop': 'content'}
        self.json_raw_text = getJSON(endpoint, raw_payload)
        for page in self.json_raw_text['query']['pages'].values():
            self.raw_text = page['revisions'][0]['*'].strip()

        parsed_payload = {'action': 'parse',
                          'page': title,
                          'prop': 'text'}
        self.json_parsed = getJSON(endpoint, parsed_payload)

        def cleanHTML(html):
            return html.strip().replace('//', 'http://').replace('href="/', 'href="' + domain + '/')

        self.html = cleanHTML(self.json_parsed['parse']['text']['*'])

    def getHTMLContent(self):
        return self.html

    def getHTMLArticle(self):
        pass # returns a cleaned up version of only the main article

    def getRawContent(self):
        return self.raw_text

    def getRawArticle(self):
        content = self.getRawContent()
        if "'''" in content[:content.index('==')]:
            content_head = content[:content.index("'''")]
            if '}}' in content_head:
                article_start = content_head.rindex('}}')+ len('}}')
                content = content[article_start:]
        article_endings = ['== See also ==', '==See also==',
                           '== References ==', '==References==',
                           '== Further reading ==', '==Further reading==',
                           '== External links ==', '==External links==']
        for ending in article_endings:
            if ending in content:
                return content[:content.index(ending)].strip()
        return content.strip()

    def getRawReferences(self):
        content = self.getRawContent()
        if '== References ==' in content:
            content = content[content.index('== References =='):]
            return content[:content.index('==', len('== References =='))].strip()
        else:
            return 'No references found.'