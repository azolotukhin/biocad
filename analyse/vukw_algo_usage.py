# coding: utf-8

import json

from algo import get_schedule
from utilities import read_file, fix_date_format

if __name__ == "__main__":
    equipment = read_file("../data/equipment.tsv")
    equipment['class'] = equipment['class'].str.replace('\\xa0', ' ')
    equipment.set_index('id', inplace=True)
    equipment.head()

    orders = read_file("../data/order.tsv")
    orders['deadline'] = orders.deadline.apply(fix_date_format)
    orders.set_index('_id', inplace=True)

    products = read_file("../data/product.tsv")
    products['equipment_class'] = products['equipment_class'].apply(
        lambda x: json.loads(x.replace("'", '"').replace("\\xa0", " ")))
    products.set_index('_id', inplace=True)

    equipment_hist = read_file("../data/eq_hist_data.tsv")

    total_possible_speed = equipment.speed_per_hour.sum() * 24
    print('total speed per day for all equipments, it/day:', total_possible_speed)
    print('total awaited products: ', orders.groupby('deadline')['amount'].sum())

    equipment_dict = (equipment[['class', 'speed_per_hour']]
                      .rename(columns={"speed_per_hour": "speed"})
                      .to_dict(orient='index'))
    products_dict = {prod_id: prod_row['equipment_class']
                     for prod_id, prod_row in products.to_dict(orient='index').items()}
    orders_dict = orders.to_dict(orient='index')

    print("start calculating schedule..")
    schedule = get_schedule(equipment_dict, orders_dict, products_dict)
    print("end calculating schedule")
