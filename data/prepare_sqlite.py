import pandas as pd
import sqlite3
from utilities import read_file
from utilities import fix_date_format
import json

if __name__ == "__main__":
    orders = read_file("../data/order.tsv")
    orders['deadline'] = orders.deadline.apply(fix_date_format)

    equipment = read_file("../data/equipment.tsv")
    equipment['class'] = equipment['class'].str.replace('\\xa0', ' ')
    equipment.head()

    product = read_file("../data/product.tsv")
    product['equipment_class'] = (
        product['equipment_class']
            .apply(
            lambda x: json.loads(x.replace("'", '"').replace("\\xa0", " "))
        )
    )

    equipment_hist = read_file("../data/eq_hist_data.tsv")

    # create sqlite file
    conn = sqlite3.connect("1.db")

    conn.execute("""create table if not exists orders 
    (id integer not null primary key,
    product_id text,
    amount integer, deadline text)""")

    for tpl in orders.itertuples():
        conn.execute("""insert into orders(id, product_id, amount, deadline)
        values ({0}, "{1}", {2}, "{3}")""".format(tpl._1, tpl.product_id, tpl.amount, tpl.deadline))
    print("orders loaded")
