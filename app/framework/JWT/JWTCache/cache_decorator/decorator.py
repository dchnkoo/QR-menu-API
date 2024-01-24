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