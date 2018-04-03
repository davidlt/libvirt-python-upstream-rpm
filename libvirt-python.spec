# -*- rpm-spec -*-

# This spec file assumes you are building on a Fedora or RHEL version
# that's still supported by the vendor. It may work on other distros
# or versions, but no effort will be made to ensure that going forward
%define min_rhel 6
%define min_fedora 25

%if (0%{?fedora} && 0%{?fedora} >= %{min_fedora}) || (0%{?rhel} && 0%{?rhel} >= %{min_rhel})
    %define supported_platform 1
%else
    %define supported_platform 0
%endif

%define _with_python2 1
%if 0%{?fedora} > 29 || 0%{?rhel} > 7
%define _with_python2 0
%endif

%define _with_python3 0
%if 0%{?fedora} || 0%{?rhel} > 7
%define _with_python3 1
%endif

# Whether py2 packages are assumed to have python2- name prefix
%define py2_versioned_deps 0
%if 0%{?fedora} || 0%{?rhel} > 7
%define py2_versioned_deps 1
%endif

%{!?with_python2: %define with_python2 %{_with_python2}}
%{!?with_python3: %define with_python3 %{_with_python3}}

Summary: The libvirt virtualization API python2 binding
Name: libvirt-python
Version: 4.2.0
Release: 1%{?dist}%{?extra_release}
Source0: http://libvirt.org/sources/python/%{name}-%{version}.tar.gz
Url: http://libvirt.org
License: LGPLv2+
Group: Development/Libraries
BuildRequires: libvirt-devel == %{version}
%if %{with_python2}
%if %{py2_versioned_deps}
BuildRequires: python2-devel
BuildRequires: python2-nose
BuildRequires: python2-lxml
%else
BuildRequires: python-devel
BuildRequires: python-nose
BuildRequires: python-lxml
%endif
%endif
%if %{with_python3}
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: python3-lxml
%endif

# Don't want provides for python shared objects
%if %{with_python2}
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/.*\.so}
%endif
%if %{with_python3}
%{?filter_provides_in: %filter_provides_in %{python3_sitearch}/.*\.so}
%endif
%{?filter_setup}

%description
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%if %{with_python2}
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
%endif

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
%if ! %{supported_platform}
echo "This RPM requires either Fedora >= %{min_fedora} or RHEL >= %{min_rhel}"
exit 1
%endif

%if %{with_python2}
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%endif
%if %{with_python3}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
%endif

%install
%if %{with_python2}
%{__python} setup.py install --skip-build --root=%{buildroot}
%endif
%if %{with_python3}
%{__python3} setup.py install --skip-build --root=%{buildroot}
%endif

%check
%if %{with_python2}
%{__python} setup.py test
%endif
%if %{with_python3}
%{__python3} setup.py test
%endif

%if %{with_python2}
%files -n python2-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{python_sitearch}/libvirt.py*
%{python_sitearch}/libvirt_qemu.py*
%{python_sitearch}/libvirt_lxc.py*
%{python_sitearch}/libvirtmod*
%{python_sitearch}/*egg-info
%endif

%if %{with_python3}
%files -n python3-libvirt
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README COPYING COPYING.LESSER examples/
%{python3_sitearch}/libvirt.py*
%{python3_sitearch}/libvirtaio.py*
%{python3_sitearch}/libvirt_qemu.py*
%{python3_sitearch}/libvirt_lxc.py*
%{python3_sitearch}/__pycache__/libvirt.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_qemu.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirt_lxc.cpython-*.py*
%{python3_sitearch}/__pycache__/libvirtaio.cpython-*.py*
%{python3_sitearch}/libvirtmod*
%{python3_sitearch}/*egg-info
%endif

%changelog
* Tue Apr  3 2018 Daniel P. Berrangé <berrange@redhat.com> - 4.2.0-1
- Update to 4.2.0 release
- Set python2 to be disabled from Fedora 30 onwards

* Mon Mar  5 2018 Daniel P. Berrange <berrange@redhat.com> - 4.1.0-1
- Update to 4.1.0 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Daniel P. Berrange <berrange@redhat.com> - 4.0.0-1
- Update to 4.0.0 release

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
