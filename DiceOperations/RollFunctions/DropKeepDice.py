from ErrorHandler import drop_keep_modifier_too_high


def drop(result, modifier_number, function):
    for _ in range(0, modifier_number):
        result.remove(function(result))
    return result


def keep(result, modifier_number, function):
    kept_result = []
    for _ in range(0, modifier_number):
        kept_result.append(function(result))
        result.remove(function(result))
    return kept_result


def drop_keep(result, modifier, modifier_number):
    if modifier_number > len(result):
        raise drop_keep_modifier_too_high()
    function_dictionary = {"d": (drop, min),
                           "dl": (drop, min),
                           "dh": (drop, max),
                           "k": (keep, max),
                           "kh": (keep, max),
                           "kl": (keep, min)}
    functions = function_dictionary[modifier]
    return functions[0](result, modifier_number, functions[1])
