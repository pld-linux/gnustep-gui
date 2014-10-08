#
# Conditional build:
%bcond_without	cups		# GSCUPS bundle
%bcond_without	magick		# ImageMagick support
%bcond_without	portaudio	# gsnd tool
#
Summary:	GNUstep GUI library package
Summary(pl.UTF-8):	Biblioteka GNUstep GUI
Name:		gnustep-gui
%define	ver	0.24
Version:	%{ver}.0
Release:	2
License:	LGPL v2+ (library), GPL v3+ (applications)
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	bd289f0c7b2626d093ad92364069b9a7
Patch0:		%{name}-nocompressdocs.patch
Patch1:		%{name}-doc.patch
Patch2:		%{name}-giflib.patch
URL:		http://www.gnustep.org/
%{?with_magick:BuildRequires:	ImageMagick-devel}
BuildRequires:	aspell-devel
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	flite-devel
BuildRequires:	gcc-objc
BuildRequires:	giflib-devel
BuildRequires:	gnustep-base-devel >= 1.13.0
BuildRequires:	gnustep-make-devel
BuildRequires:	libao-devel
BuildRequires:	libicns-devel
BuildRequires:	libicu-devel >= 4.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig
%{?with_portaudio:BuildRequires:	portaudio-devel >= 19}
BuildRequires:	zlib-devel
Requires:	gnustep-base >= 1.13.0
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	gnustep-base-devel >= 1.13.0
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

%build
export GNUSTEP_MAKEFILES=%{_datadir}/GNUstep/Makefiles
export GNUSTEP_FLATTENED=yes
# disable gsnd - not ready for current portaudio
%configure \
	%{!?with_cups:--disable-cups} \
	%{!?with_portaudio:--disable-gsnd} \
	%{?with_magick:--enable-imagemagick} \
	--enable-libgif \
	--disable-ungif

# with __make -jN we can got non-deterministic errors
%{__make} -j1 \
	messages=yes

%install
rm -rf $RPM_BUILD_ROOT
export GNUSTEP_MAKEFILES=%{_datadir}/GNUstep/Makefiles
export GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
export GNUSTEP_FLATTENED=yes

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install -C Documentation \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation \
	-type f -name .cvsignore | xargs rm -f

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation \
	-type f -a ! -name '*.html' -a ! -name '*.gz' -a ! -name '*.jpg' -a ! -name '*.css' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%docdir %{_datadir}/GNUstep/Documentation
%dir %{_datadir}/GNUstep/Documentation/Developer
%dir %{_datadir}/GNUstep/Documentation/Developer/Gui
%{_datadir}/GNUstep/Documentation/Developer/Gui/ReleaseNotes
%{_datadir}/GNUstep/Documentation/User

%{_mandir}/man1/gclose.1*
%{_mandir}/man1/gcloseall.1*
%{_mandir}/man1/gopen.1*
%{_mandir}/man1/make_services.1*
%{_mandir}/man1/set_show_service.1*

%attr(755,root,root) %{_bindir}/GSSpeechServer
%attr(755,root,root) %{_bindir}/gclose
%attr(755,root,root) %{_bindir}/gcloseall
%attr(755,root,root) %{_bindir}/gopen
%attr(755,root,root) %{_bindir}/make_services
%attr(755,root,root) %{_bindir}/say
%attr(755,root,root) %{_bindir}/set_show_service
%attr(755,root,root) %{_libdir}/libgnustep-gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnustep-gui.so.%{ver}

# XXX: shared with WindowMaker - move to gnustep-dirs?
%dir %{_libdir}/GNUstep/Applications

%dir %{_libdir}/GNUstep/Applications/GSSpeechServer.app
%attr(755,root,root) %{_libdir}/GNUstep/Applications/GSSpeechServer.app/GSSpeechServer
%{_libdir}/GNUstep/Applications/GSSpeechServer.app/Resources
%{_libdir}/GNUstep/Applications/GSSpeechServer.app/stamp.make

%dir %{_libdir}/GNUstep/Bundles

%dir %{_libdir}/GNUstep/Bundles/AudioOutput.nssound
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/AudioOutput.nssound/AudioOutput
%{_libdir}/GNUstep/Bundles/AudioOutput.nssound/Resources
%{_libdir}/GNUstep/Bundles/AudioOutput.nssound/stamp.make

