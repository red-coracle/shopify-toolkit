import csv
import requests
from config import STORE_URL
from io import open as iopen
from os import makedirs
from os.path import exists
from urllib.parse import urlsplit


def get_product(id):
    return requests.get(f'{STORE_URL}/products/{id}.json').json()


def save_image(image_url, directory=''):
    filename = urlsplit(image_url)[2].split('/')[-1]
    r = requests.get(image_url)
    if r.status_code == 200:
        if len(directory) > 0 and not exists(directory):
            makedirs(directory)
        with iopen(f'{directory}{filename}', 'wb') as file:
            file.write(r.content)


def list_to_dict(list, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(list))


if __name__ == '__main__':
    product = get_product(input('Product ID: '))['product']
    images = list_to_dict(product['images'], 'id')

    for image in product['images']:
        save_image(image['src'], f'{image["product_id"]}/')

    with open(f'{product["id"]}/{product["id"]}.csv', 'w') as csvfile:
        fieldnames = ['title', 'item_sku', 'main_image_url', 'option1', 'option2',
                      'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'title': product['title'],
                         'item_sku': product['id']})
        for variant in product['variants']:
            writer.writerow({'title': variant['title'],
                             'item_sku': variant['id'],
                              'main_image_url': images[variant['image_id']]['src'][:-13],
                              'option1': variant['option1'],
                              'option2': variant['option2'],
                              'price': variant['price']})
