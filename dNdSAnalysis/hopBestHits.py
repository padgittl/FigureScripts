import sys,re,os
from Bio import SeqIO
from Bio.Seq import Seq
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

###############
# SUBROUTINES #
###############

def readBlastpOutputFile_gene_vs_uniprot(pepBlastpOutputFile1,eValueThreshold):
    bestHits_gene_vs_uniprot = {}
    lowestEValue = {}
    bestScore = {}
    bestQueryCov = {}
    bestPercIden = {}
    with open(pepBlastpOutputFile1,'r') as BF1:
        for line in BF1:
            # 001620F.g33.t1  sp|O80438|MAK3_ARATH    74.444  180     46      0       17      196     11      190     6.62e-100       287     88
            geneID,fullUniprotID,pIdent,length,mismatch,gapOpen,qStart,qEnd,sStart,sEnd,eValue,bitScore,queryCov = line.strip().split("\t")
            eValue = float(eValue)
            bitScore = float(bitScore)
            queryCov = int(queryCov)
            extractUniprotID = re.search('sp\|(.+)\|',fullUniprotID)
            uniprotID = extractUniprotID.group(1)
            if eValue < eValueThreshold:
                if geneID in bestHits_gene_vs_uniprot:
                    if bestScore[geneID] < bitScore:
                        bestScore[geneID] = bitScore
                        bestHits_gene_vs_uniprot[geneID] = (uniprotID,pIdent,eValue,bitScore,queryCov)
                else:
                    bestScore[geneID] = bitScore
                    bestHits_gene_vs_uniprot[geneID] = (uniprotID,pIdent,eValue,bitScore,queryCov)
    return(bestHits_gene_vs_uniprot)

def readBlastpOutputFile_uniprot_vs_gene(pepBlastpOutputFile2,eValueThreshold):
    bestHits_uniprot_vs_gene = {}
    lowestEValue = {}
    bestScore = {}
    bestQueryCov = {}
    bestPercIden = {}
    with open(pepBlastpOutputFile2,'r') as BF2:
        for line in BF2:
            fullUniprotID,geneID,pIdent,length,mismatch,gapOpen,qStart,qEnd,sStart,sEnd,eValue,bitScore,queryCov = line.strip().split("\t")
            eValue = float(eValue)
            bitScore = float(bitScore)
            queryCov = int(queryCov)
            extractUniprotID = re.search('sp\|(.+)\|',fullUniprotID)
            uniprotID = extractUniprotID.group(1)
            if eValue < eValueThreshold:
                if geneID in bestHits_uniprot_vs_gene:
                    if bestScore[geneID] < bitScore:
                        bestScore[geneID] = bitScore
                        bestHits_uniprot_vs_gene[geneID] = (uniprotID,pIdent,eValue,bitScore,queryCov)
                else:
                    bestScore[geneID] = bitScore
                    bestHits_uniprot_vs_gene[geneID] = (uniprotID,pIdent,eValue,bitScore,queryCov)
    return(bestHits_uniprot_vs_gene)

########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <blastp output file 1> <blastp output file 2> \n"
if len(sys.argv) != 3:
    print usage
    sys.exit()

pepBlastpOutputFile1 = sys.argv[1]
pepBlastpOutputFile2 = sys.argv[2]

eValueThreshold = 1e-5

bestHits_hop_vs_uniprot = readBlastpOutputFile_gene_vs_uniprot(pepBlastpOutputFile1,eValueThreshold)
bestHits_uniprot_vs_hop = readBlastpOutputFile_uniprot_vs_gene(pepBlastpOutputFile2,eValueThreshold)

for hopGene1 in bestHits_hop_vs_uniprot:
    hUniprotID1,hPIdent1,hEValue1,hBitScore1,hQueryCov1 = bestHits_hop_vs_uniprot[hopGene1]
    print("%s\t%s\t%s\t%s\t%s\t%s\t" % (hopGene1,hUniprotID1,hPIdent1,hEValue1,hBitScore1,hQueryCov1))

for hopGene2 in bestHits_uniprot_vs_hop:
    hUniprotID2,hPIdent2,hEValue2,hBitScore2,hQueryCov2 = bestHits_uniprot_vs_hop[hopGene2]
    print("%s\t%s\t%s\t%s\t%s\t%s\t" % (hopGene2,hUniprotID2,hPIdent2,hEValue2,hBitScore2,hQueryCov2))



