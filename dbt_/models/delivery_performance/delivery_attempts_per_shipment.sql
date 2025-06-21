SELECT SHIPMENT_ID, COUNT(1) ATTEMPT_COUNT
FROM {{ source('silver_data', 'delivery_status') }}
GROUP BY 1
ORDER BY 2 DESC