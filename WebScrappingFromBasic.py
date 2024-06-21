import logging
from PIL import Image

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import xlsxwriter

import WebScrapperInnerUrl
from Attributes import Attributes

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Scrape:

    def __init__(self, url):
        self.url = url
        self.page = 1
        self.workbook = xlsxwriter.Workbook('File.xlsx')

    def configure_firefor_driver(self):
        # Add additional options to the webdriver
        firefox_options = FirefoxOptions()
        # Add the argument and make the browser Headless
        firefox_options.add_argument("--headless")

        # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
        # If driver is in PATH, no need to provide executable_path
        driver = webdriver.Firefox(executable_path="./geckodriver", options=firefox_options)
        return driver

    def get_html_page(self):
        headless_browser = self.configure_firefor_driver()
        headless_browser.get(self.url)
        return headless_browser.page_source

    def get_html_page_using_request_lib(self):
        return requests.get(f'{self.url}{self.page}/').text

    def create_worksheet(self, name):
        # Bold format for cells
        bold_format = self.workbook.add_format()
        bold_format.set_bold()
        bold_format.set_align('vcenter')

        # Vertically center aligned format for cells
        align_format = self.workbook.add_format()
        align_format.set_align('vcenter')
        align_format.set_text_wrap()

        # Create worksheet
        worksheet = self.workbook.add_worksheet(name)

        # Setting column width
        columns = [(5, 'S.no'), (45, 'Image'), (50, 'Title'), (50, 'Description'), (7, 'Rating'),
                   (5, 'Year'), (80, 'Link'), (50, 'Tags'), (5, 'Number of Episodes'), (10, 'Status')]

        for i in range(len(columns)):
            worksheet.set_column(i, i, columns[i][0], align_format)
            worksheet.write(0, i, columns[i][1], bold_format)

        return worksheet

    def add_details_in_worksheet(self, row, attributes, worksheet):
        # Setting the height for the row
        worksheet.set_row(row, 300)

        worksheet.write(row, 0, row)
        resize_scale = self.calculate_scale(f'./DownloadedImage/{attributes.image_count}.jpg', (240, 240))
        worksheet.insert_image(row, 1, f'./DownloadedImage/{attributes.image_count}.jpg',
                               {'x_scale': resize_scale, 'y_scale': resize_scale})
        worksheet.write(row, 2, attributes.title)
        worksheet.write(row, 3, attributes.description)
        worksheet.write(row, 4, attributes.rating)
        worksheet.write(row, 5, attributes.year)
        worksheet.write(row, 6, attributes.link)
        worksheet.write(row, 7, attributes.tags)
        worksheet.write(row, 8, attributes.number_of_episodes)
        worksheet.write(row, 9, attributes.status)

    def calculate_scale(self, file_path, bound_size):
        # check the image size without loading it into memory
        im = Image.open(file_path)
        original_width, original_height = im.size

        # calculate the resize factor, keeping original aspect and staying within boundary
        bound_width, bound_height = bound_size
        ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
        return min(ratios)

    def download_image(self, image_link, count):
        filename = f'{count}.jpg'
        with open(f'./DownloadedImage/{filename}', 'wb') as f:
            res = requests.get(image_link)
            f.write(res.content)

    def scrape(self):
        # html = self.get_html_page()
        all_hentai_worksheet = self.create_worksheet("All")
        best_hentai_worksheet = self.create_worksheet("Best")

        all_hentai_count = best_hentai_count = 1
        while True:
            html = self.get_html_page_using_request_lib()
            soup = BeautifulSoup(html, 'lxml')
            # print(soup.prettify())
            articles = soup.find_all('article')

            if articles:
                for article in articles:
                    attributes = Attributes()
                    attributes.rating = article.find('div', class_='rating').text
                    # image = article.find('div', class_='poster').img.get('src')
                    # self.download_image(image, count1)
                    data = article.find('div', class_='data')
                    attributes.title = data.h3.a.text
                    attributes.year = data.span.text
                    attributes.link = data.h3.a.get('href')
                    attributes.image_count = all_hentai_count

                    # Scrape inner urls to get other details for attributes
                    WebScrapperInnerUrl.Scrape(attributes).scrape_inner_url()

                    # Add details in the Excel file
                    self.add_details_in_worksheet(
                        all_hentai_count, attributes, all_hentai_worksheet)

                    if float(attributes.rating) >= 9.0:
                        self.add_details_in_worksheet(
                            best_hentai_count, attributes, best_hentai_worksheet)
                        best_hentai_count += 1

                    all_hentai_count += 1
                    print(attributes)
            else:
                break
            self.page += 1

        print(f'Total Pages: {self.page-1}, Total Movies: {all_hentai_count-1}, Best Movies: {best_hentai_count-1}')
        self.workbook.close()

    def scrape_inner_url(self, url):
        html = self.get_html_page_using_request_lib()
        soup = BeautifulSoup(html, 'lxml')
        print(soup.prettify())


if __name__ == '__main__':
    Scrape('').scrape() # Pushing without link
