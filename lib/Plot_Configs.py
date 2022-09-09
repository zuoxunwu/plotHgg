import os
import sys
import Analyzer_Configs as AC
from ROOT import *

class Plot_Config:

    def __init__(self, ana_cfg):
	self.ana_cfg = ana_cfg
	self.colors     = {}
        self.var_labels = {}
	self.logY       = True
	self.lumi       = '59.7'
	self.sig_scale  = 100 

	self.LoadColors()
        self.LoadLabels()

    def LoadColors(self):
	self.colors["Data"] = kBlack

        self.colors["ttH"]     = kRed + 2
        self.colors["ZH"]      = kBlue - 6
        self.colors["ggZH"]    = kBlue + 2
        self.colors["WplusH"]  = kGreen + 1
        self.colors["WminusH"] = kGreen -2

	# trying to use blue for Z, green for W, yellow for top, red for g/q
        self.colors["DY"]  = kAzure + 7
        self.colors["QCD"] = kAzure - 9
 
	self.colors["photj"]  = kYellow - 8
        self.colors["diphot"] = kYellow - 9

        self.colors["Wphot"] = kTeal + 2
        self.colors["Zphot"] = kTeal + 6
        self.colors["tphot"] = kSpring + 3

	self.colors["WW"] = kBlue + 1
        self.colors["WZ"] = kBlue - 4
	self.colors["ZZ"] = kBlue - 9

        self.colors["tW_top"]      = kMagenta - 4
        self.colors["tW_antitop"]  = kMagenta - 7

        self.colors["tt"]       = kRed - 5
        self.colors["ttW"]      = kMagenta - 1
        self.colors["ttZ"]      = kMagenta - 5
        self.colors["ttphot"]   = kRed - 10
        self.colors["ttdiphot"] = kOrange - 9

    def LoadLabels(self):
        self.var_labels['CMS_hgg_mass'] = 'm(\gamma\gamma)'
        self.var_labels['whmva']        = 'MVA score'
        self.var_labels['dipho_sumpt']  = 'p_{T}(\gamma\gamma)'
        self.var_labels['dipho_lead_ptoM']     = 'p_{T}(\gamma_{1})/m(\gamma\gamma)'
        self.var_labels['dipho_sublead_ptoM']  = 'p_{T}(\gamma_{2})/m(\gamma\gamma)'
        self.var_labels['dipho_leadEta']       = '\eta(\gamma_{1})'
        self.var_labels['dipho_subleadEta']    = '\eta(\gamma_{2})'
        self.var_labels['CosPhi']       = 'cos(\Delta\phi(\gamma\gamma))'

    def SetHistStyles(self, hist, sample):
	if sample == 'data':
	    hist.SetMarkerStyle(20)
	elif sample in self.ana_cfg.sig_names:
	    hist.SetLineColor(self.colors[sample])
	    hist.SetLineWidth(2)
	    hist.SetFillColor(kGray)
	elif sample in self.ana_cfg.bkg_names:
	    hist.SetFillColor(self.colors[sample])

	
