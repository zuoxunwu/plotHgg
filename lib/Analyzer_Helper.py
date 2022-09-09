
import os
from Plot_Helper import MakeStack
import Plot_Configs as PC
import Analyzer_Configs as AC
from ROOT import *

#####################################################################
class MuPair:
    def __init__(self, vec, idx1, idx2):
	self.dimu_vec = vec
	self.mass     = vec.M()
	self.pt       = vec.Pt()
	self.mu1_idx  = idx1
	self.mu2_idx  = idx2

def DimuCandidates(ntup):
    muPairs = []
    mu1_vec = TLorentzVector(0,0,0,0)
    mu2_vec = TLorentzVector(0,0,0,0)
    for mu_idx1 in range(ntup.nMuons):
	mu1_vec.SetPtEtaPhiM(ntup.muon_pt[mu_idx1], ntup.muon_eta[mu_idx1], ntup.muon_phi[mu_idx1], 0.105658367)
	for mu_idx2 in range(ntup.nMuons):
            if ntup.muon_charge[mu_idx2] != ntup.muon_charge[mu_idx1]:
		mu2_vec.SetPtEtaPhiM(ntup.muon_pt[mu_idx2], ntup.muon_eta[mu_idx2], ntup.muon_phi[mu_idx2], 0.105658367)

		muPair = MuPair(mu1_vec + mu2_vec, mu_idx1, mu_idx2)
	 	muPairs.append(muPair)
    return muPairs



def IsBtagLoose(year, deepCSV):
    if year == '2016' and deepCSV > 0.2217: return True
    if year == '2017' and deepCSV > 0.1522: return True
    if year == '2018' and deepCSV > 0.1241: return True
    return False


def IsBtagMed(year, deepCSV):
    if year == '2016' and deepCSV > 0.6321: return True
    if year == '2017' and deepCSV > 0.4941: return True
    if year == '2018' and deepCSV > 0.4184: return True
    return False

def IsBtagTight(year, deepCSV):
    if year == '2016' and deepCSV > 0.8953: return True
    if year == '2017' and deepCSV > 0.8001: return True
    if year == '2018' and deepCSV > 0.7527: return True
    return False


def CountYield(ana_cfg, histos): # take dimu_mass histos as input
    bin_100 = histos['data'].FindBin(100 + 0.01)
    bin_180 = histos['data'].FindBin(180 - 0.01)
    bin_120 = histos['data'].FindBin(120 + 0.01) 
    bin_130 = histos['data'].FindBin(130 - 0.01) 
    bin_123 = histos['data'].FindBin(123 + 0.01) 
    bin_127 = histos['data'].FindBin(127 - 0.01) 

    stacks = MakeStack(histos, ana_cfg, 'CMS_hgg_mass')
    sum_sig = stacks['sig'].GetStack().Last()
    sum_bkg = stacks['bkg'].GetStack().Last()

    print 'Printing event yield: '
    print 'sample'.ljust(20) + 'in [100, 180]'.ljust(15) + 'in [120, 130]'.ljust(15) + 'in [123, 127]'.ljust(15)
    for sample in ana_cfg.sig_names:
	print sample.ljust(20) + ('%f'%histos[sample].Integral(bin_100, bin_180)).ljust(15) + ('%f'%histos[sample].Integral(bin_120, bin_130)).ljust(15) + ('%f'%histos[sample].Integral(bin_123, bin_127)).ljust(15)
    for sample in ana_cfg.bkg_names:
        print sample.ljust(20) + ('%f'%histos[sample].Integral(bin_100, bin_180)).ljust(15) + ('%f'%histos[sample].Integral(bin_120, bin_130)).ljust(15) + ('%f'%histos[sample].Integral(bin_123, bin_127)).ljust(15)
    print '================================='
    print 'sum_sig'.ljust(20) + ('%f'%sum_sig.Integral(bin_100, bin_180)).ljust(15) + ('%f'%sum_sig.Integral(bin_120, bin_130)).ljust(15) + ('%f'%sum_sig.Integral(bin_123, bin_127)).ljust(15)
    print 'sum_bkg'.ljust(20) + ('%f'%sum_bkg.Integral(bin_100, bin_180)).ljust(15) + ('%f'%sum_bkg.Integral(bin_120, bin_130)).ljust(15) + ('%f'%sum_bkg.Integral(bin_123, bin_127)).ljust(15)

    print 'Data'.ljust(20) + ('%f'%histos['data'].Integral(bin_100, bin_180)).ljust(15) + ('%f'%histos['data'].Integral(bin_120, bin_130)).ljust(15) + ('%f'%histos['data'].Integral(bin_123, bin_127)).ljust(15)

    print '====================='
    print 'W+-'.ljust(20) + '%f'%( (histos['WplusH'].Integral(bin_100, bin_180) + histos['WminusH'].Integral(bin_100, bin_180))/sum_sig.Integral(bin_100, bin_180) )
    for sample in ana_cfg.sig_names:
        print sample.ljust(20) + '%f'%(histos[sample].Integral(bin_100, bin_180)/sum_sig.Integral(bin_100, bin_180))
#    print 'S/(S+B)'.ljust(20) + '%f'%(sum_sig.Integral(bin_123, bin_127)/(sum_sig.Integral(bin_123, bin_127)+sum_bkg.Integral(bin_123, bin_127)))
    # Do not rely on bkg MC in small window, estimate as a ratio to full window (based on inclusive selection)
    print 'S/(S+B)'.ljust(20) + '%f'%(sum_sig.Integral(bin_123, bin_127)/(sum_sig.Integral(bin_123, bin_127)+ 0.0875 * sum_bkg.Integral(bin_100, bin_180)))
    print 'W+/W-'.ljust(20) + '%f'%(histos['WplusH'].Integral(bin_100, bin_180)/histos['WminusH'].Integral(bin_100, bin_180))


