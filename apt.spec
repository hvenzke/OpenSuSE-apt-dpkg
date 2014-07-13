#
# spec file for package apt (Version 0.5.15lorg3.2)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           apt
BuildRequires:  automake gcc-c++ rpm-devel sgml-skel xmlto
BuildRequires:  cvs gettext-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
BuildRequires:  libzio-devel
BuildRequires:  fdupes
Version:        0.5.15lorg3.2
Release:        125
Summary:        A port of Debian's apt tools for RPM based distributions
Group:          System/Packages
License:        GPL v2 or later
Url:            http://apt-rpm.org
Source0:        http://apt-rpm.org/releases/%{name}-%{version}.tar.bz2
Source1:        apt.conf
Source2:        rpmpriorities.in
Source4:        sources.list.in
Source5:        security.list.in
Source6:        basesystem.list.in
Source7:        sources1.list.in
Source8:        basesystem1.list.in
Source12:       apt-wrap.tar.bz2
Source13:       README.lua
Source14:       apt-rpmlintrc
Patch0:         apt-nocow.patch
Patch1:         apt-0.5.15lorg3.x-archremove.patch
Patch2:         usr_lib_scripts.patch
Patch3:         apt-honour_post_conf.patch
Patch4:         apt-minmax_gcc42.patch
Patch5:         apt-missing_includes.patch
Patch6:         avoid-shlibs-name-mess.diff
PreReq:         coreutils sed grep diffutils gpg2
Recommends:     cron
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A port of Debian's apt tools for RPM based distributions.It provides
the apt-get utility that provides a safe and simple way to install and
upgrade packages. APT features complete installation ordering, multiple
source capability and several other unique features.



Authors:
--------
    Panu Matilainen <pmatilai@laiskiainen.org>
    Gustavo Niemeyer <niemeyer@conectiva.com>
    Alfredo K. Kojima <kojima@conectiva.com.br>

%package        devel
License:        GPL v2 or later
Summary:        Development Files and Documentation for APT's libapt-pkg
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release} 
Requires:       rpm-devel popt-devel glibc-devel bzip2 zlib-devel libstdc++-devel
Requires:       libxml2-devel

%description devel
This package contains the header files and static libraries for
developing with APT's manipulation library, modified for RPM.



Authors:
--------
    Gustavo Niemeyer <niemeyer@conectiva.com>
    Alfredo K. Kojima <kojima@conectiva.com.br>

%package     -n libapt-pkg2
License:        GPL v2 or later
Summary:        Libraries for APT for RPM
Group:          System/Libraries
PreReq:         coreutils fillup
Provides:       %name-libs = %version
Obsoletes:      %name-libs < %version

%description -n libapt-pkg2
This package contains libraries needed by apt and some other packages.



Authors:
--------
    Gustavo Niemeyer <niemeyer@conectiva.com>
    Alfredo K. Kojima <kojima@conectiva.com.br>

%package        server
License:        GPL v2 or later
Summary:        Tools to Create an APT Repository
Group:          System/Packages

%description server
This package provides the tools to create an apt repository, modified
for RPM.



Authors:
--------
    Gustavo Niemeyer <niemeyer@conectiva.com>
    Alfredo K. Kojima <kojima@conectiva.com.br>

%prep
%setup -q -a 12
%patch0
%patch1
%patch2 -p1
%patch3
%patch4
%patch5
%patch6 -p1
mv po/it_IT.po po/it.po
sed -e 's/it_IT/it/g' po/LINGUAS >po/LINGUAS.new && mv po/LINGUAS.new po/LINGUAS
# The man 8 apt manual page does not provide any usefull information.
# It says the page is not even started.
rm doc/apt.8

%build
export CXXFLAGS="%{optflags}"
autoreconf -f -i
%configure --enable-docdir=%{_defaultdocdir} --disable-docs
make
# workaround to get the xml manpages processed, until they are
# officially incorperated into apt-rpm
cd doc
for MAN in apt-cache.8.xml apt-cdrom.8.xml apt.conf.5.xml apt-config.8.xml apt-get.8.xml apt_preferences.5.xml sources.list.5.xml vendors.list.5.xml apt.1.xml; do
        xmlto man $MAN
