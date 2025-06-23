SELECT 
    EXTRACT(MONTH FROM metadata.order_date) AS month, 
    SUM(shipments.revenue_generated) AS total_revenue, 
    SUM(shipments.shipment_cost) AS total_cost
FROM {{ source('silver_data', 'shipments') }} AS shipments
JOIN {{ source('silver_data', 'metadata') }} AS metadata USING(shipment_id)
GROUP BY 1
ORDER BY 1