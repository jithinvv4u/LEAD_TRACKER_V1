"""Commonly used helper function are defined here."""

import io

import ast

import binascii
from PIL import Image

from Crypto.Cipher import AES
from hashids import Hashids
import phonenumbers
import hashlib
import enum
from time import mktime
from time import time
from uuid import uuid4
import json
import requests
from random import randint
from random import random
from pytz import timezone
from collections import OrderedDict
from functools import partial

from datetime import datetime

from rest_framework.response import Response
from rest_framework import status

from django.core.files.base import File
from django.core.validators import validate_email
from django.conf import settings
from django.db.models.expressions import RawSQL
from django.utils.timezone import localtime
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from .exceptions import BadRequest


prev_time_log = int(time() * 100000)
prev_stage = ""
stage_times = {}
stage_count = {}


def reset_time_stages():
    global prev_time_log
    global stage_times
    global prev_stage
    global stage_count
    stage_times = {}
    stage_count = {}
    prev_stage = ""


def time_since(stage="", intend=0):
    """
    Function to dubug delays in execution times.
    Call this function at stags where you need to check the time, and it will
    print the time since the function was previously called.
    Args:
        stage: Optional message to append before the time

    Returns: time in seconds

    """
    global prev_time_log
    global stage_times
    global prev_stage
    global stage_count

    current_time = int(time() * 10)
    time_since = current_time - prev_time_log
    prev_time_log = current_time
    if not stage:
        return time_since, stage_times, stage_count
    if prev_stage in stage_times:
        stage_times[prev_stage] += time_since
    else:
        stage_times[prev_stage] = time_since
    if stage in stage_count:
        stage_count[stage] += 1
    else:
        stage_count[stage] = 1

    print("\t" * intend, stage, time_since)
    prev_stage = stage
    return time_since, stage_times, stage_count


class ChoiceAdapter(enum.IntEnum):
    @classmethod
    def choices(cls):
        return ((item.value, item.name.replace("_", " ")) for item in cls)


def get_location_from_ip(ip):
    """
    Function to get location from IP.

    Input Params:
        ip(str): ip address of user.
    Returns:
        (str): location
    """
    try:
        address = ""
        location = json.loads(requests.get(settings.GEO_IP_URL + ip).content)
        if location["city"]:
            address = location["city"] + ", "
        if location["region_name"]:
            address += location["region_name"] + ", "
        if location["country_name"]:
            address += location["country_name"]

        if address:
            return address
    except:
        return "Unknown Location"


def generate_random_number(digits):
    """
    Function to generate n dig random number.

    Input Params:
        digits(int): number of digits
    Returns:
        (int): number
    """
    range_start = 10 ** (digits - 1)
    range_end = (10**digits) - 1
    return randint(range_start, range_end)


def pop_out_from_dictionary(dictionary, keys):
    """
    Function to remove keys from dictionary.

    Input Params:
        dictionary(dict): dictionary
        keys(list)
    Returns:
        dictionary(dictionary): updated dictionary.
    """
    for key in keys:
        dictionary.pop(key, None)
    return dictionary


def success_response(data={}, message=None, status=status.HTTP_200_OK):
    """
    Function to create success Response.

    This function will create the standardized success response.
    """
    response = {"success": True, "detail": message, "code": status, "data": data}
    if not message:
        response["detail"] = "Success."
    return Response(response, status=status)


def validate_phone(number):
    """
    Function to validate phone number.

    Input Params:
        number(str): international phone number
    Returns:
        dictionary with
        phone(str): phone number
        code(str): country code
    """
    try:
        number = number.replace(" ", "")
        number = number.replace("-", "")
        number = phonenumbers.parse(number)
        phone = str(number.national_number)
        code = "+" + str(number.country_code)
        return code + phone
    except:
        return None


def split_phone(number):
    """
    Function to split phone number into dial code and phone number.

    Args:
        number: concatenated phone number
    Returns:
        dial_code: International dialing code
        phone: National phone number.
    """
    number = number.replace(" ", "")
    number = number.replace("-", "")
    try:
        number = phonenumbers.parse(number)
        phone = str(number.national_number)
        code = "+" + str(number.country_code)
        return code, phone
    except:
        return "", number


def convert_to_timestamp(date):
    """Function to convert Unix timestamps to date time."""
    try:
        unix = mktime(date.timetuple())
    except:
        unix = 0.0

    return unix


def validate_password(password):
    """
    Function to validate password.

    Input Params:
        password(str): password.
    Returns:
        valid(bool): valid status.
        message(str): validity message.
    """
    try:
        password_validation.validate_password(password)
        valid = True
        message = "Valid Password."
    except ValidationError as e:
        valid = False
        message = "; ".join(e.messages)
    return (valid, message)


