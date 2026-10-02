Based on the data provided by the API, Timestamps are UTC, which I converted to Pacific for my time zone.
The values came as strings which was converted to numeric using .to_numeric
EIA reports net generation, so a plant's own nighttime equipment use appears as a small negative value. 
Rows aren't sorted.
EIA throws intermittent 500/504 errors
A 200 status doesn't guarantee data 
Pages cap at 5000 rows