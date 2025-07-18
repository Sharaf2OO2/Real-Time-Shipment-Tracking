SELECT 
    WAREHOUSE_ID, 
    COUNT(*) TOTAL_SHIPMENTS
FROM {{ source('silver_data', 'metadata') }}
GROUP BY WAREHOUSE_ID
ORDER BY TOTAL_SHIPMENTS DESC