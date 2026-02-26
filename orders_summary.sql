-- orders_summary.sql
-- This model joins orders and customers into one clean table.
-- dbt reads this file and creates a table in DuckDB automatically.

with orders as (
    -- ref() is dbt syntax — it tells dbt to use our seeds/orders.csv table
    select * from {{ ref('orders') }}
),

customers as (
    select * from {{ ref('customers') }}
)

select
    o.order_id,
    o.customer_id,
    c.name,
    c.email,
    o.amount,
    o.status,
    o.created_at
from orders o
left join customers c on o.customer_id = c.customer_id
