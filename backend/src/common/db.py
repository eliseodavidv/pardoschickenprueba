import os
import boto3

_dynamodb = boto3.resource("dynamodb")

TENANTS_TABLE = os.environ["TENANTS_TABLE"]
MENU_TABLE = os.environ["MENU_TABLE"]
ORDERS_TABLE = os.environ["ORDERS_TABLE"]
ORDER_EVENTS_TABLE = os.environ["ORDER_EVENTS_TABLE"]

def tenants_table():
    return _dynamodb.Table(TENANTS_TABLE)

def menu_table():
    return _dynamodb.Table(MENU_TABLE)

def orders_table():
    return _dynamodb.Table(ORDERS_TABLE)

def order_events_table():
    return _dynamodb.Table(ORDER_EVENTS_TABLE)
