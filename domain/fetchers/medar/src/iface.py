
import abc 
import typing 
import functools
import json 

# import jsonschema


# with open("src/schema.json") as f:
#     schema = json.load(f)


class Product:
    def __init__(self, data: dict) -> None:
        self._data = data
        
        # jsonschema.validate(instance=data, schema=schema)

    @property
    def _dict(self) -> dict:
        return self._data


    def __repr__(self) -> str:
        return f"Product({self._data})"
    

# Inject Intializer on every class. 
# We need a handle that ultimately will absorb the 
# data operations on data(source|dest) 



class Connectable(abc.ABC):

    @abc.abstractmethod
    @functools.cached_property
    def connector(self) -> typing.Any: 
        """
        Return a connector to the data source/destination.

        The connector is a lower-level interface to the data source/destination.
        It is intended to be used by the data source/destination itself and
        should not be used directly by users of this interface.

        Returns:
            typing.Any: The connector.
        """
        return None


class DataSource(Connectable):
    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator[Product]: 
        """
        Iterate over all Products in the DataSource.

        Yields:
            Product
        """
        ...


class DataDestination(Connectable):
    @abc.abstractmethod
    def push(self, product: Product): 
        """
        Push a product into the destination.

        Args:
            product (Product): The product to be pushed.
        """
        
        ...

