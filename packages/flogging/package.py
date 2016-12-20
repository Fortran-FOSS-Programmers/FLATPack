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


class Flogging(Package):
    """Flogging provides an easy-to-use interface for logging events and
    errors in Fortran applications and libraries. Its use and
    functionality is similar to that of logging library in Python. It
    is meant to be used for providing warnings, error messages, debug
    information, or routine output which should be logged. It is not
    ideal for all output, such as that used to prompt the user for
    input.
    """

    homepage = "https://cmacmackin.github.io/flogging/"
    url      = "https://github.com/cmacmackin/flogging/archive/v1.0.0.tar.gz"

    version('1.0.0', 'e81ad12a45a6af8c1e673ab97956e27f')
    
    depends_on('face')
    depends_on('py-fobis-py', type='build')

    variant('shared', default=True, description='Build shared libraries')
    variant('static', default=True, description='Build static library')

    def install(self, spec, prefix):
        fobis = which('FoBiS.py')
        mkdirp(prefix.lib, prefix.include)
        if spec.satisfies('%gcc'):
            compiler = 'gnu'
        elif spec.satisfies('%intel'):
            compiler = 'intel'
        
        if spec.satisfies('+shared'):
            fobis('build', '-mode', '{}-shared'.format(compiler))
            install(join_path('build', 'libflogging.so'), prefix.lib)
        if spec.satisfies('+static'):
            fobis('build', '-mode', '{}-static'.format(compiler))
            install(join_path('build', 'libflogging.a'), prefix.lib)

        if spec.satisfies('+shared') or spec.satisfies('+static'):
            install(join_path('build', 'include', 'logger_mod.mod'),
                    prefix.include)
