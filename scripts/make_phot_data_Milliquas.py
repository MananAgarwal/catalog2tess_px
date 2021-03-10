#!/usr/bin/env python

import scipy as sp
import os
import sys
sys.path.insert(0, os.path.abspath(   os.path.dirname(__file__)) + '/..') 
import argparse
from catalogs.MilliquasCsv import MilliquasCsv


def get_inputs(args):
    parser = argparse.ArgumentParser(
        description="Specify Sector, Camera/CCD, and time range, and make a phot.data file for DIA photometry.")
    parser.add_argument('--cam', type=int, nargs="*",  help="Camera Number (1--4)")
    parser.add_argument('--ccd', type=int, nargs="*",   help="CCD Number (1--4)")
    parser.add_argument('--sector', type=int, nargs="*", help="Sector Number (for start/stop time")
    parser.add_argument('--mag', type=float, default=20.0, help="Magnitude limit: collect all sources brighter than this value (default = 20)")
    parser.add_argument('--outdir',default='./', help="Output directory stem: phot.data appears in subdirs sectorP/camN_ccdM")
    parser.add_argument('--doall', action='store_true', help="If set, do all cams and CCDs in the sectors")
    parser.add_argument('--savecoords', action='store_true', help="If set, save ra/dec of targets on the ccd")
    # arguments needed?

    return parser.parse_args()


def main():

    args = get_inputs(sys.argv[1:])
    if args.doall:
        cam_use = [1,2,3,4]
        ccd_use = [1,2,3,4]
    else:
        cam_use = args.cam
        ccd_use = args.ccd
    for sector in args.sector:        
        for cam in cam_use:
            for ccd in ccd_use:
                #find the catalog file
                
                path1 = os.path.abspath(__file__)
                path2 = os.path.split(path1)
                path3 = os.path.split(path2[0])
                pathfinal = path3[0] + "/Milliquas/"

                catfile = 's{s_use:02d}/milliquas_s{s_use:02d}_cam{cam:d}.txt'.format(
                    s_use = sector,
                    cam   = cam )
                catfile = os.path.join(pathfinal, catfile)

                #instantiate the catalog object
                cat = MilliquasCsv(catfile)
                
                
                #select the masks
                mag_mask  = cat.rmag < args.mag
                ccd_mask  = cat.ccd == ccd

                mask = mag_mask & ccd_mask
                
                l2 = sp.array([i.replace(' ', '_') for i in cat.name])

                #make the file
                outdir = os.path.join(args.outdir,'sector{:02d}'.format(sector),'cam'+str(cam)+'_ccd'+str(ccd))
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)
                cat.make_phot_data(cat.ccdcol[mask],
                                   cat.ccdrow[mask],
                                   l2[mask],
                                   outdir )

                if args.savecoords:                                                       
                    with open('milliquas_save.txt', 'a') as fout:                              
                        for ii in range(len(cat.name[mask])):                        
                            fout.write('{:15.8f} {:15.8f}\n'.format(cat.ra[mask][ii], cat.dec[mask][ii])) 

if __name__ == '__main__':
    main()

