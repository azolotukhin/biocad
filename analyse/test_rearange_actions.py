from algo import _rearrange_actions

if __name__ == "__main__":
    inpt = [1, 2, 5, 7, 4, 3]
    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]

    res = _rearrange_actions(actions,
                             actions_pos=2,
                             real_start_item=3,
                             wanted_item=5)
    assert ([r['order_id'] for r in res] == [0, 1, 3, 2, 3, 4, 5])
    print("test1 passed")
    assert ([r['amount'] for r in res] == [1, 2, 2, 5, 5, 4, 3])
    print("test2 passed")

    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]
    res = _rearrange_actions(actions,
                             actions_pos=2,
                             real_start_item=3,
                             wanted_item=10)
    assert ([r['order_id'] for r in res] == [0, 1, 3, 2, 4, 5])
    print("test3 passed")
    assert ([r['amount'] for r in res] == [1, 2, 7, 5, 4, 3])
    print("test4 passed")

    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]
    res = _rearrange_actions(actions,
                             actions_pos=2,
                             real_start_item=3,
                             wanted_item=3)
    assert ([r['order_id'] for r in res] == [0, 1, 2, 3, 4, 5])
    print("test5 passed")
    assert ([r['amount'] for r in res] == [1, 2, 5, 7, 4, 3])
    print("test6 passed")

    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]
    res = _rearrange_actions(actions,
                             actions_pos=2,
                             real_start_item=3,
                             wanted_item=12)
    assert ([r['order_id'] for r in res] == [0, 1, 3, 4, 2, 4, 5])
    print("test7 passed")
    assert ([r['amount'] for r in res] == [1, 2, 7, 2, 5, 2, 3])
    print("test8 passed")

    inpt = [1, 2, 5, 7, 4, 3]
    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]
    res = _rearrange_actions(actions,
                             actions_pos=0,
                             real_start_item=0,
                             wanted_item=5)
    assert ([r['order_id'] for r in res] == [1, 2, 0, 2, 3, 4, 5])
    print("test9 passed")
    assert ([r['amount'] for r in res] == [2, 3, 1, 2, 7, 4, 3])
    print("test10 passed")

    inpt = [5, 2, 5, 7, 4, 3]
    actions = [{"order_id": ic, "amount": v} for ic, v in enumerate(inpt)]
    res = _rearrange_actions(actions,
                             actions_pos=0,
                             real_start_item=0,
                             wanted_item=1)
    assert ([r['order_id'] for r in res] == [1, 0, 1, 2, 3, 4, 5])
    print("test11 passed")
    assert ([r['amount'] for r in res] == [1, 5, 1, 5, 7, 4, 3])
    print("test12 passed")
