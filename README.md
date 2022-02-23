# Bull Freeware Github Repository

**ATTENTION!** It is inofficial repository. It has nothing to do with companies Bull or Atos!

Bull Freeware (https://www.bullfreeware.com) was one of the first sites with open source software, built for IBM AIX. 
They ported a lot of different software to AIX, but because of unknown reasons Atos decided to
close the site on March 01, 2022.

This repository is an attempt to save the work, done by brilliant engineers at Bull and later at Atos. 
You can find here SPEC-files, needed to recompile software, and patches for the software. All SPECs and
patches were downloaded from Bull Freeware site in February, 2022.

There are no plans to continue the work done by Bull/Atos. If you need fresh RPMs, visit IBM AIX Toolbox
for Open Source software (https://www.ibm.com/support/pages/aix-toolbox-open-source-software-downloads-alpha).

## Where to find binary RPMs

We saved binary RPMs too and made a YUM repository for your convinience. The whole archive of binary RPMs
can be found on https://dl.power-devops.com/bull/RPMS/.

### How to configure YUM to use the RPMs

```
[BullFreeware]
name=BullFreeware AIX generic repository
baseurl=https://dl.power-devops.com/bull/RPMS/ppc/
enabled=1
gpgcheck=0
```

```
[BullFreeware_noarch]
name=BullFreeware AIX noarch repository
baseurl=https://dl.power-devops.com/bull/RPMS/noarch/
enabled=1
gpgcheck=0
```

```
[BullFreeware_71]
name=BullFreeware AIX 7.1 repository
baseurl=https://dl.power-devops.com/bull/RPMS/ppc-7.1/
enabled=1
gpgcheck=0
```

```
[BullFreeware_72]
name=BullFreeware AIX 7.2 repository
baseurl=https://dl.power-devops.com/bull/RPMS/ppc-7.2/
enabled=1
gpgcheck=0
```

```
[BullFreeware_73]
name=BullFreeware AIX 7.3 repository
baseurl=https://dl.power-devops.com/bull/RPMS/ppc-7.3/
enabled=1
gpgcheck=0
```

## Where to find source RPMs

Source RPMs (SRPMs) can be found at https://dl.power-devops.com/bull/SRPMS/.
