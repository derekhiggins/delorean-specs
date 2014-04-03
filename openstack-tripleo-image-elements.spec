# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:		openstack-tripleo-image-elements
Summary:	OpenStack TripleO Image Elements for diskimage-builder
Version:	0.6.3
Release:	6%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://wiki.openstack.org/wiki/TripleO
Source0:	http://tarballs.openstack.org/tripleo-image-elements/tripleo-image-elements-%{version}.tar.gz

# https://review.openstack.org/#/c/81368/
# git format-patch -1 77471bc5f5abb9b950f8e401634d5d2ef0a856a6
Patch0001:	0001-Remove-mostly-empty-directories.patch

# https://review.openstack.org/#/c/81804/
# git format-patch -1 c787432bc589cced563e4b565d76f000f8f5ef77
Patch0002:	0002-Fix-tgt-target-in-cinder-element.patch

# https://review.openstack.org/#/c/81927/
# git format-patch -1 3c843ec24d7d76c5a2203575f4284585467ae603
Patch0003:	0003-Enable-os-collect-config-for-the-package-install.patch

# No review for this upstream yet, but we need this to have a working horizon
# from packages install.
Patch0004:	0004-Fix-horizon-local_settings.py.patch

# https://review.openstack.org/#/c/81901/
# git format-patch -1 f21444ce2f453608a48e40b5750652caee2776a0
Patch0005:	0005-Custom-service-file-is-not-needed-for-qpidd-on-syste.patch

# https://review.openstack.org/#/c/81908/
# git format-patch -1 4c4f957f63218a8afdc0cddaad1d412d97103f6e
Patch0006:	0006-qpidd-user-should-own-sasldb-file.patch

# We can't run neutron-db-manage....upgrade head in reset-db from boot-stack
# due to this bug:
# https://bugs.launchpad.net/neutron/+bug/1254246
# The fix is merged: https://review.openstack.org/#/c/61663/
# However that fix is not in openstack-neutron from rdo icehouse. It will only
# be in the icehouse-3 package which is not yet available.
Patch0007:	0007-No-neutron-db-manage-upgrade-head.patch

# https://review.openstack.org/82387
# git format-patch -1 3769f6c6c393a62a33a3b7c680943d3ddc70eaeb
Patch008:	0008-Add-missing-x.patch

# https://review.openstack.org/82529
# git format-patch -1 2e37cf5ba9499ae99d86f017ecb9cf72a206a022
Patch0009:	0009-Create-and-use-libvirtd-group-for-package-install.patch

# No service for swift-container-sync exists in rdo, temporarily patch the
# enable and restart for this service out until we figure out the right fix.
# https://review.openstack.org/#/c/82625/
Patch0010:	0010-No-swift-continer-sync-service.patch

# Workaround for:
# https://bugzilla.redhat.com/show_bug.cgi?id=1080438
# /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini should be in the neutron group.
# Should probably be submitted upstream if we don't get a fixed RDO package.
Patch0011:	0011-ovs-neutron-plugin-ini-neutron-group

# openstack-cinder no longer requires scsi-target-utils, so we must install the
# package manually.
# Once upstream is refactored into cinder-tgt and cinder-lio support, we can
# just build images with the element we need:
# https://review.openstack.org/#/c/78462/
Patch0012:	0012-cinder-install-tgt.patch

# https://review.openstack.org/#/c/82804/
# git format-patch -1 1f3d64e5a21f0a9e32d76d0fb1cdf6c68f0b5614
Patch0013:	0013-Expose-dnsmasq-options.patch

# Patch cinder.conf to set lock_path, volumes_dir, iscsi_helper.
# Needs to be submitted upstream.
Patch0014:	0014-Cinder-conf-patch.patch

# Next 5 patches are fixes for SELinux support.
# https://review.openstack.org/#/c/84949/
Patch0015:	0015-Relabel-tftpboot-if-selinux-is-used.patch
# https://review.openstack.org/#/c/82981/
Patch0016:	0016-Update-keystone-s-selinux-policies.patch
# https://review.openstack.org/#/c/82980/
Patch0017:	0017-Update-neutron-s-selinux-policies.patch
# https://review.openstack.org/#/c/82978/
Patch0018:	0018-Update-glance-s-selinux-policies.patch
# https://review.openstack.org/#/c/82976/
Patch0019:	0019-Update-nova-s-selinux-policies.patch

BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python-d2to1
BuildRequires:	python-pbr

Requires:	diskimage-builder

%description
OpenStack TripleO Image Elements is a collection of elements for
diskimage-builder that can be used to build OpenStack images for the TripleO
program.

%prep
%setup -q -n tripleo-image-elements-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

# remove .git-keep-empty files that get installed
find %{buildroot} -name .git-keep-empty | xargs rm -f

%files
%doc LICENSE
%doc README.md
%doc AUTHORS
%doc ChangeLog
%{python_sitelib}/tripleo_image_elements*
%{_datadir}/tripleo-image-elements

%changelog
* Thu Apr 03 2014 James Slagle <jslagle@redhat.com> - 0.6.3-6
- Add patches for improved SELinux support.

* Thu Mar 27 2014 James Slagle <jslagle@redhat.com> - 0.6.3-5
- Add patch for cinder.conf

* Wed Mar 26 2014 James Slagle <jslagle@redhat.com> - 0.6.3-4
- Fix 0002-Fix-tgt-target-in-cinder-element.patch, which was misgenerated
  before

* Tue Mar 25 2014 James Slagle <jslagle@redhat.com> - 0.6.3-3
- Add additional patches for some needed workarounds.

* Sun Mar 23 2014 James Slagle <jslagle@redhat.com> - 0.6.3-2
- Add Patch 0008-Add-missing-x.patch
- Add Patch 0009-Create-and-use-libvirtd-group-for-package-install.patch

* Fri Mar 21 2014 James Slagle <jslagle@redhat.com> - 0.6.3-1
- Rebase onto 0.6.3

* Tue Mar 18 2014 James Slagle <jslagle@redhat.com> - 0.6.0-4
- Add patch 0018-Remove-mostly-empty-directories.patch

* Tue Mar 11 2014 James Slagle <jslagle@redhat.com> - 0.6.0-3
- Update based on review feedback
- Added patch 0017-Add-missing-x.patch

* Mon Feb 24 2014 James Slagle <jslagle@redhat.com> - 0.6.0-2
- Add patches for swift package support.

* Thu Feb 20 2014 James Slagle <jslagle@redhat.com> - 0.6.0-1
- Update to 0.6.0 upstream release.

* Mon Feb 17 2014 James Slagle <jslagle@redhat.com> - 0.5.1-1
- Initial rpm build.
