# -*- encoding: utf-8 -*-
import glob
import os
import os.path

import pandas as pd

from etdcode.metabeqc import (
    BePress,
    chext,
    lazy_encode,
    PDFPress,
    proquest2bepress,
    roottag,
    SortDocuments,
    Validate,
    xmltransform,
)

# Set your paths
pdf_reader = "C:\\Program Files (x86)\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"

py_code = os.getcwd()
pq_path = "Y:\\Scholarly Publishing Services\\DR Projects\\proquest_etd\\r20190607"
path = "C:\\Users\\wteal\\Projects\\etd\\OUTPUT"

# Change python's OS path to working folder
os.chdir(path)

# Create sort object
# folders now includes XML, PDF, and any multimedia
SD = SortDocuments(path)

# Unzip Proquest files and move them
# to the working directory
SD.set_up_proquest_files(pq_path)

# Transform ProQuest Metadata to BePress
proquest2bepress(py_code, path)

# Declare fields for error report
names = []
titles = []
authors = []
title_correction = []
author_correction = []

# Initiate for-loop to create document objects
# XML-Transformed is the folder generated from proquest2bepress() method

for file in glob.glob(path + "\\XML-Transformed\\*.xml")[27:]:
    # Create BePress xml Object
    BP = BePress(file)
    be_name = BP.xmlname()
    be_author = BP.xmlauthor()
    print(be_author)
    be_title = BP.xmltitle()

    # Create PDF title page Object
    pdf_file = os.path.join(SD.pdf_path, chext(file, ".xml", ".pdf"))
    PDP = PDFPress(pdf_file, pdf_reader)
    # These codes format pdf extracted text
    PDP.genfile()
    PDP.genlines()

    # Now we need to find the major, this will probably bring some documents for manual review
    PDP.findmajor()
    authority = py_code + "\\Sup\\ListofMajors.csv"
    major = PDP.reconcilemajor(authority)
    # Need a better solution to sorting documents with more than one major

    BP.set_and_commitmajor(major)
    # Now we need to validate the title
    PDP.validatekeyword(be_title, title=True, author=False)
    try:
        vtitle = Validate(BP.title, PDP.pdftitle, pdf_file, pdf_reader)
    except AttributeError:
        vtitle = Validate(
            BP.title, pdftitle="Error", pdfpath=pdf_file, pdfreader=pdf_reader
        )

    vtitle.validatetitle()
    trs = vtitle.titleresolve()
    if trs is not None:
        chng = input("Commit change to BePress XML? [y|n]")
        if chng == "y" or chng == "Y":
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
    vauthor = Validate(BP.author, PDP.pdfauthor, pdf_file, pdf_reader)
    vauthor.validateauthor(fname, mname, lname, be_author)
    ars = vauthor.authorresolve(fname, mname, lname)
    if ars is not None:
        chng = input("Commit change to BePress XML? [y|n]")
        if chng == "y" or chng == "Y":
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

# Finally done with the for loop, we can submit our error report and merge the corrected xmls for batch uploading

# Write error report with pandas
error_data_set = list(zip(names, titles, title_correction, authors, author_correction))
df = pd.DataFrame(
    data=error_data_set, columns=["File", "Title", "Correction", "Author", "Correction"]
)
df.to_csv("ErrorReport.csv", index=True, header=True)

# Merge document XML using Kelly Thompson's merge XSLT
inpath = path + "\\XML-Transformed"
fileinpath = os.listdir(inpath)[0]
newinpath = inpath + "\\" + fileinpath

outpath = path + "\\outfile.xml"
merge = py_code + "\\Sup\\merge.xsl"

xmltransform(newinpath, merge, outpath)
roottag(path + "\\outfile.xml")
