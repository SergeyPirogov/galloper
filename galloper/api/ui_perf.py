from flask_restful import Resource

from galloper.database.models.project import Project
from galloper.database.models.ui_report import UIReport
from galloper.utils.api_utils import build_req_parser


class UIReportsAPI(Resource):
    post_rules = (
        dict(name="test_name", type=str, location="json"),
        dict(name="time", type=str, location="json")
    )

    put_rules = (
        dict(name="time", type=str, location="json"),
    )

    def __init__(self):
        self.__init_req_parsers()

    def __init_req_parsers(self):
        self._parser_post = build_req_parser(rules=self.post_rules)
        self._parser_put = build_req_parser(rules=self.put_rules)

    def get(self):
        return {'task': 'Hello world'}

    def post(self, project_id: int):
        args = self._parser_post.parse_args()
        project = Project.query.get_or_404(project_id)

        report = UIReport(
            test_name=args["test_name"],
            project_id=project.id,
            start_time=args["time"],
            is_active=True
        )

        report.insert()

        return report.to_json()

    def put(self, project_id: int, report_id: int):
        args = self._parser_put.parse_args()

        report = UIReport.query.filter_by(project_id=project_id, id=report_id).first_or_404()
        report.is_active = False
        report.stop_time = args["time"]
        report.commit()

        return report.to_json()
