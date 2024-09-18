#
# Conditional build:
%bcond_without	system_expat	# system expat
%bcond_without	system_freetype	# system freetype
%bcond_without	system_jbig2dec	# system jbig2dec
%bcond_with	system_lcms2	# system lcms2
%bcond_with	system_libjpeg	# system libjpeg (incompatible with D_MAX_BLOCKS_IN_MCU=64 variant)
%bcond_with	system_libtiff	# system libtiff (incompatible with modified libjpeg)
%bcond_without	system_openjp2	# system openjpeg2
%bcond_without	system_tesseract	# system tesseract+leptonlib
#
Summary:	PostScript, PDF and XPS interpreter and renderer
Summary(pl.UTF-8):	Interpreter i renderer PostScriptu, PDF oraz XPS
Name:		ghostpdl
Version:	10.04.0
Release:	1
License:	AGPL v3+
Group:		Applications/Graphics
#Source0Download: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases
Source0:	https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10040/%{name}-%{version}.tar.xz
# Source0-md5:	599e2cbbf492414d68d8462cfd911427
Patch0:		%{name}-fonts_locations.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-system-libs.patch
URL:		https://ghostscript.com/
BuildRequires:	autoconf >= 2.63
BuildRequires:	cups-devel >= 1.5
%{?with_system_expat:BuildRequires:	expat-devel >= 1:2.5.0}
BuildRequires:	fontconfig-devel
BuildRequires:	libidn-devel
%{?with_system_freetype:BuildRequires:	freetype-devel >= 1:2.13.0}
%{?with_system_jbig2dec:BuildRequires:	jbig2dec-devel >= 0.20}
%{?with_system_lcms2:BuildRequires:	lcms2-devel >= 2.10}
%{?with_system_libjpeg:BuildRequires:	libjpeg-devel >= 9e}
BuildRequires:	libpaper-devel
BuildRequires:	libpng-devel >= 2:1.6.39
%{?with_system_libtiff:BuildRequires:	libtiff-devel >= 4.2.0}
%{?with_system_openjp2:BuildRequires:	openjpeg2-devel >= 2.4.0}
BuildRequires:	tar >= 1:1.22
%{?with_system_tesseract:BuildRequires:	tesseract-devel >= 4.1.0}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.2.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GhostPCL is Artifex Software's implementation of the PCL-5(TM) and
PCL-XL(TM) family of page description languages. For more information
please see the documentation included with the source package.

%description -l pl.UTF-8
GhostPCL jest implementacją języków z rodzin PCL-5(TM) i PCL-XL(TM)
opisujących stronę. Więcej informacji znajduje się w dokumentacji
załączonej do pakietu.

%package -n ghostpcl
Summary:	PCL-5 and PCL-XL implementation
Summary(pl.UTF-8):	Implementacja PCL-5 oraz PCL-XL
Group:		Applications/Graphics
URL:		http://ghostscript.com/GhostPCL.html
Requires:	cups-lib >= 1.5
%{?with_system_expat:Requires:	expat >= 1:2.5.0}
%{?with_system_freetype:Requires:	freetype >= 1:2.13.0}
Requires:	ghostscript = %{version}
%{?with_system_jbig2dec:Requires:	jbig2dec >= 0.20}
%{?with_system_libjpeg:Requires:	libjpeg >= 9e}
Requires:	libpng >= 2:1.6.39
%{?with_system_libtiff:Requires:	libtiff >= 4.2.0}
%{?with_system_openjp2:Requires:	openjpeg2 >= 2.4.0}
Requires:	zlib >= 1.2.13
Suggests:	fonts-TTF-urw
Conflicts:	ghostpcl < 9

%description -n ghostpcl
GhostPCL is Artifex Software's implementation of the PCL-5 and PCL-XL
family of page description languages.

%description -n ghostpcl -l pl.UTF-8
GhostPCL to rozwijana przez Artifex Software implementacja rodzin
języków opisu strony PCL-5 oraz PCL-XL.

