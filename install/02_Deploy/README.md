# EcuapassBot Directories

## EcuapassBot6-dev
Development site

## EcuapassBot6-prd
Final and clean site (Not working)

## EcuapassBot6-win
Current win repo used by clients 

## EcuapassBot6-windev
Test dir with last changes

## EcuapassBot6-winstable
Last stable win repo

## EcuapassBot6-wintest
Mirror of win repo for testing

## EcuapassBot6-wintest-links
Deployment site for EcuapassBot6 with links to production files and dirs
Steps for deployment:
- Update README.txt and VERSION.txt
- Copy site to wintest dir:
    rsync -Lra EcuapassBot6-wintest-links wintest
- Copy .git dir: first for wintest, then for win

