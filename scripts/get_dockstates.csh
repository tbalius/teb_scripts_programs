
# here are the fileds for the table approved_requests 
# | idx | dock_version | requestor_name             | requestor_title             | project_title                                                      | email_address              | telephone_number | fax_number      | institution                                                                   | address1                                                   | address2                | city_state                       | zip_code   | advisor_name                   | advisor_title       | web_address                                    | date_submitted           | password        | download_credits | distribution_type                                                                                                                                                                                                                                          |
#

mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(*) from approved_requests group by dock_version order by count(*);"

# DOCK6 spesific
mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(*) from approved_requests where dock_version = 'dock_6';"
mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(DISTINCT(requestor_name)) from approved_requests where dock_version = 'dock_6';"
mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(DISTINCT(institution)) from approved_requests where dock_version = 'dock_6';"
mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(DISTINCT(email_address)) from approved_requests where dock_version = 'dock_6';"

echo "download_credits != '5' -- count those who did downloaded at lest one copy"
mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select dock_version,count(*) from approved_requests where dock_version = 'dock_6' and download_credits != '5';"

# mysql -u dock_license -pok1298hg%^ -h dock.compbio.ucsf.edu dock -e "select web_address from approved_requests where dock_version = 'dock_6';" > web_address.txt
# 
# cat web_address.txt | sed -e 's/http:\/\///' -e 's/https://' | awk -F'/' '{print $1}' | sort -u > web_address_clean_uniq.txt
#
# echo -n "" >! web_address_clean_uniq_ext.txt
# foreach address (`cat web_address_clean_uniq.txt`) 
#     set extention = $address:e
#     echo $extention >> web_address_clean_uniq_ext.txt
# end
# cat web_address_clean_uniq_ext.txt | tr A-Z a-z | sort | uniq -c | sort

