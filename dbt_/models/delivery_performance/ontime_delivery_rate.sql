SELECT 
    ROUND(AVG(
        CASE
            WHEN ACTUAL_DELIVERY_DATE <= ESTIMATED_DELIVERY_DATE THEN 1
            ELSE 0
        END
    ) * 100.0, 2) ON_TIME_PERCENTAGE
FROM {{ source('silver_data', 'delivery_status') }}