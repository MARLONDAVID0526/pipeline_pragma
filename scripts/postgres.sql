SELECT * FROM chess_data.fact_tablex

SELECT * FROM chess_data._dlt_loads;

SELECT * FROM chess_data.user


SELECT * FROM chess_data.generic_fact_table
order by timestamp asc

SELECT * FROM chess_data.statistics

select count(*)  FROM chess_data.generic_fact_table
group by _dlt_load_id


SELECT AVG(price) FROM chess_data.generic_fact_table

SELECT * FROM chess_data_staging.fact_tablex
order by timestamp asc

select * from chess_data._dlt_pipeline_state




DROP SCHEMA IF EXISTS chess_data_staging CASCADE;
DROP SCHEMA IF EXISTS chess_data CASCADE;
