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


class Lapack95(Package):
    """LAPACK95 is a Fortran95 interface to LAPACK."""

    homepage = "http://www.netlib.org/lapack95/index.html"
    url      = "http://www.netlib.org/lapack95/lapack95.tgz"

    version('1.0', 'a49ac8f061d7cd429e5279e69bbe334d',
            url='http://www.netlib.org/lapack95/lapack95.tgz')

    variant('shared', default=True, description='Build shared libraries')
    variant('static', default=True, description='Build static library')

    depends_on('blas')
    depends_on('lapack')

    parallel = False

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        if spec.satisfies('%gcc'):
            cflags = '-O3'
            lflags = '-O3'
            free_flag = '-ffree-form'
            fixed_flag = '-ffixed-form'
            shared_cflag = ' -fPIC'
            shared_lflag = ' -shared'
        elif spec.satisfies('%intel'):
            cflags = '-fast'
            lflags = '-fast'
            free_flag = '-free'
            fixed_flag = '-fixed'
            shared_cflag = ' -fpic'
            shared_lflag = ' -shared'
        else:
            raise InstallError("Unsported compiler. Why don't you add "\
                               "support for it?")

        filter_file(r'FC\s*= f95 -free',
                    'FC = {} {}'.format(self.compiler.fc, free_flag),
                    'make.inc')
        filter_file(r'FC1\s*= f95 -fixed',
                    'FC1 = {} {}'.format(self.compiler.fc, fixed_flag),
                    'make.inc')
        linalg = spec['lapack'].lapack_libs + spec['blas'].blas_libs
        filter_file(r'LIBS\s*=.*',
                    'LIBS = {}'.format(linalg.ld_flags),
                    'make.inc')
        
        mkdirp(prefix.lib, prefix.include)
        mkdirp('lapack95_modules')

        if spec.satisfies('+static'):
            filter_file(r'OPTS0\s*=.*',
                        'OPTS0 = {}'.format(cflags), 'make.inc')
            make('-C', 'SRC', 'single_double_complex_dcomplex')
            fc = which('fc')
            install('lapack95.a', join_path(prefix.lib, 'liblapack95.a'))

        if spec.satisfies('+shared'):
            filter_file(r'OPTS0\s*=.*',
                        'OPTS0 = {}'.format(cflags+shared_cflag),
                        'make.inc')
            filter_file(r'la_\wlagge\.o', '', join_path('SRC', 'makefile'))
            libname = 'liblapack95.so'
            soname = libname + '.' + spec.version.up_to(1)
            filename = libname + '.' + spec.version.dotted
            link = r'\1$(FC) {} -o ../{} \2 {} -Wl,--no-undefined '\
                   '-Wl,-soname,{}'
            link = link.format(lflags+shared_lflag, filename,
                               linalg.ld_flags, soname)
            filter_file(r'(\s*)ar cr \.\./lapack95\.a (.*)', link,
                        join_path('SRC', 'makefile'))
            filter_file(r'\s*ranlib .*', '', join_path('SRC', 'makefile'))
            make('-C', 'SRC', 'clean')
            make('-C', 'SRC', 'single_double_complex_dcomplex')
            install(filename, prefix.lib)
            with working_dir(prefix.lib):
                ln = which('ln')
                ln('-s', filename, soname)
                ln('-s', soname, libname)

        if spec.satisfies('+shared') or spec.satisfies('+static'):
            install(join_path('lapack95_modules', 'f95_lapack.mod'),
                    prefix.include)
            install(join_path('lapack95_modules', 'f77_lapack.mod'),
                    prefix.include)
            install(join_path('lapack95_modules', 'la_auxmod.mod'),
                    prefix.include)
            install(join_path('lapack95_modules', 'la_precision.mod'),
                    prefix.include)
