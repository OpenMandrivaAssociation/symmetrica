%define old_libsymmetrica	%mklibname symmetrica 0
%define old_libsymmetrica_devel	%mklibname symmetrica -d

Name:           symmetrica
Version:        2.0
Release:        13%{?dist}
Summary:        A Collection of Routines for Solving Symmetric Groups
# Note: they claim it's 'public domain' but then provide this:
# http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/copyright_engl.html
License:        MIT
URL:            https://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/
Source0:        http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/SYM2_0_tar.gz
Source1:        %{name}.rpmlintrc
# Sent upstream 8 May 2012.  Sagemath patch to fix namespace collisions on the
# names "sort" and "sum".
Patch0:		symmetrica-sort_sum_rename.patch
# Sent upstream 8 May 2012.  The INT type should always be a 4-byte type, but
# the sources use an incorrect and outdated method of ensuring this.
Patch1:         symmetrica-int.patch
# Will not be sent upstream, as it is GCC-specific.  Add function attributes
# to quiet GCC warnings and improve opportunities for optimization.
Patch2:         symmetrica-attribute.patch
%rename %{old_libsymmetrica}

%description
Symmetrica is a collection of routines, written in the programming
language C, through which the user can readily write his/her own
programs. Routines which manipulate many types of mathematical objects
are available.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%rename %{old_libsymmetrica_devel}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -c
%patch0
%patch1
%patch2

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

%files
%doc *.doc
%{_libdir}/lib%{name}.so.0.0.0
%{_libdir}/lib%{name}.so.0

%files devel
%doc test.c
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
