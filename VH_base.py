####################################################
####################################################

import os
import sys

sys.path.insert(0, '%s/lib' % os.getcwd())
from ROOT import *
from Plot_Helper import LoadNtuples, MakeStack, CreateCanvas, DrawOnCanv, SaveCanvPic, MakeLumiLabel, MakeCMSDASLabel, ScaleSignal, MakeRatioPlot, MakeLegend
from Analyzer_Helper import MuPair, DimuCandidates, IsBtagLoose, IsBtagMed, IsBtagTight, CountYield
import Analyzer_Configs as AC
import Plot_Configs     as PC

gROOT.SetBatch(True)


def main():
    out_name = "VH_exercise_out.root"    
    if not os.path.exists('plots'):
	os.makedirs('plots')
    out_file = TFile( "plots/" + out_name , "RECREATE")

    analyzer_cfg = AC.Analyzer_Config('WHLeptonicTag')
    analyzer_cfg.Print_Config()
    ntuples = LoadNtuples(analyzer_cfg)


    var_names = ['CMS_hgg_mass', 'whmva']#, 'dipho_sumpt', 'dipho_leadE', 'dipho_leadEta', 'dipho_subleadE', 'dipho_subleadEta',
                # 'nele', 'lep_Charge', 'lep_Pt', 'lep_Eta', 'met_Pt']
    plot_cfg = PC.Plot_Config(analyzer_cfg)

    histos = {}
    for var_name in var_names:
        histos[var_name] = {}
    for sample in analyzer_cfg.samp_names:
	ntup = ntuples[sample] # just a short name
	print '\n\nOn sample: %s' %sample
        print 'total events: %d' %ntup.GetEntries()

        for var in var_names:
          if ntup.GetEntries() == 0:
            if var == 'CMS_hgg_mass': histos[var][sample] = TH1D('%s_%s'%(var, sample), '', 40, 100, 180)
            if var == 'whmva':        histos[var][sample] = TH1D('%s_%s'%(var, sample), '', 40,  -1,   1)
          else:
            wgt_str = "weight * " + plot_cfg.lumi
            VH_hasZ = '* 1.0'
            blind_str = '* (CMS_hgg_mass < 120 || CMS_hgg_mass > 130)'
            file_wgt = '* %f'%analyzer_cfg.file_wgts[sample]
            if sample == 'data': wgt_str = '1.0'
            if sample == 'WminusH': wgt_str += '* 0.5328 / 0.6865'
            if sample == 'WplusH':  wgt_str += '* 0.8400 / 0.6865'
            if sample == 'ZH': VH_hasZ = '* hasZ'
            if sample in analyzer_cfg.sig_names: blind_str = '* 1.0'
            final_wgt = wgt_str + VH_hasZ + blind_str + file_wgt

            if var == 'CMS_hgg_mass':  ntup.Draw("%s >> %s_%s(40,100,180)"%(var, var, sample), final_wgt)            
            elif var == 'whmva':       ntup.Draw("%s >> %s_%s(40, -1,  1)"%(var, var, sample), final_wgt)
            else: print 'invalid var name'

            histos[var][sample] = gDirectory.Get('%s_%s'%(var, sample))
            histos[var][sample]. SetDirectory(0)



    out_file.cd()
    for var_name in var_names:
        for sample in analyzer_cfg.samp_names:
	    plot_cfg.SetHistStyles(histos[var_name][sample], sample)
            histos[var_name][sample].Write()

    lumi_label = MakeLumiLabel(plot_cfg.lumi)
    cms_label  = MakeCMSDASLabel()

    for var_name in var_names:
	stacks = MakeStack(histos[var_name], analyzer_cfg, var_name)
	scaled_sig = ScaleSignal(plot_cfg, stacks['sig'], var_name)
	ratio_plot = MakeRatioPlot(plot_cfg, histos[var_name]['data'], stacks['all'].GetStack().Last(), var_name)
	legend = MakeLegend(plot_cfg, histos[var_name], scaled_sig)

 	canv = CreateCanvas(var_name)
	DrawOnCanv(canv, var_name, plot_cfg, stacks, histos[var_name], scaled_sig, ratio_plot, legend, lumi_label, cms_label)
	canv.Write()
        SaveCanvPic(canv, 'plots', analyzer_cfg.channel + '_' + var_name)

    print '\n\n'
    CountYield(analyzer_cfg, histos['CMS_hgg_mass'])
    out_file.Close()

main()











	
