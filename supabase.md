# Database Built on PostGres

I would usually script out when tables as create scripts that would be in `SQL\` I would store my supabase api key inside `.env` with my Polygon key, create a module to connect to my database and `main.py` would be able to create the entire database schema if it doesn't exist.

As a first pass I stored my data in 2 parquet files (these would be tables in the next iteration).