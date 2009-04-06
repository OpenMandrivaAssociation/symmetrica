%define name		symmetrica
%define staticname	%mklibname %{name} -d -s

Name:		%{name}
Group:		Sciences/Mathematics
# http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/copyright_engl.html
License:	Public Domain
Summary:	Collection of math routines in the C programming language
Version:	2.0
Release:	%mkrel 2
Source:		http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/SYM2_0_tar.gz
URL:		http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	%{staticname}

%description
Symmetrica is a program developed by Lehrstuhl Mathematik II of the
University of Bayreuth. It has routines to handle the following topics:
    o ordinary representation theory of the symmetric group and related groups
    o ordinary representation theory of the classical groups
    o modular representation theory of the symmetric group
    o projective representation theory of the symmetric group
    o combinatorics of tableaux
    o symmetric functions and polynomials
    o commutative and non commutative Schubert polynomials
    o operations of finite groups.
    o ordinary representation theory of Hecke algebras of type An 

Symmetrica is a collection of routines, written in the programming
language C, through which the user can readily write his/her own programs.
Routines which manipulate many types of mathematical objects are available.
Their use is facilitated by Symmetrica's object oriented style.

%package	-n %{staticname}
Group:		System/Libraries
Summary:	Symmetrica development files

%description	-n %{staticname}
Symmetrica development files.

%prep
%setup -q -c

%build
%make
ar crs libsymmetrica.a *.o

%install
mkdir -p %{buildroot}%{_usrsrc}/%{name}
cp -fa *.c makefile %{buildroot}%{_usrsrc}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -fa README *.doc %{buildroot}%{_docdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
cp -f test %{buildroot}%{_bindir}/%{name}-test

# make docs easily reachable from srcdir
ln -sf %{_docdir}/%{name} %{buildroot}%{_usrsrc}/%{name}/doc

mkdir -p %{buildroot}%{_includedir}/%{name}
cp *.h %{buildroot}%{_includedir}/%{name}
ln -sf %{_includedir}/%{name}/def.h %{buildroot}%{_usrsrc}/%{name}
ln -sf %{_includedir}/%{name}/macro.h %{buildroot}%{_usrsrc}/%{name}

mkdir -p %{buildroot}%{_libdir}
cp -f libsymmetrica.a %{buildroot}%{_libdir}

chmod -R a+r %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}-test
%dir %{_usrsrc}/%{name}
%{_usrsrc}/%{name}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*

%files		-n %{staticname}
%{_libdir}/*.a
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
