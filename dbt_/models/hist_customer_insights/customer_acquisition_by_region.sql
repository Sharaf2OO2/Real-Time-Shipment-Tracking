SELECT 
    EXTRACT(MONTH FROM metadata.order_date) AS month, 
    customers.customer_region, 
    COUNT(DISTINCT customers.customer_id) AS new_customers
FROM {{ source('silver_data', 'shipments') }} AS shipments
JOIN {{ source('silver_data', 'metadata') }} AS metadata USING(shipment_id)
JOIN {{ source('silver_data', 'customers') }} AS customers USING(customer_id)
GROUP BY 1, 2
ORDER BY 1, 3 DESC