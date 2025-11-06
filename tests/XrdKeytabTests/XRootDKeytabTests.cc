#include "XrdPfc/XrdPfcPathParseTools.hh"

#include <gtest/gtest.h>

namespace {
    constexpr FILE_PATH = "/tmp/cta-taped.sss.keytab"
}

class PathParseToolTest : public ::testing::Test {};

TEST_F(PathParseToolTest, SplitParser)
{
    XrdOucErrInfo eInfo;
    XrdSecsssKT *kTab;
    kTab = new XrdSecsssKT(&eInfo, Opt.KeyFile, XrdSecsssKT::isAdmin);
    EXPECT_TRUE(kTab);
}

