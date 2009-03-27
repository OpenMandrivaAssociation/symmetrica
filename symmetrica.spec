Name:		symmetrica
Group:		Sciences/Mathematics
# http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/copyright_engl.html
License:	Public Domain
Summary:	Collection of math routines in the C programming language
Version:	2.0
Release:	%mkrel 1
Source:		http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/SYM2_0_tar.gz
URL:		http://www.algorithm.uni-bayreuth.de/en/research/SYMMETRICA/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%prep
%setup -q -c

%build
%make

%install
mkdir -p %{buildroot}%{_usrsrc}/%{name}
cp -fa *.c *.h makefile %{buildroot}%{_usrsrc}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -fa README *.doc %{buildroot}%{_docdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
cp -f test %{buildroot}%{_bindir}/%{name}-test

# make docs easily reachable from srcdir
ln -sf %{_docdir}/%{name} %{buildroot}%{_usrsrc}/%{name}/doc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}-test
%dir %{_usrsrc}/%{name}
%{_usrsrc}/%{name}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
