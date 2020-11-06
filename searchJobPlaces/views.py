from django.shortcuts import render
from bs4 import BeautifulSoup
from .Page import Page


def index(request):
    if request.method == "POST":
        context = {
            'search': request.POST.get('search'),
            'place': request.POST.get('place'),
        }
        url = "https://www.pracuj.pl/praca/" + context['search'] + ";kw/" + context['place'] + ';wp'
        source = Page(url)
        soup = BeautifulSoup(source.html, 'html.parser')

        results = soup.find('div', class_="results")
        positions = results.find_all("li", class_="results__list-container-item")

        names = []
        links = []
        employers = []
        locations = []
        contracts_type = []
        for position in positions:
            name = position.find('a', class_="offer-details__title-link")
            location = position.find('li', class_="offer-labels__item offer-labels__item--location")
            employer = position.find('a', class_="offer-company__name")
            contract_type = position.find('li', {'data-test': 'list-item-offer-type-of-contract'})
            if name is not None:
                names.append(name.find(text=True))
                links.append(name['href'])
                employers.append(employer.find(text=True))
                locations.append(location.find(text=True))
                if contract_type is None:
                    contracts_type.append("<i class='red-text'>Brak danych</i>")
                else:
                    contracts_type.append(contract_type.find(text=True))
        context['jobsList'] = zip(names, links, employers, locations, contracts_type)
        return render(request, 'result.html', context)
    else:
        return render(request, 'index.html')
