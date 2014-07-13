#
# spec file for package perl-libapt-pkg (Version 0.1.13)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           perl-libapt-pkg
BuildRequires:  apt-devel gcc-c++
Summary:        Perl interface to libapt-pkg
Version:        0.1.13
Release:        122
License:        GPL v2 or later
Group:          Development/Libraries/Perl
Url:            http://packages.qa.debian.org/liba/libapt-pkg-perl
Source0:        libapt-pkg-perl_%{version}.tar.gz
Patch:          perl-libapt-pkg-missing_includes.patch
Patch1:         perl-libapt-pkg-deprecated_conversion.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       perl >= 5.8.8 apt-libs

%description
A Perl interface to APT's libapt-pkg which provides modules for
configuration file/command line parsing, version comparison, inspection
of the binary package cache and source package details.



Authors:
--------
    Brendan O'Dea <bod@debian.org>

%prep
%setup -q -n libapt-pkg-perl-%{version}
%patch
#%patch1

%build
perl Makefile.PL
make
# test suite currently fails
#make test

%install
%perl_make_install
%perl_process_packlist

%clean
# rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{perl_vendorarch}/AptPkg.pm
%{perl_vendorarch}/AptPkg
%{perl_vendorarch}/auto/AptPkg
%{_mandir}/*/*
%doc debian/changelog debian/copyright examples
/var/adm/perl-modules/%{name}
%changelog
* Fri Oct 26 2007 - pth@suse.de
- Add missing includes.
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Aug 15 2005 - ro@suse.de
- fixed filelist
* Fri Aug 12 2005 - pth@suse.de
- Initial package, based on the work of Richard Bos <richard@radoeka.nl>
