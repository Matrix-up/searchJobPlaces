import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from bs4 import BeautifulSoup

app = None

class Page(QWebEnginePage):
    def __init__(self, url):
        global app
        app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        app.exec()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        global app
        app.quit()


if __name__ == '__main__':
    for i in range(3):
        url = "https://www.pracuj.pl/praca/hydraulik;kw"
        source = Page(url)
        soup = BeautifulSoup(source.html, 'html.parser')
        results = soup.find('div', class_="results")
        tags = results.find_all("li", class_="results__list-container-item")
        for tag in tags:
            # print(tag.html)
            name = tag.find('.offer-details__title-link', first=True)
            if name is not None:
                print(name.text)
