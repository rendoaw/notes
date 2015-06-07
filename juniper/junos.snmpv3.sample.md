sample config
```
user@mx04> show configuration snmp | no-more
location "lab";
v3 {
    usm {
        local-engine {
            user user1_noauth {
                authentication-none;
            }
            user user2_authnopriv {
                authentication-md5 {
                    authentication-key "$9$LZkxbsgoJUik8X-wY2GU/CAp0IylKW87n/lKMW-d.PfzF/BIEhylmfSrKv7NjHk.Tz3nCOIECA0IESeKoJZD.PQz6u0IGDHmTQn6yleW87wYgaGDg4Tzn/0OVwsg4ZmfT3/CoJHm5Qn6lKv8-V24aUikvW7VY2GU.P5F9ABIEyevB1wY4ojimfTQ9A"; ## SECRET-DATA
                }
                privacy-none;
            }
            user user3_authpriv {
                authentication-md5 {
                    authentication-key "$9$v-OWNdwYgaGDKMX-VboaFn69A0EcyeK8QFcyleXxikqf5Fp0B1EcHqRhyr8LZUDimfTQnt0Bn6A0BRSyYg4JikPfzCA0oJUHmPQzEcSeK8-Vw2oJwsmfQFAt7-dws4HqmTFnYgUH.PQzcyrKX7bs2aGDre87Vboaik.536p0BESrpu-VsYZGHqmP36"; ## SECRET-DATA
                }
                privacy-des {
                    privacy-key "$9$CCI2pu1SyKW87/CM87-ws36/ApBEhrW87CtWLN-2gn/9A1RcSev8XIRhrvMN-k.m536O1RcSeQFEcSrvMJGUjHmQFn/ApTQhSreXxjHk.mTFn/01R6/revMXxjHkqTz9CuIRS/9pBEhKv8X7db2JZji.P7-ikmfzFAp0BcyrevL7-/Cu1hSeKxNdsYo"; ## SECRET-DATA
                }
            }
            user user4_authpriv_sha {
                authentication-sha {
                    authentication-key "$9$gjaJDmPQF69TQ6Apu1IEcyeK87-V2oJRhgoGUHk5QFntuSreLX-yrvL7-2gz3n6uOrevW87EhyKMW-dfTQ3Ctp0BSlKfThSylMWoJZji.f5F9Cu6/tO1EyrJGUHP5n/CtO1ikuOBRSyKM87bs24aGjHKMoJDjPfTz369p0BIRSrfTRhrlMWjHkq5Q"; ## SECRET-DATA
                }
                privacy-aes128 {
                    privacy-key "$9$gCaJDHqmPQFji9Ap0hcwY2gZUiHmF39kqEcylMWUji.mTF39pO1zFnCu0hcoJZDjqQz6pu1CAxNdVY24aZGDkQFnpu1At7-wYoa36/CA0ylKLX-vMik.mTQFn/tBIrevL7-MWjH.PQzSrlvxN4aZUHqKMik.mTQlKvWNd4aZDjqJZFn6/tpRhSleW"; ## SECRET-DATA
                }
            }
            user user5 {
                authentication-md5 {
                    authentication-key "$9$sR2ZUik.fQFwYoGDjPf1REcyKX7-bwgO17-Vboan/9pu1lKMWX769Lx-dg4TzFnAp0ORrKMREyKMLN-k.m5n/tpBSyKP5z6AtOBX7NbwgGDiqP5iHApO1yrJGUiHm69A01Rk.z6CtOB7-dwoJjHqfQFdbgJDjPfn/CuIElKMXNdleGDHkTQ69AtIE"; ## SECRET-DATA
                }
                privacy-aes128 {
                    privacy-key "$9$wu2gJiHm5T3VwfT36AtNdVs2aUDk5T3wY5Qn6u0-VbsJGji.PTzZGDkPfn6lKv8NdoJGji.X7UjikPfIEhSrvX7-Vs2LXDik.zFSrlKvL7-V4JGdVk.PfzFSrleLxbwgZGiVb2aUDmPTz3/CuIRSyKM36ylvWx7s24ajHk.PQ36VwgJDi.mFn/tpB"; ## SECRET-DATA
                }
            }
            user user6 {
                authentication-sha {
                    authentication-key "$9$J2UDkTQn/Ap3nA0B1hcylKW87VwYaGDSrJGiHmPFn/CO1evWN-wKvLNVwaJ69CA1RvWLx7VyrK8Xxwsz3n9uOBIEeM8z3reKMXxGDjq.5zF/pu1AtORhyKvDiHmQFCtuORh.P1RESeK8X7V24aZUiqm8XGDkqQz369ApBIEcSevz3SrvMXxqmPfFn"; ## SECRET-DATA
                }
                privacy-des {
                    privacy-key "$9$CuESpu1EcyrvWIR7-VwaJn/9C0BREyW87hcoJGDkqBIRSyKW87Vs2MWLNbwaJtu01IcvMXVb2N-fTzF/9Ap0O1hvWLVb2-d5Qn/tp8XxN-wGDimPQHkRhSyKvWLxdYgUjHm5QkqIESrvMZUDHfTAp0BEcikRhSyKvDiHqTzAp01Icu0WLXxdV4aZDjq"; ## SECRET-DATA
                }
            }
        }
    }
    vacm {
        security-to-group {
            security-model usm {
                security-name v3test {
                    group v3test;
                }
                security-name user1_noauth {
                    group v3test;
                }
                security-name user2_authnopriv {
                    group v3test_authnopriv;
                }
                security-name user3_authpriv {
                    group v3test_authpriv;
                }
                security-name user4_authpriv_sha {
                    group v3test_authpriv;
                }
                security-name user5 {
                    group v3test_authpriv;
                }
                security-name user6 {
                    group v3test_authpriv;
                }
            }
        }
        access {
            group v3test {
                default-context-prefix {
                    security-model any {
                        security-level none {
                            read-view v3testview;
                            write-view v3testview;
                            notify-view v3testview;
                        }
                    }
                }
            }
            group v3test_authnopriv {
                default-context-prefix {
                    security-model any {
                        security-level authentication {
                            read-view v3testview;
                            write-view v3testview;
                            notify-view v3testview;
                        }
                    }
                }
            }
            group v3test_authpriv {
                default-context-prefix {
                    security-model any {
                        security-level privacy {
                            read-view v3testview;
                            write-view v3testview;
                            notify-view v3testview;
                        }
                    }
                }
            }
        }
    }
    snmp-community v3test {
        security-name v3test;
    }
}
view v3testview {
    oid system include;
    oid .1 include;
}
community comm1 {
    authorization read-only;
}
trap-group comm1-dev {
    version v2;
    targets {
        192.25.152.29;
        192.25.152.74;
        192.25.152.76;
    }
}
```

sample query
```
1. User "user1_noauth" will not require password
snmpwalk -On -v 3 -u user1_noauth -c v3test 192.25.152.44

2. User "user2_authnopriv" requires authentication using md5 password "jnprpass" but no privacy/no encryption
snmpwalk -v3 -u user2_authnopriv -a MD5 -A jnprpass -l authNoPriv 192.25.152.44

3. User "user3_authpriv" requires authentication using md5 password "jnprpass" and privacy/encryption using DES with key = jnprprivacy
snmpwalk -v3 -u user3_authpriv -a MD5 -A jnprpass -x DES -X jnprprivacy -l authPriv 192.25.152.44
```