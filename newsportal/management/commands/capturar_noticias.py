from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, Timeout, RequestException, ConnectionError

from newsportal.models import News

class Command(BaseCommand):
    help = 'Update Database'

    def handle(self, *args, **kwargs):
        session = requests.Session()
        session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        url = 'https://www.tecmundo.com.br/'
        try:
            content = session.get(url, timeout=(2, 10))
            content.raise_for_status()
            if content.status_code == 200:
                soup = BeautifulSoup(content.text, "lxml")
                itens = soup.find_all('a', {'class':'tec--carousel__item__title__link'})
                if len(itens) > 0:
                    for link in itens:
                            try:
                                new_news = News(title=link.get('title'))
                                new_news.save()
                            except Exception as error:
                                self.stdout.write(self.style.ERROR('error - data not saved in database:' % error))
                    self.stdout.write(self.style.SUCCESS('Successfully update database'))
                else:
                    self.stdout.write(self.style.ERROR('error - database not updated. Retry the action.'))
            else:
                self.stdout.write(self.style.HTTP_NOT_FOUND('http_not_found - A 404 HTTP Not Found server response.'))
        except HTTPError as error_http:
            self.stdout.write(self.style.ERROR('error - HTTP error occurred:' % error_http))
        except ConnectionError as error_conection:
            self.stdout.write(self.style.ERROR('error - Error Connecting:' % error_conection))
        except Timeout as error_timeout:
            self.stdout.write(self.style.HTTP_BAD_REQUEST('http_bad_request - The request timed out:' % error_timeout))
        except RequestException as error_request:
            self.stdout.write(self.style.ERROR('error - request exception occurred:' % error_request))
        