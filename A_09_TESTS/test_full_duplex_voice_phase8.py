from A_09_INTERFACE.voice_session import VoiceActivityDetector, VoiceSessionManager


class FakeSTT:
    def __init__(self, transcripts):
        self.transcripts = iter(transcripts)
        self.started = 0
        self.chunks = []
        self.cancelled = 0

    def start(self):
        self.started += 1

    def feed(self, audio):
        self.chunks.append(audio)

    def finish(self):
        return next(self.transcripts)

    def cancel(self):
        self.cancelled += 1


class FakeTTS:
    def __init__(self):
        self.spoken = []
        self.cancelled = 0

    def start(self, text):
        self.spoken.append(text)

    def cancel(self):
        self.cancelled += 1


class FakeCoordinator:
    def __init__(self):
        self.calls = []

    def execute(self, query, context=None):
        self.calls.append((query, context))
        return {"ok": True, "text": f"answer: {query}"}


def make_session(transcripts=("hello",)):
    coordinator, stt, tts = FakeCoordinator(), FakeSTT(transcripts), FakeTTS()
    manager = VoiceSessionManager(
        coordinator, stt, tts,
        VoiceActivityDetector(threshold=0.5, end_silence_chunks=2),
    )
    return manager, coordinator, stt, tts


def finish_turn(manager):
    manager.accept_audio(b"voice-1", 0.8)
    manager.accept_audio(b"voice-2", 0.9)
    manager.accept_audio(b"pause-1", 0.0)
    return manager.accept_audio(b"pause-2", 0.0)


def test_voice_turn_routes_transcript_through_coordinator_and_streams_tts():
    manager, coordinator, stt, tts = make_session()

    turn = finish_turn(manager)

    assert turn["transcript"] == "hello"
    assert coordinator.calls[0][0] == "hello"
    assert coordinator.calls[0][1]["input_method"] == "voice"
    assert coordinator.calls[0][1]["voice_session_id"] == manager.session_id
    assert stt.chunks == [b"voice-1", b"voice-2", b"pause-1"]
    assert tts.spoken == ["answer: hello"]
    assert manager.snapshot().state == "speaking"


def test_barge_in_cancels_tts_and_starts_the_next_turn():
    manager, coordinator, stt, tts = make_session(("first", "second"))
    finish_turn(manager)

    manager.accept_audio(b"interrupt", 0.8)

    assert tts.cancelled == 1
    assert manager.snapshot().interrupted is True
    assert manager.snapshot().state == "listening"
    assert stt.started == 2
    assert len(coordinator.calls) == 1


def test_silence_does_not_open_a_session_and_close_stops_active_io():
    manager, _, stt, tts = make_session()
    assert manager.accept_audio(b"silence", 0.0) is None
    assert manager.snapshot().state == "idle"

    manager.accept_audio(b"voice", 0.8)
    manager.close()

    assert manager.snapshot().state == "closed"
    assert stt.cancelled == 1
    assert tts.cancelled == 0
