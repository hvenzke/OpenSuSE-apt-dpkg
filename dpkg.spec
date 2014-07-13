Name:           dpkg
Version:        1.14.4
Release:        1
License:        GPL
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Group:          Development/Tools
Summary:        package maintenance system for Debian
%if %{suse_version} > 1020
BuildRequires:  libbz2-devel
%endif
BuildRequires:  gcc-c++ ncurses-devel pkg-config zlib-devel
Source0:	dpkg_1.14.4.tar.gz

%description
This package contains the low-level commands for handling the installation
and removal of packages on your system.
.
In order to unpack and build Debian source packages you will need to
install the developers' package `dpkg-dev' as well as this one.


%package -n dpkg-devel
Group:		Development/Tools
Summary:	package building tools for Debian
Requires:	dpkg perl patch make binutils cpio

%description -n dpkg-devel
This package contains the tools (including dpkg-source) required to
unpack, build and upload Debian source packages.
.
Most Debian source packages will require additional tools to build -
for example, most packages need the `make' and the C compiler `gcc'.


%prep
%setup -q

%build
./configure --prefix=%{_prefix} --sysconfdir=/etc \
	--without-dselect
# Fixup debian canonical architecture if it didn't get detected.
%ifarch %ix86
%define debarch i386
%endif
%ifarch x86_64
%define debarch amd64
%endif
sed -i  -e 's/#define ARCHITECTURE ""/#define ARCHITECTURE "'%debarch'"/' \
	config.h
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Remove stuff we don't want to have for now
rm -Rf $RPM_BUILD_ROOT/etc/alternatives
rm -Rf $RPM_BUILD_ROOT/etc/logrotate.d
rm -Rf $RPM_BUILD_ROOT/sbin
rm $RPM_BUILD_ROOT/usr/sbin/cleanup-info
rm $RPM_BUILD_ROOT/usr/sbin/install-info
rm $RPM_BUILD_ROOT/usr/sbin/update-alternatives
rm $RPM_BUILD_ROOT/usr/sbin/start-stop-daemon
rm $RPM_BUILD_ROOT/usr/share/man/man8/cleanup-info*
rm $RPM_BUILD_ROOT/usr/share/man/man8/install-info*
rm $RPM_BUILD_ROOT/usr/share/man/man8/update-alternatives*
rm $RPM_BUILD_ROOT/usr/share/man/man8/start-stop-daemon*
rm $RPM_BUILD_ROOT/usr/share/man/man1/dselect*
rm $RPM_BUILD_ROOT/usr/share/man/man5/dselect.cfg*
rm -Rf $RPM_BUILD_ROOT/usr/share/man/[^m]*

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
/etc/dpkg
/usr/bin/dpkg
/usr/bin/dpkg-deb
/usr/bin/dpkg-query
/usr/bin/dpkg-split
%dir /usr/lib/dpkg
/usr/lib/dpkg/dpkg-gettext.pl
/usr/lib/dpkg/enoent
/usr/lib/dpkg/mksplit
/usr/sbin/dpkg*
/usr/share/dpkg
/usr/share/locale/*/*/dpkg.mo
/usr/share/man/man1/dpkg*
/usr/share/man/man5/dpkg.cfg.5.gz
/usr/share/man/man8/dpkg-*

%files -n dpkg-devel
%defattr(-,root,root)
/usr/bin/822-date
/usr/bin/dpkg-architecture
/usr/bin/dpkg-buildpackage
/usr/bin/dpkg-checkbuilddeps
/usr/bin/dpkg-distaddfile
/usr/bin/dpkg-genchanges
/usr/bin/dpkg-gencontrol
/usr/bin/dpkg-name
/usr/bin/dpkg-parsechangelog
/usr/bin/dpkg-scanpackages
/usr/bin/dpkg-scansources
/usr/bin/dpkg-shlibdeps
/usr/bin/dpkg-source
/usr/lib/dpkg/controllib.pl
/usr/lib/dpkg/parsechangelog/debian
/usr/share/locale/*/*/dpkg-dev.mo
/usr/share/man/man1/822-date*
/usr/share/man/man5/deb*

%changelog
