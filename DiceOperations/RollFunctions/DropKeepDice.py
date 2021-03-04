from Utility.ErrorHandler import drop_keep_modifier_too_high


def drop(result, modifier_number, function):
    discarded_result = []
    for _ in range(0, modifier_number):
        discarded_result.append(function(result))
        result.remove(function(result))
    return result, discarded_result


def keep(result, modifier_number, function):
    kept_result = []
    for _ in range(0, modifier_number):
        kept_result.append(function(result))
        result.remove(function(result))
    discarded_roll = result
    return kept_result, discarded_roll


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
