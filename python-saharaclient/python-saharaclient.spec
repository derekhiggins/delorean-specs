%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:             python-saharaclient
Version:          0.7.0
Release:          4%{?dist}
Provides:         python-savannaclient = %{version}-%{release}
Obsoletes:        python-savannaclient <= 0.5.0-2
Summary:          Client library for OpenStack Sahara API
License:          ASL 2.0
URL:              https://launchpad.net/sahara
Source0:          http://tarballs.openstack.org/python-saharaclient/python-saharaclient-%{version}.tar.gz
Patch0001:        0001-remove-runtime-dep-on-python-pbr.patch
BuildArch:        noarch

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-d2to1
BuildRequires:    python-pbr >= 0.5.19


Requires:         python-iso8601
Requires:         python-requests
Requires:         python-six
Requires:         python-setuptools
Requires:         python-babel
Requires:         python-netaddr


%description
Python client library for interacting with OpenStack Sahara API.


%prep
%setup -q -n %{name}-%{version}

%patch0001 -p0

sed -i s/REDHAT_SAHARACLIENT_VERSION/%{version}/ saharaclient/version.py
sed -i s/REDHAT_SAHARACLIENT_RELEASE/%{release}/ saharaclient/version.py

rm -rf python_saharaclient.egg-info
rm -rf test-requirements.txt


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
# Building on koji with virtualenv requires test-requirements.txt and this
# causes errors when trying to resolve the package names, also turning on pep8
# results in odd exceptions from flake8.
# TODO mimccune fix up unittests
# sh run_tests.sh --no-virtual-env --no-pep8

%files
%doc LICENSE ChangeLog README.rst
%{_bindir}/sahara
%{python_sitelib}/saharaclient
%{python_sitelib}/*.egg-info


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 0.7.0-3
- Changing the version/release temp for patch

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 0.7.0-2
- Adding patch to remove runtime pbr dep

* Thu Apr  3 2014 Michael McCune <mimccune@redhat> - 0.7.0-1
- 0.7.0 release and rename from python-savannaclient

* Sat Mar  1 2014 Matthew Farrellee <matt@redhat> - 0.5.0-1
- 0.5.0 release

* Fri Jan 17 2014 Matthew Farrellee <matt@redhat> - 0.4.1-1
- 0.4.1 release - introduced Savanna CLI

* Sun Oct 20 2013 Matthew Farrellee <matt@redhat> - 0.3-1
- 0.3 release

* Fri Oct 11 2013 Matthew Farrellee <matt@redhat> - 0.3-0.2
- 0.3 rc3 build

* Sat Aug 17 2013 Matthew Farrellee <matt@redhat> - 0.3-0.1.f816386git
- Initial package
