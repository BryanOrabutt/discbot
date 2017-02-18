#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from botinfo import *
import wolframalpha
from PIL import Image
import re, urlmarker


client = wolframalpha.Client('L247V6-5JHVJQVEYE')
res = client.query('temperature in Washington, DC on October3, 2012')
results = ''
for pod in res.pods:
    for sub in pod.subpods:
         imgs = re.findall(urlmarker.URL_REGEX, str(sub))
         for s in imgs:
             results = results + s + '\n'

print(str(results))
