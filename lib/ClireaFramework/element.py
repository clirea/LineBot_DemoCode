
class EnumElement():
    """
    EnumElementクラスは、Enumの要素を定義するクラスです。
    """
    class VoiceOrTextIDs():
        """VoiceOrTextIDsクラスは、ユーザーがテキストか音声かを定義するクラスです。"""
        Text = 0
        Voice = 1


    class SystemRoleIDs():
        """SystemRoleIDsクラスは、ChatGPTとのメッセージのロールを定義するクラスです。"""
        system = 1
        assistant = 2
        user = 3