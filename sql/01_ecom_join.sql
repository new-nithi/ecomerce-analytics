SELECT 
    o.order_id,
    o.order_date,
    o.channel,
    o.payment_method,
    o.shipping_type,
    o.status,
    c.customer_id,
    c.customer_name,
    c.country,
    c.city,
    c.segment,
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    oi.quantity,
    oi.unit_price,
    oi.discount_rate,
    oi.line_total,
    m.ad_spend
FROM orders o
JOIN customers c 
    ON o.customer_id = c.customer_id
JOIN order_items oi 
    ON o.order_id = oi.order_id
JOIN products p 
    ON oi.product_id = p.product_id
LEFT JOIN marketing_spend m 
    ON m.channel = o.channel
    AND DATE_FORMAT(o.order_date, '%Y-%m-01') = m.month
ORDER BY o.order_date ASC;
