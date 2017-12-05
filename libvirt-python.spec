
%define with_python3 0
%if 0%{?fedora}
%define with_python3 1
%endif

Summary: The libvirt virtualization API python2 binding
Name: libvirt-python
Version: 3.10.0
Release: 1%{?dist}%{?extra_release}
Source0: http://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
BuildRequires: libvirt-devel >= %{version}
BuildRequires: python-devel
BuildRequires: python-nose
BuildRequires: python-lxml
%if %{with_python3}
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: python3-lxml
%endif

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/.*\.so}
%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%package -n python2-libvirt
Summary: The libvirt virtualization API python2 binding
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
%{?python_provide:%python_provide python2-libvirt}
Provides: libvirt-python = %{version}-%{release}
Obsoletes: libvirt-python <= 3.6.0-1%{?dist}

%description -n python2-libvirt
The python2-libvirt package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%if %{with_python3}
%package -n python3-libvirt
Summary: The libvirt virtualization API python3 binding
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
%{?python_provide:%python_provide python3-libvirt}
Provides: libvirt-python3 = %{version}-%{release}
Obsoletes: libvirt-python3 <= 3.6.0-1%{?dist}

%description -n python3-libvirt
The python3-libvirt package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%prep
%setup -q

# Unset execute bit for example scripts; it can introduce spurious
# RPM dependencies, like /usr/bin/python which can pull in python2
# for the -python3 package
find examples -type f -exec chmod 0644 \{\} \;

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%if %{with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%{__python} setup.py install --skip-build --root=%{buildroot}
%if %{with_python3}
%{__python3} setup.py install --skip-build --root=%{buildroot}
%endif

%check
%{__python} setup.py test
%if %{with_python3}
%{__python3} setup.py test
%endif

%files -n python2-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python2*/site-packages/libvirt.py*
%{_libdir}/python2*/site-packages/libvirt_qemu.py*
%{_libdir}/python2*/site-packages/libvirt_lxc.py*
%{_libdir}/python2*/site-packages/libvirtmod*
%{_libdir}/python2*/site-packages/*egg-info

%if %{with_python3}
%files -n python3-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python3*/site-packages/libvirt.py*
%{_libdir}/python3*/site-packages/libvirtaio.py*
%{_libdir}/python3*/site-packages/libvirt_qemu.py*
%{_libdir}/python3*/site-packages/libvirt_lxc.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_qemu.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_lxc.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirtaio.cpython-*.py*
%{_libdir}/python3*/site-packages/libvirtmod*
%{_libdir}/python3*/site-packages/*egg-info
%endif

%changelog
* Tue Dec  5 2017 Daniel P. Berrange <berrange@redhat.com> - 3.10.0-1
- Update to 3.10.0 release

* Fri Nov  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.9.0-1
- Update to 3.9.0 release

* Wed Oct  4 2017 Daniel P. Berrange <berrange@redhat.com> - 3.8.0-1
- Update to 3.8.0 release

* Mon Sep  4 2017 Daniel P. Berrange <berrange@redhat.com> - 3.7.0-1
- Update to 3.7.0 release

* Fri Aug 11 2017 Daniel P. Berrange <berrange@redhat.com> - 3.6.0-2
- Rename sub-RPMs to python2-libvirt & python3-libvirt
- Re-add py3 conditionals for benefit of RHEL/CentOS builds

* Thu Aug 10 2017 Daniel P. Berrange <berrange@redhat.com> - 3.6.0-1
- Update to 3.6.0 release
- Always build py3 package

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.5.0-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul  6 2017 Daniel P. Berrange <berrange@redhat.com> - 3.5.0-1
- Update to 3.5.0 release

* Mon Jun  5 2017 Daniel P. Berrange <berrange@redhat.com> - 3.4.0-1
- Update to 3.4.0 release

* Mon May  8 2017 Daniel P. Berrange <berrange@redhat.com> - 3.3.0-1
- Update to 3.3.0 release

* Mon Apr  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-1
- Update to 3.2.0 release

* Fri Mar  3 2017 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-1
- Update to 3.1.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Daniel P. Berrange <berrange@redhat.com> - 3.0.0-1
- Update to 3.0.0 release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-2
- Rebuild for Python 3.6

* Mon Dec  5 2016 Daniel P. Berrange <berrange@redhat.com> - 2.5.0-1
- Update to 2.5.0 release

* Wed Nov  2 2016 Daniel P. Berrange <berrange@redhat.com> - 2.4.0-1
- Update to 2.4.0 release

* Thu Oct  6 2016 Daniel P. Berrange <berrange@redhat.com> - 2.3.0-1
- Update to 2.3.0 release

* Mon Sep  5 2016 Daniel P. Berrange <berrange@redhat.com> - 2.2.0-1
- Update to 2.2.0 release

* Tue Aug  2 2016 Daniel P. Berrange <berrange@redhat.com> - 2.1.0-1
- Update to 2.1.0 release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul  1 2016 Daniel P. Berrange <berrange@redhat.com> - 2.0.0-1
- Update to 2.0.0 release

* Mon Jun  6 2016 Daniel P. Berrange <berrange@redhat.com> - 1.3.5-1
- Update to 1.3.5 release

* Mon May 02 2016 Cole Robinson <crobinso@redhat.com> - 1.3.4-1
- Rebased to version 1.3.4

* Wed Apr 20 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.3-2
- Restore the setting of documentation to be non-executable.  Executable
  documentation introduces spurious dependencies (in this case, making
  the python3 package depend on python2).

* Thu Apr 07 2016 Cole Robinson <crobinso@redhat.com> - 1.3.3-1
- Rebased to version 1.3.3

* Tue Mar  1 2016 Daniel P. Berrange <berrange@redhat.com> - 1.3.2-2
- Ensure we build against new enough libvirt

* Tue Mar  1 2016 Daniel P. Berrange <berrange@redhat.com> - 1.3.2-1
- Update to 1.3.2 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Daniel P. Berrange <berrange@redhat.com> - 1.3.1-1
- Update to 1.3.1 release

* Fri Dec 11 2015 Daniel P. Berrange <berrange@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Nov 11 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.21-1
- Update to 1.2.21 release

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov  3 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.20-2
- Remove executable bit on documentation so it doesn't pull in extra
  dependencies.  This satisfies guidelines and fixes the problem of
  the libvirt-python3 package requiring python2.

* Fri Oct 02 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.20-1
- Update to 1.2.20 release

* Thu Sep 03 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.19-1
- Update to 1.2.19 release

* Sun Aug 09 2015 Cole Robinson <crobinso@redhat.com> - 1.2.18-1
- Rebased to version 1.2.18

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.16-1
- Update to 1.2.16 release

* Mon May 04 2015 Cole Robinson <crobinso@redhat.com> - 1.2.15-1
- Rebased to version 1.2.15

* Thu Apr 02 2015 Cole Robinson <crobinso@redhat.com> - 1.2.14-1
- Rebased to version 1.2.14

* Sun Mar 22 2015 Cole Robinson <crobinso@redhat.com> - 1.2.13-1
- Rebased to version 1.2.13

* Tue Jan 27 2015 Daniel P. Berrange <berrange@redhat.com> - 1.2.12-1
- Update to v1.2.12 release

* Mon Dec 15 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.11-1
- Update to v1.2.11 release

* Fri Dec 12 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.10-2
- Include upstream patch to add .c_pointer() method to classes.

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 1.2.10-1
- Update to v1.2.10

* Wed Oct  1 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.9-1
- Update to 1.2.9 release

* Mon Sep  8 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.8-1
- Update to 1.2.8 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Cole Robinson <crobinso@redhat.com> - 1.2.7-1
- Rebased to version 1.2.7

* Wed Jul  2 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.6-1
- Update to 1.2.6 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.5-1
- Update to 1.2.5 release

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May  6 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.4-1
- Update to 1.2.4 release

* Mon Apr  7 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.3-1
- Update to 1.2.3 release
- Run tests during build

* Mon Mar  3 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.2-1
- Update to 1.2.2 release

* Tue Jan 21 2014 Daniel P. Berrange <berrange@redhat.com> - 1.2.1-1
- Update to 1.2.1 release
- Add libvirt-python3 package

* Mon Nov 25 2013 Daniel P. Berrange <berrange@redhat.com> - 1.2.0-1
- Initial package after split from libvirt RPM (rhbz #1034347)
