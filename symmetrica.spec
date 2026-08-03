%define old_libsymmetrica	%mklibname symmetrica 0
%define old_libsymmetrica_devel	%mklibname symmetrica -d

Name:		symmetrica
Version:	3.1.0
Release:	1
Summary:	A Collection of Routines for Solving Symmetric Groups
# Historical Bayreuth text claimed public domain; SageMath fork is ISC.
License:	ISC
URL:		https://gitlab.com/sagemath/symmetrica
Source0:	https://github.com/sagemath/sage-package/releases/download/tars/symmetrica-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
# Sent upstream 8 May 2012 (applied as SYM_sort/SYM_sum). Keep historical
# OMV API aliases sym_sort/sym_sum and consistent diagnostics.
Patch0:		symmetrica-sort_sum_rename.patch
# Sent upstream 8 May 2012. INT is a 4-byte type; residual SCNINT fixes
# for remaining INT scanf uses.
Patch1:		symmetrica-int.patch
# GCC-specific: function attributes for pure/const helpers.
Patch2:		symmetrica-attribute.patch
BuildSystem:	autotools
BuildOption:	--disable-static
%rename %{old_libsymmetrica}

%description
Symmetrica is a collection of routines, written in the programming
language C, through which the user can readily write his/her own
programs. Routines which manipulate many types of mathematical objects
are available.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{EVRD}
%rename %{old_libsymmetrica_devel}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%install -a
find %{buildroot} -name '*.la' -delete

%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}.so.3*

%files devel
%doc doc
%{_includedir}/%{name}/
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
