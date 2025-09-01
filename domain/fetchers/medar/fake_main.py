import boto3
import decimal

# --- Configuration ---
TABLE_NAME = "products"
CLIENT_ID = "medar"

# --- DynamoDB Resource ---
ddb = boto3.resource("dynamodb")
products_table = ddb.Table(TABLE_NAME)

# --- Product Data ---
PRODUCTS = [
    {
        "id": "1",
        "title": "Wireless Noise-Cancelling Headphones",
        "description": "Over-ear Bluetooth headphones with 30h battery life.",
        "price": decimal.Decimal("149.99"),
    },
    {
        "id": "2",
        "title": "Ergonomic Office Chair",
        "description": "Adjustable lumbar support, breathable mesh back.",
        "price": decimal.Decimal("249.00"),
    },
    {
        "id": "3",
        "title": "4K Ultra HD Monitor",
        "description": "27-inch IPS display with HDR and 144Hz refresh rate.",
        "price": decimal.Decimal("399.99"),
    },
    {
        "id": "4",
        "title": "Mechanical Keyboard",
        "description": "Compact TKL design with hot-swappable switches.",
        "price": decimal.Decimal("129.50"),
    },
    {
        "id": "5",
        "title": "Smart LED Light Bulbs (4-pack)",
        "description": "Wi-Fi enabled, compatible with Alexa and Google Home.",
        "price": decimal.Decimal("49.99"),
    },
    {
        "id": "6",
        "title": "Electric Standing Desk",
        "description": "Adjustable height with memory presets, 120x60 cm.",
        "price": decimal.Decimal("359.00"),
    },
    {
        "id": "7",
        "title": "Portable SSD 1TB",
        "description": "USB-C, 1050MB/s transfer speed, shock-resistant.",
        "price": decimal.Decimal("119.99"),
    },
    {
        "id": "8",
        "title": "Gaming Mouse",
        "description": "RGB lighting, 16000 DPI sensor, 8 programmable buttons.",
        "price": decimal.Decimal("59.90"),
    },
    {
        "id": "9",
        "title": "Air Purifier",
        "description": "HEPA filter for rooms up to 50 m², 3 fan speeds.",
        "price": decimal.Decimal("199.00"),
    },
    {
        "id": "10",
        "title": "Smart Coffee Maker",
        "description": "Wi-Fi enabled, brew scheduling via mobile app.",
        "price": decimal.Decimal("179.00"),
    },
]


# --- Logic ---
def insert_products(products: list[dict]) -> None:
    for product in products:
        products_table.put_item(
            Item={
                "product_id": product["id"],
                "client_id": CLIENT_ID,
                "body": product,
            }
        )
    print(f"Inserted {len(products)} products into '{TABLE_NAME}'.")


def main():
    insert_products(PRODUCTS)


if __name__ == "__main__":
    main()

# --- Output ---
