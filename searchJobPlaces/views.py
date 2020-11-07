from django.shortcuts import render
from bs4 import BeautifulSoup
from .Page import Page


def index(request):
    if request.method == "POST":
        context = {
            'search': request.POST.get('search'),
            'place': request.POST.get('place'),
        }

        names = []
        links = []
        employers = []
        locations = []

        page = 1
        positions = 1  # Value 1 is set for entrance to loop

        while positions:
            url = "https://www.pracuj.pl/praca/" + context['search'] + ";kw/" + context['place'] + ';wp?rd=0&pn=' + \
                  str(page)
            source = Page(url)
            soup = BeautifulSoup(source.html, 'html.parser')

            results = soup.find('div', class_="results")
            positions = results.find_all("li", class_="results__list-container-item")
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
        context['jobsList'] = zip(names, links, employers, locations)
        return render(request, 'result.html', context)
    else:
        return render(request, 'index.html')
