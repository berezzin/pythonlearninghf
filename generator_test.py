from url_utils import gen_from_urls


urls = ('https://www.onliner.by/', 'https://www.youtube.com/', 'https://yandex.by/')

for content_len, status_code, url in gen_from_urls(urls):
    print(content_len, '->', status_code, '->', url)