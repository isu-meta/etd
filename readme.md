
Etd
====

Creates BePress XML from ProQuest metadata

Prerequisites
-------------

* saxon he

This code assumes you have saxon available for xslt transformations. We
are using the [Saxon HE for .Net](http://saxon.sourceforge.net/)

Getting Started
----------------

Clone the repository and create an anaconda2 environment.

``` {.sourceCode .console}
$ git clone https://github.com/wryan14/etd.git
$ cd etd
$ conda create -n "etd_env" python=2.7
$ pip install -r requirements.txt
```

#### Set Up

1.  Update paths in *workflow.py*

| Variable Name | Description | ----------------------------------| |
pdf\_reader | Path to Adobe or similar reader | | path | Path to a blank
output directory | | pq\_path | Path to proquest .zip files |

2.  Modify ETD-ProQuestXML2bepressXML-2017.xsl as desired. For Non-ISU
    institutions, this means changing the fulltext-url target path.

``` {.sourceCode .xml}
<fulltext-url>
<xsl:variable name="pdfpath">
    <xsl:value-of select="DISS_content/DISS_binary"/>
</xsl:variable>
<xsl:value-of select="concat('https://behost.lib.iastate.edu/DR/uploads/', $pdfpath)"/>
</fulltext-url>
```

3.  Confirm Sup files are appropriate. Non-ISU institutions can replace
    ListofMajors.csv.

### Run

``` {.sourceCode .console}
(base) C:\etd> activate etd_env
(etd_env) C:\etd> python workflow.py
```
