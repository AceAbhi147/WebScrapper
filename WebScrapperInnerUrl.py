from bs4 import BeautifulSoup
import requests

from Attributes import Attributes


class Scrape:
    def __init__(self, attributes):
        self.attributes = attributes

    def scrape_inner_url(self):
        html = requests.get(self.attributes.link).text
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())

        tags = soup.find('div', class_='sgeneros')
        if tags:
            tags = tags.find_all('a')
        if tags:
            self.attributes.tags = ', '.join(tag.text for tag in tags)

        description = soup.find('div', class_='wp-content')
        if description and description.p:
            self.attributes.description = description.text

        custom_fields = soup.find_all('div', class_='custom_fields')
        for custom_field in custom_fields:
            if custom_field.b.text == 'Episodes':
                self.attributes.number_of_episodes = custom_field.span.text
            if custom_field.b.text == 'Status':
                self.attributes.status = custom_field.span.text
        # print(attributes)


if __name__ == '__main__':
    attributes = Attributes()
    attributes.link = '' # Pushing without link
    Scrape(attributes).scrape_inner_url()
