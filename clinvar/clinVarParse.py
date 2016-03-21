#!/usr/bin/env python
"""
clinVarParse: parse the ClinVar XML file and output the data of interest
"""
import argparse
import clinvar
import codecs
import re
import sys
import xml.etree.ElementTree as ET

def printHeader():
    print("\t".join(("HGVS", "Submitter", "ClinicalSignificance",
                     "DateLastUpdated", "SCV", "Origin", "Method",
                     "Genomic_Coordinate", "Symbol", "Protein")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("clinVarXmlFilename")
    parser.add_argument('-a', "--assembly", default="GRCh38")
    args = parser.parse_args()

    printHeader()


    tree = ET.parse(args.clinVarXmlFilename)
    root = tree.getroot()
    for cvs in root.findall("ClinVarSet"):
        if clinvar.isCurrent(cvs):
            submissionSet = clinvar.clinVarSet(cvs)
            ra = submissionSet.referenceAssertion
            for oa in submissionSet.otherAssertions.values():
                submitter = oa.submitter
                if oa.method != "literature only" or oa.submitter == "Counsyl":
                    if oa.origin != "somatic" and oa.clinicalSignificance != "none provided" and oa.clinicalSignificance != "not provided":
                        variant = ra.variant
                        hgvs = re.sub("\(" + "(BRCA[1|2])" + "\)", 
                                      "", variant.name.split()[0])
                        proteinChange = None
                        if variant.attribute.has_key("HGVS, protein, RefSeq"):
                            proteinChange = variant.attribute["HGVS, protein, RefSeq"]
                        if not re.search("^NP", hgvs):
                            chrom = None
                            start = None
                            referenceAllele = None
                            alternateAllele = None
                            genomicCoordinate = "chrNone:None:None>None"
                            if args.assembly in variant.coordinates:
                                genomicData = variant.coordinates[args.assembly]
                                chrom = genomicData.chrom
                                start = genomicData.start
                                referenceAllele = genomicData.referenceAllele
                                alternateAllele = genomicData.alternateAllele
                                genomicCoordinate = "chr%s:%s:%s>%s" % (chrom,
                                                        start, referenceAllele,
                                                        alternateAllele)
                            print("\t".join((str(hgvs), 
                                             str(oa.submitter), 
                                             str(oa.clinicalSignificance),
                                             str(oa.dateLastUpdated),
                                             str(oa.accession),
                                             str(oa.origin),
                                             str(oa.method),
                                             genomicCoordinate,
                                             str(variant.geneSymbol),
                                             str(proteinChange)
                                         )))
                        

if __name__ == "__main__":
    # execute only if run as a script
    main()
