
# ALL
CMM1="init_application|SANCHEZPOLO|/home/lg/BIO/ecuapassdocs/EcuapassBot/EcuapassBot6-dev/ecugui|null|null"

# TRNASCOMERINTER
#CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/EcuapassSamples/samples-TRANSCOMERINTER/CPI-TRANSCOMERINTER-TEST-0010000000082.pdf|TRANSCOMERINTER|null|null"

# BYZA
#CMM2="doc_processing|/home/lg/Documents/Ecuapassdocs/DUMMY-BYZA-CPI-CO6861.pdf|BYZA|COLOMBIA|TULCAN"

# SANCHEZPOLO
CMM2="get_initial_pdf_info|/home/lg/BIO/ecuapassdocs/EcuapassSamples/samples-SANCHEZPOLO/CPI-SANCHEZPOLO-TEST-061984-24.pdf|SANCHEZPOLO|null|null"

ecuapass_commander.py<<EOF
$CMM1
$CMM2
