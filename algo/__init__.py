from tqdm import tqdm
from datetime import datetime as dt, timedelta as td
from typing import Dict


def _diff_dates(dt1: dt, dt2: dt):
    return (dt1 - dt2).days


def _is_weekend(dt1: dt):
    return dt1.weekday() > 4


def _get_possible_equipments_for_product(equipment: Dict, products: Dict):
    possible_equipments_for_product = {}
    equipment_by_class = {eq_row['class']: [] for eq_row in equipment.values()}
    for eq_id, eq_row in equipment.items():
        equipment_by_class[eq_row['class']].append({'id': eq_id, 'speed': eq_row['speed']})

    for product_id, possible_classes in products.items():
        res = []
        for c_name in possible_classes:
            possible_equipments = equipment_by_class[c_name]
            for eq_row in possible_equipments:
                res.append({"id": eq_row['id'], "speed": eq_row['speed']})
        possible_equipments_for_product[product_id] = res
    return possible_equipments_for_product


def _calculate_raw_schedule(equipment: Dict, orders: Dict, products: Dict,
                            verbose, max_order_price):
    """
    calculates schedule in raw format
    :rtype: {eq_id: [{'order_id': order_id, 'amount': amount}, ..], ..}
    """
    possible_equipments_for_product = _get_possible_equipments_for_product(equipment, products)

    # if deadline is on weekend, move deadline to Friday cos' no equipment works on weekend
    for order in orders.values():
        if _is_weekend(order['deadline']):
            order['deadline'] = order['deadline'] - td(days=order['deadline'].weekday() - 4)
    sorted_orders = sorted(list(orders.items()), key=lambda x: (x[1]['deadline'], x[1]['amount']))

    # TODO: Range equipments not by left_items, but by expecting awaiting futures
    schedule = {eq_id: {"left_items": 0, "actions": []}
                for eq_id in equipment}
    prev_date = dt.strptime("2019-03-17", "%Y-%m-%d")
    n_placed = 0
    n_failed = 0

    # TODO: take into account if order have fixed start time
    for idx, row in tqdm(sorted_orders, disable=not verbose):
        current_date = row['deadline']
        if prev_date != current_date:
            if verbose:
                print(f"new date! {current_date}, good: {n_placed} , bad: {n_failed}")
            if not _is_weekend(current_date):
                new_hours = _diff_dates(current_date, prev_date) * 24
                for eq_id, v in schedule.items():
                    # TODO: take into account if maintenance is planned for equipment
                    v['left_items'] += new_hours * equipment[eq_id]['speed']
            prev_date = current_date

        amount = row['amount']
        order_id = idx
        possible_equipments = possible_equipments_for_product[row['product_id']]
        best_eq = None
        best_eq_score = 0

        if (not max_order_price) or (amount <= max_order_price):
            for eq in possible_equipments:
                eq_id = eq['id']
                current_score = schedule[eq_id]['left_items']
                if current_score > best_eq_score:
                    best_eq = eq_id
                    best_eq_score = current_score

        if best_eq and (best_eq_score >= amount):
            n_placed += 1
            schedule[best_eq]["actions"].append({"order_id": order_id, "amount": amount})
            schedule[best_eq]["left_items"] -= amount
        else:
            n_failed += 1
    if verbose:
        print(f"total placed good: {n_placed} , bad: {n_failed}")
    schedule = {eq_id: v['actions'] for eq_id, v in schedule.items()}
    return schedule


def _get_time_by_item(start_time: dt, start_item, speed):
    return start_time + td(hours=start_item / speed)


def get_schedule(equipment: Dict, orders: Dict, products: Dict,
                 verbose=False, max_order_price=None):
    """
    get schedule in appropriate format to proceed with backend
    :rtype:
    {'equipment_schedule':
        {%equipment_id%: [
            {'order_id': %order_id%,
            'amount': %order_amount%,
            'start': %datetime%,
            'end': %datetime%}, ...
            ], ...
        },
    'orders_stat': {???}
    }

    :param equipment:
    {eq_id:
        {'class': class,
        'speed': speed,
        (opt)'maintenance': [
            {'start': maintenance_start,
            'end': maintenance_end
            }, ...
            ]
        }, ...
    }
    :param orders:
    {order_id:
        {'product_id': product_id,
         'amount': amount,
          'deadline': deadline,
        (opt)'start': fixed_start_time
        }, ...
    }
    :param products:
    {product_id: [list of classes] , ...}
    :param verbose: if verbose, prints some mid-data to output
    :param max_order_price: if defined, all orders with amount > max_order_price are automatically failed
    """
    raw_schedule = _calculate_raw_schedule(equipment, orders, products,
                                           verbose=verbose, max_order_price=max_order_price)
    schedule = {}
    orders_stat = {}
    for eq_id, actions in raw_schedule.items():
        eq_actions = []
        eq_speed = equipment[eq_id]['speed']
        actual_item_time = 0
        zero_time = dt.strptime("2019-03-18", "%Y-%m-%d")
        for act in actions:
            order_id = act['order_id']
            amount = act['amount']
            eq_action = {'order_id': order_id,
                         'amount': amount,
                         'start': _get_time_by_item(zero_time, actual_item_time, eq_speed),
                         'end': _get_time_by_item(zero_time, actual_item_time + amount, eq_speed)}

            if order_id not in orders_stat:
                orders_stat[order_id] = {'is_placed': False, 'actions': []}
            orders_stat[order_id]['actions'].append({'eq_id': eq_id,
                                                     'amount': amount,
                                                     'start': eq_action['start'],
                                                     'end': eq_action['end']})
            orders_stat[order_id]['is_placed'] = True
            actual_item_time += amount
            eq_actions.append(eq_action)
        schedule[eq_id] = eq_actions
    for order_id in orders.keys():
        if order_id not in orders_stat:
            orders_stat[order_id] = {'is_placed': False, 'actions': []}

    return {'equipment_schedule': schedule, 'orders_stat': orders_stat}
