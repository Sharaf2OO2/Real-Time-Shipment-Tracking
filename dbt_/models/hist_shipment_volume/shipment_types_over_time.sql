SELECT 
    EXTRACT(MONTH FROM metadata.order_date) AS month, 
    shipments.shipment_type, 
    COUNT(*) AS shipment_count
FROM {{ source('silver_data', 'shipments') }} AS shipments
JOIN {{ source('silver_data', 'metadata') }} AS metadata USING(shipment_id)
GROUP BY 1, 2
ORDER BY 1, 3 DESC