
import typing
import operator
import functools

import json 

import iface


raw_mock_data="""
    [{
        "id": "1",
        "title": "Wireless Noise-Cancelling Headphones",
        "description": "Over-ear Bluetooth headphones with 30h battery life.",
        "price": 149.99
    },
    {
        "id": "2",
        "title": "Ergonomic Office Chair",
        "description": "Adjustable lumbar support, breathable mesh back.",
        "price": 249.00
    },
    {
        "id": "3",
        "title": "4K Ultra HD Monitor",
        "description": "27-inch IPS display with HDR and 144Hz refresh rate.",
        "price": 399.99
    },
    {
        "id": "4",
        "title": "Mechanical Keyboard",
        "description": "Compact TKL design with hot-swappable switches.",
        "price": 129.50
    },
    {
        "id": "5",
        "title": "Smart LED Light Bulbs (4-pack)",
        "description": "Wi-Fi enabled, compatible with Alexa and Google Home.",
        "price": 49.99
    },
    {
        "id": "6",
        "title": "Wireless Gaming Mouse",
        "description": "RGB lighting, 16000 DPI sensor, 8 programmable buttons.",
        "price": 59.90
    },
    {
        "id": "7",
        "title": "Air Purifier",
        "description": "HEPA filter for rooms up to 50 m², 3 fan speeds.",
        "price": 199.00
    }]
"""

class products(iface.DataSource):
    
    @functools.cached_property
    def connector(self) -> typing.Any:
        
        return operator.call(type(
            "DataSourceConnector",
            (), 
            {
                "fetch": lambda self: json.loads(raw_mock_data)
            }
        ))


    #def __iter__(self): return iter(map(iface.Product, self.connector.fetch()))

    def __iter__(self): return map(iface.Product, self.connector.fetch())


class dump_stdout(iface.DataDestination):

    @functools.cached_property
    def connector(self) -> typing.Any:
        return operator.call(type(
            "DataDestinationConnector",
            (),
            {
                "push": lambda self, product: print(product)
            }
        ))

    def push(self, product: iface.Product) -> None:
        self.connector.push(product._dict)
