import typing

T = typing.TypeVar('T')

def elong_list(original_list: list[T], target_length: int):
    integer_part = int(target_length / len(original_list))
    remainder = target_length - (len(original_list) * integer_part)
    extended_list = [item for sublist in [[element] * integer_part for element in original_list] for item in sublist]

    if remainder == 0:
        return extended_list

    step = int(len(extended_list) / remainder)
    start_step = int(step / 2)
    insertion_positions = reversed([start_step + step * i for i in range(int(len(extended_list) / step))])

    for position in insertion_positions:
        if position < len(extended_list) - 1:
            extended_list.insert(position, extended_list[position])

    return extended_list
