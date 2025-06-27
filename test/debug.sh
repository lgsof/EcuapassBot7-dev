# Batch file for debug python ecuapass_commander
#
# ALL
#CMM1="init_globals|BOTEROSOTO|/home/lg/BIO/ecuapassdocs/EcuapassBot/EcuapassBot6-dev/ecugui|null|null"

# TRANSCOMERINTER
#CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/EcuapassSamples/samples-TRANSCOMERINTER/CPI-TRANSCOMERINTER-TEST-0010000000082.pdf|TRANSCOMERINTER|null|null"

# BYZA
#CMM2="doc_processing|/home/lg/Documents/Ecuapassdocs/DUMMY-BYZA-CPI-CO6861.pdf|BYZA|COLOMBIA|TULCAN"

# SANCHEZPOLO
#CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/EcuapassSamples/samples-SANCHEZPOLO/TEST-CPI-SANCHEZPOLO-061984-24.pdf|SANCHEZPOLO|null|null"
#
# BOTEROSOTO
#CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/EcuapassSamples/samples-BOTEROSOTO/TEST-CPI-BOTERO-ADIQUIM.pdf|BOTEROSOTO|null|null"

#CMM1="get_installkey_cloud|LOGITRANS|102030|null|null"
CMM1="init_application|LOGITRANS|/home/lg/BIO/ecuapassdocs/EcuapassBot7/EcuapassBot7-dev/ecugui|null|null"

CMM1="init_application|ALCOMEXCARGO|/home/lg/BIO/ecuapassdocs/EcuapassBot7/EcuapassBot7-dev/ecugui|null|null"
CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/ecuapassdocs-samples/samples-ALCOMEXCARGO/TEST-CPI-ALCOMEXCARGO-COCO000215.pdf|ALCOMEXCARGO|null|null"
CMM3="doc_processing|/home/lg/Documents/Ecuapassdocs/DUMMY-ALCOMEXCARGO-CPI-CO000216.pdf|ALCOMEXCARGO|COLOMBIA|TULCAN"

echo ">>>" $CMM1
echo ">>>" $CMM2
echo ">>>" $CMM3
commander/ecuapass_commander.py<<EOF
$CMM1
$CMM2
$CMM3