done
cd ..
# Organize the example lua scripts into 1 directory that will be stored
# in %{_docdir}
mkdir -p examples/lua-scripts
cp -R contrib/* examples/lua-scripts
cp %{S:13} examples/lua-scripts
# Remove the lua scripts that are going to be installed, the left overs
# are going to be installed in the doc directory
for DIR in apt-groupinstall apt-wrapper list-extras list-nodeps; do
        rm -rf lua-scripts/$DIR
done

%install
%makeinstall
# The config files and empty dirs
install -d -m 755 %{buildroot}%{_sysconfdir}/apt/{apt.conf.d,sources.list.d}
install -d -m 755 %{buildroot}%{_libdir}/apt/scripts
cp -a %{SOURCE1} %{buildroot}%{_sysconfdir}/apt/apt.conf.d
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/apt/rpmpriorities
dist_version=%{suse_version}
if [ $dist_version -lt 1000 ]; then
   suse_version_string="${dist_version:0:1}.${dist_version:1:1}"
elif [ $dist_version -lt 1009 ]; then
   suse_version_string="${dist_version:0:2}.${dist_version:3:1}"
else
   suse_version_string="${dist_version:0:2}.${dist_version:2:1}"
fi
> apt_security.list
if [ $dist_version -lt 1020 ]; then
  sed -e "s|@ftp_dir@|SuSE/${suse_version_string}-%{_arch}|g" %{SOURCE4} > %{buildroot}%{_sysconfdir}/apt/sources.list
  sed -e "s|@ftp_dir@|SuSE/${suse_version_string}-%{_arch}|g" %{SOURCE5} > %{buildroot}%{_sysconfdir}/apt/security.list
  sed -e "s|@ftp_dir@|SuSE/${suse_version_string}-%{_arch}|g" %{SOURCE6} > %{buildroot}%{_sysconfdir}/apt/basesystem.list
  echo "%config(noreplace) %{_sysconfdir}/apt/security.list" > apt_security.list
else
  sed -e "s|@opensuse_version@|${suse_version_string}|g" %{SOURCE7} > %{buildroot}%{_sysconfdir}/apt/sources.list
  sed -e "s|@opensuse_version@|${suse_version_string}|g" %{SOURCE8} > %{buildroot}%{_sysconfdir}/apt/basesystem.list
fi
# Mode 644 seems sufficient for lua scripts
install -m 644 contrib/list-extras/list-extras.lua  %{buildroot}%{_libdir}/apt/scripts
install -m 644 contrib/list-extras/list-extras.conf %{buildroot}%{_sysconfdir}/apt/apt.conf.d
install -m 644 contrib/list-nodeps/list-nodeps.lua  %{buildroot}%{_libdir}/apt/scripts
install -m 644 contrib/list-nodeps/list-nodeps.conf %{buildroot}%{_sysconfdir}/apt/apt.conf.d
install -m 644 my-lua-scripts/*.lua  %{buildroot}%{_libdir}/apt/scripts
install -m 644 my-lua-conf/*.conf %{buildroot}%{_sysconfdir}/apt/apt.conf.d
install -m 755 my-lua-scripts/groupinstall-backend-suse %{buildroot}%{_libdir}/apt/scripts
install -d -m 755 %{buildroot}%{_mandir}/man{1,5,8}
for section in 1 5 8; do
    install -d -m 755 %{buildroot}%{_mandir}/man${section}
    install -m 644 doc/*${section} %{buildroot}%{_mandir}/man${section}
done
install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
install -m 755 cmdline/apt %{buildroot}%{_bindir}/
install -m 755 cmdline/apt-upgrade %{buildroot}%{_sysconfdir}/cron.daily/suse-apt-upgrade
install -m 644 -D cmdline/autoupdate %{buildroot}/var/adm/fillup-templates/sysconfig.autoupdate
# cache and state directories
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/lib/apt/lists/partial
(cd %{buildroot}%{_datadir}/locale; mv -T de_DE de)
if [ -d %{buildroot}%{_defaultdocdir}/%{name}/lua-scripts ]; then
	mv %{buildroot}%{_defaultdocdir}/%{name}/lua-scripts/* %{buildroot}%{_defaultdocdir}/%{name}/examples/lua-scripts/
	rm -rf %{buildroot}%{_defaultdocdir}/%{name}/lua-scripts
fi
%fdupes -s %{buildroot}
%find_lang %name

%post
if [ -s /etc/apt/apt.conf ]; then
        # /etc/apt/apt.conf.d/apt.conf is delivered with the apt rpm
        # just assume it exists...
        if diff -q /etc/apt/apt.conf /etc/apt/apt.conf.d/apt.conf; then
                # They are the same.  It is save to remove /etc/apt/apt.conf
                rm /etc/apt/apt.conf
                echo "/etc/apt/apt.conf has been moved to /etc/apt/apt.conf.d/apt.conf"
        else
                # They differ
                echo "Note: it is adviced to move the configuration file:"
                echo " /etc/apt/apt.conf to /etc/apt/apt.conf.d/apt.conf"
        fi
fi
FILE=/etc/apt/apt.conf.d/gpg-checker.conf
if [ -s $FILE ]; then
        if grep -q RPM::GPG-Check $FILE; then
                sed s,RPM::GPG-Check,GPG::Check, $FILE > /tmp/gpg-checker.$$
                mv /tmp/gpg-checker.$$ $FILE
        fi
fi

%post -n libapt-pkg2
/sbin/ldconfig
%{fillup_only -n autoupdate }

%postun -n libapt-pkg2 -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f apt_security.list -f %name.lang
%defattr(-, root, root)
%doc AUTHORS* COPYING* TODO doc/examples/ 
%dir %{_sysconfdir}/apt
%config %{_sysconfdir}/apt/rpmpriorities
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/apt.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/list-extras.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/list-nodeps.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/pkglog.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/post.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/gpg-import.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/gpg-checker.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/apt-groupinstall.conf
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/basesystem.list
# %config(noreplace) %{_sysconfdir}/apt/vendors.list
%dir %{_sysconfdir}/apt/apt.conf.d
%dir %{_sysconfdir}/apt/sources.list.d
%{_bindir}/countpkglist
%{_bindir}/apt*
%{_libdir}/apt
%doc %{_mandir}/man?/*
## %{_datadir}/locale/*/LC_MESSAGES/apt.mo
%{_localstatedir}/cache/apt
%{_localstatedir}/lib/apt
/var/adm/fillup-templates/sysconfig.autoupdate
%{_sysconfdir}/cron.daily/suse-apt-upgrade

%files devel
%defattr(-, root, root)
%{_includedir}/apt-pkg
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%files -n libapt-pkg2
%defattr(-, root, root)
%{_libdir}/*.so.*

%files server
%defattr(-, root, root)
%{_bindir}/gen*

%changelog
