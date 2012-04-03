# This file is part of Elsim
#
# Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
# All rights reserved.
#
# Elsim is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Elsim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Elsim.  If not, see <http://www.gnu.org/licenses/>.


import zlib
from ctypes import cdll, c_float, c_double, c_int, c_uint, c_ulong, c_void_p, Structure, addressof, cast, c_size_t

#struct libsimilarity {
#   void *orig;
#   unsigned int size_orig;
#   void *cmp;
#   unsigned size_cmp;

#   unsigned int *corig;
#   unsigned int *ccmp;
#   
#   float res;
#};
class LIBSIMILARITY_T(Structure) :
    _fields_ = [("orig", c_void_p),
                ("size_orig", c_size_t),
                ("cmp", c_void_p),
                ("size_cmp", c_size_t),

                ("corig", c_size_t),
                ("ccmp", c_size_t),

                ("res", c_float),
               ]

ZLIB_COMPRESS =         0
BZ2_COMPRESS =          1
SMAZ_COMPRESS =         2
LZMA_COMPRESS =         3
XZ_COMPRESS =           4
SNAPPY_COMPRESS =       5
VCBLOCKSORT_COMPRESS =  6
class SIMILARITY :
    def __init__(self, path="./libsimilarity/libsimilarity.so") :
        self._u = cdll.LoadLibrary( path )

        self._u.compress.restype = c_uint
        self._u.ncd.restype = c_int
        self._u.ncs.restype = c_int
        self._u.cmid.restype = c_int
        self._u.entropy.restype = c_double
        self._u.levenshtein.restype = c_uint
        
        self._u.kolmogorov.restype = c_uint
        self._u.bennett.restype = c_double
        self._u.RDTSC.restype = c_double

        self._level = 9

        self.__libsim_t = LIBSIMILARITY_T()

        self.__caches = {
           ZLIB_COMPRESS : {},
           BZ2_COMPRESS : {},
           SMAZ_COMPRESS : {},
           LZMA_COMPRESS : {},
           XZ_COMPRESS : {},
           SNAPPY_COMPRESS : {},
           VCBLOCKSORT_COMPRESS : {},
        }
        
        self.__rcaches = {
           ZLIB_COMPRESS : {},
           BZ2_COMPRESS : {},
           SMAZ_COMPRESS : {},
           LZMA_COMPRESS : {},
           XZ_COMPRESS : {},
           SNAPPY_COMPRESS : {},
           VCBLOCKSORT_COMPRESS : {},
        }
       
        self.__ecaches = {}

        self.set_compress_type( ZLIB_COMPRESS )

    def raz(self) :
        del self._u
        del self.__libsim_t

    def set_level(self, level) :
        self._level = level

    def get_in_caches(self, s) :
        try :
            return self.__caches[ self._type ][ zlib.adler32( s ) ]
        except KeyError :
            return c_size_t( 0 )

    def get_in_rcaches(self, s1, s2) :
        try :
            return self.__rcaches[ self._type ][ zlib.adler32( s1 + s2 ) ]
        except KeyError :
            try :
                return self.__rcaches[ self._type ][ zlib.adler32( s2 + s1 ) ]
            except KeyError :
                return -1, -1

    def add_in_caches(self, s, v) :
        h = zlib.adler32( s )
        if h not in self.__caches[ self._type ] :
            self.__caches[ self._type ][ h ] = v
    
    def add_in_rcaches(self, s, v, r) :
        h = zlib.adler32( s )
        if h not in self.__rcaches[ self._type ] :
            self.__rcaches[ self._type ][ h ] = (v, r)

    def clear_caches(self) :
        for i in self.__caches :
            self.__caches[i] = {}

    def add_in_ecaches(self, s, v, r) :
        h = zlib.adler32( s )
        if h not in self.__ecaches :
            self.__ecaches[ h ] = (v, r)
    
    def get_in_ecaches(self, s1) :
        try :
            return self.__ecaches[ zlib.adler32( s1 ) ]
        except KeyError :
            return -1, -1

    def compress(self, s1) :
        res = self._u.compress( self._level, cast( s1, c_void_p ), len( s1 ) )
        return res

    def _sim(self, s1, s2, func) :
        end, ret = self.get_in_rcaches( s1, s2 )
        if end != -1 :
            return end, ret

        self.__libsim_t.orig = cast( s1, c_void_p )
        self.__libsim_t.size_orig = len(s1)

        self.__libsim_t.cmp = cast( s2, c_void_p )
        self.__libsim_t.size_cmp = len(s2)

        corig = self.get_in_caches(s1)
        ccmp = self.get_in_caches(s2)
        
        self.__libsim_t.corig = addressof( corig )
        self.__libsim_t.ccmp = addressof( ccmp )

        ret = func( self._level, addressof( self.__libsim_t ) )

        self.add_in_caches(s1, corig)
        self.add_in_caches(s2, ccmp)
        self.add_in_rcaches(s1+s2, self.__libsim_t.res, ret)

        return self.__libsim_t.res, ret

    def ncd(self, s1, s2) :
        return self._sim( s1, s2, self._u.ncd )

    def ncs(self, s1, s2) :
        return self._sim( s1, s2, self._u.ncs )

    def cmid(self, s1, s2) :
        return self._sim( s1, s2, self._u.cmid )
    
    def kolmogorov(self, s1) :
        ret = self._u.kolmogorov( self._level, cast( s1, c_void_p ), len( s1 ) )
        return ret, 0
    
    def bennett(self, s1) :
        ret = self._u.bennett( self._level, cast( s1, c_void_p ), len( s1 ) )
        return ret, 0

    def entropy(self, s1) :
        end, ret = self.get_in_ecaches( s1 )
        if end != -1 :
            return end, ret

        res = self._u.entropy( cast( s1, c_void_p ), len( s1 ) )
        self.add_in_ecaches( s1, res, 0 )
        
        return res, 0

    def RDTSC(self) :
        return self._u.RDTSC()

    def levenshtein(self, s1, s2) :
        res = self._u.levenshtein( cast( s1, c_void_p ), len( s1 ), cast( s2, c_void_p ), len( s2 ) )
        return res, 0
    
    def set_compress_type(self, t):
        self._type = t
        self._u.set_compress_type(t)

    def __nb_caches(self, caches) :
        nb = 0
        for i in caches :
            nb += len(caches[i])
        return nb

    def simhash(self, x) :
        import simhash
        return simhash.simhash(x)

    def show(self) :
        print "ECACHES", len(self.__ecaches)
        print "RCACHES", self.__nb_caches( self.__rcaches )
        print "CACHES", self.__nb_caches( self.__caches )

