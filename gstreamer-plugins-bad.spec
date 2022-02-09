%define majorminor   0.10
%define gstreamer    gstreamer

%define gst_minver   0.10.36
%define gstpb_minver %{gst_minver}

Summary: GStreamer streaming media framework "bad" plug-ins
Name: gstreamer-plugins-bad
Version: 0.10.23
Release: 20%{?dist}
# The freeze and nfs plugins are LGPLv2 (only)
License: LGPLv2+ and LGPLv2
URL: https://gstreamer.freedesktop.org/
Source: https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
# Based on upstream 04909e2c50e68
Patch0: vp8enc-bitrate-fix.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=677698 / rhbz#797188
Patch1: 0001-gstcamerabin-Fix-spelling-error-in-debug-logging.patch
Patch2: 0002-camerabin-Add-a-camerabin_create_view_finder_caps-he.patch
Patch3: 0003-camerabin-Add-gst_camerabin_get_video_source_propert.patch
Patch4: 0004-camerabin-Set-src_filter-and-zoom_src_filter-caps-wh.patch
# Cherry picked from upstream git for rhbz#820959
Patch5: 0005-geometrictransform-crash-fix1.patch
Patch6: 0006-geometrictransform-crash-fix2.patch
Patch8: 0001-modplug-Specify-directory-when-including-stdafx.h.patch
# No longer needed, actually break build if we have them now.
Patch9: gst-plugins-bad-0.10.23-drop-vpx-compat-defines.patch
# Fix for libtimidity-0.2.x
Patch11: gst-plugins-bad-0.10.23-timidity2.diff
Patch12: 0001-vmncdec-Sanity-check-width-height-before-using-it.patch
Patch13: 0002-h264parse-Ensure-codec_data-has-the-required-size-wh.patch
Patch14: 0001-fix-faad2-version-check.patch
# Fix build with make-4.3
Patch15: %{name}-make43.patch

Provides: %{name}-free = %{version}-%{release}
Obsoletes: %{name}-free < 0.10.36-15
Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}
BuildRequires: gcc-c++
BuildRequires: check
BuildRequires: gettext-devel
BuildRequires: libXt-devel
BuildRequires: bzip2-devel
BuildRequires: exempi-devel
BuildRequires: gsm-devel
BuildRequires: jasper-devel
BuildRequires: ladspa-devel
BuildRequires: libdvdnav-devel
BuildRequires: libexif-devel
BuildRequires: libiptcdata-devel
BuildRequires: libmpcdec-devel
BuildRequires: libofa-devel
BuildRequires: liboil-devel
BuildRequires: librsvg2-devel
BuildRequires: libsndfile-devel
BuildRequires: libvpx-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: orc-devel
Buildrequires: wavpack-devel
BuildRequires: chrpath

BuildRequires: opus-devel
BuildRequires: soundtouch-devel
BuildRequires: liboil-devel
BuildRequires: libdca-devel
BuildRequires: faad2-devel
BuildRequires: xvidcore-devel
BuildRequires: libmms-devel
BuildRequires: mjpegtools-devel >= 2.0.0
BuildRequires: twolame-devel
BuildRequires: libmimic-devel
BuildRequires: librtmp-devel
BuildRequires: vo-amrwbenc-devel
BuildRequires: libass-devel
BuildRequires: libcdaudio-devel
BuildRequires: libcurl-devel
BuildRequires: libdc1394-devel
BuildRequires: libkate-devel
BuildRequires: libmodplug-devel
BuildRequires: libtimidity-devel
BuildRequires: libvdpau-devel
BuildRequires: opencv-devel
BuildRequires: schroedinger-devel
BuildRequires: SDL-devel
BuildRequires: slv2-devel
BuildRequires: wildmidi-devel
BuildRequires: zbar-devel
BuildRequires: zvbi-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that aren't tested
well enough, or the code is not of good enough quality.


