# $Id: gstreamer-plugins-bad.spec,v 1.3 2008/08/16 07:28:54 jwrdegoede Exp $
# Authority: matthias
# ExclusiveDist: fc5 fc6 el5 fc7

%define majorminor   0.10
%define gstreamer    gstreamer

%define gst_minver   0.10.10.1
%define gstpb_minver 0.10.10.1

Summary: GStreamer streaming media framework "bad" plug-ins
Name: gstreamer-plugins-bad
Version: 0.10.5
Release: 15%{?dist}
License: LGPLv2+
Group: Applications/Multimedia
URL: http://gstreamer.freedesktop.org/
Source: http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
Patch0: gst-plugins-bad-0.10.5-faad2.patch
Patch1: gstreamer-plugins-bad-0.10.5-mjpegtools.patch
Patch2: gstreamer-plugins-bad-0.10.5-real-search.patch
Patch3: gstreamer-plugins-bad-0.10.5-wildmidi-cfg.patch
Patch4: gstreamer-plugins-bad-0.10.5-mod-mimetypes.patch
Patch5: gstreamer-plugins-bad-0.10.5-sys-modplug.patch
Patch6: gstreamer-plugins-bad-gmyth.patch
Patch7: gst-plugins-bad-0.10.5-mms-connections-speed.patch
Patch8: gst-plugins-bad-0.10.5-mms-seek.patch
Patch9: gst-plugins-bad-0.10.5-flv.patch
Patch10: gst-plugins-bad-0.10.5-new-mjpegtools.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{gstreamer} >= %{gst_minver}
BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires: check
BuildRequires: gettext-devel
BuildRequires: PyXML
BuildRequires: libXt-devel
BuildRequireS: gtk-doc

BuildRequires: liboil-devel
BuildRequires: directfb-devel
BuildRequires: libdca-devel
BuildRequires: faac-devel
BuildRequires: faad2-devel
BuildRequires: gsm-devel
BuildRequires: libmpcdec-devel
BuildRequires: SDL-devel
BuildRequires: soundtouch-devel
#BuildRequires: swfdec-devel
Buildrequires: wavpack-devel
BuildRequires: xvidcore-devel
BuildRequires: bzip2-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: neon-devel
BuildRequires: libmms-devel
BuildRequires: libmusicbrainz-devel
BuildRequires: libcdaudio-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: mjpegtools-devel
BuildRequires: nas-devel
BuildRequires: x264-devel
BuildRequires: wildmidi-devel
BuildRequires: libsndfile-devel
BuildRequires: libmodplug-devel
BuildRequires: libtimidity-devel
BuildRequires: gmyth-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that have licensing issues, aren't tested
well enough, or the code is not of good enough quality.


%package extras
Summary: Extra GStreamer "bad" plugins (less often used "bad" plugins)
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description extras
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that have licensing issues, aren't
tested well enough, or the code is not of good enough quality.

This package (gstreamer-plugins-bad-extras) contains extra "bad" plugins for
sources (mythtv), sinks (jack, nas) and effects (pitch) which are not used
very much and require additional libraries to be installed.


%package devel
Summary: Development files for the GStreamer streaming media framework "bad" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gstreamer-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package cocntains the development files for the plug-ins that have
licensing issues, aren't tested well enough, or the code is not of good
enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}
%patch0 -p1 -b .faad2
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
### Use correct soundtouch pkgconfig package name
%{__sed} -i -e 's|libSoundTouch|soundtouch-1.0|g' configure*
### only check minimum versions for mjpegtools and neon
%{__sed} -i -e 's/mjpegtools >= 1.8.0 mjpegtools < 1.9.0/mjpegtools >= 1.8.0/g' \
  -e 's/neon >= 0.25.5  neon <= 0.26.99/neon >= 0.25.5/g' configure*
### fix detection of gmyth
%{__sed} -i -e 's/gmyth-0.1/gmyth/g' configure*
### fix detection and linking of the dtsdec plugin
%{__sed} -i -e 's/dts_pic/dca/g' -e 's/dts_init/dca_init/g' configure*
### we use the system version of libmodplug
%{__rm} -r gst/modplug/libmodplug/*
touch gst/modplug/libmodplug/Makefile.in


%build
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug \
    --disable-static \
    --enable-gtk-doc \
    --disable-ladspa
# Don't use rpath!   
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang gst-plugins-bad-%{majorminor}

# Clean out files that should not be part of the rpm.
%{__rm} -f %{buildroot}%{_libdir}/gstreamer-%{majorminor}/*.la
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f gst-plugins-bad-%{majorminor}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/libgstapp-0.10.so.*
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdxaparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstdeinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstequalizer.so
%{_libdir}/gstreamer-%{majorminor}/libgstfilter.so
%{_libdir}/gstreamer-%{majorminor}/libgstflvdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgsth264parse.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterleave.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultifile.so
%{_libdir}/gstreamer-%{majorminor}/libgstnsf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnuvdemux.so
%ifarch %{ix86} x86_64
%{_libdir}/gstreamer-%{majorminor}/libgstreal.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstreplaygain.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanager.so
%{_libdir}/gstreamer-%{majorminor}/libgstspectrum.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgstswitch.so
%{_libdir}/gstreamer-%{majorminor}/libgsttrm.so
%{_libdir}/gstreamer-%{majorminor}/libgsttta.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgstxingheader.so
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsaspdif.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstdfbvideosink.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaac.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
%{_libdir}/gstreamer-%{majorminor}/libgstglimagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstmms.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegvideoparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmusepack.so
%{_libdir}/gstreamer-%{majorminor}/libgstmve.so
%{_libdir}/gstreamer-%{majorminor}/libgstneonhttpsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdl.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
#%{_libdir}/gstreamer-%{majorminor}/libgstswfdec.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimidity.so
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstx264.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvid.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4menc.so

%files extras
%defattr(-,root,root,-)
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so
%{_libdir}/gstreamer-%{majorminor}/libgstmythtvsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstnassink.so
%{_libdir}/gstreamer-%{majorminor}/libgstpitch.so

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-0.10
%{_includedir}/gstreamer-0.10/gst/app/
%{_libdir}/libgstapp-0.10.so


%changelog
* Wed Jul 23 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-15
- Release bump for rpmfusion

* Tue Feb  5 2008  Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-14
- Add flv demuxer from CVS (livna bug 1846)

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

* Wed Mar 30 2007 Matthias Saou <http://freshrpms.net/> 0.10.4-1
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

