# This file is return the cache key

from custom_cache_page.utils import hash_key
# key = 'prefix:cached_views:0:/blog/Python/blog-of-test-new-20365/'
# hashed_key = hash_key(key)
# print(hashed_key)


def get_cache_key(prefix, group_function, versioned, path):
    key = f'{prefix}:{group_function}:{versioned}:{path}'
    # hashed_key = hash_key(key)
    return hash_key(key)
