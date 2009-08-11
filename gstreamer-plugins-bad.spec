%define majorminor   0.10
%define gstreamer    gstreamer

%define gst_minver   0.10.22.1
%define gstpb_minver 0.10.22.1

Summary: GStreamer streaming media framework "bad" plug-ins
Name: gstreamer-plugins-bad
Version: 0.10.13
Release: 6%{?dist}
# The freeze and nfs plugins are LGPLv2 (only)
License: LGPLv2+ and LGPLv2
Group: Applications/Multimedia
URL: http://gstreamer.freedesktop.org/
Source: http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
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
BuildRequires: wildmidi-devel
BuildRequires: libsndfile-devel
BuildRequires: libmodplug-devel
BuildRequires: libtimidity-devel
BuildRequires: gmyth-devel >= 0.4
BuildRequires: libdc1394-devel
BuildRequires: libexif-devel
BuildRequires: libiptcdata-devel
BuildRequires: exempi-devel
BuildRequires: dirac-devel 
BuildRequires: libofa-devel
BuildRequires: libdvdnav-devel
BuildRequires: jasper-devel
BuildRequires: openssl-devel
BuildRequires: twolame-devel
BuildRequires: celt-devel
BuildRequires: libass-devel
BuildRequires: libmimic-devel

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
Summary: Development files for the GStreamer media framework "bad" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gstreamer-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that have
licensing issues, aren't tested well enough, or the code is not of good
enough quality.


%package devel-docs
Summary: Development documentation for the GStreamer "bad" plug-ins
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description devel-docs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development documentation for the plug-ins that have
licensing issues, aren't tested well enough, or the code is not of good
enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}


%build
# Disable ladspa, selector & mpegdemux, they are patched into Fedora's packages
# Disable amrwb as it does not belong in rpmfusion-free
# Disable libmimic plugin until libmimic is reviewed
# Disable other farsight plugins, they are patched into Fedora's packages
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static --enable-gtk-doc --enable-experimental \
    --disable-ladspa --disable-mpegdemux --disable-selector \
    --disable-amrwb \
    --disable-valve --disable-dtmf --disable-autoconvert \
    --disable-liveadder --disable-rtpmux --disable-rtpmanager
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
%{_libdir}/libgstphotography-0.10.so.*
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstaacparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiffparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstamrparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdxaparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstdccp.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so
%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgsth264parse.so
%{_libdir}/gstreamer-%{majorminor}/libgsthdvparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg4videoparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegvideoparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstmve.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnsf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnuvdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstqtmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
%ifarch %{ix86} x86_64
%{_libdir}/gstreamer-%{majorminor}/libgstreal.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstscaletempoplugin.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstshapewipe.so
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgststereo.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgsttta.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgstxdgmime.so

# System (Linux) specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstoss4audio.so
%{_libdir}/gstreamer-%{majorminor}/libgstvcdsrc.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsaspdif.so
%{_libdir}/gstreamer-%{majorminor}/libgstapexsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstcelt.so
%{_libdir}/gstreamer-%{majorminor}/libgstdc1394.so
%{_libdir}/gstreamer-%{majorminor}/libgstdfbvideosink.so
%{_libdir}/gstreamer-%{majorminor}/libgstdirac.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaac.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2k.so
%{_libdir}/gstreamer-%{majorminor}/libgstmms.so
%{_libdir}/gstreamer-%{majorminor}/libgstmetadata.so
%{_libdir}/gstreamer-%{majorminor}/libgstmimic.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmplex.so
%{_libdir}/gstreamer-%{majorminor}/libgstmusepack.so
%{_libdir}/gstreamer-%{majorminor}/libgsttrm.so
%if 0%{?fedora} >= 9
%{_libdir}/gstreamer-%{majorminor}/libgstneonhttpsrc.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstofa.so
%{_libdir}/gstreamer-%{majorminor}/libresindvd.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdl.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
#%{_libdir}/gstreamer-%{majorminor}/libgstswfdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvid.so

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so

%files extras
%defattr(-,root,root,-)
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so
%{_libdir}/gstreamer-%{majorminor}/libgstmythtvsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstnassink.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimidity.so
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgstphotography-0.10.so
%{_includedir}/gstreamer-0.10/gst/interfaces/photography*

%files devel-docs
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-0.10


%changelog
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

