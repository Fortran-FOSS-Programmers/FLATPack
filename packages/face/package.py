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
from os import remove as rm

class Face(Package):
    """Fortran Ansi Colors (and Styles) Environment."""

    homepage = "https://github.com/szaghi/FACE"
    url      = "https://github.com/szaghi/FACE/archive/v1.0.1.tar.gz"

    version('1.0.1', 'c0e3a48c1d459137674e66f729282545')
    version('1.0.0', '2716d4215cf44d4cafc50fbb433c3260')

    variant('shared', default=True, description='Build shared libraries')
    variant('static', default=True, description='Build static library')
#    variant('docs', default=True, description='Generate API documentation.')

    depends_on('py-fobis-py', type='build')
#    depends_on('py-ford', type='build', when='+docs')

    def install(self, spec, prefix):
        fobis = which('FoBiS.py')
        command = ["build", "-ch", "-dbld", "."]
        compiler = ["-fc", "${FC}", "-compiler"]
        cflags = "-c"
        lflags = ""
        cflags_shared = " "
        lflags_shared = " "
        target = ["-t", "face.f90"]

        mkdirp(prefix.lib, prefix.include)

        rm("fobos")
        if spec.satisfies('%gcc'):
            compiler.append("gnu")
            cflags += " -Ofast -frealloc-lhs -std=f2008 -fall-intrinsics"
            lflags += " -Ofast"
            cflags_shared += " -fPIC"
            lflags_shared += " -shared "
        elif spec.satisfies('%intel'):
            compiler.append("intel")
            cflags += " -fast -assume realloc_lhs -standard-semantics -std08"
            lflags += " -fast"
            cflags_shared += " -fpic"
            lflags_shared += " -shared"
        else:
            raise InstallError("Unsported compiler.")

        if spec.satisfies('+shared'):
            libname = 'libface.so'
            soname = libname + '.' + spec.version.up_to(1)
            filename = libname + '.' + spec.version.dotted
            fobis_options = command + compiler + \
                            ["-cflags", cflags + cflags_shared] + \
                            ["-lflags", lflags + lflags_shared +
                             '-Wl,-soname,' + soname] + \
                            ["-mklib", "shared"] + target + \
                            ["-o", filename]
            fobis(*fobis_options)
            install(filename, prefix.lib)
            with working_dir(prefix.lib):
                ln = which('ln')
                ln('-s', filename, soname)
                ln('-s', soname, libname)

        if spec.satisfies('+static'):
            fobis_options = command + compiler + ["-cflags", cflags] + \
                            ["-lflags", lflags] + ["-mklib", "static"] + \
                            target + ["-o", "libface.a"]
            fobis(*fobis_options)
            install('libface.a', prefix.lib)

        if spec.satisfies('+shared') or spec.satisfies('+static'):
            install(join_path('mod', 'face.mod'), prefix.include)
