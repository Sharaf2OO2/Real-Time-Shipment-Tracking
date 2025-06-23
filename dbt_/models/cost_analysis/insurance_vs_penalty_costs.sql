SELECT 
    SUM(INSURANCE_COVERAGE) AS TOTAL_INSURANCE,
    SUM(DELIVERY_PENALTY) AS TOTAL_PENALTY
FROM {{ source('silver_data', 'shipments') }}
JOIN {{ source('silver_data', 'delivery_status') }} USING (SHIPMENT_ID)