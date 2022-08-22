def get_kwarg_or_env(env, kwargs, key):
    '''
    Check kwargs for key first, if not found check env
    '''
    result = kwargs.get(key, env.get(key, []))
    if isinstance(result, list) or isinstance(result, dict):
        return result.copy()
    else:
        return result

