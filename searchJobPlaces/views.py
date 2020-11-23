from django.shortcuts import render
from bs4 import BeautifulSoup
from .Page import Page


def index(request):
    if request.method != "POST":
        return render(request, 'index.html')

    context = {
        'search': request.POST.get('search'),
        'place': request.POST.get('place'),
    }

    context = pracuj_pl(context)
    context = praca_pl(context)
    context = infoPraca_pl(context)

    return render(request, 'result.html', context)


def pracuj_pl(context):
    names = []
    links = []
    employers = []
    locations = []

    page = 1

    positions = True  # Value True is set for entrance to loop

    while positions:
        url = "https://www.pracuj.pl/praca/" + context['search'] + ";kw/" + context['place'] + ';wp?rd=0&pn=' + \
              str(page)
        source = Page(url)
        soup = BeautifulSoup(source.html, 'html.parser')

        offers = soup.find('div', class_="results")
        positions = offers.find_all("li", class_="results__list-container-item")
        for position in positions:
            name = position.find('a', class_="offer-details__title-link")
            location = position.find('li', class_="offer-labels__item offer-labels__item--location")
            employer = position.find('a', class_="offer-company__name")

            if name is None:
                name = position.find('button', class_="offer-details__title-link")
                if name is None:
                    continue
                location = position.findAll('a', class_="offer-regions__label")
                for loc in location:
                    names.append(name.find(text=True))
                    links.append(loc['href'])
                    locations.append(loc.find(text=True))
                    employers.append(employer.find(text=True))
            else:
                names.append(name.find(text=True))
                links.append(name['href'])
                locations.append(location.find(text=True))
                employers.append(employer.find(text=True))
        page += 1
    context['pracuj_pl'] = list(zip(names, links, employers, locations))
    return context


def praca_pl(context):
    names = []
    links = []
    employers = []
    locations = []
    first_site = ""

    search = context['search'].replace(", ", ",").replace(" ", ",")
    place = removePolishLetters(context['place'])

    page = 1
    while True:
        if page == 1:
            url = 'https://www.praca.pl/s-' + search + ',' + place + '.html'
        else:
            url = 'https://www.praca.pl/s-' + search + ',' + place + '_' + str(page) + '.html'
        source = Page(url)
        soup = BeautifulSoup(source.html, 'html.parser')
        offers = soup.find('div', class_="listing--with-blocks")
        if page == 1:
            first_site = offers
        if page > 1 and first_site == offers:
            break
        positions = offers.findAll('li', class_='listing__item')
        for position in positions:
            name = position.find('a', class_="listing__offer-title")
            location = position.find('div', class_="listing__location")
            employer = position.find('a', class_="listing__employer-name")
            if employer is None:
                employer = position.find('span', class_="listing__employer-name")

            if name is None:
                name = position.find('button', class_="listing__offer-title")
                if name is None:
                    continue
                location = position.findAll('a', class_="listing__multiregion-link")
                for loc in location:
                    names.append(name.find(text=True))
                    links.append(loc['href'])
                    locations.append(loc.find(text=True))
                    employers.append(employer.find(text=True))
            else:
                names.append(name.find(text=True))
                links.append(name['href'])
                locations.append(location.find(text=True))
                employers.append(employer.find(text=True))
        page += 1

    context['praca_pl'] = list(zip(names, links, employers, locations))

    return context


def removePolishLetters(text):
    letters = 'ąćęłńóśźż'
    ascii_replacements = 'acelnoszz'

    translator = str.maketrans(letters, ascii_replacements)

    return text.translate(translator)


def infoPraca_pl(context):
    names = []
    links = []
    employers = []
    locations = []

    page = 1

    positions = True  # Value True is set for entrance to loop

    while positions:
        url = "https://www.infopraca.pl/praca?q=" + context['search'] + '&d=0&pg=' + str(page)
        if context['place'] is not '':
            url += "&lc=" + context['place']
        source = Page(url)
        soup = BeautifulSoup(source.html, 'html.parser')

        positions = soup.find_all("div", class_="position-head container")
        for position in positions:
            name = position.find('a', class_="job-offer")
            location = position.find('h4', class_="serp-one-location")
            employer = position.find('h3', class_="p-name company")

            name_text = name['title'].rsplit(' ', 1)[0].split(' ', 1)[1]

            if location is None:
                location = position.findAll('a', class_="mr-loc")

                for loc in location:
                    names.append(name_text)
                    links.append(loc['href'])
                    locations.append(loc.find(text=True))
                    employers.append(employer.find(text=True))
            else:
                names.append(name_text)
                links.append(name['href'])
                locations.append(location.find(text=True))
                employers.append(employer.find(text=True))
        page += 1
    context['infoPraca_pl'] = list(zip(names, links, employers, locations))
    return context
