Name: apt-repo-tools
Version: 0.6.0.17
Release: alt2

Summary: Utilities to create APT repositories
License: GPLv2+
Group: Development/Other

Source: %name-%version.tar

Provides: apt-utils = 0.5.15lorg4
Obsoletes: apt-utils <= 0.5.15lorg4

BuildRequires: gcc-c++ libapt-devel librpm-devel

%description
This package contains the utility programs that can prepare a repository
of RPMS binary and source packages for future access by APT (by
generating the indices): genbasedir, genpkglist, gensrclist.

%prep
%setup

%build
%autoreconf
%configure
%make_build

%install
%makeinstall_std
mkdir -p %buildroot/var/cache/apt/gen{pkg,src}list

%files
/usr/bin/genpkglist
/usr/bin/gensrclist
/usr/bin/genbasedir
/usr/bin/pkglist-query
%defattr(2770,root,rpm,2770)
%dir /var/cache/apt/genpkglist
%dir /var/cache/apt/gensrclist

%changelog
