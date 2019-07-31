from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup

from newsportal.models import News

class Command(BaseCommand):
    help = 'Update Database'

    def handle(self, *args, **kwargs):
        session = requests.Session()
        session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        url = 'https://www.tecmundo.com.br/'
        content = session.get(url)
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, "lxml")
            itens = soup.find_all('a', {'class':'tec--carousel__item__title__link'})
            if len(itens) > 0:
                for link in itens:
                        new_news = News(title=link.get('title'))
                        new_news.save()
                self.stdout.write(self.style.SUCCESS('Successfully update database'))
            else:
                self.stdout.write(self.style.ERROR('error - database not updated.'))
        else:
            self.stdout.write(self.style.HTTP_NOT_FOUND('http_not_found - A 404 HTTP Not Found server response.'))