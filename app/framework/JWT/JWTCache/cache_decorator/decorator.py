import json
from ... import CACHE_JWT


def jwtcache(func):

    def save(instance, *args, **kwargs):
        result = func(instance, *args, **kwargs)
        tokens = instance.__class__.__getattribute__(instance, '_tokens')

        with open(CACHE_JWT, 'w+') as f:
            json.dump(tokens, f)
        
        return result
    
    return save


def jwtgetcache(func):

    def get(instance, *args, **kwargs):
        with open(CACHE_JWT, 'a+') as f:
            f.seek(0)
            content = f.read()
            data = json.loads(content) if content else {}

        result = func(instance, *args, **kwargs)
        instance.__class__.__setattr__(instance, '_tokens', data)

        return result
    
    return get