import json
class DBFormat:
    def __init__(self, filename):
        self.filename = filename
       
        self.D = {}

        try :
            fd = open(self.filename, "r")
            self.D = json.load( fd )
            fd.close()
        except IOError :
            pass

        self.H = {}
        for i in self.D :
            self.H[i] = {}
            for j in self.D[i] :
                self.H[i][j] = set()
                for k in self.D[i][j] :
                    self.H[i][j].add( k )

    def add_element(self, name, sname, elem):
        try :
            if elem not in self.D[ name ] :
                self.D[ name ][ sname ].append( elem )
        except KeyError :
            if name not in self.D :
                self.D[ name ] = {}
                self.D[ name ][ sname ] = []
                self.D[ name ][ sname ].append( elem )
            if sname not in self.D[ name ] :
                self.D[ name ][ sname ] = []
                self.D[ name ][ sname ].append( elem )

    def is_present(self, elem) :
        for i in self.D :
            if elem in self.D[i] :
                return True, i
        return False, None

    def elems_are_presents(self, elems) :
        ret = {}
        for i in self.H:
            for j in self.H[i] :
                ret[ j ] = [self.H[i][j].intersection(elems), len(self.H[i][j]), i]
                if ((float(len(ret[j][0]))/(ret[j][1] / 2.0)) * 100) >= 20 :
                #if len(ret[j][0]) >= (ret[j][1] / 2.0) :
                    ret[j].append(True)
                else:
                    ret[j].append(False)

        return ret

    def show(self) :
        for i in self.D :
            print i, ":"
            for j in self.D[i] :
                print "\t", j, len(self.D[i][j])

    def save(self):
        fd = open(self.filename, "w")
        json.dump(self.D, fd)
        fd.close()
