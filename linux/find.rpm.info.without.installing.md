
* get complete info

  ```
  # rpm -qpi uuid-1.6.1-10.el6.x86_64.rpm
  Name        : uuid                         Relocations: (not relocatable)
  Version     : 1.6.1                             Vendor: CentOS
  Release     : 10.el6                        Build Date: Sun 22 Aug 2010 03:16:27 AM EDT
  Install Date: (not installed)               Build Host: c6b1.bsys.dev.centos.org
  Group       : System Environment/Libraries   Source RPM: uuid-1.6.1-10.el6.src.rpm
  Size        : 115448                           License: MIT
  Signature   : RSA/8, Sun 03 Jul 2011 01:04:41 AM EDT, Key ID 0946fca2c105b9de
  Packager    : CentOS BuildSystem <http://bugs.centos.org>
  URL         : http://www.ossp.org/pkg/lib/uuid/
  Summary     : Universally Unique Identifier library
  Description :
  OSSP uuid is a ISO-C:1999 application programming interface (API)
  and corresponding command line interface (CLI) for the generation
  of DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally
  Unique Identifier (UUID). It supports DCE 1.1 variant UUIDs of version
  1 (time and node based), version 3 (name based, MD5), version 4
  (random number based) and version 5 (name based, SHA-1). Additional
  API bindings are provided for the languages ISO-C++:1998, Perl:5 and
  PHP:4/5. Optional backward compatibility exists for the ISO-C DCE-1.1
  and Perl Data::UUID APIs.
  ```

* get specific attribute
  
  ```
  rpm -qp --queryformat '%{Name},%{Version},%{License},%{Summary}\n' uuid-1.6.1-10.el6.x86_64.rpm
  uuid,1.6.1,MIT,Universally Unique Identifier library
  ```
