SELECT 
    EXTRACT(MONTH FROM metadata.order_date) AS month, 
    COUNT(DISTINCT shipments.customer_id) AS repeat_customers
FROM {{ source('silver_data', 'shipments') }} AS shipments
JOIN {{ source('silver_data', 'metadata') }} AS metadata USING(shipment_id)
GROUP BY 1
ORDER BY 1