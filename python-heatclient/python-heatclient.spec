Name:    python-heatclient
Version: 0.2.9
Release: 3%{?dist}
Summary: Python API and CLI for OpenStack Heat

Group:   Development/Languages
License: ASL 2.0
URL:     http://pypi.python.org/pypi/python-heatclient
Source0: http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=0.2.9
#
Patch0001: 0001-Nuke-pbr-requirements-handling.patch
Patch0002: 0002-Remove-runtime-dependency-on-python-pbr.patch

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr

Requires: python-argparse
Requires: python-httplib2
Requires: python-iso8601
Requires: python-keystoneclient
Requires: python-prettytable
Requires: python-six
Requires: PyYAML

%description
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

%package doc
Summary: Documentation for OpenStack Heat API Client
Group:   Documentation

BuildRequires: python-sphinx

%description doc
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

This package contains auto-generated documentation.

%prep
%setup -q

%patch0001 -p1
%patch0002 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATHEATCLIENTVERSION/%{version}/ heatclient/__init__.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config.
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
echo "%{version}" > %{buildroot}%{python_sitelib}/heatclient/versioninfo

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/heatclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/heat
%{python_sitelib}/heatclient
%{python_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Thu Jul 10 2014 Derek Higgins <derekh@redhat.com> - 0.2.9-3
- Remove patches that are merged upstream and update others.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.2.9-1
- Update to upstream 0.2.9

* Mon Jan 06 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.2.6-3
- Add support for resource_types

* Tue Dec 10 2013 Jeff Peeler <jpeeler@redhat.com> 0.2.6-2
- Update to upstream version 0.2.6
- New dependency: python-six
- Remove runtime dependency on python-pbr

* Wed Nov 06 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-1
- Update to upstream version 0.2.5

* Mon Sep 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.4-1
- Update to upstream version 0.2.4.
- Add BuildRequires: python2-devel.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-1
- Updated to upstream version 0.2.3.
- Add new dependency: PyYAML.
- Add new build requires: python-d2to1 and python-pbr.
- Remove requirements.txt file.
- Generate versioninfo file.

* Mon Mar 11 2013 Steven Dake <sdake@redhat.com> 0.2.1-1
- copied from python-novaclient spec file and tailored to suit
