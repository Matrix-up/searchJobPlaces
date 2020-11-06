from django.shortcuts import render
from requests_html import HTMLSession


def index(request):
    if request.method == "GET":
        context = {'search': request.GET.get('search')}
        url = "https://www.pracuj.pl/praca/" + context['search'] + ";kw"
        session = HTMLSession()
        r = session.get(url)
        r.html.render()
        tags = r.html.find('.results__list-container-item')
        names = []
        links = []
        for tag in tags:
            #print(tag.html)
            name = tag.find('.offer-details__title-link', first=True)
            if name is not None:
                names.append(name.text)
                links.append(name.attrs['href'])
        context['jobsList'] = zip(names, links)
        return render(request, 'result.html', context)
    return render(request, 'index.html')
