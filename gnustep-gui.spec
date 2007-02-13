#
# Conditional build:
%bcond_without	cups		# GSCUPS bundle
%bcond_without	portaudio	# gsnd tool
#
Summary:	GNUstep GUI library package
Summary(pl.UTF-8):	Biblioteka GNUstep GUI
Name:		gnustep-gui
Version:	0.11.0
Release:	1
License:	LGPL/GPL
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	7821a516ce5f683885116d78ac09b79e
Patch0:		%{name}-themes.patch
Patch1:		%{name}-nocompressdocs.patch
Patch2:		%{name}-segv.patch
Patch3:		%{name}-doc.patch
URL:		http://www.gnustep.org/
BuildRequires:	aspell-devel
BuildRequires:	audiofile-devel
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	gcc-objc
BuildRequires:	giflib-devel
BuildRequires:	gnustep-base-devel >= 1.13.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
%{?with_portaudio:BuildRequires:	portaudio-devel >= 19}
BuildRequires:	zlib-devel
Requires:	gnustep-base >= 1.13.0
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/%{_lib}/GNUstep

%description
It is a library of graphical user interface classes written completely
in the Objective-C language; the classes are based upon the OpenStep
specification as release by NeXT Software, Inc. The library does not
completely conform to the specification and has been enhanced in a
number of ways to take advantage of the GNU system. These classes
include graphical objects such as buttons, text fields, popup lists,
browser lists, and windows; there are also many associated classes for
handling events, colors, fonts, pasteboards and images.

%description -l pl.UTF-8
To jest biblioteka klas graficznego interfejsu użytkownika napisana w
Objective-C. Klasy bazują na specyfikacji OpenStep wypuszczonej przez
NeXT Software. Biblioteka nie jest całkowicie zgodna ze specyfikacją i
została rozszerzona, aby wykorzystać możliwości systemu GNU. Klasy
zawierają graficzne obiekty takie jak przyciski, pola tekstowe, listy
rozwijane, listy przewijane i okienka; jest także wiele klas do
obsługi zdarzeń, kolorów, fontów i obrazków.

%package devel
Summary:	GNUstep GUI headers and libs
Summary(pl.UTF-8):	Pliki nagłówkowe GNUstep GUI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	audiofile-devel
Requires:	gnustep-base-devel >= 1.13.0
Requires:	libjpeg-devel
Requires:	libtiff-devel
Conflicts:	gnustep-core

%description devel
Header files required to build applications against the GNUstep GUI
library.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do budowania aplikacji korzystających z
biblioteki GNUstep GUI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export GNUSTEP_MAKEFILES=%{_prefix}/System/Library/Makefiles
export GNUSTEP_FLATTENED=yes
# disable gsnd - not ready for current portaudio
%configure \
	%{!?with_cups:--disable-cups} \
	%{!?with_portaudio:--disable-gsnd}

%{__make} \
	messages=yes

%install
rm -rf $RPM_BUILD_ROOT
export GNUSTEP_MAKEFILES=%{_prefix}/System/Library/Makefiles
export GNUSTEP_FLATTENED=yes

%{__make} install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \
	INSTALL_ROOT_DIR=$RPM_BUILD_ROOT
%{__make} install -C Documentation \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \
	INSTALL_ROOT_DIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation \
	-type f -name .cvsignore | xargs rm -f
# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation \
	-type f -a ! -name '*.html' | xargs gzip -9nf

mv $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation/info/manual.info.gz $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation/info/gnustep-gui.info.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog

%docdir %{_prefix}/System/Library/Documentation
%dir %{_prefix}/System/Library/Documentation/Developer/Gui
%{_prefix}/System/Library/Documentation/Developer/Gui/ReleaseNotes
%{_prefix}/System/Library/Documentation/User/Gui
%{_prefix}/System/Library/Documentation/man/man1/*

%dir %{_prefix}/System/Library/Bundles/GSPrinting
%if %{with cups}
# R: cups-lib - separate?
%dir %{_prefix}/System/Library/Bundles/GSPrinting/GSCUPS.bundle
%{_prefix}/System/Library/Bundles/GSPrinting/GSCUPS.bundle/Resources
%{_prefix}/System/Library/Bundles/GSPrinting/GSCUPS.bundle/GSCUPS
%endif
%dir %{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle
%{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle/Resources
%{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle/GSLPR

%dir %{_prefix}/System/Library/Bundles/TextConverters
%dir %{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle
%{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle/RTFConverter
%dir %{_prefix}/System/Library/Bundles/libgmodel.bundle
%{_prefix}/System/Library/Bundles/libgmodel.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgmodel.bundle/libgmodel

%dir %{_prefix}/System/Library/ColorPickers
%dir %{_prefix}/System/Library/ColorPickers/NamedPicker.bundle
%{_prefix}/System/Library/ColorPickers/NamedPicker.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/NamedPicker.bundle/NamedPicker
%dir %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle
%dir %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/*.tiff
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/*.plist
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/English.lproj
%lang(fr) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/French.lproj
%lang(sv) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/Swedish.lproj
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/StandardPicker
%dir %{_prefix}/System/Library/ColorPickers/WheelPicker.bundle
%{_prefix}/System/Library/ColorPickers/WheelPicker.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/WheelPicker.bundle/WheelPicker

%{_prefix}/System/Library/Images/*
%{_prefix}/System/Library/KeyBindings/*.dict

%dir %{_prefix}/System/Library/Libraries/Resources/gnustep-gui
%{_prefix}/System/Library/Libraries/Resources/gnustep-gui/*.plist
%{_prefix}/System/Library/Libraries/Resources/gnustep-gui/English.lproj
%lang(eo) %{_prefix}/System/Library/Libraries/Resources/gnustep-gui/Esperanto.lproj
%lang(de) %{_prefix}/System/Library/Libraries/Resources/gnustep-gui/German.lproj
%lang(it) %{_prefix}/System/Library/Libraries/Resources/gnustep-gui/Italian.lproj
%lang(jbo) %{_prefix}/System/Library/Libraries/Resources/gnustep-gui/Lojban.lproj

%attr(755,root,root) %{_prefix}/System/Library/Libraries/libgnustep-gui.so.*

%dir %{_prefix}/System/Library/PostScript
%{_prefix}/System/Library/PostScript/GSProlog.ps
%dir %{_prefix}/System/Library/PostScript/PPD
%{_prefix}/System/Library/PostScript/PPD/English.lproj
%dir %{_prefix}/System/Library/Services/GSspell.service
%{_prefix}/System/Library/Services/GSspell.service/Resources
%attr(755,root,root) %{_prefix}/System/Library/Services/GSspell.service/GSspell

%attr(755,root,root) %{_prefix}/System/Tools/*

%files devel
%defattr(644,root,root,755)
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Gui/Additions
%{_prefix}/System/Library/Documentation/Developer/Gui/General
%{_prefix}/System/Library/Documentation/Developer/Gui/ProgrammingManual
%{_prefix}/System/Library/Documentation/Developer/Gui/Reference
%{_prefix}/System/Library/Documentation/info/gnustep-gui.info*

%{_prefix}/System/Library/Headers/AppKit
%{_prefix}/System/Library/Headers/Cocoa
%{_prefix}/System/Library/Headers/GNUstepGUI
%{_prefix}/System/Library/Headers/gnustep/gui

%attr(755,root,root) %{_prefix}/System/Library/Libraries/libgnustep-gui.so
%{_prefix}/System/Library/Makefiles/Additional/gui.make
