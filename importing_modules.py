from xml.etree.ElementTree import ParseError as parse_error
from urllib.error import HTTPError as http_error
from xml.etree import ElementTree as et
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.request import Request
from googlesearch import search
from numba import jit
from io import open
import pandas as pd
import numpy as np
import requests
import urllib3
import time
import tqdm
import sys
import os
import re