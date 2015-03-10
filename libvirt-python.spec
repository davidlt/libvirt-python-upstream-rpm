
%define with_python3 0
%if 0%{?fedora} > 18
%define with_python3 1
%endif

Summary: The libvirt virtualization API python2 binding
Name: libvirt-python
Version: 1.2.9
Release: 2%{?dist}%{?extra_release}
Source0: http://libvirt.org/sources/python/%{name}-%{version}.tar.gz

# Fix virDomainBlockCopy (bz #1199682)
Patch0001: 0001-flags-cannot-get-right-value-for-blockCopy-function.patch
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
BuildRequires: libvirt-devel >= 0.9.11
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

%if %{with_python3}
%package -n libvirt-python3
Summary: The libvirt virtualization API python3 binding
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries

%description -n libvirt-python3
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%prep
%setup -q

# Fix virDomainBlockCopy (bz #1199682)
%patch0001 -p1

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
rm -f %{buildroot}%{_libdir}/python*/site-packages/*egg-info

%check
%{__python} setup.py test
%if %{with_python3}
%{__python3} setup.py test
%endif

%files
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python2*/site-packages/libvirt.py*
%{_libdir}/python2*/site-packages/libvirt_qemu.py*
%{_libdir}/python2*/site-packages/libvirt_lxc.py*
%{_libdir}/python2*/site-packages/libvirtmod*

%if %{with_python3}
%files -n libvirt-python3
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{_libdir}/python3*/site-packages/libvirt.py*
%{_libdir}/python3*/site-packages/libvirt_qemu.py*
%{_libdir}/python3*/site-packages/libvirt_lxc.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_qemu.cpython-*.py*
%{_libdir}/python3*/site-packages/__pycache__/libvirt_lxc.cpython-*.py*
%{_libdir}/python3*/site-packages/libvirtmod*
%endif

%changelog
* Tue Mar 10 2015 Cole Robinson <crobinso@redhat.com> - 1.2.9-2
- Fix virDomainBlockCopy (bz #1199682)

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
