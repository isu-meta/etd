# -*- encoding: iso-8859-1 -*-
import os
import pandas as pd
from etdcode.metabeqc import *

# Set your paths
pdf_reader = 'C:\\Program Files (x86)\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe'

py_code = os.getcwd()
pq_path = "Y:\\Scholarly Publishing Services\\DR Projects\\proquest_etd\\r20190117"
path = 'C:\\Users\\wteal\\Projects\\etd\\OUTPUT'

# Uncomment next line to unzip
#unzip(pq_path, path)

# Change python's OS path to working folder
os.chdir(path)

# Create sort object
# folders now includes XML, PDF, and any multimedia
SD = SortDocuments(path)
SD.pdfpath = path + "\\PDF\\"
"""try:
    SD.makefolders()
except Exception:
    pass
try:
    SD.sort()
except Exception:
    pass"""

# Transform ProQuest Metadata to BePress
#proquest2bepress(py_code, path)

# Declare fields for error report
names = []
titles = []
authors = []
title_correction = []
author_correction = []
embargodate = []
embargoname = []

# Initiate for-loop to create document objects
# XML-Transformed is the folder generated from proquest2bepress() method

for file in glob.glob(path + '\\XML-Transformed\\*.xml')[27:]:
    # Create BePress xml Object
    BP = BePress(file)
    be_name = BP.xmlname()
    be_author = BP.xmlauthor()
    print(be_author)
    be_title = BP.xmltitle()

    # Create PDF title page Object
    pdf_file = chext(file, '.xml', '.pdf')
    pdf_path_file = SD.pdfpath + "\\" + pdf_file
    PDP = PDFPress(pdf_path_file, pdf_reader)
    # These codes format pdf extracted text
    PDP.genfile()
    PDP.genlines()

    # Now we need to find the major, this will probably pring some documents for manual review
    PDP.findmajor()
    authority = py_code + '\\Sup\\ListofMajors.csv'
    x = (PDP.reconcilemajor(authority))
    # Need a better solution to sorting documents with more than one major

    # -----------------------------------------------------------------------------------------------------------------------
    # uncomment to add major for the first time. Proceed with caution, this will cause duplicates if run more than once.

    BP.set_and_commitmajor(x)
    # ------------------------------------------------------------------------------------------------------------------------
    # Now we need to validate the title
    PDP.validatekeyword(be_title, title=True, author=False)
    try:
        vtitle = Validate(BP.title, PDP.pdftitle, pdf_path_file, pdf_reader)
    except AttributeError:
        vtitle=Validate(BP.title,pdfitem="Error",pdfpath=pdf_path_file, pdfreader=pdf_reader)

    vtitle.validatetitle()
    trs = vtitle.titleresolve()
    if trs is not None:
        chng = input('Commit change to BePress XML? [y|n]')
        if chng == 'y' or chng == 'Y':
            BP.chtitle(trs)
            BP.committitle()
    else:
        pass

    # Author validation is similar to above
    PDP.validatekeyword(be_author, title=False, author=True)
    # Need to split full name since BePress uses fname, mname, and lname
    fname = BP.fname
    mname = BP.mname
    lname = BP.lname
    vauthor = Validate(BP.author, PDP.pdfauthor, pdf_path_file, pdf_reader)
    vauthor.validateauthor(fname, mname, lname, be_author)
    ars = vauthor.authorresolve(fname, mname, lname)
    if ars is not None:
        chng = input('Commit change to BePress XML? [y|n]')
        if chng == 'y' or chng == 'Y':
            BP.chfname(ars[0])
            BP.chmname(ars[1])
            BP.chlname(ars[2])
            BP.commitauthor()
    else:
        pass
    BP.xmlauthor()
    BP.updaterights_holder()
    # Now we need to append our correction data to the empty lists we created earlier
    if ars is not None or trs is not None:
        basetitle = os.path.basename(file)
        names.append(basetitle)
        titles.append(lazy_encode(be_title))
        title_correction.append(trs)
        authors.append(lazy_encode(be_author))
        if ars != None:
            newauthor = [" ".join(ars)]
            author_correction.append(newauthor)
        else:
            author_correction.append(ars)
    else:
        pass

    # find and move Files with upcoming embargo dates
    ed = BP.xmlfield('embargo_date')
    edtitle = os.path.basename(file)
    embv = SD.findembargo(file, ed, pdf_file)
    if embv != 'None':
        embargodate.append(ed)
        embargoname.append(edtitle)
    else:
        pass
    continue

# Finally done with the for loop, we can submit our error report and merge the corrected xmls for batch uploading

# Write error report with pandas
ErrorDataSet = list(zip(names, titles, title_correction, authors, author_correction))
df = pd.DataFrame(data=ErrorDataSet, columns=['File', 'Title', 'Correction', 'Author', 'Correction'])
df.to_csv('ErrorReport.csv', index=True, header=True)

# Write embargo report
EmbargoDataSet = list(zip(embargoname, embargodate))
ef = pd.DataFrame(data=EmbargoDataSet, columns=['File', 'Date'])
ef.to_csv('EmbargoReport.csv', index=True, header=True)

# Merge non-embargoed xml using Kelly's merge XSLT
inpath = path + '\\XML-Transformed'
fileinpath = os.listdir(inpath)[0]
newinpath = inpath + "\\" + fileinpath

outpath = path + '\\outfile.xml'
merge = py_code + '\\Sup\\merge.xsl'

xmltransform(newinpath, merge, outpath)
roottag(path + '\\outfile.xml')

# sort embargod docs
embargo_path = path + "\\Embargo"
emb = SortDocuments(embargo_path)
emb.sort()
