ref_samps = ['diphot', 'DY', 'phot_j', 'ttX', 't_phot', 'tW', 'ttV', 'Wphot', 'Zphot', 'VV', 'total', 'data']

ref_table = {'diphot':  668.4,
             'DY'    :  833.5,
             'phot_j':  688.4,
             'ttX'   :  524.0,
             't_phot':   37.7,
             'tW'    :   31.8,
             'ttV'   :    3.2,
             'Wphot' : 1250.6,
             'Zphot' : 1274.2,
             'VV'    :   53.5,
             'total' : 5367.2,
             'data'  : 5933.0
            }

rep_table = {'tt_diphot' :    7.01,
             'tt_phot'   :  102.19,
             'ttZ'       :    0.66,
             'ttW'       :    0.83,
             'tt'        :  172.19,
             'tW_top'    :    8.79,
             'tW_antitop':   11.14,
             'WW'        :   20.78,
             'WZ'        :    8.27,
             'ZZ'        :    5.33,
             'DY'        :  546.22,
             't_phot'    :    8.07,
             'Wphot'    :  606.76,
             'Zphot'    :  685.07,
             'phot_j'    :  181.85,
             'diphot'    :  236.39, 
             'total'     : 2601.88,
             'data'      : 2749.0
            }


rep_table['tW'] = rep_table['tW_top'] + rep_table['tW_antitop']
rep_table['VV'] = rep_table['WW'] + rep_table['WZ'] + rep_table['ZZ']
rep_table['ttV'] = rep_table['ttW'] + rep_table['ttZ']
rep_table['ttX'] = rep_table['tt'] + rep_table['tt_phot'] + rep_table['tt_diphot']


print 'process'.ljust(15) + 'ref_yield'.ljust(15) + 'rep_yield'.ljust(15) + 'ratio'.ljust(15)
for samp in ref_samps:
  print samp.ljust(15) + ('%f'%ref_table[samp]).ljust(15) + ('%f'%rep_table[samp]).ljust(15) + ('%f'%(rep_table[samp]/ref_table[samp]/59.7*137))
