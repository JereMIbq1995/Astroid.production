from genie.script.action import OutputAction
from genie.services.PygameAudioService import PygameAudioService

class PlayBackgroundMusicAction(OutputAction):
    def __init__(self, priority, path):
        super().__init__(priority)
        self._audio_service = PygameAudioService()
        self._background_playing = False
        self._path = path
    
    def execute(self, actors, actions, clock, callback):
        if not self._background_playing:
            self._audio_service.play_sound(self._path, 1)
            self._background_playing = True