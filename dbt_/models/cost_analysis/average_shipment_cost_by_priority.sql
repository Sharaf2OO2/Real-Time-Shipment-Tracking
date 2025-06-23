SELECT 
    priority_level, 
    AVG(SHIPMENT_COST) AS AVG_COST
FROM {{ source('silver_data', 'shipments') }}
GROUP BY priority_level
ORDER BY AVG_COST DESC