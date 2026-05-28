select
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
from raw.order_payments
where order_id is not null