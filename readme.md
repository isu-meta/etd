
# etd

Creates BePress XML from ProQuest metadata

## Prerequisites

* [Saxon HE](http://saxon.sourceforge.net/)

This code assumes you have Saxon available for XSLT transformations. We
are using the [Saxon HE for .Net](http://saxon.sourceforge.net/)

## Getting Started

Clone the repository and create a virtual environment.

```
> git clone https://github.com/isu-meta/etd
> cd etd
> python -m venv etd_env
> etd_env\Scripts\activate
> pip install -r requirements.txt
```

Update paths in [workflow.py](workflow.py)

| Variable Name | Description                      |
|---------------|----------------------------------|
| pdf_reader    | Path to Adobe or similar reader  |
| path          | Path to a blank output directory |
| pq_path       | Path to proquest .zip files      |

### Run

From your anaconda environment.

```
> python workflow.py
```

Results will appear in the output directory mentioned above.

## Other Institutions

Non-ISU institutions will need to change the fulltext-url path in [ETD-ProQuestXML2bepressXML-2017.xsl](Sup/ETD-ProQuestXML2bepressXML-2017.xsl).

```xml
<fulltext-url>
<xsl:variable name="pdfpath">
    <xsl:value-of select="DISS_content/DISS_binary"/>
</xsl:variable>
<xsl:value-of select="concat('https://behost.lib.iastate.edu/DR/uploads/', $pdfpath)"/>
</fulltext-url>
```

A new [ListofMajors.csv](Sup/ListofMajors.csv) will also need to be included.

## Documentation

**This documentation was written for an older version of etd. Some parts may
no longer be applicable.** https://mddocs.readthedocs.io/en/latest/theses.html#etds
