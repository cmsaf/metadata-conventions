# CM SAF Metadata Conventions for Data Catalogs

CM SAF Metadata Conventions for Data Catalogs, Version 3 (CDOP-4), May 2025.

## Introduction

The CM SAF Metadata Conventions for Data Catalogs describe the information published in data catalogs. They are
mandatory for newly generated datasets.

The goal is to make our datasets Findable, Accessible, Interoperable and Re-usable
([FAIR](https://www.go-fair.org/fair-principles/)).

## Metadata

The following metadata must be prepared before publishing a dataset.

| Property             | Description                                                | DataCite Schema                                                                                                                                 | Comment                                      | Changelog      |
|----------------------|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|----------------|
| Type                 | Resource type                                              | [ResourceType](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/resourcetype/) with resourceType="Dataset"                  | "grid"                                       |                |
| Identifier           | Unique identifier for the dataset                          | [Identifier](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/identifier/)                                                  | DOI                                          |                |
| Title                | Primary name of the dataset                                | [Title](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/title/)                                                            |                                              |                |
| Description          | Detailed information about the dataset content and purpose | [Description](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/description/)                                                |                                              |                |
| Keywords             | Keywords describing the dataset                            | [Subject](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/subject/)                                                        | GCMD Science Keywords                        | New in CDOP-4  |
| Authors              | Individuals responsible for creating the dataset           | [Creator](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/creator/)                                                        |                                              |                |
| Publisher            | Entity responsible for making the dataset available        | [Publisher](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/publisher/)                                                    |                                              |                |
| Publication year     | Year when the dataset will be released                     | [PublicationYear](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/publicationyear/)                                        |                                              |                |
| Version              | Version number                                             | [Version](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/version/)                                                        |                                              |                |
| Size                 | The dataset's total volume, typically in GB or TB          | [Size](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/size/)                                                              |                                              |                |
| File format          | Technical format of the dataset files (e.g. NetCDF)        | [Format](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/format/)                                                          |                                              |                |
| Temporal coverage    | Time period covered by the dataset                         | [Date](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/date/)                                                              |                                              |                |
| Spatial coverage     | Geographic area covered by the dataset                     | [GeoLocation](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/geolocation/)                                                |                                              |                |
| Related publications | Publications that cite, document, or use the dataset       | [RelatedIdentifier](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/relatedidentifier/) with relationType="IsDocumentedBy" |                                              |                |
| Previous versions    | Links to earlier versions of this dataset                  | [RelatedIdentifier](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/relatedidentifier/) with relationType="IsNewVersionOf" |                                              |                |
| Input datasets       | Source datasets that were used to create this dataset      | [RelatedIdentifier](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/relatedidentifier/) with relationType="IsDerivedFrom"  |                                              | New in CDOP-4  |
| License              | Dataset license                                            | [Rights](https://datacite-metadata-schema.readthedocs.io/en/latest/properties/rights/)                                                          | https://creativecommons.org/licenses/by/4.0/ | New in CDOP-4  |

We're currently registering our datasets at DataCite, who require the metadata in XML format. Here's an example

```xml
<?xml version="1.0" encoding="utf-8"?>
<resource xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://datacite.org/schema/kernel-4" xsi:schemaLocation="http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4/metadata.xsd">
  <resourceType resourceTypeGeneral="Dataset">grid</resourceType>
  <identifier identifierType="DOI">10.5676/EUM_SAF_CM/CLAAS/V003</identifier>
  <titles>
    <title xml:lang="en-us">CLAAS-3: CM SAF CLoud property dAtAset using SEVIRI - Edition 3</title>
  </titles>
  <descriptions>
    <description xml:lang="en-us" descriptionType="Abstract">
      Detailed dataset description goes here. The degree character is not available, instead use:
      My dataset is available on a 0.05&#x00b0; x 0.05&#x00b0; grid.
    </description>
  </descriptions>
  <subjects>
    <subject subjectScheme="GCMD Science Keywords, Version 8.6"> CLOUD PROPERTIES &gt; CLOUD FRACTION </subject>
  </subjects>
  <creators>
    <creator>
      <creatorName>Meirink, Jan Fokke</creatorName>
      <givenName>Jan Fokke</givenName>
      <familyName>Meirink</familyName>
      <affiliation>Koninklijk Nederlands Meteorologisch Instituut (KNMI)</affiliation>
    </creator>
    <creator>
      <creatorName>Karlsson, Karl-Göran</creatorName>
      <givenName>Karl-Göran</givenName>
      <familyName>Karlsson</familyName>
      <affiliation>Sveriges Meteorologiska och Hydrologiska Institut (SMHI)</affiliation>
    </creator>
  </creators>
  <publisher>Satellite Application Facility on Climate Monitoring (CM SAF)</publisher>
  <publicationYear>2022</publicationYear>
  <version>3.0</version>
  <sizes>
    <size>78.3 TiB</size>
  </sizes>
  <formats>
    <format>NetCDF-4</format>
  </formats>
  <dates>
    <date dateType="Issued">2022-12-06</date>
    <date dateType="Valid">2004-01-19/present</date>
  </dates>
  <geoLocations>
    <geoLocation>
      <geoLocationBox>
        <westBoundLongitude>-81.25</westBoundLongitude>
        <eastBoundLongitude>81.25</eastBoundLongitude>
        <southBoundLatitude>-81.30</southBoundLatitude>
        <northBoundLatitude>81.30</northBoundLatitude>
      </geoLocationBox>
    </geoLocation>
  </geoLocations>
  <relatedIdentifiers>
    <relatedIdentifier relatedIdentifierType="DOI" relationType="IsDocumentedBy">10.5194/essd-15-5153-2023</relatedIdentifier>
    <relatedIdentifier relatedIdentifierType="DOI" relationType="IsNewVersionOf">10.5676/EUM_SAF_CM/CLAAS/V002_01</relatedIdentifier>
    <relatedIdentifier relatedIdentifierType="URL" relationType="IsDerivedFrom">https://user.eumetsat.int/catalogue/EO:EUM:DAT:MSG:HRSEVIRI</relatedIdentifier>
    <relatedIdentifier relatedIdentifierType="DOI" relationType="IsDerivedFrom">10.24381/cds.bd0915c6</relatedIdentifier>
  </relatedIdentifiers>
  <rightsList>
    <rights xml:lang="en" schemeURI="https://spdx.org/licenses/" rightsIdentifierScheme="SPDX" rightsIdentifier="CC-BY-4.0" rightsURI="https://creativecommons.org/licenses/by/4.0/">
      Creative Commons Attribution 4.0 International
    </rights>
  </rightsList>
</resource>
```
