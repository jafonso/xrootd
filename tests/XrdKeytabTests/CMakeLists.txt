add_executable(xrootd-keytab-tests XRootDKeytabTests.cc)

target_link_libraries(xrootd-keytab-tests GTest::GTest GTest::Main)

gtest_discover_tests(xrootd-keytab-tests
        PROPERTIES DISCOVERY_TIMEOUT 10)