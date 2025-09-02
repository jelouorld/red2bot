
import typing
import functools

import boto3
import decimal

import iface 


DynamoDBTable = typing.TypeVar("DynamoDBTable")
PostgresQLConnection = typing.TypeVar("PostgresConnection")

class products(iface.DataSource): 

    @functools.cached_property
    def handle(self) -> PostgresQLConnection:
        # TODO
        return {}

    def __iter__(self) -> typing.Iterator[iface.Product]:
        # TODO
        # code for real implementation here.
        pass 


class dynamodb(iface.DataDestination):

    @functools.cached_property
    def connector(self) -> DynamoDBTable:
        """
        Return the DynamoDB table instance for this data destination.

        The DynamoDB table is returned as a cached property, meaning that
        the first time it is accessed, the table is retrieved and stored
        in the property. Subsequent accesses will return the cached value.

        Returns:
            DynamoDBTable: The DynamoDB table instance.
        """
        ddbr = boto3.resource("dynamodb")
        ddbt = ddbr.Table("products")
        return ddbt

    def push(self, product: iface.Product) -> None:

        # build adapters bound methods
        """
        Push a product into the DynamoDB table.

        The product is adapted by applying the sequence of adapters
        (i.e., functions with the name starting with "adapt_") to it.
        The adapted product is then inserted into the DynamoDB table.

        Args:
            product (Product): The product to be pushed.
        """
        adapters = [
            getattr(self, name) for name in dir(self) if name.startswith("adapt_")
        ]

        # run the adapters. 
        # Equivalent to composition of functions 
        # p' = f1 · f2 · f3 · ... · fn(p)
        adapted_product = functools.reduce(
            lambda x, f:f(x), reversed(adapters), product
        )

        self.connector.put_item(Item=adapted_product._dict)
    

    def adapt_price(self, product: iface.Product) -> iface.Product:
        """
        Mutation: float -> decimal(str(float))
        
        We need to adapt the price attribute from `float` to `decimal.Decimal`
        because DynamoDB does not support `float`.
        """
        price = product._data['price']
        product._data['price'] = decimal.Decimal(str(price))

        return product


    def adapt_dynamodb_identity(self, product: iface.Product) -> iface.Product:

        """
        Mutation: adds client_id and product_id
        
        We need to adapt the product attribute by adding client_id and product_id
        for DynamoDB. DynamoDB does not allow us to use attribute names as
        primary keys but we can use a combination of two attributes as primary key.
        client_id will be used as partition key and product_id will be used as sort key.
        """
        
        product._data['client_id'] = "medar"
        product._data['product_id'] = product._data['id']

        return product



