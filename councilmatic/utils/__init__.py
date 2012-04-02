import json
import os
import tempfile
import requests
import urllib

# Adapted from Scraperwiki utils

def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

def pdftotxt(pdfdata):
    """converts pdf file to txt file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    txtin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptxt = txtin.name # "temph.xml"
    cmd = '/usr/bin/pdftotext -enc UTF-8 -layout "%s" "%s"' % (pdffout.name, txtin.name)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    txtdata = txtin.read()
    txtin.close()
    return txtdata

def geocode(address, retries=5):
    """attempts to geocode an address"""
    response = requests.get(
        'http://maps.googleapis.com/maps/api/geocode/json',
        params={'address': address, 'sensor': 'false'})

    if response.status_code != 200 and retries > 0:
        return geocode(address, retries-1)
    if response.status_code != 200:
        return None

    response.encoding = 'UTF8'
    result = json.loads(response.text)
    return result
