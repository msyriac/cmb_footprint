import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

#import pylab as pl
import healpy as hp

from cmb_footprint import footprint
import astropy.table as t

if __name__ == '__main__':


    #fp = footprint.SurveyStack('PLANCK-DUSTPOL', projection='mollweide', coord_plot='C', rot=[0,0],
    #                           config='footprint_hsc.cfg')
    fp = footprint.SurveyStack('PLANCK-DUSTPOL', projection='mollweide', coord_plot='C', rot=[-90,0],
                               config='footprint_hsc.cfg')

    cmass = hp.read_map('/astro/astronfs01/workarea/msyriac/maps/archived/DR12N1024_nocfhtwts_spec_hp_ct_noMagCut_zFrom0.43To0.7.fits')
    fp.superimpose_hpxmap(cmass,label='BOSS',color='deeppink', coord_in='G')
    
    d56 = hp.read_map('/gpfs01/astro/www/msyriac/d56_healpix.fits')
    fp.superimpose_hpxmap(d56,label='ACT-D56',color='green')
    

    d5 = hp.read_map('/gpfs01/astro/www/msyriac/d5_healpix.fits')
    fp.superimpose_hpxmap(d5,label='ACT-D5',color='cyan')
    
    d6 = hp.read_map('/gpfs01/astro/www/msyriac/d6_healpix.fits')
    fp.superimpose_hpxmap(d6,label='ACT-D6',color='orange')
    
    bossn = hp.read_map('/gpfs01/astro/www/msyriac/bossn_healpix.fits')
    fp.superimpose_hpxmap(bossn,label='ACT-BOSSN',color='mediumpurple')
    FDFC = hp.read_map('/astro/astronfs01/workarea/msyriac/hscxact/s16A/S16A_wide2_fdfc_i_limitmag_hp.fits')
    fp.superimpose_hpxmap(FDFC,label='HSC-FDFC',color='red')
    fp.superimpose_survey_outline('HSC',color='lightsalmon',label='HSC-planned')
    fp.superimpose_survey_outline('POLARBEAR',color='blue',label='PB')
        
    pl.savefig('act_hsc_pbear_footprint.pdf')
    #pl.show()