def validate_email(email):
    """Function to validate email address."""
    try:
        validate_email(email)
        return (True, "Valid Email address.")
    except ValidationError as e:
        message = "; ".join(e.messages)
        return (False, message)


def unix_to_datetime(unix_time):
    """Function to convert Unix timestamps to date time."""
    try:
        unix_time = float(unix_time)
        localtz = timezone(settings.TIME_ZONE)
        date = localtz.localize(datetime.fromtimestamp(unix_time))
        return date
    except:
        raise BadRequest("Unix timestamps must be float or int")


def datetime_to_unix(date):
    """Function to convert Unix timestamps to date time."""
    try:
        unix = mktime(date.timetuple())
    except:
        unix = 0.0

    return unix


def encode(value):
    """
    Function to  hash hid the int value.

    Input Params:
        value(int): int value
    Returns:
        hashed string.
    """
    hasher = Hashids(min_length=settings.HASHID_MIN_LENGTH, salt=settings.HASHHID_SALT)
    try:
        value = int(value)
        return hasher.encode(value)
    except:
        return None


def decode(value):
    """
    Function to  decode hash hid value.

    Input Params:
        value(str): str value
    Returns:
        int value.
    """
    hasher = Hashids(min_length=settings.HASHID_MIN_LENGTH, salt=settings.HASHHID_SALT)
    try:
        return hasher.decode(value)[0]
    except:
        return None


def date_time_desc(date):
    """Function to format date time."""
    try:
        date = localtime(date)
    except:
        pass
    date = date.strftime("%d %B %Y, %H:%M %p")
    date += ", Timezone: %s" % settings.TIME_ZONE
    return date


def gcd_get_raw_sql_distance(latitude, longitude, max_distance=None):
    """
    Function to create raw SQL distance with GCD.

    This function will compute raw SQL distance with
    Great circle distance formula.
    Input Params:
        latitude(float): reference location latitude.
        longitude(float): reference location longitude
        max_distance(float): max distance in KM
    Returns:
        (obj): distance in raw SQL object.
    """
    gcd_formula = "6371 * acos(least(greatest(\
        cos(radians(%s)) * cos(radians(latitude)) \
        * cos(radians(longitude) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(latitude)) \
        , -1), 1))"
    distance_raw_sql = RawSQL(gcd_formula, (latitude, longitude, latitude))
    return distance_raw_sql


def encrypt(message):
    """Function to encrypt a message."""
    try:
        iv = str.encode(settings.SECRET_KEY[-16:])
        key = str.encode(settings.SECRET_KEY[:16])
        cipher = AES.new(key, AES.MODE_CFB, iv)
        msg = cipher.encrypt(message)
        return binascii.hexlify(msg).decode("utf-8")
    except:
        return None


def decrypt(code):
    """Function to decrypt the message."""
    try:
        iv = str.encode(settings.SECRET_KEY[-16:])
        key = str.encode(settings.SECRET_KEY[:16])
        cipher = AES.new(key, AES.MODE_CFB, iv)
        code = binascii.unhexlify(code)
        message = cipher.decrypt(code)
        return message.decode("utf-8")
    except:
        return None


def decode_list(items):
    """Function to decode a list of items."""
    if type(items) != list:
        return []
    data = []
    for item in items:
        item = decode(item)
        if item:
            data.append(item)
    return data


def anonymise_email(email):
    """Function to get anonymity email."""
    email = str(email)
    if len(email) < 4:
        return "******"
    try:
        name = email.split("@")[0]
        privider = email.split("@")[1].split(".")[0]
        doamin = email.split("@")[1].split(".")[1]
        value = name[0:2] + "*******@" + privider[0] + "**" + doamin
    except:
        value = email[0:2] + "*****" + email[-2:]
    return value


def anonymise_value(value):
    """Function to get anonymity value."""
    value = str(value)
    if len(value) < 4:
        return "******"
    return "*****" + value[-4:]


def is_image_valid(image):
    """Function to check the image is valid."""
    valid = image.name.lower().endswith(
        (
            ".bmp",
            ".dib",
            ".gif",
            ".tif",
            ".tiff",
            ".jfif",
            ".jpe",
            ".jpg",
            ".jpeg",
            ".pbm",
            ".pgm",
            ".ppm",
            ".pnm",
            ".png",
            ".apng",
            ".blp",
        )
    )
    if valid:
        return True
    return False
    # try:
    #     print ('verifying')
    #     image = Image.open(image)
    #     image.verify()
    #     image.close()
    #     print ('success _is_image_valid')
    #     return True
    # except:
    #     return False


