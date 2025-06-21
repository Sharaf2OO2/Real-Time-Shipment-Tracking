SELECT 
    SHIPMENT_ID,
    CURRENT_STATUS,
    CURRENT_ADDRESS,
    CURRENT_COUNTRY,
    LAST_UPDATED
FROM {{ source('silver_data', 'delivery_status') }}
WHERE CURRENT_STATUS != 'delivered'