rm -f *.csv
yest_date=$(date -d '-1 day' '+%Y_%m_%d')
commods_name="CFTC_CUMULATIVE_COMMODITIES_${yest_date}.zip"
commods_url="kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_COMMODITIES_${yest_date}.zip"
credits_name="CFTC_CUMULATIVE_CREDITS_${yest_date}.zip"
credits_url="kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_CREDITS_${yest_date}.zip"
forex_name="CFTC_CUMULATIVE_FOREX_${yest_date}.zip"
forex_url="kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_FOREX_${yest_date}.zip"
rates_name="CFTC_CUMULATIVE_RATES_${yest_date}.zip"
rates_url="kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_RATES_${yest_date}.zip"
mkdir -p data
curl $commods_url --output $commods_name
curl $credits_url --output $credits_name
curl $forex_url --output $forex_name
curl $rates_url --output $rates_name
unzip $commods_name
unzip $credits_name
unzip $forex_name
unzip $rates_name
rm $commods_name
rm $credits_name
rm $forex_name
rm $rates_name