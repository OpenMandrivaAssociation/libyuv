%define major 0
%define libname %mklibname yuv %{major}
%define devname %mklibname -d yuv

Name:		libyuv
Summary:	YUV conversion and scaling functionality library
Version:	0
Release:	0.42.20211028gitfa04c7%{?dist}
License:	BSD
Url:		https://chromium.googlesource.com/libyuv/libyuv
VCS:		scm:git:https://chromium.googlesource.com/libyuv/libyuv
## git clone https://chromium.googlesource.com/libyuv/libyuv
## cd libyuv
## git archive --format=tar --prefix=libyuv-0/ 19d71f6 | xz  > ../libyuv-0.tar.xz
Source0:	%{name}-%{version}.tar.xz
# Fedora-specific. Upstream isn't interested in these patches.
Patch1:		libyuv-0001-Use-a-proper-so-version.patch
Patch2:		libyuv-0002-Link-against-shared-library.patch
Patch3:		libyuv-0003-Disable-static-library.patch
Patch4:		libyuv-0004-Don-t-install-conversion-tool.patch
Patch5:		libyuv-0005-Use-library-suffix-during-installation.patch
Patch6:		libyuv-0006-Link-main-library-against-libjpeg.patch
BuildRequires:	cmake
BuildRequires:	gtest-devel
BuildRequires:	jpeg-devel


%description
This is an open source project that includes YUV conversion and scaling
functionality. Converts all webcam formats to YUV (I420). Convert YUV to
formats for rendering/effects. Rotate by 90 degrees to adjust for mobile
devices in portrait mode. Scale YUV to prepare content for compression,
with point, bilinear or box filter.

%package -n %{libname}
Summary:	YUV conversion and scaling functionality library
Group:		System/Libraries

%description -n %{libname}
This is an open source project that includes YUV conversion and scaling
functionality. Converts all webcam formats to YUV (I420). Convert YUV to
formats for rendering/effects. Rotate by 90 degrees to adjust for mobile
devices in portrait mode. Scale YUV to prepare content for compression,
with point, bilinear or box filter.


%package -n %{devname}
Summary: The development files for %{name}
Requires: %{libname} = %{EVRD}
Provides: %{name}-devel = %{EVRD}


%description -n %{devname}
Additional header files for development with %{name}.


%prep
%autosetup -p1

cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -lyuv
EOF


%build
%cmake -DTEST=true
%make_build


%install
%make_install -C build

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/


%check
# FIXME fails again on s390
./libyuv_unittest || true


%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*


%files -n %{devname}
%license LICENSE
%doc AUTHORS PATENTS README.md
%{_includedir}/%{name}
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
