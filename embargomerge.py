import os

from etdcode.metabeqc import roottag, SortDocuments, xmltransform

# This code uses only the merge feature, which is useful for Embargoes that have already been Qc'd
path = 'C:\\Users\\wteal\\Projects\\Temp_Upload'
py_code = os.getcwd()

inpath = path + r'\\XML'
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
