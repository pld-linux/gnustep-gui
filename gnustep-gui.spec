Summary:	GNUstep GUI library package
Summary(pl):	Biblioteka GNUstep GUI
Name:		gnustep-gui
Version:	0.9.4
Release:	3
License:	LGPL/GPL
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	399b3a2341899d12710f4d1ed36f3002
Patch0:		%{name}-themes.patch
Patch1:		%{name}-nocompressdocs.patch
Patch2:		%{name}-segv.patch
Patch3:		%{name}-doc.patch
URL:		http://www.gnustep.org/
BuildRequires:	audiofile-devel
BuildRequires:	gcc-objc
BuildRequires:	gnustep-base-devel >= 1.10.0
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
Requires:	gnustep-base >= 1.10.0
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/%{_lib}/GNUstep

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%(echo %{_target_cpu} | sed -e 's/amd64/x86_64/;s/ppc/powerpc/')
%endif

%description
It is a library of graphical user interface classes written completely
in the Objective-C language; the classes are based upon the OpenStep
specification as release by NeXT Software, Inc. The library does not
completely conform to the specification and has been enhanced in a
number of ways to take advantage of the GNU system. These classes
include graphical objects such as buttons, text fields, popup lists,
browser lists, and windows; there are also many associated classes for
handling events, colors, fonts, pasteboards and images.

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
Requires:	%{name} = %{version}-%{release}
Requires:	audiofile-devel
Requires:	gnustep-base-devel >= 1.9.0
Requires:	libjpeg-devel
Requires:	libtiff-devel
Conflicts:	gnustep-core

%description devel
Header files required to build applications against the GNUstep GUI
library.

%description devel -l pl
Pliki nag³ówkowe potrzebne do budowania aplikacji korzystaj±cych z
biblioteki GNUstep GUI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
. %{_prefix}/System/Library/Makefiles/GNUstep.sh
%configure

%{__make} \
	messages=yes

%install
rm -rf $RPM_BUILD_ROOT
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

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

mv $RPM_BUILD_ROOT/%{_prefix}/System/Library/Documentation/info/manual.info.gz $RPM_BUILD_ROOT/%{_prefix}/System/Library/Documentation/info/gnustep-gui.info.gz

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

%dir %{_prefix}/System/Library/Bundles/TextConverters
%dir %{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle
%{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/TextConverters/RTFConverter.bundle/%{gscpu}
%dir %{_prefix}/System/Library/Bundles/libgmodel.bundle
%{_prefix}/System/Library/Bundles/libgmodel.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgmodel.bundle/%{gscpu}

%dir %{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle
%{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle/Resources
%{_prefix}/System/Library/Bundles/GSPrinting/GSLPR.bundle/%{gscpu}


%dir %{_prefix}/System/Library/ColorPickers
%dir %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle
%dir %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/*.tiff
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/*.plist
%{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/English.lproj
%lang(fr) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/French.lproj
%lang(sv) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/Resources/Swedish.lproj
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/StandardPicker.bundle/%{gscpu}
%dir %{_prefix}/System/Library/ColorPickers/NamedPicker.bundle
%{_prefix}/System/Library/ColorPickers/NamedPicker.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/NamedPicker.bundle/%{gscpu}
%dir %{_prefix}/System/Library/ColorPickers/WheelPicker.bundle
%{_prefix}/System/Library/ColorPickers/WheelPicker.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/ColorPickers/WheelPicker.bundle/%{gscpu}

%{_prefix}/System/Library/Images/*
%{_prefix}/System/Library/KeyBindings/*.dict

%dir %{_prefix}/System/Library/Libraries/Resources/gnustep-gui
%{_prefix}/System/Library/Libraries/Resources/gnustep-gui/English.lproj
%lang(it) %{_prefix}/System/Library/Libraries/Resources/gnustep-gui/Italian.lproj

%{_prefix}/System/Library/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so.*

%dir %{_prefix}/System/Library/PostScript
%{_prefix}/System/Library/PostScript/GSProlog.ps
%dir %{_prefix}/System/Library/PostScript/PPD
%{_prefix}/System/Library/PostScript/PPD/English.lproj
%dir %{_prefix}/System/Library/Services/GSspell.service
%{_prefix}/System/Library/Services/GSspell.service/Resources
%attr(755,root,root) %{_prefix}/System/Library/Services/GSspell.service/%{gscpu}

%attr(755,root,root) %{_prefix}/System/Tools/%{gscpu}/%{gsos}/%{libcombo}/*

%files devel
%defattr(644,root,root,755)
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Gui/Additions
%{_prefix}/System/Library/Documentation/Developer/Gui/General
%{_prefix}/System/Library/Documentation/Developer/Gui/ProgrammingManual
%{_prefix}/System/Library/Documentation/Developer/Gui/Reference
%{_prefix}/System/Library/Documentation/info/gnustep-gui.info*

%{_prefix}/System/Library/Headers/%{libcombo}/AppKit
%{_prefix}/System/Library/Headers/%{libcombo}/GNUstepGUI
%{_prefix}/System/Library/Headers/%{libcombo}/gnustep/gui

%{_prefix}/System/Library/Libraries/%{gscpu}/%{gsos}/%{libcombo}/lib*.so
%{_prefix}/System/Library/Makefiles/Additional/gui.make
