import validators

import zero
import one


LATEST = 1
G1_MAIN_DEFAULT = 'index.html'
G1_KEEP_FORMATTING_DEFAULT = False

DICT = {
    '0': zero,
    '1': one,
}

def get_generation(data):
    """ Takes dict, looks for gen key, returns it or 0 """
    if 'gen' in data:
        gen = data['gen']
    else:
        gen = 0
    return gen


def get_validator(data):
    """ Takes dict, checks gen and returns appropriate validator object """
    gen = get_generation(data)
    values = DICT[str(gen)]
    validator = validators.spec_validator(
        values.SPECS, key=lambda k: lambda obj: obj.get(k))
    return validator


def gen_0_to_1(data):
    """ Takes a gen0 dict and converts it to gen1 """
    for ignored in ('images', 'multipage'):
        data.pop(ignored, None)

    main = data.pop('index', G1_MAIN_DEFAULT)
    keep_formatting = data.pop('keep_formatting', G1_KEEP_FORMATTING_DEFAULT)
    data['gen'] = 1
    data['content'] = {
        'html': {
            'main': main,
            'keep_formatting': keep_formatting
        }
    }
    return data


def return_latest_gen(data):
    """ Takes a dict, checks the generation and returns a gen1 compliant dict """
    gen = get_generation(data)
    if gen > LATEST:
        raise ValueError(
            'Generation must not be greater than {}; was {}'.format(LATEST, gen)
        )
    elif gen == 0:
        data = gen_0_to_1(data)
    return data
