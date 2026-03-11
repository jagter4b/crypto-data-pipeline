CREATE USER etl_user WITH SUPERUSER PASSWORD 'password'

create database coingecko_api; 

GRANT ALL PRIVILEGES ON DATABASE coingecko_api to etl_user

\c coingecko_api; 


-- table: public.coins_list 

CREATE TABLE IF NOT EXISTS public.coins_list 
(

id varchar(100) PRIMARY KEY, 
name varchar(100) NOT NULL, 
symbol varchar(100) NOT NULL, 
insertion_date TIMESTAMP NOT NULL DEFAULT NOW()

) ;

-- table market chart 

CREATE TABLE IF NOT EXISTS public.market_chart (

id SERIAL PRIMARY KEY, 
coin_id varchar(100) NOT NULL, 
vs_currency varchar(10) NOT NULL, 
"timestamp" TIMESTAMP NOT NULL, 
price numeric(18,4) NOT NULL, 
market_cap numeric(22,4) NOT NULL, 
total_volume numeric(22,4) NOT NULL, 
insertion_date timestamp NOT NULL DEFAULT NOW() 

) ; 