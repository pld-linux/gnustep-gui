Summary:	GNUstep GUI library package
Name:		gnustep-gui
Version:	0.6.0
Release:	1
License:	GPL
Vendor:		The Seawood Project
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Source0:	/cvs/gnustep-gui-%{version}-%{date}.tar.gz
Patch0:		gstep-gui-headers.patch
URL:		http://www.gnustep.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	gnustep-core
Requires:	gnustep-base

%description
It is a library of graphical user interface classes written completely
in the Objective-C language; the classes are based upon the OpenStep
specification as release by NeXT Software, Inc. The library does not
completely conform to the specification and has been enhanced in a
number of ways to take advantage of the GNU system. These classes
include graphical objects such as buttons, text fields, popup lists,
browser lists, and windows; there are also many associated classes for
handling events, colors, fonts, pasteboards and images.

Library combo is %{libcombo}. %{_buildblurb}

%package devel
Summary:	GNUstep GUI headers and libs.
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}, gnustep-base-devel
Conflicts:	gnustep-core

%description devel
Header files required to build applications against the GNUstep GUI
library. Library combo is %{libcombo}. %{_buildblurb}

%prep
%setup -q -n gstep-%{ver}/gui
%patch -p2

%build
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
   . %{_prefix}/GNUstep/Makefiles/GNUstep.sh 
fi
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}/GNUstep --with-library-combo=%{libcombo}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
   . %{_prefix}/GNUstep/Makefiles/GNUstep.sh 
fi
install -d ${RPM_BUILD_ROOT}%{_prefix}/GNUstep/Library/Services

%{__make} install GNUSTEP_INSTALLATION_DIR=${RPM_BUILD_ROOT}%{_prefix}/GNUstep

cat > filelist.rpm.in << EOF
%defattr (-, bin, bin)
%doc ANNOUNCE COPYING* ChangeLog INSTALL NEWS NOTES README SUPPORT Version

%dir %{_prefix}/GNUstep/Library

%{_prefix}/GNUstep/Libraries/GSARCH/GSOS/%{libcombo}/lib*.so.*
%{_prefix}/GNUstep/Libraries/Resources
%{_prefix}/GNUstep/Library/Model
%{_prefix}/GNUstep/Library/Services/*
%{_prefix}/GNUstep/Tools/make_services
%{_prefix}/GNUstep/Tools/set_show_service
# gpbs is now provided by xgps
#%{_prefix}/GNUstep/Tools/GSARCH/GSOS/%{libcombo}/gpbs
%{_prefix}/GNUstep/Tools/GSARCH/GSOS/%{libcombo}/make_services
%{_prefix}/GNUstep/Tools/GSARCH/GSOS/%{libcombo}/set_show_service

EOF

cat > filelist-devel.rpm.in  << EOF
%defattr(-, bin, bin)
%{_prefix}/GNUstep/Headers/gnustep/gui
%{_prefix}/GNUstep/Libraries/GSARCH/GSOS/%{libcombo}/lib*.so

EOF

sed -e "s|GSARCH|${GNUSTEP_HOST_CPU}|" -e "s|GSOS|${GNUSTEP_HOST_OS}|" < filelist.rpm.in > filelist.rpm
sed -e "s|GSARCH|${GNUSTEP_HOST_CPU}|" -e "s|GSOS|${GNUSTEP_HOST_OS}|" < filelist-devel.rpm.in > filelist-devel.rpm

# Don't worry about ld.so.conf on linux as gnustep-base should take care of it.

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist.rpm
%defattr(644,root,root,755)

%files -f filelist-devel.rpm devel
%defattr(644,root,root,755)

%changelog
* %{date} PLD Team <pld-list@pld.org.pl>
All persons listed below can be reached at <cvs_login>@pld.org.pl

$Log: gnustep-gui.spec,v $
Revision 1.5  2000-06-09 07:54:42  kloczek
- more %%{__make} macros.

Revision 1.4  2000/06/09 07:22:52  kloczek
- added using %%{__make} macro.

Revision 1.3  2000/05/20 13:37:50  kloczek
- spec adapterized and partialy rewrited.

* Sat Sep 18 1999 Christopher Seawood <cls@seawood.org>
- Version 0.6.0
- Added headers patch

* Sat Aug 07 1999 Christopher Seawood <cls@seawood.org>
- Updated to cvs dawn_6 branch

* Sat Jun 26 1999 Christopher Seawood <cls@seawood.org>
- Split into separate rpm from gnustep-core
- Build from cvs snapshot
- Split into -devel, -libs & -zoneinfo packages
