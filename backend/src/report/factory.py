from src.report.core import ReportType
from src.report.implements.base import BaseReportGenerator


class ReportFactory:
    __report_map = {
        ReportType.BASE: BaseReportGenerator
    }

    @classmethod
    def create(cls, report_type: ReportType):
        if not isinstance(report_type, ReportType):
            raise TypeError(f"A ReportFactory can only create child classes based on the ReportType\nGot {type(report_type)}, expect {ReportType}")
        if report_type not in cls.__report_map:
            raise KeyError(f"Type {report_type} not in factory map")

        return cls.__report_map[report_type]()


report_factory = ReportFactory()