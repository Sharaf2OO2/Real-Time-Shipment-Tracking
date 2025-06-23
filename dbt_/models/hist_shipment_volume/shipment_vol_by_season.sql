SELECT 
    EXTRACT(QUARTER FROM metadata.order_date) AS quarter, 
    COUNT(*) AS shipment_volume
FROM {{ source('silver_data', 'metadata') }} AS metadata
GROUP BY 1
ORDER BY 1
