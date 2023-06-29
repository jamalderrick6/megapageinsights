from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import DomainSerializer
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

     
     

class AddDomainView(generics.CreateAPIView):
        serializer_class = DomainSerializer
        
        def post(self, request,):
            domain = request.data.get("domain")
            sitemapUrl = f'https://{domain}/sitemap.xml'
            try:
                 urls = UrlsExtractor(sitemapUrl)
                 _domain = Domain()
                 _domain.title = domain
                 _domain.sitemap = sitemapUrl
                 _domain.description = f'Url pageInsights for {domain}'
                 _domain.created_at = datetime.now(timezone('Africa/Nairobi'))
                 _domain.total_urls = len(urls)

                 _domain.save()

                 dom = Domain.objects.filter(title=domain)
                 print("dom saved", dom)

                 for url in urls:
                      _url = Url()
                      _url.title = url
                      _url.domain = dom.hash_value

                      _url.save()

                 return Response({"data": dom}, status=status.HTTP_200_OK)
            except:
                 return Response({"error": "This domain does not have a sitemap"}, status=status.HTTP_400_BAD_REQUEST)



class UrlsView(generics.ListAPIView):
    pass