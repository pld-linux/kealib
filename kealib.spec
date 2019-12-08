#
# Conditional build:
%bcond_with	gdal	# GDAL module [since 2.0 GDAL has builtin KEA support]
#
Summary:	KEALib - HDF5 based raster file format library
Summary(pl.UTF-8):	KEALib - biblioteka rastrowego formatu plików opartego na HDF5
Name:		kealib
Version:	1.4.6
Release:	6
License:	MIT
Group:		Libraries
Source0:	http://downloads.sourceforge.net/kealib/%{name}-%{version}.tar.gz
# Source0-md5:	789174bd519736ac1e726613b6eb7672
Patch0:		%{name}-config.patch
URL:		http://kealib.org/
BuildRequires:	cmake >= 2.6.0
%{?with_gdal:BuildRequires:	gdal-devel}
BuildRequires:	hdf5-c++-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibKEA is a project to provide an implementation of the GDAL
specification within the the HDF5 file format. Specifically, the
format will support raster attribute tables (commonly not included
within other formats), image pyramids, GDAL meta-data, in-built
statistics while also providing large file handling with compression
used throughout the file. Being based on the HDF5 standard, it will
also provide a base from which other formats could be derived and will
be a good choice for long term data archiving. An independent software
library (libKEA) has been provided through which complete access to
the KEA image format is provided alongside a GDAL driver allowing KEA
images to be used through any GDAL supported software.

%description -l pl.UTF-8
LibKEA to projekt dostarczający implementację specyfikacji GDAL
wewnątrz formatu plików HDF5. W szczególności format obsługuje tablice
atrybutów rastrowych (zwykle nie zawartych w innych formatach),
piramidy obrazów, metadane GDAL i statystyki wbudowane, zapewniając
także obsługę dużych plików z kompresją. Dzięki oparciu na standardzie
HDF5, zapewnia także podstawę, z której mogą wywodzić się inne
formaty; jest także dobrym wyborem do długoterminowej archiwizacji
danych. Udostępniono niezależną bibliotekę (libKEA), dającą pełny
dostęp do formatu obrazów KEA, a także sterownik GDA pozwalający na
używanie obrazów KEA w programach obsługujących GDAL.

%package devel
Summary:	Header files for LibKEA library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibKEA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hdf5-c++-devel
Requires:	libstdc++-devel

%description devel
Header files for LibKEA library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibKEA.

%package -n gdal-kea
Summary:	KEA plugin for GDAL library
Summary(pl.UTF-8):	Wtyczka KEA do biblioteki GDAL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with gdal}
%requires_ge	gdal
%endif

%description -n gdal-kea
KEA plugin for GDAL library.

%description -n gdal-kea -l pl.UTF-8
Wtyczka KEA do biblioteki GDAL.

%prep
%setup -q
%patch0 -p1

%build
cd trunk
%cmake . \
%if %{with gdal}
	-DGDAL_INCLUDE_DIR=%{_includedir}/gdal \
	-DGDAL_LIB_PATH=%{_libdir} \
%endif
	-DHDF5_INCLUDE_DIR=%{_includedir} \
	-DHDF5_LIB_PATH=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C trunk install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libkea.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kea-config
%attr(755,root,root) %{_libdir}/libkea.so
%{_includedir}/libkea

%if %{with gdal}
%files -n gdal-kea
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gdalplugins/gdal_KEA.so
%endif
