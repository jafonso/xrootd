#-------------------------------------------------------------------------------
# The eos-xrootd package provides a series of libraries which might clash with
# the vanilla xrootd packages. To avoid such conflicts, we disable RPMS's
# automatic dependency processing when it  comes to the list of capabilities
# the current package provides.
#-------------------------------------------------------------------------------
Autoprov: 0
%global __requires_exclude ^libXrd.*$|^perl.*$
%define _prefix /opt/eos/xrootd/
%define _unpackaged_files_terminate_build 0
%define cmake cmake

%bcond_with asan
%bcond_with tsan
%bcond_with clang

Summary:        EOS XRootD version
Name:           eos-xrootd
Version:        5.8.4
Release:        4%{?dist}%{?with_clang:clang}%{?_with_asan:.asan}%{?_with_tsan:.tsan}
License:        BSD
URL:            https://github.com/xrootd/xrootd
Source:         http://xrootd.web.cern.ch/download/v%{version}/xrootd-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: krb5-devel
BuildRequires: readline-devel
BuildRequires: fuse-devel
BuildRequires: libxml2-devel
BuildRequires: krb5-devel
BuildRequires: zlib-devel
BuildRequires: ncurses-devel
BuildRequires: libuuid-devel
BuildRequires: json-c-devel
BuildRequires: libcurl-devel
BuildRequires: voms-devel
BuildRequires: libmacaroons-devel
BuildRequires: scitokens-cpp-devel
BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: libxcrypt-devel

%if %{with clang}
BuildRequires: clang
%endif

%if %{with asan}
BuildRequires: libasan
Requires: libasan
%endif

%if %{with tsan}
BuildRequires: libtsan
Requires: libtsan
%endif

%description
An xrootd installation with RPATH set to /opt/eos/xrootd/

%prep
%setup -n xrootd-%{version}

%build

%if %{with asan}
export CXXFLAGS='-fsanitize=address'
%endif

%if %{with tsan}
export CXXFLAGS='-fsanitize=thread'
%endif

%if %{with clang}
export CC=clang
export CXX=clang++
%endif

mkdir build
pushd build

%{cmake} ../ \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo         \
  -DCMAKE_INSTALL_PREFIX=%{_prefix}         \
  -DCMAKE_INSTALL_RPATH=%{_prefix}/lib64/   \
  -DCMAKE_SKIP_BUILD_RPATH=false            \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=false    \
  -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=true  \
  -DXRD_PYTHON_REQ_VERSION=3                \
  -DPython_FIND_UNVERSIONED_NAMES=FIRST     \
  -DXRootD_VERSION_STRING=%{version}        \
  -DPIP_OPTIONS=--verbose

make %{?_smp_mflags}
popd

%install
export QA_RPATHS=3
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/xrootd/utils/netchk
rm -f %{buildroot}%{_datadir}/xrootd/utils/XrdCmsNotify.pm
rm -f %{buildroot}%{_datadir}/xrootd/utils/XrdOlbMonPerf
popd

%clean
rm -rf %{buildroot}

%files
%{_prefix}/
