
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

Update paths in [workflow.py](workflow.py)

| Variable Name | Description                      |
|---------------|----------------------------------|
| pdf_reader    | Path to Adobe or similar reader  |
| path          | Path to a blank output directory |
| pq_path       | Path to proquest .zip files      |


### Run

From the anaconda prompt.

``` {.sourceCode .console}
(base) C:\etd> activate etd_env
(etd_env) C:\etd> python workflow.py
```

Other Institutions
-------------------

Non-ISU institutions will need to change the fulltext-url path in [ETD-ProQuestXML2bepressXML-2017.xsl](Sup/ETD-ProQuestXML2bepressXML-2017.xsl).

``` {.sourceCode .xml}
<fulltext-url>
<xsl:variable name="pdfpath">
    <xsl:value-of select="DISS_content/DISS_binary"/>
</xsl:variable>
<xsl:value-of select="concat('https://behost.lib.iastate.edu/DR/uploads/', $pdfpath)"/>
</fulltext-url>
```

A new [ListofMajors.csv](Sup/ListofMajors.csv) will also need to be included.
