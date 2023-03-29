
class Uploader:
    @staticmethod
    def upload_logo_game_company(instance, filename):
        return f"companies/{instance}/{filename}"
   

    @staticmethod
    def upload_logo_game_category(instance, filename):
        return f"game-categories/{instance}/{filename}"

    @staticmethod
    def upload_image_game(instance, filename):
        return f"games/{instance.game}/{filename}"
    

    @staticmethod
    def upload_logo_game_tournament_category(instance, filename):
        return f"game-tournaments-categories/{instance}/{filename}"

    @staticmethod
    def upload_image_game_tournament(instance, filename):
        return f"game-tournaments/{instance.gametournament}/{filename}"