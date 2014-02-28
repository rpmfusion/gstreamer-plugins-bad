%define majorminor   0.10
%define gstreamer    gstreamer

%define gst_minver   0.10.29
%define gstpb_minver 0.10.29

# which plugins to actually build and install
%ifarch %{ix86} x86_64
%define gstdirs gst/asfmux gst/dvdspu gst/mpegpsmux gst/mpegtsmux gst/qtmux gst/real gst/siren
%else
%define gstdirs gst/asfmux gst/dvdspu gst/mpegpsmux gst/mpegtsmux gst/qtmux gst/siren
%endif
%define extdirs ext/dts ext/faad ext/libmms ext/mimic ext/mpeg2enc ext/mplex ext/xvid sys/vdpau

Summary:        GStreamer streaming media framework "bad" plug-ins
Name:           gstreamer-plugins-bad
Version:        0.10.19
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2

# http://cgit.freedesktop.org/gstreamer/gst-plugins-bad/commit/?id=407b02578689804dc6bc47e53be9e87cc1b25597
Patch0:         gst-plugins-bad-0.10.19-mpeg2enc-support-mjpegtools-2.patch

Requires:       %{gstreamer} >= %{gst_minver}
# Drag in the free plugins which are in Fedora now, for upgrade path
Requires:       gstreamer-plugins-bad-free >= %{version}

BuildRequires:  %{gstreamer}-devel >= %{gst_minver}
BuildRequires:  %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires:  check
BuildRequires:  faad2-devel
BuildRequires:  gettext-devel
BuildRequires:  gtk-doc
BuildRequires:  libdca-devel
BuildRequires:  libmimic-devel
BuildRequires:  libmms-devel
BuildRequires:  liboil-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libXt-devel
BuildRequires:  mjpegtools-devel
BuildRequires:  PyXML
BuildRequires:  twolame-devel
BuildRequires:  xvidcore-devel


%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that have licensing issues, aren't tested well
enough, or the code is not of good enough quality.


%package freeworld-devel
Summary:        Development files for the GStreamer "bad" plug-ins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer-plugins-bad-free-devel

%description freeworld-devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that aren't tested
well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}
%patch0 -p1


%build
# Note we don't bother with disabling everything which is in Fedora, that
# is unmaintainable, instead we selectively run make in subdirs
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static --enable-experimental
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
for i in %{gstdirs} %{extdirs}; do
    pushd $i
    make %{?_smp_mflags} V=2
    popd
done


%install
for i in %{gstdirs} %{extdirs}; do
    pushd $i
    make install V=2 DESTDIR=%{buildroot}
    popd
done

# Clean out files that should not be part of the rpm.
rm -f %{buildroot}/%{_libdir}/gstreamer-%{majorminor}/*.la \
      %{buildroot}/%{_libdir}/*.la


%files
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/libgstvdp-%{majorminor}.so.0
%{_libdir}/libgstvdp-%{majorminor}.so.0.0.0
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstqtmux.so
%ifarch %{ix86} x86_64
%{_libdir}/gstreamer-%{majorminor}/libgstreal.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
%{_libdir}/gstreamer-%{majorminor}/libgstmms.so
%{_libdir}/gstreamer-%{majorminor}/libgstmimic.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmplex.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvid.so

%files freeworld-devel
%{_libdir}/libgstvdp-%{majorminor}.so
%{_includedir}/gstreamer-%{majorminor}/gst/vdpau


%changelog
* Wed Feb 05 2014 Simone Caronni <negativo17@gmail.com> - 0.10.19-2
- Remove obsolete spec file directives.
- Add VDPAU plugin and create freeworld-devel subpackage. See:
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=3110#c9.

* Sun Jun 13 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.19-1
- New upstream release 0.10.19

* Sun Mar 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.18-1
- New upstream release 0.10.18

* Thu Feb  4 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-4
- Require new gstreamer-plugins-bad-free which is now in Fedora
- Drop all files found in gstreamer-plugins-bad-free
- Drop all subpackages (all subpackages of gstreamer-plugins-bad-free now)
