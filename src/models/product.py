from typing import Optional

from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    id: Optional[int] = None
    name: str #название

    price: float # цена
    human_volume: str #объем товара в понятной для покупателя форме.
    volume: float #объем товара
    volume_type: str #тип объема
    price_type: str #тип цены, указывающий, что цена указана за килограмм

    slug: str #удобный для чтения идентификатор, используемый в URL
    sku: str #код товара для магазина.
    image_urls: str #массив URL-адресов изображений товара
    canonical_url:str #ссылка на страницу товара в магазине


    model_config = ConfigDict(from_attributes=True)

'''
id: '557198' — уникальный идентификатор товара.
sku: '10712' — код товара для магазина.
retailer_sku: '557198' — код товара у розничного продавца, совпадает с id.
available: True — товар доступен для покупки.
legacy_offer_id: 1604411402 — идентификатор старого предложения.
name: 'Бананы' — название товара.
price: 79.5 — текущая цена товара.
original_price: 79.5 — изначальная цена товара, совпадает с текущей.
discount: 0 — размер скидки, в данном случае отсутствует.
human_volume: '500 г' — объем товара в понятной для покупателя форме.
volume: 500 — объем товара в граммах.
volume_type: 'g' — тип объема (граммы).
items_per_pack: 1 — количество единиц товара в упаковке.
discount_ends_at: '1970-01-01T00:00:00.000+00:00' — дата окончания скидки (отсутствует).
price_type: 'per_kilo' — тип цены, указывающий, что цена указана за килограмм.
grams_per_unit: 500 — количество граммов в одной единице товара.
unit_price: 159 — цена за единицу (здесь это цена за 500 г).
original_unit_price: 159 — изначальная цена за единицу, совпадает с текущей.
promo_badge_ids: [] — нет идентификаторов промо-акций.
score: 4 — оценка товара (например, от покупателей).
labels: [] — отсутствуют метки на товаре.
image_urls: — массив URL-адресов изображений товара:
['https://imgproxy.kuper.ru/imgproxy/width-auto/czM6Ly9jb250ZW50LWltYWdlcy1wcm9kL3Byb2R1Y3RzLzEwNzEyL29yaWdpbmFsLzEvMjAyNC0wNC0wMlQwOCUzQTQwJTNBMjguODU2NzEwJTJCMDAlM0EwMC8xMDcxMl8xLmpwZw==.jpg'] — одно изображение бананов.
requirements: [] — отсутствуют требования к товару.
slug: 'banany-802130f' — удобный для чтения идентификатор, используемый в URL.
max_select_quantity: 999 — максимальное количество товара, которое можно выбрать.
canonical_url: 'https://sbermarket.ru/products/10712-banany-802130f' — ссылка на страницу товара в магазине.
vat_info: None — информация о НДС отсутствует.
bmpl_info: {} — дополнительная информация (пока отсутствует).
max_per_order: 180 — максимальное количество товара, которое можно заказать за раз.
ads_meta: None — информация о рекламе отсутствует.
with_options: False — товар без дополнительных опций.
is_beneficial: True — товар считается выгодным.
store_id: '211' — идентификатор магазина, где продается товар.
price_per_base_human_volume: '' — цена за базовый объем отсутствует.
prices_bank: объект с ценовой информацией:
price: 79.5 — текущая цена.
offer_price: 159 — цена за единицу.
discount: 0 — размер скидки.
'''