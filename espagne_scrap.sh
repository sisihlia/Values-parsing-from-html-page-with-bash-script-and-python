#!/bin/bash

curl=$(which curl)
contents="contents.txt"
url="https://voyages.carrefour.fr/serp?origin=homePage,recherche_sejours&s_c.site=B2C&s_c.type_produit=sejour_etranger,circuits&s_c.destination=MCPI.ES&ref_mmp=0,5000&s_st=base_price&byPage=12"
email="admin@orchestra.eu"
result="result.txt"

#dump contents of website
function dump_contents() {
	$curl -sv $url >  $contents 2>&1
 	handle_errors
}

#handle errors when curl fails
function handle_errors(){
	if [ $? -ne 0 ]
	then
  		echo "Error downloading page"
  		exit -1
	fi
}

#extract the variable and store the prices into a file
function extract_vars_with_price(){
	product_price="$(cat  $contents | sed -n '/^<script>/ { x; s/^/\x0/; /^\x0\{3\}$/ { x; :a; p; /done/q; n; ba }; x }' | sed 's/<[^>]*>//g;/^ *$/d' | grep "product_price" | head -4 | sed -r 's/[\t ]*//;s/,*$//')" 	
}

#print the price list 
function print_prices(){
	echo "Print the 4 cheapest prices to Spain"
	echo $product_price

}

#parse the contents to get header age
function get_header_age(){
	age="$(cat  $contents | grep "\s\bage\b" | sed 's/<//g' )"
	#echo "Header" $age
}

#concatenate both values and send email to
function send_info_to_mail() {
	echo -e "$product_price \n" $age > $result
	#result="$(echo -e "$product_price \n" $age)"
        #echo -e "$product_price \n" $age | mail -s "result" $email 
}
###MAIN###
dump_contents
extract_vars_with_price
get_header_age	
send_info_to_mail
