%define name			symmetrica
%define libsymmetrica		%mklibname %{name} 0
%define libsymmetrica_devel	%mklibname %{name} -d
%define libsymmetrica_static	%mklibname %{name} -d -s

Name:		%{name}
Version:	2.0
Release:	11
Summary:	A Collection of Routines for Solving Symmetric Groups
Group:		Sciences/Mathematics
# Note: they claim it's 'public domain' but then provide this:
# http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/copyright_engl.html
License:	MIT
URL:		http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/
Source0:	http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/SYM2_0_tar.gz
# Sent upstream 8 May 2012.  Sagemath patch to fix namespace collisions on the
# names "sort" and "sum".
Patch0:		symmetrica-sort_sum_rename.patch
# Sent upstream 8 May 2012.  The INT type should always be a 4-byte type, but
# the sources use an incorrect and outdated method of ensuring this.
Patch1:		symmetrica-int.patch
# Will not be sent upstream, as it is GCC-specific.  Add function attributes
# to quiet GCC warnings and improve opportunities for optimization.
Patch2:		symmetrica-attribute.patch

%description
Symmetrica is a collection of routines, written in the programming
language C, through which the user can readily write his/her own
programs. Routines which manipulate many types of mathematical objects
are available.

%package	-n %{libsymmetrica}
Group:		System/Libraries
Summary:	Symmetrica runtime files
Obsoletes:	symmetrica < %{version}-%{release}

%description	-n %{libsymmetrica}
Symmetrica runtime files.

%package	-n %{libsymmetrica_devel}
Group:		Development/C
Summary:	Symmetrica development files
Requires:	%{libsymmetrica} = %{version}-%{release}
Provides:	symmetrica-devel = %{version}-%{release}
Obsoletes:	symmetrica-devel < %{version}-%{release}
Obsoletes:	%{libsymmetrica_static} < %{version}-%{release}

%description	-n %{libsymmetrica_devel}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p0
%patch2 -p0

# Don't print the banner on every library load and API function call
sed -i "s/^\(INT no_banner = \)FALSE/\1TRUE/" de.c

%build
# All the silly *TRUE defines:
#DFLAGS=$(for def in $(grep '#ifdef' *.c | cut -d':' -f2 | cut -d' ' -f2 | egrep .*TRUE | sort | uniq); do echo -D${def}; done)
DFLAGS="-DBINTREETRUE -DBRUCHTRUE -DCHARTRUE -DCYCLOTRUE -DDGTRUE \
  -DELMSYMTRUE -DFFTRUE -DGRALTRUE -DGRAPHTRUE -DGRTRUE -DHOMSYMTRUE \
  -DINTEGERTRUE -DKOSTKATRUE -DKRANZTRUE -DLAURENTTRUE -DLISTTRUE \
  -DLONGINTTRUE -DMATRIXTRUE -DMONOMIALTRUE -DMONOMTRUE \
  -DMONOPOLYTRUE -DNUMBERTRUE -DPARTTRUE -DPERMTRUE -DPLETTRUE \
  -DPOLYTRUE -DPOWSYMTRUE -DREIHETRUE -DSABTRUE -DSCHUBERTTRUE \
  -DSCHURTRUE -DSHUFFLETRUE -DSKEWPARTTRUE -DSQRADTRUE -DTABLEAUXTRUE \
  -DVECTORTRUE -DWORDTRUE -DZYKTRUE"

for file in *.c; do
  if [ $file != "test.c" ] ; then
    gcc %{optflags} -c ${file} -I. -DFAST ${DFLAGS}
  fi
done
ar rcs lib%{name}.a *.o
rm -f *.o
for file in *.c; do
  if [ $file != "test.c" ] ; then
    gcc %{optflags} -fPIC -c ${file} -I. -DFAST ${DFLAGS}
  fi
done
gcc %{optflags} $RPM_LD_FLAGS -shared -Xlinker -hlib%{name}.so.0 \
    -o lib%{name}.so.0.0.0 *.o

%install
chmod -R a+r .
mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m 755 lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/
ln -s lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
install -m 644 *.h $RPM_BUILD_ROOT%{_includedir}/%{name}/

%files		-n %{libsymmetrica}
%doc *.doc
%{_libdir}/lib%{name}.so.0.0.0
%{_libdir}/lib%{name}.so.0

%files		-n %{libsymmetrica_devel}
%doc test.c
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Fri Aug 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.0-11
+ Revision: 815716
- Rebuild.
- Bump release and rebuild.

* Fri Aug 24 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.0-9
+ Revision: 815699
- Bump release and rebuild.
- Bump release, rename packages to match library policy and rebuild.

* Thu Aug 16 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.0-7
+ Revision: 814996
- Bump release and rebuild due to partial package upload.

* Wed Aug 15 2012 Paulo Andrade <pcpa@mandriva.com.br> 2.0-6
+ Revision: 814885
- Build only a dynamically linked library.
- Rework package to match fedora symmetrica package.

* Wed Jun 17 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.0-5mdv2010.0
+ Revision: 386505
- Rebuild using sagemath patches.

* Tue May 19 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.0-4mdv2010.0
+ Revision: 377751
- Rebuild with -fPIC as suggested by the x86_64 link error.

* Thu May 14 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.0-3mdv2010.0
+ Revision: 375760
+ rebuild (emptylog)

* Tue Apr 07 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.0-2mdv2009.1
+ Revision: 364567
- Split package to have minimal devel files in libsymmetrica-static-devel.
  required to link sage math python modules.

* Fri Mar 27 2009 Paulo Andrade <pcpa@mandriva.com.br> 2.0-1mdv2009.1
+ Revision: 361687
- Initial import of symmetrica, version 2.0
  Collection of math routines in the C programming language
  http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/
- symmetrica

