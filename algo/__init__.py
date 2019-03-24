from tqdm import tqdm
from datetime import datetime as dt, timedelta as td
from typing import Dict


def transform_equipments_sqlite(equipments):
    res = {}
    for eq in equipments:
        eq_dict = {'class': eq.equipment_class.name,
                   'speed': eq.speed_per_hour}
        if eq.start_maintenance:
            eq_dict['maintenance'] = {'start': eq.start_maintenance,
                                      'end_maintenance': eq.end_maintenance}
        res[eq.id] = eq_dict
    return res


def transform_orders_sqlite(orders):
    res = {}
    for order in orders:
        order_dict = {'product_id': order.product_id,
                      'amount': order.amount,
                      'deadline': order.deadline}
        execution_restrictions = {}
        if order.start_work_datetime:
            execution_restrictions['start'] = order.start_work_datetime
        if order.equipment:
            execution_restrictions['equipment'] = order.start_work_datetime
        if execution_restrictions:
            order_dict['execution_restrictions'] = execution_restrictions
        res[order.id] = order_dict
    return res


def transform_products_sqlite(products):
    return {pr.id: [cl.name for cl in pr.equipment_classes.all()]
            for pr in products}


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


def _order_key(order_id, order):
    is_liberate_time = (('execution_restrictions' in order)
                        and 'start' in order['execution_restrictions'])
    restricted_time = order.get('execution_restrictions', {}).get('start')
    restricted_equipment = order.get('execution_restrictions', {}).get('equipment')
    pseudo_deadline = order['deadline']
    if restricted_time:
        pseudo_deadline = restricted_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return (pseudo_deadline,
            not bool(restricted_equipment),
            not bool(restricted_time),
            order['amount'])


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
    sorted_orders = sorted(list(orders.items()), key=lambda x: _order_key(x[0], x[1]))

    schedule = {eq_id: {"left_items": 0, "actions": []}
                for eq_id in equipment}
    prev_date = dt.strptime("2019-03-17", "%Y-%m-%d")
    n_placed = 0
    n_failed = 0

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

        if (('execution_restrictions' in row)
                and ('equipment' in row['execution_restrictions'])):
            best_eq = row['execution_restrictions']['equipment']
            best_eq_score = min(amount, schedule[best_eq]['left_items'])
        elif (not max_order_price) or (amount <= max_order_price):
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


def _rearrange_actions(actions, actions_pos, real_start_item, wanted_item):
    if real_start_item == wanted_item:
        return actions
    total_items = real_start_item
    actual_action = actions[actions_pos]
    eq_actions_end_pos = actions_pos
    wanted_end = wanted_item + actual_action['amount']
    for ac in actions[actions_pos:]:
        eq_actions_end_pos += 1
        total_items += ac['amount']
        if total_items >= wanted_end:
            break
    total_items -= actual_action['amount']
    item_to_split = actions[eq_actions_end_pos - 1]
    if total_items == wanted_item:
        splitted_last_action_start = [item_to_split]
        splitted_last_action_end = []
    else:  # total_items > wanted_item
        split_to_end = total_items - wanted_item
        splitted_last_action_start = item_to_split.copy()
        splitted_last_action_start['amount'] -= split_to_end
        splitted_last_action_end = item_to_split.copy()
        splitted_last_action_end['amount'] = split_to_end
        splitted_last_action_start = [splitted_last_action_start]
        splitted_last_action_end = [splitted_last_action_end]
    new_actions = (actions[:actions_pos]
                   + actions[actions_pos + 1:eq_actions_end_pos - 1]
                   + splitted_last_action_start
                   + [actions[actions_pos]]
                   + splitted_last_action_end
                   + actions[eq_actions_end_pos:])
    return new_actions


def _find_closest_item(wanted_start, default_zero_time, speed):
    return int((wanted_start - default_zero_time).total_seconds() / 3600 * speed)


def _find_real_start(order_id, raw_schedule):
    for eq_id, actions in raw_schedule.items():
        total_items_before = 0
        for eq_actions_pos, ac in enumerate(actions):
            if ac['order_id'] == order_id:
                return eq_id, eq_actions_pos, total_items_before
            total_items_before += ac['amount']


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
    'orders_stat': {order_id:
        {'is_placed': bool,
        'actions': [
            {'eq_id': eq_id,
             'amount': amount,
             'start': start,
             'end': end}, ...
             ]
        }, ...
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
        (opt)'fixed_execution': {'start': fixed_start_time, 'equipment': fixed_equipment_id}
        }, ...
    }
    :param products:
    {product_id: [list of classes] , ...}
    :param verbose: if verbose, prints some mid-data to output
    :param max_order_price: if defined, all orders with amount > max_order_price are automatically failed
    """
    default_zero_time = dt.strptime("2019-03-18", "%Y-%m-%d")
    fixed_orders = {}
    for order_id, order in orders.items():
        if 'execution_restrictions' in order:
            # order already has fixed date-time and/or fixed equipment
            fixed_orders[order_id] = order

    raw_schedule = _calculate_raw_schedule(equipment, orders, products,
                                           verbose=verbose, max_order_price=max_order_price)

    #### fix orders whose start time is restricted
    for order_id, order in fixed_orders.items():
        if 'start' not in order['execution_restrictions']:
            continue
        wanted_start = order['execution_restrictions']['start']  # datetime
        eq_id, eq_actions_pos, real_start_item = _find_real_start(order_id, raw_schedule)
        wanted_item = _find_closest_item(wanted_start,
                                         default_zero_time,
                                         equipment[eq_id]['speed'])
        raw_schedule[eq_id] = _rearrange_actions(actions=raw_schedule[eq_id],
                                                 actions_pos=eq_actions_pos,
                                                 real_start_item=real_start_item,
                                                 wanted_item=wanted_item)

    #### end fix orders
    schedule = {}
    orders_stat = {}
    for eq_id, actions in raw_schedule.items():
        eq_actions = []
        eq_speed = equipment[eq_id]['speed']
        actual_item_time = 0
        zero_time = default_zero_time
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
