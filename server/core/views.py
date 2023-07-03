from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import DomainSerializer, UrlSerializer
from .models import Domain, Url
from datetime import datetime
from pytz import timezone

import requests
import xml.etree.ElementTree as ET

def UrlsExtractor(sitemap_url):
     response = requests.get(sitemap_url)
     root = ET.fromstring(response.content)
     namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

     urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]

     return urls

def DomainHasSitemap(domain):
    _link = f'https://{domain}/sitemap.xml'
    response = requests.get(_link)

    if response.status_code == 200:
         return True
    
    return False

     
class AddDomainView(generics.CreateAPIView):
        serializer_class = DomainSerializer
        
        def post(self, request):
            domain = request.data.get("domain")
            if DomainHasSitemap(domain):
                try:
                     _domain = Domain.objects.get(title=domain)
                     return Response({"id": _domain.hash_value}, status=status.HTTP_200_OK)
                except Domain.DoesNotExist:
                    sitemapUrl = f'https://{domain}/sitemap.xml'
                    _domain = Domain()
                    _domain.title = domain
                    _domain.sitemap = sitemapUrl
                    _domain.description = f'Url pageInsights for {domain}'
                    _domain.created_at = datetime.now(timezone('Africa/Nairobi'))
                    _domain.save()
                    return Response({"id": _domain.hash_value}, status=status.HTTP_200_OK)
                    
            else:
               return Response({"error": "This domain does not have a sitemap"}, status=status.HTTP_400_BAD_REQUEST)



class UrlsView(generics.ListAPIView):
    serializer_class = UrlSerializer
    
    def get_queryset(self):
         domain_hash = self.request.GET.get('id');

         if domain_hash:
               urls = Url.objects.filter(domain__hash_value = domain_hash)
               if len(urls) == 0:
                   dom = Domain.objects.filter(hash_value = domain_hash)
                   _urls = UrlsExtractor(dom.sitemap)
                   for url in _urls:
                         _url = Url()
                         _url.title = url
                         _url.domain = domain_hash

                         _url.save()
               return urls
                       
                   