import numpy as np
import pylab as pl
import healpy as H
import matplotlib.cm as cm
import pyfits
from astropy import wcs
import scipy.sparse

class SurveyStack(object):

	def __init__(self,background,xsize=800,nside=None,fignum=None):
		self.xsize = xsize
		self.fn_background = background
		self.fig = pl.figure(fignum)

		maps = H.read_map(background,field=(1,2)) #Q,U should be fields 1 and 2. Background should be a Healpix map

		if nside is None:
			nside = H.npix2nside(len(maps[0]))

		self.nside = nside

		polamp = np.sqrt(maps[0]**2 + maps[1]**2)

		map2d = project_healpix_mollview(polamp,coord=['G','C'])

		vmax_val = 0.80*np.max(map2d)

		pl.imshow(map2d,cmap=cm.Greys,vmin=0.0,vmax=0.001,origin='lower')


	def superimpose(self,fns,color='red'):
		'''Superimpose the footprint of an experiment on the background image. Can be a single fits file or a list of them that will 
		be added together'''

		#Determine type of map. Most likely flat sky map
		if type(fns) is list:
			fn0 = fns[0]			
		else:
			fn0 = fns
			fns = [fns]

		hdulist = pyfits.open(fn0)
		hdulist.close()

		hpx_map = np.zeros(H.nside2npix(self.nside))
		for fn in fns:
			hdulist = pyfits.open(fn)
			hpx_map += wcs_to_healpix(hdulist,self.nside)
			hdulist.close()

		hpx_map_2d = project_healpix_mollview(hpx_map)
		
		hpx_map_2d[hpx_map_2d == 0] = np.NaN

		if color == 'red':
			color_val = 255.0
		elif color == 'blue':
			color_val = 0.0

		hpx_map_2d[np.isfinite(hpx_map_2d)] = color_val

		pl.figure(self.fig.number) #probably a better way to do this
		pl.imshow(hpx_map_2d,alpha=0.5,origin='lower',vmin=0.0,vmax=255.0) #need to work on color. Possible just figure out values for the colormap

def project_healpix_mollview(mapinp,coord=None):

	#Change this to the minimal function calls needed to get the projection

	map2d = H.mollview(mapinp,xsize=1600,coord=coord,return_projected_map=True)
	pl.close()

	return map2d

def wcs_to_healpix(hdulist,nside):
	'''Converts data in an opened FITS file from a generic WCS to Healpix'''
	
	#use wcs_pix2world to get ra/dec coordinates, then use ang2pix to get Healpix coordinates and 
	#sum over all pixels with the same Healpix pixel numer

	w = wcs.WCS(hdulist[0].header)

	data = hdulist[0].data

	xsize, ysize = data.shape
	print "x/ysize = ", xsize, ysize

	pixcrd = [(x,y) for x in xrange(xsize) for y in xrange(ysize)]

	print "np.array"
	pixcrd2 = np.array(pixcrd)

	#pix2world to get ra/dec values of each pixel
	print "wcs_pix2world"
	world = w.wcs_pix2world(pixcrd,1)

	idx = np.isfinite(world[:,0])

	pixcrd2 = pixcrd2[idx,:]
	world = world[idx,:]

	#Use Healpy to do ang2pix for Healpix pixel numbers
	theta = np.radians(world[:,0])
	phi = -np.radians(world[:,1]) #CHECK SIGN
	print "ang2pix"
	pixnum = H.ang2pix(nside,theta,phi)
	

	print "hpx_data"
	npix = H.nside2npix(nside)
	row = pixnum
	col = np.zeros_like(row)

	#coo_matrix will sum entries that have multiple elements
	hpx_data = scipy.sparse.coo_matrix((data[(pixcrd2[:,0],pixcrd2[:,1])], (row, col)), shape=np.array([npix,1])).A.transpose()
	hpx_data.shape = (npix)

	return hpx_data

if __name__=='__main__':
	
	fn_background = 'maps/Planck/HFI_SkyMap_353_2048_R2.00_full.fits'
	
	footprint = SurveyStack(fn_background,fignum=1)
	
	fn_148_south_s2 = 'maps/ACT/ACT_148_south_season_2_1way_hits_v3.fits'
	fn_148_equ_s3 = 'maps/ACT/ACT_148_equ_season_3_1way_hits_v3.fits'
	fn_148_south_s3 = 'maps/ACT/ACT_148_south_season_3_1way_hits_v3.fits'
	fn_148_equ_s4 = 'maps/ACT/ACT_148_equ_season_4_1way_hits_v3.fits'
	fn_148_south_s4 = 'maps/ACT/ACT_148_south_season_4_1way_hits_v3.fits'

	fn_220_equ_s4 = 'maps/ACT/ACT_220_equ_season_4_1way_hits_v3.fits'
	fn_220_south_s4 = 'maps/ACT/ACT_220_south_season_4_1way_hits_v3.fits'

	fns_ACT = [fn_148_equ_s4,fn_148_south_s4,fn_148_equ_s3,fn_148_south_s3,fn_148_south_s2]

	footprint.superimpose(fns_ACT,color='red')

	pl.show()
