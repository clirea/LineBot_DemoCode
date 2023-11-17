class SystemErrorMessage:
    def __init__(self, lang):
        self.lang = lang

    def get(self, error_code):
        if self.lang == "ja":
            return SystemErrorMessageJA[error_code]
        else:
            return SystemErrorMessageEn[error_code]
        
SystemErrorMessageJA = {
    "db_error": "データベース接続エラー：データベースへの接続に失敗しました。開発者に連絡してください。",
    "msg_parse_error": "メッセージ解析エラー：受信したメッセージを解析できませんでした。開発者に連絡してください。",
    "gpt_timeout": "GPT接続タイムアウト：GPT-3サービスへの接続がタイムアウトしました。しばらく待ってからもう一度試してみてください。",
    "gpt_error": "GPT接続エラー：GPT-3サービスに接続できませんでした。開発者に連絡してください。"
}

SystemErrorMessageEn = {
    "db_error": "Database Error: Failed to connect to the database. Please contact the developer.",
    "msg_parse_error": "Message Parse Error: Failed to parse the received message. Please contact the developer.",
    "gpt_timeout": "GPT Connection Timeout: Connection to the GPT-3 service timed out. Please try again later.",
    "gpt_error": "GPT Connection Error: Failed to connect to the GPT-3 service. Please contact the developer."
}