%dir %{_libdir}/GNUstep/Bundles/GSPrinting
%dir %{_libdir}/GNUstep/Bundles/GSPrinting/GSLPR.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/GSPrinting/GSLPR.bundle/GSLPR
%{_libdir}/GNUstep/Bundles/GSPrinting/GSLPR.bundle/Resources
%{_libdir}/GNUstep/Bundles/GSPrinting/GSLPR.bundle/stamp.make
%if %{with cups}
# R: cups-lib - separate?
%dir %{_libdir}/GNUstep/Bundles/GSPrinting/GSCUPS.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/GSPrinting/GSCUPS.bundle/GSCUPS
%{_libdir}/GNUstep/Bundles/GSPrinting/GSCUPS.bundle/Resources
%{_libdir}/GNUstep/Bundles/GSPrinting/GSCUPS.bundle/stamp.make
%endif

%dir %{_libdir}/GNUstep/Bundles/Sndfile.nssound
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/Sndfile.nssound/Sndfile
%{_libdir}/GNUstep/Bundles/Sndfile.nssound/Resources
%{_libdir}/GNUstep/Bundles/Sndfile.nssound/stamp.make

%dir %{_libdir}/GNUstep/Bundles/TextConverters
%dir %{_libdir}/GNUstep/Bundles/TextConverters/RTFConverter.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/TextConverters/RTFConverter.bundle/RTFConverter
%{_libdir}/GNUstep/Bundles/TextConverters/RTFConverter.bundle/Resources
%{_libdir}/GNUstep/Bundles/TextConverters/RTFConverter.bundle/stamp.make

%dir %{_libdir}/GNUstep/Bundles/libgmodel.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/libgmodel.bundle/libgmodel
%{_libdir}/GNUstep/Bundles/libgmodel.bundle/Resources
%{_libdir}/GNUstep/Bundles/libgmodel.bundle/stamp.make

%dir %{_libdir}/GNUstep/ColorPickers

%dir %{_libdir}/GNUstep/ColorPickers/NamedPicker.bundle
%attr(755,root,root) %{_libdir}/GNUstep/ColorPickers/NamedPicker.bundle/NamedPicker
%{_libdir}/GNUstep/ColorPickers/NamedPicker.bundle/Resources
%{_libdir}/GNUstep/ColorPickers/NamedPicker.bundle/stamp.make

%dir %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle
%attr(755,root,root) %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/StandardPicker
%dir %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources
%{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/*.tiff
%{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/*.plist
%{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/English.lproj
%lang(fr) %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/French.lproj
%lang(es) %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/Spanish.lproj
%lang(sv) %{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/Resources/Swedish.lproj
%{_libdir}/GNUstep/ColorPickers/StandardPicker.bundle/stamp.make

%dir %{_libdir}/GNUstep/ColorPickers/WheelPicker.bundle
%attr(755,root,root) %{_libdir}/GNUstep/ColorPickers/WheelPicker.bundle/WheelPicker
%{_libdir}/GNUstep/ColorPickers/WheelPicker.bundle/Resources
%{_libdir}/GNUstep/ColorPickers/WheelPicker.bundle/stamp.make

%{_libdir}/GNUstep/Images
%{_libdir}/GNUstep/KeyBindings

%dir %{_libdir}/GNUstep/Libraries/gnustep-gui
%dir %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions
%dir %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}
%dir %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources
%{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/*.plist
%{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/English.lproj
%lang(eo) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/Esperanto.lproj
%lang(fr) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/French.lproj
%lang(de) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/German.lproj
%lang(it) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/Italian.lproj
%lang(jbo) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/Lojban.lproj
%lang(es) %{_libdir}/GNUstep/Libraries/gnustep-gui/Versions/%{ver}/Resources/Spanish.lproj

%dir %{_libdir}/GNUstep/PostScript
%{_libdir}/GNUstep/PostScript/GSProlog.ps
%dir %{_libdir}/GNUstep/PostScript/PPD
%{_libdir}/GNUstep/PostScript/PPD/English.lproj

%dir %{_libdir}/GNUstep/Services

%dir %{_libdir}/GNUstep/Services/GSspell.service
%attr(755,root,root) %{_libdir}/GNUstep/Services/GSspell.service/GSspell
%{_libdir}/GNUstep/Services/GSspell.service/Resources

%{_libdir}/GNUstep/Sounds

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnustep-gui.so
%{_includedir}/AppKit
%{_includedir}/Cocoa
%{_includedir}/GNUstepGUI
%{_includedir}/gnustep/gui

%docdir %{_datadir}/GNUstep/Documentation
%{_datadir}/GNUstep/Documentation/Developer/Gui/Additions
%{_datadir}/GNUstep/Documentation/Developer/Gui/General
%{_datadir}/GNUstep/Documentation/Developer/Gui/ProgrammingManual
%{_datadir}/GNUstep/Documentation/Developer/Gui/Reference
%{_infodir}/AppKit.info*

%{_datadir}/GNUstep/Makefiles/Additional/gui.make
