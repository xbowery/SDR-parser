rm -f *.csv
yest_date=$(date -d '-1 day' '+%Y_%m_%d')

name_concat() {
    local input_string=$1
    local first_part="CFTC_CUMULATIVE_"
    local second_part="${yest_date}.zip"

    # Concatenate the strings
    local result="$first_part$input_string"_"$second_part"

    # Return the result
    echo "$result"
}

url_concat() {
    local input_string=$1
    local first_part="kgc0418-tdw-data-0.s3.amazonaws.com/cftc/eod/CFTC_CUMULATIVE_"
    local second_part="${yest_date}.zip"

    # Concatenate the strings
    local result="$first_part$input_string"_"$second_part"

    # Return the result
    echo "$result"

}

action() {
    local input_one=$1
    local input_two=$2

    curl $input_one --output $input_two
    unzip $input_two
    rm $input_two
}

commods_name=$(name_concat "COMMODITIES")
commods_url=$(url_concat "COMMODITIES")
credits_name=$(name_concat "CREDITS")
credits_url=$(url_concat "CREDITS")
forex_name=$(name_concat "FOREX")
forex_url=$(url_concat "FOREX")
rates_name=$(name_concat "RATES")
rates_url=$(url_concat "RATES")

mkdir -p data

action $commods_url $commods_name
action $credits_url $credits_name
action $forex_url $forex_name
action $rates_url $rates_name