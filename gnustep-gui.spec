Summary:	GNUstep GUI library package
Summary(pl):	Biblioteka GNUstep GUI
Name:		gnustep-gui
Version:	0.7.0
Release:	1
License:	GPL
Vendor:		The Seawood Project
Group:		Development/Tools
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
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

%description -l pl
To jest biblioteka klas graficznego interfejsu u¿ytkownika napisana w
Objective-C. Klasy bazuj± na specyfikacji OpenStep wypuszczonej przez
NeXT Software. Biblioteka nie jest ca³kowicie zgodna ze specyfikacj± i
zosta³a rozszerzona, aby wykorzystaæ mo¿liwo¶ci systemu GNU. Klasy
zawieraj± graficzne obiekty takie jak przyciski, pola tekstowe, listy
rozwijane, listy przewijane i okienka; jest tak¿e wiele klas do
obs³ugi zdarzeñ, kolorów, fontów i obrazków.

%package devel
Summary:	GNUstep GUI headers and libs
Summary(pl):	Pliki nag³ówkowe GNUstep GUI
Group:		Development/Libraries
Requires:	%{name} = %{version}, gnustep-base-devel
Conflicts:	gnustep-core

%description devel
Header files required to build applications against the GNUstep GUI
library. Library combo is %{libcombo}. %{_buildblurb}

%description devel -l pl
Pliki nag³ówkowe potrzebne do budowania aplikacji korzystaj±cych z
biblioteki GNUstep GUI.

%prep
%setup -q -n gstep-%{ver}/gui
%patch -p2

%build
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
   . %{_prefix}/GNUstep/Makefiles/GNUstep.sh 
fi
CFLAGS="%{rpmcflags}" ./configure --prefix=%{_prefix}/GNUstep --with-library-combo=%{libcombo}
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
%defattr(-, root, root)
%{_prefix}/GNUstep/Headers/gnustep/gui
%{_prefix}/GNUstep/Libraries/GSARCH/GSOS/%{libcombo}/lib*.so

EOF

sed -e "s|GSARCH|${GNUSTEP_HOST_CPU}|" -e "s|GSOS|${GNUSTEP_HOST_OS}|" < filelist.rpm.in > filelist.rpm
sed -e "s|GSARCH|${GNUSTEP_HOST_CPU}|" -e "s|GSOS|${GNUSTEP_HOST_OS}|" < filelist-devel.rpm.in > filelist-devel.rpm

# Don't worry about ld.so.conf on linux as gnustep-base should take care of it.

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f filelist.rpm
%defattr(644,root,root,755)

%files -f filelist-devel.rpm devel
%defattr(644,root,root,755)
