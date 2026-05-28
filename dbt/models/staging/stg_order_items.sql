select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    price,
    freight_value
from raw.order_items
where order_id is not null