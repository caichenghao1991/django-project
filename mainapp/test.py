import hashlib
import os

import time
sha224 = hashlib.sha224("hello".encode('utf-8'))
print(sha224)
print(sha224.hexdigest())
