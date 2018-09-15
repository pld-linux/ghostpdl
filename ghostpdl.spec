#
# Conditional build:
%bcond_without	system_expat	# build with included expat
%bcond_without	system_freetype	# build with included freetype
%bcond_without	system_jbig2dec	# build with included jbig2dec
%bcond_without	system_lcms2	# build with included lcms2
#
Summary:	PostScript, PDF and XPS interpreter and renderer
Summary(pl.UTF-8):	Interpreter i renderer PostScriptu, PDF oraz XPS
Name:		ghostpdl
Version:	9.22
Release:	2
License:	AGPL v3+
Group:		Applications/Graphics
#Source0Download: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases
Source0:	https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs922/%{name}-%{version}.tar.xz
# Source0-md5:	4b6fd53f0b7ffca24cdf98456fecc22e
Patch0:		%{name}-fonts_locations.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-system-libs.patch
URL:		http://ghostscript.com/
BuildRequires:	autoconf >= 2.63
BuildRequires:	cups-devel
%{!?with_system_expat:BuildRequires:	expat-devel >= 1.95}
BuildRequires:	fontconfig-devel
BuildRequires:	libidn-devel
%{!?with_system_freetype:BuildRequires:	freetype-devel >= 1:2.6}
%{?with_system_jbig2dec:BuildRequires:	jbig2dec-devel >= 0.12}
%{?with_system_lcms2:BuildRequires:	lcms2-devel >= 2.6}
BuildRequires:	libjpeg-devel
BuildRequires:	libpaper-devel
BuildRequires:	libpng-devel >= 2:1.6.17
BuildRequires:	libtiff-devel >= 4.0.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
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
Requires:	ghostscript = %{version}
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
Requires:	ghostscript = %{version}

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
# freetype 2.5.5 + few pre-2.6 fixes from git
%{?with_system_freetype:%{__rm} -r freetype}
# jbig2dec 0.13 + minor fix
%{?with_system_jbig2dec:%{__rm} -r jbig2dec}
# (unmodified) libpng 1.6.17 and zlib 1.2.8
%{__rm} -r libpng zlib
# (unmodified) libjpeg 9a is built with different configuration (D_MAX_BLOCKS_IN_MCU=64)
# openjpeg is 2.1.0 + fixes; stick to bundled for now
# lcms2 is 2.6 with some minor future changes (one already in 2.7, two post-2.7, extra_xform.h ???)
%{?with_system_lcms2:%{__rm} -r lcms2}
%{?with_system_expat:%{__rm} -r expat}
%{__autoconf}
%configure \
	--with-system-libtiff

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
%{__rm} $RPM_BUILD_ROOT%{_mandir}/de/man1/{dvipdf,eps2eps,gsnd,pdf2*,printafm,ps2*}.1
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ghostscript

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
