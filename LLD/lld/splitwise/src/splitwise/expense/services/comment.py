class Comment:

    def __init__(self, user_id: int, comment_content: str, expense_id: int) -> None:
        self.__user_id: int = user_id
        self.__comment_content: str = comment_content
        self.__expense_id: int = expense_id

    def get_user_id(self) -> int:
        return self.__user_id

    def get_comment_content(self) -> str:
        return self.__comment_content

    def get_expense_id(self) -> int:
        return self.__expense_id

    def __repr__(self) -> str:
        return f'Comment(User({self.__user_id}), Expense({self.__expense_id}): {self.__comment_content})'
