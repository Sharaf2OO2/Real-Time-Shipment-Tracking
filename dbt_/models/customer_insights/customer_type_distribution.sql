SELECT
    AVG(
    CASE 
        WHEN CUSTOMER_TYPE = 'individual' THEN 1 
        ELSE 0 
    END) * 100 INDIVIDUAL_CUSTOMER_PERCENTAGE,
    AVG(
    CASE 
        WHEN CUSTOMER_TYPE = 'business' THEN 1 
        ELSE 0 
    END) * 100 BUSINESS_CUSTOMER_PERCENTAGE
FROM {{ source('silver_data', 'customer') }}