def elong(_list, length: int):
    商 = int(length / len(_list))
    餘 = length - (len(_list) * 商)
    _list = [j for r in [[i] * 商 for i in _list] for j in r]
    if 餘 == 0: return _list
    步 = int(len(_list) / 餘)
    起步 = int(步 / 2)
    盈位 = reversed([起步 + 步 * i for i in range(int(len(_list) / 步))])
    for 位 in 盈位:
        if 位 < len(_list) - 1:
            _list.insert(位, _list[位])
    return _list