%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Requires: %{name} = %{version}-%{release}
Requires: gstreamer-plugins-base-devel
Provides: %{name}-free-devel = %{version}-%{release}
Obsoletes: %{name}-free-devel < 0.10.36-15

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


%prep
%autosetup -n gst-plugins-bad-%{version} -p1


%build
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static --disable-gtk-doc --enable-experimental \
    --disable-nsf --disable-apexsink \

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install
%find_lang gst-plugins-bad-%{majorminor}

# Some of the plugins somehow get an rpath embedded ??
chrpath --delete %{buildroot}%{_libdir}/gstreamer-%{majorminor}/*.so

# Clean out files that should not be part of the rpm.
rm %{buildroot}%{_libdir}/gstreamer-%{majorminor}/*.la
rm %{buildroot}%{_libdir}/*.la
rm -r %{buildroot}%{_datadir}/gtk-doc


%files -f gst-plugins-bad-%{majorminor}.lang
%doc AUTHORS COPYING README REQUIREMENTS
# Take the whole dir for proper dir ownership (shared with other plugin pkgs)
%{_datadir}/gstreamer-0.10

%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.*
%{_libdir}/libgstbasevideo-%{majorminor}.so.*
%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
%{_libdir}/libgstphotography-%{majorminor}.so.*
%{_libdir}/libgstsignalprocessor-%{majorminor}.so.*
%{_libdir}/libgstvdp-%{majorminor}.so.*
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiovisualizers.so
%{_libdir}/gstreamer-%{majorminor}/libgstautoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin2.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdxaparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstcog.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstcolorspace.so
%{_libdir}/gstreamer-%{majorminor}/libgstdataurisrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstdccp.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtmf.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaceoverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstfieldanalysis.so
%{_libdir}/gstreamer-%{majorminor}/libgstfragmented.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeverb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgstfrei0r.so
%{_libdir}/gstreamer-%{majorminor}/libgstgaudieffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstgeometrictransform.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsettingselements.so
%{_libdir}/gstreamer-%{majorminor}/libgsth264parse.so
%{_libdir}/gstreamer-%{majorminor}/libgsthdvparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstinter.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstivfparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2kdecimator.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstliveadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegvideoparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmve.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnuvdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstpatchdetect.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstpnm.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
%ifarch %{ix86} x86_64
%{_libdir}/gstreamer-%{majorminor}/libgstreal.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstremovesilence.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpvp8.so
%{_libdir}/gstreamer-%{majorminor}/libgstscaletempoplugin.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdi.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgststereo.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgsttta.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofiltersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideomaxrate.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideomeasure.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so

# System (Linux) specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsuboverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstvcdsrc.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2k.so
%{_libdir}/gstreamer-%{majorminor}/libgstladspa.so
%{_libdir}/gstreamer-%{majorminor}/libgstmms.so
%{_libdir}/gstreamer-%{majorminor}/libgstmimic.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmplex.so
%{_libdir}/gstreamer-%{majorminor}/libgstmusepack.so
%{_libdir}/gstreamer-%{majorminor}/libgstofa.so
%{_libdir}/gstreamer-%{majorminor}/libgstopus.so
%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtmp.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
%{_libdir}/gstreamer-%{majorminor}/libgstvoamrwbenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvp8.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvid.so
%{_libdir}/gstreamer-%{majorminor}/libresindvd.so

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so

#data for plugins
%{_datadir}/glib-2.0/schemas/org.freedesktop.gstreamer-%{majorminor}.default-elements.gschema.xml

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstdc1394.so
%{_libdir}/gstreamer-%{majorminor}/libgstkate.so
%{_libdir}/gstreamer-%{majorminor}/libgstlv2.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstschro.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdl.so
%{_libdir}/gstreamer-%{majorminor}/libgstteletextdec.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimidity.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstzbar.so
# Linux specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstlinsys.so

%files devel
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstbasevideo-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgstsignalprocessor-%{majorminor}.so
%{_libdir}/libgstvdp-%{majorminor}.so
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography*
%{_includedir}/gstreamer-%{majorminor}/gst/signalprocessor
%{_includedir}/gstreamer-%{majorminor}/gst/video
%{_includedir}/gstreamer-%{majorminor}/gst/vdpau

# pkg-config files
%{_libdir}/pkgconfig/gstreamer-basevideo-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc


%changelog
* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.10.23-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.23-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.10.23-18
- Rebuilt

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.23-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 2020 Leigh Scott <leigh123linux@gmail.com> - 0.10.23-16
- Rebuild for new libdvdread

* Sun Sep 06 2020 Dominik Mierzejewski <rpm@greysector.net> - 0.10.23-15
- add missing Provides/Obsoletes for gstreamer-plugins-bad-free{,-devel}

* Fri Sep 04 2020 Dominik Mierzejewski <rpm@greysector.net> - 0.10.23-14
- merge with -free from Fedora
- fix build with make 4.3

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.10.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.10.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.10.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 27 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.23-7
- Add a patch from upstream fixing a faad2 crash (rf3664)

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.10.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jan 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.10.23-5
- Rebuilt for librtmp

* Sun Nov 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.10.23-4
- Rebuilt for mjpegtools update to 2.1.0

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.23-3
- Drop no longer needed PyXML BuildRequires (rf#2572)

* Sat Nov 10 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.23-2
- Add/enable vo-amrwbenc plugin

* Thu Jul 12 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.23-1
- New upstream release 0.10.23 (rf#2377)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.22-4
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.22-2
- Rebuild for new mjpegtools-2.0.0 (rf#1841)

* Tue May 17 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.22-1
- New upstream release 0.10.22

* Thu Apr 21 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.21-3
- Rebuild for proper package kit magic provides (rhbz#695730)

* Tue Mar 08 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.21-2
- Enable rtmp plugin (rf#1651)

* Fri Jan 28 2011 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.10.21-1
- New upstream release 0.10.21

* Thu Jan 20 2011 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.10.20-3
- Drop mux-es (moved to Fedora's gstreamer-plugins-bad-free)

* Fri Oct 15 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.10.20-2
- Rebuilt for gcc bug

* Sun Sep 12 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.20-1
- New upstream release 0.10.20

* Sun Jun 13 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.19-1
- New upstream release 0.10.19

* Sun Mar 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.18-1
- New upstream release 0.10.18

* Thu Feb  4 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-4
- Require new gstreamer-plugins-bad-free which is now in Fedora
- Drop all files found in gstreamer-plugins-bad-free
- Drop all subpackages (all subpackages of gstreamer-plugins-bad-free now)

* Sat Dec 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-3
- Disable muscbrainz / trm plugin (#1001)

* Fri Dec  4 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-2
- Enable LADSPA plugins (#992)

* Wed Nov 18 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-1
- New upstream release 0.10.17

* Sat Nov  7 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.16-1
- New upstream release 0.10.16

* Sun Oct 25 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-10
- Disable faac AAC (MPEG 2 / 4 audio) encode plugin as faac was moved to
  non free (rf 898)

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.10.13-9
- disable libgstneonhttpsrc

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.10.13-8
- rebuilt

* Mon Aug 31 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-7
- Rebuild for new libass

* Tue Aug 11 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-6
- Enable mimic plugin now that we have libmimic in RPM Fusion

* Thu Aug  6 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-5
- Re-enable siren as it also has not been added to gst-plugins-good (#749)

* Tue Jul 07 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.10.13-4
- rebuild for new directfb

* Sat Jun 27 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-3
- Disable rtpmanager as it also has been added to gstreamer-plugins-good (#689)

* Tue Jun 23 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-2
- Disable farsight plugins again, they have been added to Fedora's
  gstreamer-plugins-good package

* Fri Jun 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.13-1
- New upstream release 0.10.13
- Disable input-selector plugin as it has been added to Fedora's
  gstreamer-plugins-base as rythmbox needs it
- Enable plugins moved from farsight into -bad, as rawhide now
  has a new gstreamer-plugins-farsight, which no longer contains them

* Wed Jun 17 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.12-2
- Rebuild for changes in the gstreamer provides script

* Sun May 31 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.12-1
- New upstream release 0.10.12
- Resolves rf 622, rf 592

* Wed Apr 15 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.11-4
- Rebuild for new mjpegtools

* Fri Apr  3 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.11-3
- Disable mpegdemux plugin as it conflicts with
  gstreamer-plugins-flumpegdemux (rf 474)

* Sun Mar 29 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.11-2
- Rebuild for new faad2 and x264
- Enable libass plugin
- Move the midi plugins to the -extras package, so that people who do not
  need / want midi playback support do not have to download 200 MB of
  wavetable instruments. For people who do want this the automatic gstreamer
  plugin install should take care of installing them.

* Sun Mar 22 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.11-1
- New upstream release 0.10.11
- Enable celt plugin (rf 380)
- Fix broken libBPM dep (rf 412)
- Rebuild for new soundtouch (rf 457)
- Disable plugins moved from gst-plugins-farsight for now, until a new
  gst-plugins-farsight release solving the conflicts is available
- Bring back -devel and -devel-doc subdirs for new libgstphotography

* Wed Jan 21 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.10-1
- New upstream release 0.10.10
- Drop -devel and -devel-docs subpackages now that libgstapp has moved to
  the base plugins
- Disable gtk-doc now that we no longer have a -devel subpackage
- This release fixes the file conflicts with the new gstreamer-0.10.22 release

* Sat Dec 27 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-3
- Put devel docs in seperate subpackage to avoid multilib conflict (rf 276)

* Wed Dec 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-2
- Rebuild for new x264 (using patch from Rathann)

* Sun Oct 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-1
- New upstream release 0.10.9
- Rebuild for new directfb

* Sun Sep 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-4
- Rebuild for new x264 and to generate new magic gstreamer provides

* Sat Aug 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-3
- Enable DVD navigation plugin

* Fri Aug  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-2
- Release bump to keep rpmfusion version higher then livna

* Fri Aug  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-1
- New upstream release 0.10.8
- Merge changes from latest freshrpms package: enable ofa and dirac plugins

* Fri Jun 27 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.7-2
- Rebuild for new x264

* Thu Apr 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.7-1
- New upstream release 0.10.7
- Drop many upstreamed patches

* Sun Mar  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-3
- Rebuild for new x264

* Tue Feb 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-2
- Enable dc1394 plugin

* Sun Feb 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-1
- New upstream release 0.10.6-1
- Drop many upstreamed patches
- Fixes conflict with the latest gstreamer-plugins-good (livna 1884)

* Tue Feb  5 2008  Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-15
- Fix compilation with gcc 4.3

* Tue Feb  5 2008  Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-14
- Add flv demuxer from CVS (livna bug 1846)

* Sun Dec  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-13
- Add patch fixing compilation with mjpegtools 1.9.0rc3

* Sun Dec  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-12
- Add patch from upstream vcs which makes mms honor your connection speed
  settings
- Add (painstakingly self written) patch adding support for mms / mmsh seeking! 

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-11
- Rebuild for new faad2

* Sun Nov  4 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-10
- Rebuild for new libdca

* Thu Oct 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-9
- Rebuild for new (old) faad2 (livna bug 1679)

* Sat Sep 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-8
- Update mythtvsrc code to CVS version (livna bug 1660)

* Thu Sep 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-7
- No libgstreal.so on ppc / ppc64

* Thu Sep 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-6
- Fix detection of libdts with current livna libtds, this might need to be
  changed back again for rpmfusion, depending on how libdts will look there

* Sat Sep 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-5
- Add mythtvsrc plugin (livna 1646)
- Put some less often used plugins, which bring in also usually not installed
  deps in a -extras package

* Sat Sep 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-4
- Merge livna spec bugfixes into freshrpms spec for rpmfusion:
- Set release to 4 to be higher as both livna and freshrpms latest release
- Set package name and origin to rpmfusion
- Make mpeg2enc plugin compile with current mjpegtools
- Make the real plugins search for the RealPlayer .so files in various
  known possible locations instead of using only one hardcoded path to them
- Make the wildmidi plugin work with the default Fedora timidity patch set
- Add a couple of missing modtracker mimetypes to the modplug plugin
- Use the system version of libmodplug
- Fix building of the neonsrc plugin with the latest (rawhide) neon
- Disable the ladspa plugin as this has been added to Fedora's rawhide
  gstreamer-plugins-good
- Don't put an rpath in the .so's on x86_64
- Re-enable gtk-doc now that we have a -devel package again
- Enable libtimidity plugin
- Fix detection of (and linking with) libdca for the dtsdec plugin

* Tue Aug 21 2007 Matthias Saou <http://freshrpms.net/> 0.10.5-1
- Update to 0.10.5.
- Update faad2 patch : Some fixes went in, but faad2.h still produces an error.
- Remove libgstqtdemux, libgstvideocrop and libgstwavpack, all are in good now.
- Enable new nas, x264, wildmidi and libsndfile plugins.
- Re-add devel package now that we have a main shared lib and header files.
- Add check build requirement.

* Fri Mar 30 2007 Matthias Saou <http://freshrpms.net/> 0.10.4-1
- Update to 0.10.4 for F7.
- Disable swfdec... does anything/anyone even use it here? Once it stabilizes
  somewhat more, maybe then it'll be worth re-enabling.
- Re-enable wavpack, it works again now.
- Enable libcdaudio support.
- Enable jack support.
- Enable ladspa support.
- Enable mpeg2enc (mjpegtools) support.
- Remove no longer present libgstvideo4linux2.so and add all new plugins.
- Remove all gtk-doc references (all gone...?) and devel package too.

* Tue Jan  9 2007 Matthias Saou <http://freshrpms.net/> 0.10.3-3
- Update faad2 patch to also update the plugin sources, not just configure.

* Mon Dec 18 2006 Matthias Saou <http://freshrpms.net/> 0.10.3-2
- Try to rebuild against new wavpack 4.40 from Extras : Fails.
- Try to update to 0.10.3.2 pre-release : Fails, it needs a more recent gst.
- Try to include patch to update wavpack plugin source from 0.10.3.2
  pre-release : Fails to find wavpack/md5.h.
- Give up and disable wavpack support for now, sorry! Patches welcome.
- Include patch to fix faad2 2.5 detection.
- Add soundtouch support.

* Thu Jun  1 2006 Matthias Saou <http://freshrpms.net/> 0.10.3-1
- Update to 0.10.3.
- Add new translations.
- Add libgstmodplug.so, libgstvideo4linux2.so and libgstxingheader.so.
- Add new libmusicbrainz support.

* Thu Mar 23 2006 Matthias Saou <http://freshrpms.net/> 0.10.1-2
- Add libmms support, thanks to Daniel S. Rogers.

* Wed Feb 22 2006 Matthias Saou <http://freshrpms.net/> 0.10.1-1
- Update to 0.10.1.
- Add libgstcdxaparse.so and libgstfreeze.so.
- Enable libgstbz2.so, libgstglimagesink.so and libgstneonhttpsrc.so.

* Wed Jan 25 2006 Matthias Saou <http://freshrpms.net/> 0.10.0.1-1
- Update to 0.10.0.1, add new plugins.
- Spec file cleanup and rebuild for FC5.

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release with 0.10 major/minor

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- new release
- remove tta patch
- don't check for languages, no translations yet
- added gtk-doc

* Wed Oct 26 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- new release
- added speed plugin

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new release

