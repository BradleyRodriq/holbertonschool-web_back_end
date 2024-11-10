-- Using the table named 'metal_bands' from 'metal_bands.sql', ranks country origins of bands, ordered by the number of non-unique fans.
SELECT
origin    AS origin,
SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY SUM(fans) DESC;
