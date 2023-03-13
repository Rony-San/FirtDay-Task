from django.shortcuts import render
from .utils import check_translation
import random
from django.shortcuts import render
from urllib.parse import urlparse


import random
from urllib.parse import urlparse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
import requests
from bs4 import BeautifulSoup


def home_view(request):
    if request.method == 'POST':
        urls = request.POST.get('urls').split('\n')
        results = {}
        for url in urls:
            results[url] = check_translation(url)
        return render(request, 'results.html', {'results': results})
    return render(request, 'home-view.html')





def get_urls_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url and url.startswith('http'):
            urls.append(url)
    return urls


@csrf_exempt
def check_urls(request):
    if request.method == 'POST':
        urls = request.POST.get('urls').split()
        main_path = urlsplit(request.get_raw_uri()).netloc
        results = []
        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.netloc == main_path and parsed_url.path.startswith('/'):
                result = f"{url}: PASS"
            else:
                result = f"{url}: FAIL"
            results.append(result)
        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'home-view.html')