
import os
import Plot_Configs as PC
import Analyzer_Configs as AC
from CMS_style import setTDRStyle
from ROOT import *

#####################################################################

def LoadNtuples(ana_cfg):
    ntuples = {}
    for sample in ana_cfg.samp_names:
        str_125 = '' 
        if sample in ana_cfg.sig_names: str_125 = '125_'
        ntuples[sample] = TChain("tagsDumper/trees/%s_%s13TeV_%s"%(ana_cfg.tree_names[sample], str_125, ana_cfg.channel),"chain_" + sample) 
	ntuples[sample]. Add(ana_cfg.sample_loc + '/%s_2018.root' %ana_cfg.file_names[sample])
    return ntuples


def MakeStack(histos, ana_cfg, var_name):
    stacks = {}
    stacks['all']  = THStack("h_stack_"+var_name, var_name)
    stacks['sig']  = THStack("h_stack_"+var_name, var_name)
    stacks['bkg']  = THStack("h_stack_"+var_name, var_name)

    for sample in ana_cfg.sig_names:
        stacks['sig'].Add(histos[sample])
	stacks['all'].Add(histos[sample])
    for sample in ana_cfg.bkg_names:
        stacks['bkg'].Add(histos[sample])
        stacks['all'].Add(histos[sample])
    return stacks


def CreateCanvas(canv_name):
    canv = TCanvas(canv_name, canv_name, 600,600)
    return canv


def MakeLumiLabel(lumi):
    tex = TLatex()
    tex.SetTextSize(0.035)
    tex.SetTextAlign(31)
    tex.DrawLatexNDC(0.90, 0.91, '%s fb^{-1} (13 TeV)' %lumi)
    return tex


def MakeCMSDASLabel():
    tex = TLatex()
    tex.SetTextSize(0.03)
    tex.DrawLatexNDC(0.15, 0.85, '#scale[1.5]{CMS} work in progress')
    return tex


def ScaleSignal(plt_cfg, stack_sig, var_name):
    sig_hist = stack_sig.GetStack().Last()
    sig_hist.Scale(plt_cfg.sig_scale)
    sig_hist.SetLineColor(kRed)
    sig_hist.SetLineWidth(2)
    sig_hist.SetFillStyle(0)

    sig_hist.GetXaxis().SetTitle(var_name)
    sig_hist.GetXaxis().SetTitleSize(0.20)
    sig_hist.GetYaxis().SetTitle('Events / %.2f' %sig_hist.GetBinWidth(1))
    sig_hist.GetYaxis().SetTitleSize(0.20)
    return sig_hist


def MakeRatioPlot(plt_cfg, h_data, h_MC, var_name):
    ratio_plot = TGraphAsymmErrors()
    ratio_plot.Divide(h_data, h_MC, "pois")
    ratio_plot.SetName("ratiograph_" + var_name)
    ratio_plot.SetMinimum(0.4)
    ratio_plot.SetMaximum(2.0)
    ratio_plot.SetMarkerStyle(20)

    ratio_plot.GetXaxis().SetRangeUser( h_data.GetXaxis().GetXmin(), h_data.GetXaxis().GetXmax() )
    ratio_plot.GetXaxis().SetLabelSize(0.11)
    ratio_plot.GetXaxis().SetTitle(plt_cfg.var_labels[var_name])
    ratio_plot.GetXaxis().SetTitleSize(0.13)
    ratio_plot.GetXaxis().SetTitleOffset(1.2)

    ratio_plot.GetYaxis().SetNdivisions(505)
    ratio_plot.GetYaxis().SetLabelSize(0.11)
    ratio_plot.GetYaxis().SetTitle("data/MC")
    ratio_plot.GetYaxis().SetTitleSize(0.13)
    ratio_plot.GetYaxis().SetTitleOffset(0.4)

    return ratio_plot


def MakeLegend(plt_cfg, histos, scaled_signal):
    gStyle.SetLegendBorderSize(0)
    gStyle.SetLegendTextSize(0.045)
    legend = TLegend(0.43,0.55,0.92,0.9)
    legend.SetNColumns(3)

    legend.AddEntry(histos["data"], "data")
    for sample in plt_cfg.ana_cfg.sig_names:
	legend.AddEntry(histos[sample], sample, 'l')
    legend.AddEntry(scaled_signal, "signal X%d" %plt_cfg.sig_scale)
    for sample in plt_cfg.ana_cfg.bkg_names:
        legend.AddEntry(histos[sample], sample, 'f')
    return legend


def DrawOnCanv(canv, var_name, plt_cfg, stacks, histos, scaled_sig, ratio_plot, legend, lumi_label, cms_label):
    setTDRStyle()
    gStyle.SetLegendBorderSize(0)
    gStyle.SetLegendTextSize(0.045)
    canv.cd()
    upper_pad = TPad("upperpad_"+var_name, "upperpad_"+var_name, 0,0.31, 1,1)
    upper_pad.SetBottomMargin(0.01)
    upper_pad.Draw()
    upper_pad.cd()
    if plt_cfg.logY:
	upper_pad.SetLogy()
	stacks['all'].SetMinimum(1e-2)
        stacks['all'].SetMaximum(1e6)
    stacks['all'].Draw('HIST')
    histos['data'].SetMarkerStyle(20)
    histos['data'].Draw('SAMEPE')
    scaled_sig.Draw('HISTSAME')

    legend.Draw()
    cms_latex = TLatex()
    cms_latex.SetTextAlign(11)
    cms_latex.SetTextSize(0.03)
    cms_latex.DrawLatexNDC(0.15, 0.82, '#scale[2.0]{CMS #bf{#it{preliminary}}}')
    cms_latex.DrawLatexNDC(0.72, 0.94,'#font[42]{#scale[1.7]{%s fb^{-1} (13 TeV)}}' %plt_cfg.lumi) #35.9 41.5 59.7

    canv.cd()
    lower_pad = TPad("lowerpad_"+var_name, "lowerpad_"+var_name, 0, 0.05, 1,0.3)
    lower_pad.SetTopMargin(0.05)
    lower_pad.SetBottomMargin(0.36)
    lower_pad.SetGridy()
    lower_pad.Draw()
    lower_pad.cd()
    ratio_plot.Draw('SAMEAP')


def SaveCanvPic(canv, save_dir, save_name):
    canv.cd()
    #canv.SaveAs(save_dir + '/' + save_name + '.pdf')
    canv.SaveAs(save_dir + '/' + save_name + '.png')