def convert_blob_to_image(blob):
    """Function to convert blob to image file."""
    try:
        with io.BytesIO(blob) as stream:
            file = File(stream)
        return file
    except:
        return None


def strlist_to_list(value):
    """Function to convert string list to list."""
    try:
        value = ast.literal_eval(value)
        if not isinstance(value, list):
            return None
        return value
    except:
        return None


def list_to_sentence(word_list):
    """Function to convert list to sentence."""
    if not word_list[:-1]:
        return " ".join(word_list)
    return "%s and %s" % (", ".join(word_list[:-1]), word_list[-1])


def get_file_path(instance, filename):
    """
    Function to get filepath for a file to be uploaded
    Args:
        instance: instance of the file object
        filename: uploaded filename

    Returns:
        path: Path of file
    """
    type = instance.__class__.__name__.lower()
    path = "%s/%s/%s:%s" % (type, instance.id, get_random_string(10), filename)
    return path


def percentage(value, total):
    """
    Calculates the percentage without zerodivision error.
    If total is 0. returns 0 without raising error.
    Args:
        value: Value to convert to percentage
        total: Total value

    Returns:
        percentage: Percentage
    """
    try:
        return round((value / total) * 100, 2)
    except ZeroDivisionError:
        return 0


def safe_append_to_dict_key(dictionary, key, value):
    """
    Appends a value to the list in the key of a dict without raising keyerror
    Args:
        dictionary: dict to append to
        key: key containing the list
        value: value to be appended

    Returns:
        dictionary: updated dict
    """

    try:
        dictionary[key].append(value)
    except KeyError:
        dictionary[key] = [value]
    return dictionary


def safe_join_to_query(dictionary, key, query):
    """
    Appends a query to an existing query in the key of a dict without raising keyerror
    Args:
        dictionary: dict to append to
        key: key containing the query
        query: query to be appended

    Returns:
        dictionary: updated dict
    """

    try:
        dictionary[key] = combine_queries(dictionary[key], query)
    except KeyError:
        dictionary[key] = query
    return dictionary


def pseudonymize_data(field, data):
    """
    Function to pseudonymize data
    Args:
        data: Input data

    Returns:
        data: Pseudonymized data
    """
    if not data:
        return data
    data_type = type(data)
    if data_type == str:
        if field in ["name", "first_name"]:
            return "Anonymous"
        elif field in ["last_name", "dial_code"]:
            return ""
        else:
            return "Anonymized"
    if data_type == list:
        return [pseudonymize_data(i, field) for i in data]
    if data_type == dict or data_type == OrderedDict:
        return {k: pseudonymize_data(k, v) for k, v in data.items()}
    if data_type == int:
        return 999999
    if data_type == float:
        sign = (-1) ** randint(1, 2)
        return sign * data * random()
    return data


def update_list_of_dict(existing_dict, new_items, unique_key="id"):
    """
    Function to update a list of dict with new items, and remove duplicate based
    on a key.
    Args:
        existing_dict: List to be updated.
        new_items: New items to be added.
        unique_key: The dict key that should be used to check unique.

    Returns:
        updated_dict
    """
    existing_dict += new_items
    updated_dict = list({v[unique_key]: v for v in existing_dict}.values())
    return updated_dict


def combine_queries(first_query, second_query):
    """
    Function to combine two queries

    The following code looks stupid. But it kept getting an AssertionError
    when trying to combine two querysets. I was able to narrow down the cause
    and understood that the error is caused when you try to combine two querysets
    in which the first one has a count of 0 or 1.
    References:
    https://code.djangoproject.com/ticket/24525
    https://code.djangoproject.com/ticket/26522
    https://code.djangoproject.com/ticket/26959
    """
    assert (
        first_query.model == second_query.model
    ), "Cannot combine queries of two models"
    QueryModel = first_query.model

    try:
        combined = first_query | second_query
    except AssertionError:
        try:
            combined = second_query | first_query
        except AssertionError:
            sup_ids = [i.id for i in first_query]
            buy_ids = [i.id for i in second_query]
            combined = QueryModel.objects.filter(id__in=sup_ids + buy_ids).distinct(
                "id"
            )
    return combined


def hash_file(file):
    """
    Function to compute the hash of a file

    Args:
        file: file to be hashed.
        block_size: fixed block size

    Returns:

    """
    if not file:
        return ""
    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)
    return md5.hexdigest()
