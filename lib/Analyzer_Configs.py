import os
import sys
from ROOT import *


class Analyzer_Config:
  
    def __init__(self, channel):
	self.channel    = channel
	self.sample_loc = 'NONE'
	self.sig_names  = []
	self.bkg_names  = []
 	self.samp_names = []
        self.tree_names = {}
        self.file_names = {}
        self.file_wgts  = {}

	self.Config_Analyzer()

    def Config_Analyzer(self):
	if self.channel == 'inclusive' or 'WHLeptonicTag' in self.channel:
	    self.sample_loc = '/eos/cms/store/user/xzuo/Hgamgam/run2/WHLeptonic_full/hadd'
            self.sig_names = ['ggZH', 'ZH', 'ttH', 'WminusH', 'WplusH']
            self.bkg_names = ['QCD', 
                              'ttdiphot', 'ttphot', 'ttZ', 'ttW', 'tt', 'tW_top', 'tW_antitop',
                              'photj', 'diphot', 'WW', 'WZ', 'ZZ', 'DY',
                              'Wphot', 'Zphot', 'tphot']
            self.samp_names = self.sig_names + self.bkg_names + ['data']
	    self.tree_names = {'ttH': 'tth', 'ggZH': 'ggzh', 'ZH': 'vh', 'WminusH': 'whneg', 'WplusH': 'whpos',
	                       'DY': 'DY_amc', 'QCD': 'QCD',
                               'photj': 'phot_j', 'diphot': 'diphot_j',
                               'Wphot': 'Wphot', 'Zphot': 'Zphot', 'tphot': 'tphot', 
                               'WW': 'WW', 'WZ': 'WZ', 'ZZ': 'ZZ', 
                               'tW_top': 'tW_top', 'tW_antitop': 'tW_antitop',
                               'tt': 'tt_amc', 'ttW': 'ttW', 'ttZ': 'ttZ', 'ttphot': 'tt_phot',
                               'ttdiphot': 'tt_diphot',
                               'data': 'Data'}

            self.file_names = {'ttH': 'ttH', 'ggZH': 'ggZH', 'ZH': 'VH_9of10', 'WminusH': 'WminusH', 'WplusH': 'WplusH',
                               'DY': 'DY', 'QCD': 'QCD',
                               'photj': 'photj', 'diphot': 'diphot_93of100',
                               'Wphot': 'Wphot_69of100',  'Zphot': 'Zphot_91of100', 'tphot': 'tphot_78of100',
                               'WW': 'WW_90of100', 'WZ': 'WZ_97of100', 'ZZ': 'ZZ_93of100',
                               'tW_top': 'tW_top_82of100', 'tW_antitop': 'tW_antitop_96of100',
                               'tt': 'tt_24of100', 'ttW': 'ttW_5of10', 'ttZ': 'ttZ_1of10', 'ttphot': 'ttphot_97of100',
                               'ttdiphot': 'ttdiphot_9of10',
                               'data': 'data'}
            for samp in self.samp_names:
              self.file_wgts[samp] = 1.0     
            self.file_wgts['VH'] = 1.0/0.9
            self.file_wgts['diphot'] = 1.0/0.93
            self.file_wgts['Wphot'] = 1.0/0.69
            self.file_wgts['Zphot'] = 1.0/0.91
            self.file_wgts['tphot'] = 1.0/0.78
            self.file_wgts['WW'] = 1.0/0.9
            self.file_wgts['WZ'] = 1.0/0.97
            self.file_wgts['ZZ'] = 1.0/0.93
            self.file_wgts['tW_top'] = 1.0/0.82
            self.file_wgts['tW_antitop'] = 1.0/0.96
            self.file_wgts['tt'] = 1.0/0.24
            self.file_wgts['ttW'] = 1.0/0.5
            self.file_wgts['ttZ'] = 1.0/0.1
            self.file_wgts['ttphot'] = 1.0/0.97
            self.file_wgts['ttdiphot'] = 1.0/0.9
            
	else:
	    print "channel is invalid: channel = %s" %self.channel
	    sys.exit()


    def Print_Config(self):
	print 'Running analysis in channel: %s' %self.channel
	print 'getting ntuples from: %s' %self.sample_loc
	print 'using signals: '	
	print self.sig_names
	print 'using backgrounds:'
	print self.bkg_names


