SELECT DELAY_REASON, COUNT(1) OCCURRENCES
FROM {{ source('silver_data', 'delivery_status') }}
WHERE DELAY_REASON != 'n/a'
GROUP BY 1
ORDER BY 2 DESC