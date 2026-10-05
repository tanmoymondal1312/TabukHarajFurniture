import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabukHarajFurniture.settings')
import django
django.setup()
from django.test import Client
import re

client = Client()

# Check products page
response = client.get('/products/')
print('Products page:', response.status_code)
content = response.content.decode('utf-8')
checks = [
    ('title', '<title>' in content),
    ('canonical', 'canonical' in content),
    ('hreflang', 'hreflang' in content),
    ('json-ld', 'application/ld+json' in content),
    ('og:title', 'og:title' in content),
    ('og:description', 'og:description' in content),
    ('og:image', 'og:image' in content),
    ('twitter:card', 'twitter:card' in content),
    ('robots meta', 'robots' in content),
    ('ItemList schema', 'ItemList' in content),
]
for name, result in checks:
    status = 'OK' if result else 'MISSING'
    print(f'  {status}: {name}')

# Check for product detail pages
slugs = re.findall(r'product/([^/"\']+)/', content)
print(f'\nProduct slugs found: {slugs[:5]}')
if slugs:
    resp = client.get(f'/product/{slugs[0]}/')
    print(f'Product detail: {resp.status_code}')
    c = resp.content.decode('utf-8')
    checks2 = [
        ('Product schema', 'Product' in c),
        ('Offer schema', 'Offer' in c),
        ('AggregateRating', 'AggregateRating' in c),
        ('BreadcrumbList', 'BreadcrumbList' in c),
    ]
    for name, result in checks2:
        status = 'OK' if result else 'MISSING'
        print(f'  {status}: {name}')

# Check sitemap.xml content
resp = client.get('/sitemap.xml')
print(f'\nSitemap: {resp.status_code}')
sitemap_content = resp.content.decode('utf-8')
print(f'URLs in sitemap: {sitemap_content.count("<url>")}')

# Check robots.txt
resp = client.get('/robots.txt')
print(f'\nRobots.txt: {resp.status_code}')
robots_content = resp.content.decode('utf-8')
print(f'Content length: {len(robots_content)}')

# Check language attributes
print('\n--- Language/RTL checks ---')
for page in ['/', '/about/', '/faq/', '/products/']:
    resp = client.get(page)
    c = resp.content.decode('utf-8')
    has_rtl = 'dir="rtl"' in c or 'dir="RTL"' in c
    has_lang = 'lang="ar"' in c or 'lang="AR"' in c
    print(f'{page}: dir=rtl={has_rtl}, lang=ar={has_lang}')

# Check images for alt attributes
print('\n--- Image SEO checks (homepage) ---')
resp = client.get('/')
c = resp.content.decode('utf-8')
img_tags = re.findall(r'<img[^>]+>', c)
print(f'Total img tags: {len(img_tags)}')
with_alt = sum(1 for img in img_tags if 'alt=' in img)
with_loading = sum(1 for img in img_tags if 'loading=' in img)
with_width = sum(1 for img in img_tags if 'width=' in img)
print(f'Images with alt: {with_alt}/{len(img_tags)}')
print(f'Images with loading: {with_loading}/{len(img_tags)}')
print(f'Images with width/height: {with_width}/{len(img_tags)}')

# Check for missing critical pages
print('\n--- Missing standard pages ---')
missing_pages = ['/contact/', '/privacy/', '/terms/', '/shipping/', '/returns/']
for p in missing_pages:
    resp = client.get(p)
    print(f'{p}: {resp.status_code}')

# Check core web vitals related
print('\n--- Performance hints ---')
resp = client.get('/')
c = resp.content.decode('utf-8')
has_preload = 'rel="preload"' in c
has_dns_prefetch = 'dns-prefetch' in c
has_preconnect = 'preconnect' in c
print(f'Preload: {has_preload}, DNS-prefetch: {has_dns_prefetch}, Preconnect: {has_preconnect}')

# Check structured data types
print('\n--- Structured Data Types Found ---')
for page in ['/', '/about/', '/faq/', '/products/']:
    resp = client.get(page)
    c = resp.content.decode('utf-8')
    import json
    # Extract JSON-LD scripts
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    types = set()
    for script in scripts:
        try:
            data = json.loads(script.strip())
            if '@graph' in data:
                for item in data['@graph']:
                    if '@type' in item:
                        t = item['@type']
                        if isinstance(t, list):
                            types.update(t)
                        else:
                            types.add(t)
            elif '@type' in data:
                t = data['@type']
                if isinstance(t, list):
                    types.update(t)
                else:
                    types.add(t)
        except:
            pass
    print(f'{page}: {", ".join(sorted(types))}')