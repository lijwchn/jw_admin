class CommonException(Exception):
    def __init__(
            self,
            message: str = "操作失败",
            success: bool = False,
            code: int = 500,
            status_code: int = 500,
    ) -> None:
        self.code = code
        self.message = message
        self.success = success
        self.status_code = status_code
