##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class JsonFortran(CMakePackage):
    """A user-friendly, thread-safe, and object-oriented API for reading
    and writing JSON files, written in modern Fortran.
    """
    
    homepage = "https://http://jacobwilliams.github.io/json-fortran/"
    url      = "https://github.com/jacobwilliams/json-fortran/archive/"\
               "5.1.0.tar.gz"

    version('5.1.0', 'a30be27269116892e6a99a30fe237a56')
    version('5.0.2', 'bc7fd206c9dc2b562ba86bab78669f07')
    version('5.0.1', 'ec0835d7aacc222c02e1fdd32bdfb01f')
    version('5.0.0', '6d1c67081e4d9323d4dd3d6ead493e6a')
    version('4.3.0', '95fbce7955b5de78c45ce66c044a7bac')
    version('4.2.0', '955ebadd204552119355650743b2d420')
    version('4.1.1', 'e8009616a42a9cce63bfeb8151b391c0')
    version('4.1.0', '4423733bca80d67a107ea6e23fb65455')
    version('4.0.0', '29b35cc0482aefa8dbc59610b5f29d86')
    version('3.1.0', '0c9d977023570533e4e1c36f9fac2235')

    variant('unicode', default=True,
            description='Build json-fortran to support unicode text in '\
            'json objects and files')

    # FIXME: Add additional dependencies if required.
    depends_on('cmake@2.8.8:', type='build')

    def cmake_args(self):
        spec = self.spec
        args = ["-DUSE_GNU_INSTALL_CONVENTION:BOOL=TRUE",
                "-DSKIP_DOC_GEN:BOOL=TRUE"]
        if 'unicode' in spec: args.append("-DENABLE_UNICODE:BOOL=TRUE")
        return args