%package -n ghostxps
Summary:	XPS document format implementation based on Ghostscript
Summary(pl.UTF-8):	Implementacja formatu dokumentów XPS oparta na Ghostscripcie
Group:		Applications/Graphics
URL:		http://ghostscript.com/GhostXPS.html
Requires:	cups-lib >= 1.5
%{?with_system_expat:Requires:	expat >= 1:2.5.0}
%{?with_system_freetype:Requires:	freetype >= 1:2.13.0}
Requires:	ghostscript = %{version}
%{?with_system_jbig2dec:Requires:	jbig2dec >= 0.20}
%{?with_system_libjpeg:Requires:	libjpeg >= 9e}
Requires:	libpng >= 2:1.6.39
%{?with_system_libtiff:Requires:	libtiff >= 4.2.0}
%{?with_system_openjp2:Requires:	openjpeg2 >= 2.4.0}
Requires:	zlib >= 1.2.13

%description -n ghostxps
GhostXPS is an implementation of the Microsoft XPS document format
built on top of Ghostscript.

%description -n ghostxps -l pl.UTF-8
GhostXPS to implementacja formatu dokumentu XPS Microsoftu zbudowana w
oparciu o Ghostscript.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# use system libs:
# expat 2.5.0
%{?with_system_expat:%{__rm} -r expat}
# freetype 2.13.0
%{?with_system_freetype:%{__rm} -r freetype}
# jbig2dec 0.20
%{?with_system_jbig2dec:%{__rm} -r jbig2dec}
# (unmodified) libpng 1.6.39 and zlib 1.2.13
%{__rm} -r libpng zlib
# libjpeg 9e (with additional CLAMP_DC) is built with different configuration (D_MAX_BLOCKS_IN_MCU=64)
%{?with_system_libjpeg:%{__rm} -r jpeg}
# lcms2mt is thread safe version of lcms2 2.10
%{?with_system_lcms:%{__rm} -r lcms2mt}
# openjpeg 2.4.0
%{?with_system_openjp2:%{__rm} -r openjpeg}
# tesseract 5.0.0-alpha-20201231, leptonica 1.81.0-git
%{?with_system_tesseract:%{__rm} -r tesseract leptonica}
# libtiff 4.5.0rc2
%{?with_system_libtiff:%{__rm} -r tiff}

%{__autoconf}
%configure \
	%{?with_system_libtiff:--with-system-libtiff}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install pcl/tools/{pcl2pdf,pcl2pdfwr,plot2pdf.sh} $RPM_BUILD_ROOT%{_bindir}
ln -sf gpcl6 $RPM_BUILD_ROOT%{_bindir}/pcl6

# packaged in ghostscript.spec
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{dvipdf,eps2eps,gs*,lprsetup.sh,pdf2*,pf2afm,pfbtopfa,pphs,printafm,ps2*,unix-lpr.sh}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{dvipdf,eps2eps,gs*,pdf2*,pf2afm,pfbtopfa,printafm,ps2*}.1
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ghostscript
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ghostscript

%clean
rm -rf $RPM_BUILD_ROOT

%files -n ghostpcl
%defattr(644,root,root,755)
%doc doc/pclxps/ghostpdl.pdf pcl/{LICENSE,NEWS,README.txt} pcl/pcl/Anomalies.txt pcl/pxl/{pxcet,pxdiff,pxfts,pxlib,pxspec}.txt
%attr(755,root,root) %{_bindir}/gpcl6
%attr(755,root,root) %{_bindir}/pcl2pdf
%attr(755,root,root) %{_bindir}/pcl2pdfwr
%attr(755,root,root) %{_bindir}/pcl6
%attr(755,root,root) %{_bindir}/plot2pdf.sh

%files -n ghostxps
%defattr(644,root,root,755)
%doc doc/pclxps/ghostpdl.pdf xps/TODO
%attr(755,root,root) %{_bindir}/gxps
