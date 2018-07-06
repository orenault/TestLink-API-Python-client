from testlink import TestLinkHelper
from robot.libraries.BuiltIn import BuiltIn


reportTCResultParams = [
    'testcaseid', 'testplanid', 'buildname', 'status', 'notes', 'testcaseexternalid', 'buildid', 'platformid',
    'platformname', 'guess', 'bugid', 'custumfields', 'overwrite', 'user', 'execduration', 'timestamp', 'steps',
    'devkey']
robot_report_params = {str(param): 'testlink' + str(param) for param in reportTCResultParams}


def setdefault_if_not_none(di, key, val):
    if key not in di:
        if val is not None:
            di[key] = val


class RobotTestLinkHelper(TestLinkHelper):
    """
    We preface all testlink inputs with 'testlink'.

    So, to pass the serverurl as a variable in a robot test set the variable ${testlinkserverurl}.

    This is to avoid polluting the robot framework variable namespace with common variable names.
    """
    def _get_param_from_robot(self, robot_variable):
        """Returns the found robot variable, defaults to None."""
        return BuiltIn().get_variable_value("${" + str(robot_variable) + "}")

    def _get_missing_params_from_robot_variables(self, param_dict):
        for testlink_param, robot_variable in robot_report_params.items():
            setdefault_if_not_none(param_dict, testlink_param, self._get_param_from_robot(robot_variable))

    def _setParamsFromRobot(self):
        """
        fill empty slots from robot variables
        _server_url <- TESTLINK_API_PYTHON_SERVER_URL <- robot_variable`testlinkserverurl`
        _devkey     <- TESTLINK_API_PYTHON_DEVKEY     <- robot_variable`testlinkdevkey`
        _proxy      <- http_proxy                     <- robot_variable`testlinkproxy`

        If robot variables are not defined, values are kept as None for other _setParams* to handle.
        """
        if self._server_url is None:
            self._server_url = self._get_param_from_robot('testlinkserverurl')
        if self._devkey is None:
            self._devkey = self._get_param_from_robot('testlinkdevkey')
        if not self._proxy:
            self._proxy = self._get_param_from_robot('testlinkproxy')

    def _setParams(self):
        """fill slots _server_url, _devkey and _proxy
        Priority:
        1. init args
        2. robot variables
        2. environment variables
        3. default values
        """
        self._setParamsFromRobot()
        super(RobotTestLinkHelper, self)._setParams()
