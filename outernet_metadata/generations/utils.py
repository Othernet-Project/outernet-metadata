import validators

import zero
import one


LATEST = 1

DICT = {
    '0': zero,
    '1': one,
}

def get_generation(data):
    if 'gen' in data:
        gen = data['gen']
    else:
        gen = 0
    return gen


def get_validator(data):
    gen = get_generation(data)
    values = DICT[str(gen)]
    validator = validators.spec_validator(
        values.SPECS, key=lambda k: lambda obj: obj.get(k))
    return validator


def gen_0_to_1(data):
    pass


def return_latest_gen(data):
    gen = get_generation(data)
    if gen == 0:
        data = gen_0_to_1(data)
    return data
