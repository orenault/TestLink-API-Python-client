from .robottestlinkhelper import RobotTestLinkHelper
from robot.api import logger as robot_logger
from testlink import TestlinkAPIGeneric
from testlink.testlinkerrors import TLResponseError


class testlinklistener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, test_prefix, dev_key, server, *report_kwargs, **also_conosle):
        """
        This is specifically for looking at testcaseexternalids in testcase documentation and sending results to all
        testcases found.

        If you would like to set a default input from the test itself you can add 'testlink' to the beginning of the
        parameter and it will select and add if it wasn't passed in at __init__.
        For example if you wanted to pass in the platformname you would set testlinkplatformname. This is to avoid
        robot name collisions with incredibly common variable names like user and timestamp.
        Note: dev_key is set during testlink connection and used as a default by the testlink library.
              So, if `testlinkdevkey` is passed in it will effectively take priority as the second positional arg
              dev_key is *not* put into report_kwargs. This is by design.

        Since kwargs are not supported in listeners you must pass in args with an equal sign between the key and the
        value (<argument>=<value).

        :param test_prefix: The letters preceding testlink numbers. ex. abc-1234 the test_prefix would be 'abc'
        :param dev_key: API key of the user running the tests
        :param server: The testlink server
        :param report_kwargs: These are args in the format `<argument>=<value>`.
        :param also_console: py2 support for non-positional kwargs. pass in also_console=<bool>. Defaults to True.
        """
        self.test_prefix = test_prefix
        self.dev_key = dev_key
        self.testlink_server = server

        # Listeners don't support real kwargs
        self.report_kwargs = {}
        for kwarg in report_kwargs:
            try:
                arg, value = kwarg.split('=')
            except ValueError:
                raise RuntimeError("Report kwarg was passed in without equal sign. '{}'".format(kwarg))
            if isinstance(value, list):
                raise RuntimeError("Report kwarg was passed in with multiple equal signs. '{}'".format(kwarg))
            self.report_kwargs[arg] = value

        self.also_console = also_conosle.get('also_console', True)

        self._tlh = self._tls = self._testcases = None

    @property
    def tls(self):
        if not self._tls:
            self.connect_testlink()
        return self._tls

    @property
    def tlh(self):
        if not self._tlh:
            self.connect_testlink()
        return self._tlh

    def connect_testlink(self):
        self._tlh = RobotTestLinkHelper(self.testlink_server, self.dev_key)
        self._tls = self._tlh.connect(TestlinkAPIGeneric)

    @property
    def testcases(self):
        if not self._testcases:
            self._testcases = self._get_testcases()
        return self._testcases

    def _get_testcases(self, test):
        return DocTestParser(self.test_prefix).get_testcases(test)

    def _get_testlink_status(self, test):
        # testlink accepts p/f for passed and failed
        status = 'f'
        if test.passed:
            status = 'p'
        return status

    def _get_kwargs(self):
        return ReportKwargs(self.tls, self.testcases, **self.report_kwargs)

    def end_test(self, data, test):
        rkwargs = self._get_kwargs()
        rkwargs['status'] = self._get_testlink_status(test)
        # This is supposed to default to true by the API spec, but doesn't on some testlink versions
        rkwargs.setdefault('guess', True)

        for testcase in self.testcases:
            resp = self.tls.reportTCResult(testcaseexternalid=testcase, **rkwargs)
            # Listeners don't show up in the log so setting also_console to False effectively means don't log
            robot_logger.info(resp, also_console=self.also_console)


class ReportKwargs(dict):
    def __init__(self, tlh, testcases=None, *args, **kwargs):
        super(ReportKwargs, self).__init__(*args, **kwargs)
        self.tlh = tlh
        self.testcases = testcases
        self._testplanname = self._testprojectid = self._testplanid = self._plan_testcases = None
        self._get_params_from_variables()

    def _get_params_from_variables(self):
        for testlink_param, robot_variable in robot_report_params.items():
            setdefault_if_truthy(self, testlink_param, BuiltIn().get_variable_value("${" + str(robot_variable) + "}"))

    def setup_testlink(self):
        self.ensure_testcases_in_plan()

    def ensure_testcases_in_plan(self):
        for testcase in self.testcases:
            if testcase not in self.plan_tc_ext_ids:
                self.tlh.addTestCaseToTestPlan(
                    self.testprojectid, self.testplanid, testcase, self.get_latest_tc_version(testcase),
                    platformid=self.platformid
                )

    @property
    def testprojectname(self):
        if not self.get('testprojectname'):
            try:
                self['testprojectname'] = self.tlh.getProjectIDByName(self['testprojectid'])
            except IndexError:
                raise RuntimeError('Need a testprojectname or id to generate other testlink arguments.')
        return self['testprojectname']

    @property
    def testprojectid(self):
        if not self.get('testprojectid'):
            try:
                self['testprojectid'] = self.tlh.getTestProjectByName(self.testprojectname)['id']
            except TypeError:
                # TODO: Should we generate a testproject?
                raise

        return self['testprojectid']

    @property
    def testplanid(self):
        if not self._testplanid:
            try:
                self._testplanid = self.tlh.getTestPlanByName(self.testprojectname, self.testplanname)[0]['id']
            except TypeError:
                self._testplanid = self.generate_testplanid()
        return self._testplanid

    def generate_testplanid(self):
        """This won't necessarily be able to create a testplanid. It requires a planname and projectname."""
        if 'testplanname' not in self:
            raise RuntimeError("Need testplanname to generate a testplan for results.")

        tp = self.tlh.createTestPlan(self['testplanname'], self.testprojectname)
        self['testplanid'] = tp[0]['id']
        return self['testplanid']

    @property
    def platformname(self):
        """Return a platformname added to the testplan if there is one."""
        pn_kwarg = self.get('platformname')
        if pn_kwarg:
            self.generate_platformname(pn_kwarg)
        return pn_kwarg

    def generate_platformname(self, platformname):
        if platformname not in self.tlh.getTestPlanPlatforms(self.testplanid):
            try:
                self.tlh.createPlatform(self['testplanname'], platformname)
            except TLResponseError as e:
                if e.code == 12000:
                    # platform already exists
                    pass
                else:
                    raise
            self.tlh.addPlatformToTestPlan(self.testplanid, platformname)

    @property
    def platformid(self):
        if not self.get('platformid'):
            self['platformid'] = self.getPlatformID(self.platformname, self.testprojectid)
        return self['platformid']

    def getPlatformID(self, platformname, projectid, _ran=False):
        platforms = self.tlh.getProjectPlatforms(projectid)
        # key is duplicate info from key 'name' of dictionary
        for _, platform in platforms.items:
            if platform['name'] == platformname:
                return platform['id']
        else:
            if _ran:
                raise RuntimeError("Couldn't find platformid for {}.{} after creation.".format(projectid, platformname))
            self.generate_platformname(platformname)
            self.getPlatformID(platformname, projectid, _ran=True)

    @property
    def plan_tc_ext_ids(self):
        if not self._plan_testcases:
            self._plan_testcases = set()
            tc_dict = self.tlh.getTestCasesForTestPlan(self.testplanid)
            for _, platform in tc_dict.items():
                for k, v in platform.items():
                    self._plan_testcases.add(v['full_external_id'])
        return self._plan_testcases

    def get_latest_tc_version(self, testcaseexternalid):
        return self.tlh.getTestCase(None, testcaseexternalid=testcaseexternalid)[0]['version']
